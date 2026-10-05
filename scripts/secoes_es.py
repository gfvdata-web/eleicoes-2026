"""
Gera os dados de es-secoes.html: votos de cada seção eleitoral (urna) do Espírito Santo no 1º turno de 2026,
com o local de votação e as coordenadas publicadas pelo TSE. Só biblioteca padrão; rode uma vez depois que o
TSE publicar os arquivos de dados abertos (ou de novo, se o TSE atualizar).

Fontes (dados abertos do TSE, só a parte do ES é guardada):
  votacao_secao_2026_ES.zip           votos por seção: governador, senador, dep. federal e estadual
  votacao_secao_2026_BR.zip           idem, presidente (só as linhas do ES ficam, em presidente_secao_ES.csv)
  detalhe_votacao_secao_2026.zip      aptos, comparecimento, brancos, nulos por seção (_ES e as linhas do ES de _BR)
  eleitorado_local_votacao_2026.zip   local de votação de cada seção, com latitude e longitude (arquivo _ES)

Saída em docs/data/es/secoes/:
  cargos.json     candidatos e partidos de cada cargo (nome de urna, partido e situação vêm de docs/data/es/apuracao/)
  estado.json     totais do estado e de cada município, por cargo
  m/<tse>.json    locais de votação e seções do município, com os votos de cada cargo

Uso: python scripts/secoes_es.py [--baixar]
  --baixar   baixa de novo os arquivos do TSE para apuracao-bruto/es-secoes/ (senão usa os que já estão lá)
"""

import csv
import io
import json
import math
import sys
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto" / "es-secoes"
SAIDA = RAIZ / "docs" / "data" / "es" / "secoes"
CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele/"
ARQS = {
    "votacao_secao_2026_ES.zip": "votacao_secao/",
    "votacao_secao_2026_BR.zip": "votacao_secao/",
    "detalhe_votacao_secao_2026.zip": "detalhe_votacao_secao/",
    "eleitorado_local_votacao_2026.zip": "eleitorado_locais_votacao/",
}
# código do cargo no TSE → chave usada na página (igual às de docs/data/es/apuracao/)
CARGOS = {"1": "presidente", "3": "governador", "5": "senador", "6": "deputado-federal", "7": "deputado-estadual"}


def baixar():
    BRUTO.mkdir(parents=True, exist_ok=True)
    for nome, pasta in ARQS.items():
        print("baixando", nome)
        req = urllib.request.Request(CDN + pasta + nome, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=600) as r, open(BRUTO / nome, "wb") as f:
            while bloco := r.read(1 << 20):
                f.write(bloco)
    # dos arquivos nacionais, guarda só as linhas do ES (presidente) e apaga o zip
    for zip_nome, csv_nome, destino in (("votacao_secao_2026_BR.zip", "votacao_secao_2026_BR.csv", "presidente_secao_ES.csv"),
                                        ("detalhe_votacao_secao_2026.zip", "detalhe_votacao_secao_2026_BR.csv", "detalhe_presidente_ES.csv")):
        with zipfile.ZipFile(BRUTO / zip_nome) as z, z.open(csv_nome) as f, open(BRUTO / destino, "wb") as out:
            for i, ln in enumerate(f):
                if i == 0 or b';"ES";' in ln:
                    out.write(ln)
        if zip_nome != "detalhe_votacao_secao_2026.zip":
            (BRUTO / zip_nome).unlink()
    with zipfile.ZipFile(BRUTO / "detalhe_votacao_secao_2026.zip") as z:
        z.extract("detalhe_votacao_secao_2026_ES.csv", BRUTO)
    (BRUTO / "detalhe_votacao_secao_2026.zip").unlink()


def linhas(zip_nome, csv_nome):
    """Lê um CSV do TSE (latin-1, separado por ;), solto em apuracao-bruto/es-secoes/ ou dentro do zip."""
    if (BRUTO / csv_nome).exists():
        with open(BRUTO / csv_nome, encoding="latin-1", newline="") as f:
            yield from csv.DictReader(f, delimiter=";")
        return
    with zipfile.ZipFile(BRUTO / zip_nome) as z, z.open(csv_nome) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="latin-1", newline=""), delimiter=";")


def dentro(lon, lat, geom):
    """Ponto dentro de Polygon/MultiPolygon do GeoJSON (regra par-ímpar)."""
    polis = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    d = False
    for poli in polis:
        for anel in poli:
            for (x1, y1), (x2, y2) in zip(anel, anel[1:] + anel[:1]):
                if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
                    d = not d
    return d


def centro(geom):
    polis = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    anel = max((p[0] for p in polis), key=len)
    return sum(p[0] for p in anel) / len(anel), sum(p[1] for p in anel) / len(anel)


def main():
    if "--baixar" in sys.argv:
        baixar()
    mun_js = (RAIZ / "docs/data/es/municipios.js").read_text(encoding="utf-8")
    MUN = json.loads(mun_js[mun_js.index("["): mun_js.rindex("]") + 1])
    por_tse = {m["tse"]: m for m in MUN}
    geo = json.loads((RAIZ / "docs/data/es/municipios.geojson").read_text(encoding="utf-8"))
    geom = {f["properties"]["ibge"]: f["geometry"] for f in geo["features"]}

    # ---------- locais de votação ----------
    locais = {}   # (mun, zona, local) → dados
    secao_local = {}  # (mun, zona, seção) → (zona, local)   (seções agregadas apontam para o local da principal)
    agregadas = defaultdict(list)  # (mun, zona, seção principal) → [seções agregadas]
    for r in linhas("eleitorado_local_votacao_2026.zip", "eleitorado_local_votacao_2026_ES.csv"):
        mun, zona, sec, loc = r["CD_MUNICIPIO"].zfill(5), int(r["NR_ZONA"]), int(r["NR_SECAO"]), int(r["NR_LOCAL_VOTACAO"])
        k = (mun, zona, loc)
        if k not in locais:
            lat = float(r["NR_LATITUDE"].replace(",", ".") or 0)
            lon = float(r["NR_LONGITUDE"].replace(",", ".") or 0)
            locais[k] = {"nome": " ".join(r["NM_LOCAL_VOTACAO"].split()), "end": " ".join(r["DS_ENDERECO"].split()),
                         "bairro": " ".join(r["NM_BAIRRO"].split()), "lat": lat, "lon": lon,
                         "preso": r["CD_TIPO_LOCAL"] != "1", "el": 0, "secs": []}
        locais[k]["el"] += int(r["QT_ELEITOR_SECAO"])
        secao_local[(mun, zona, sec)] = k
        if r["NR_SECAO_PRINCIPAL"] not in ("-1", ""):
            agregadas[(mun, zona, int(r["NR_SECAO_PRINCIPAL"]))].append(sec)

    # coordenadas: fora do município ou ausentes → perto dos outros locais da mesma zona (marcadas como aproximadas)
    aprox = 0
    por_mun = defaultdict(list)
    for k, l in locais.items():
        por_mun[k[0]].append(k)
    for mun, ks in por_mun.items():
        g = geom[por_tse[mun]["ibge"]]
        ok = [k for k in ks if locais[k]["lat"] and dentro(locais[k]["lon"], locais[k]["lat"], g)]
        for i, k in enumerate(sorted(set(ks) - set(ok))):
            l = locais[k]
            base = [locais[o] for o in ok if o[1] == k[1]] or [locais[o] for o in ok]
            cx, cy = ((sum(b["lon"] for b in base) / len(base), sum(b["lat"] for b in base) / len(base)) if base else centro(g))
            if not dentro(cx, cy, g):
                cx, cy = centro(g)
            ang = i * 2.4
            l["lon"], l["lat"], l["aprox"] = cx + 0.002 * math.cos(ang), cy + 0.002 * math.sin(ang), True
            aprox += 1
        # coordenadas repetidas: afasta um pouco para cada local ter a sua área no mapa
        vistos = defaultdict(int)
        for k in sorted(ks):
            l = locais[k]
            p = (round(l["lon"], 5), round(l["lat"], 5))
            n = vistos[p]
            vistos[p] += 1
            if n:
                l["lon"] += 0.0004 * math.cos(n * 2.4) * math.sqrt(n)
                l["lat"] += 0.0004 * math.sin(n * 2.4) * math.sqrt(n)
    print(f"{len(locais)} locais de votação; {aprox} com posição aproximada")

    # ---------- candidatos (nome de urna, partido e situação da apuração já gravada) ----------
    cargos_saida = {}
    idx_cand, idx_part = {}, {}
    for cod, cg in CARGOS.items():
        ap = json.loads((RAIZ / f"docs/data/es/apuracao/{cg}.json").read_text(encoding="utf-8"))
        # cópia bruta do TSE (scripts/apuracao_es.py): destino do voto de cada candidato e partidos sem candidato
        bruto = RAIZ / f"apuracao-bruto/es/{cg}/ES.json"
        dvt, num_part = {}, {}
        if bruto.exists():
            for agr in json.loads(bruto.read_text(encoding="utf-8"))["carg"][0]["agr"]:
                for p in agr["par"]:
                    num_part[p["n"]] = p["sg"]
                    for c in p["cand"]:
                        dvt[c["n"]] = c.get("dvt", "Válido")
        # [número, nome de urna, partido, situação, eleito, 1 = voto válido / 0 = anulado sub judice]
        cand = [[c[0], c[1], c[2], c[4], c[5], 0 if dvt.get(c[0], "Válido").startswith("Anulado") else 1] for c in ap["cand"]]
        for c in ap["cand"]:
            num_part.setdefault(c[0][:2], c[2])
        partidos = sorted(num_part.items(), key=lambda x: int(x[0]))
        cargos_saida[cg] = {"vagas": ap.get("vagas", 1), "cand": cand, "partidos": [[n, s] for n, s in partidos]}
        idx_cand[cg] = {c[0]: i for i, c in enumerate(cand)}
        idx_part[cg] = {n: i for i, (n, s) in enumerate(partidos)}

    # ---------- detalhe por seção (aptos, comparecimento, brancos, nulos) ----------
    secoes = {}  # (mun, zona, seção) → {"apt", "comp", "hora", cargo: [vb, vn, {cand: v}, {part: v}]}
    def detalhe(zip_nome, csv_nome):
        for r in linhas(zip_nome, csv_nome):
            cg = CARGOS.get(r["CD_CARGO"])
            if not cg:
                continue
            k = (r["CD_MUNICIPIO"].zfill(5), int(r["NR_ZONA"]), int(r["NR_SECAO"]))
            s = secoes.setdefault(k, {"apt": int(r["QT_APTOS"]), "comp": int(r["QT_COMPARECIMENTO"]),
                                      "hora": r["DT_RECEBIMENTO_BU_HOR_TSE"][11:16],
                                      "urna": r["DS_MODELO_URNA"].replace("UE ", ""),
                                      "inst": r["ST_SECAO_INSTALADA"] == "Sim", "anul": r["ST_SECAO_ANULADA"] == "Sim"})
            s[cg] = [int(r["QT_VOTOS_BRANCOS"]), int(r["QT_VOTOS_NULOS"]), {}, {}]
    detalhe(None, "detalhe_votacao_secao_2026_ES.csv")
    detalhe(None, "detalhe_presidente_ES.csv")
    print(f"{len(secoes)} seções com detalhe")

    faltou = defaultdict(int)
    def votos(zip_nome, csv_nome):
        for r in linhas(zip_nome, csv_nome):
            cg = CARGOS.get(r["CD_CARGO"])
            if not cg:
                continue
            n = r["NR_VOTAVEL"]
            if n in ("95", "96", "97"):  # branco, nulo e anulado já vêm do detalhe
                continue
            k = (r["CD_MUNICIPIO"].zfill(5), int(r["NR_ZONA"]), int(r["NR_SECAO"]))
            s = secoes.get(k)
            if not s or cg not in s:
                faltou[cg] += 1
                continue
            v = int(r["QT_VOTOS"])
            if n in idx_cand[cg]:
                s[cg][2][idx_cand[cg][n]] = s[cg][2].get(idx_cand[cg][n], 0) + v
            elif len(n) == 2 and n in idx_part[cg]:
                s[cg][3][idx_part[cg][n]] = s[cg][3].get(idx_part[cg][n], 0) + v
            else:
                faltou[cg + " (número " + n + ")"] += v
    votos("votacao_secao_2026_ES.zip", "votacao_secao_2026_ES.csv")
    votos(None, "presidente_secao_ES.csv")
    if faltou:
        print("votos sem correspondência:", dict(faltou))

    # ---------- saída ----------
    (SAIDA / "m").mkdir(parents=True, exist_ok=True)
    CG = list(CARGOS.values())

    def soma(dst, s):
        dst["apt"] += s["apt"]; dst["comp"] += s["comp"]; dst["n"] += 1
        for cg in CG:
            if cg not in s:
                continue
            t = dst.setdefault(cg, [0, 0, {}, {}])
            t[0] += s[cg][0]; t[1] += s[cg][1]
            for j in (2, 3):
                for i, v in s[cg][j].items():
                    t[j][i] = t[j].get(i, 0) + v

    def compacto(t):
        """{cargo: [vb, vn, {i: v}, {p: v}]} → {cargo: [vb, vn, [i, v, i, v, ...], [p, v, ...]]}, do maior para o menor."""
        out = {}
        for cg in CG:
            if cg in t:
                vb, vn, c, p = t[cg]
                out[cg] = [vb, vn, [x for i, v in sorted(c.items(), key=lambda a: -a[1]) for x in (i, v)],
                           [x for i, v in sorted(p.items(), key=lambda a: -a[1]) for x in (i, v)]]
        return out

    estado = {"apt": 0, "comp": 0, "n": 0}
    muns_saida = {}
    for mun in sorted(por_mun):
        ks = sorted(por_mun[mun], key=lambda k: (k[1], k[2]))
        lidx = {k: i for i, k in enumerate(ks)}
        tot_mun = {"apt": 0, "comp": 0, "n": 0}
        zonas = sorted({k[1] for k in ks})
        lista_sec = []
        for k_sec in sorted(k for k in secoes if k[0] == mun):
            s = secoes[k_sec]
            lk = secao_local.get(k_sec)
            if lk is None:
                print("seção sem local:", k_sec)
                continue
            soma(tot_mun, s)
            soma(estado, s)
            lista_sec.append([k_sec[1], k_sec[2], lidx[lk], s["apt"], s["comp"], s["hora"], s["urna"],
                              (1 if s["inst"] else 0) + (2 if s["anul"] else 0),
                              agregadas.get(k_sec, []), compacto(s)])
        locais_saida = []
        for k in ks:
            l = locais[k]
            locais_saida.append([k[1], k[2], l["nome"], l["bairro"], l["end"], round(l["lon"], 5), round(l["lat"], 5),
                                 (1 if l.get("aprox") else 0) + (2 if l["preso"] else 0)])
        j = {"tse": mun, "nome": por_tse[mun]["nome"], "zonas": zonas, "locais": locais_saida, "secoes": lista_sec}
        (SAIDA / "m" / f"{mun}.json").write_text(json.dumps(j, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        muns_saida[mun] = {"apt": tot_mun["apt"], "comp": tot_mun["comp"], "n": tot_mun["n"], "zonas": zonas,
                           "locais": len(ks), "v": compacto(tot_mun)}
    est = {"apt": estado["apt"], "comp": estado["comp"], "n": estado["n"], "v": compacto(estado)}
    (SAIDA / "cargos.json").write_text(json.dumps(cargos_saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (SAIDA / "estado.json").write_text(json.dumps({"fonte": "TSE, dados abertos (votação por seção), arquivos de 05/10/2026",
                                                  "es": est, "mun": muns_saida}, ensure_ascii=False, separators=(",", ":")),
                                       encoding="utf-8")
    tam = sum(f.stat().st_size for f in SAIDA.rglob("*.json"))
    print(f"{estado['n']} seções, {estado['apt']} aptos, {estado['comp']} comparecimento; {tam / 1e6:.1f} MB em {SAIDA}")


if __name__ == "__main__":
    main()
