"""
Gera os dados de voto-cruzado.html para os 27 estados: votos de cada seção eleitoral (urna) no 1º turno de 2026,
somados por campo político (esquerda / centro / direita, pelo partido do candidato) em cada cargo.
Só biblioteca padrão. Substitui o antigo voto_cruzado_es.py (mesmo formato de saída).

Entrada (dados abertos do TSE em apuracao-bruto/secoes-br/, baixados de https://cdn.tse.jus.br/estatistica/sead/odsele/):
  votacao_secao_2026_<UF>.zip         votos por seção: governador, senador, dep. federal e estadual/distrital
  votacao_secao_2026_BR.zip           idem, presidente (todas as UFs)
  detalhe_votacao_secao_2026.zip      aptos, comparecimento, seção instalada/anulada
  eleitorado_local_votacao_2026.zip   bairro e coordenadas dos locais de votação
Partido e destino do voto (válido ou sub judice) de cada número vêm de apuracao-bruto/<cargo>/<UF>.json
(de scripts/apuracao.py). Nomes dos municípios: docs/data/uf/<uf>/municipios.json e docs/data/es/municipios.js.

Saída em docs/data/voto-cruzado/:
  <uf>.json   grupos, partidos, cargos, mun {tse: nome}, locais [[tse, zona, nome, bairro, lon, lat]],
              secoes [[local, zona, seção, aptos, comparecimento, lula, flávio, e para cada cargo: válidos, esq, centro, dir]]
  brasil.json grupos, cargos, ufs {UF: totais (mesma ordem das seções, a partir de aptos)}, modelo nacional por campo
              {b: [constante, governador, senado, dep. federal, dep. estadual], r2, erro}, ajustado em todas as seções do país

Uso: python scripts/voto_cruzado.py [UF ...]   (sem UF: todas; brasil.json só é gravado quando roda todas)
"""

import csv
import io
import json
import math
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto"
SECOES = BRUTO / "secoes-br"
SAIDA = RAIZ / "docs" / "data" / "voto-cruzado"

UFS = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
       "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
GRUPOS = ["Esquerda", "Centro", "Direita"]
# Mesma divisão de camara.html (uso comum na imprensa), com os partidos que faltavam lá.
PARTIDOS = {
    "PT": 0, "PSOL": 0, "PCDOB": 0, "REDE": 0, "PSB": 0, "PDT": 0, "PV": 0, "UP": 0, "PSTU": 0, "PCB": 0, "PCO": 0,
    "MDB": 1, "PSD": 1, "PSDB": 1, "PODE": 1, "SOLIDARIEDADE": 1, "AVANTE": 1, "CIDADANIA": 1, "AGIR": 1, "MOBILIZA": 1,
    "PL": 2, "NOVO": 2, "PP": 2, "REPUBLICANOS": 2, "UNIÃO": 2, "PRD": 2, "MISSÃO": 2, "DC": 2, "PRTB": 2, "DEMOCRATA": 2,
}
CARGOS = ["presidente", "governador", "senador", "deputado-federal", "deputado-estadual"]
COD_CARGO = {"3": "governador", "5": "senador", "6": "deputado-federal", "7": "deputado-estadual", "8": "deputado-estadual"}
LULA, FLAVIO = "13", "22"
SEM_GRUPO = set()


def linhas(zip_nome, csv_nome):
    with zipfile.ZipFile(SECOES / zip_nome) as z, z.open(csv_nome) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")


def numeros(cargo, uf):
    """número votável → (grupo ou None, válido?) a partir da apuração do TSE."""
    d = json.loads((BRUTO / cargo / f"{uf}.json").read_text(encoding="utf-8"))
    t = {}
    for c in d["carg"]:
        for a in c["agr"]:
            for p in a["par"]:
                sg = p["sg"].upper().replace(" ", "")
                g = PARTIDOS.get(sg)
                if g is None:
                    SEM_GRUPO.add(sg)
                if p.get("dvt", "").startswith("Válido"):
                    t[p["n"]] = (g, True)
                for cd in p["cand"]:
                    t[cd["n"]] = (g, cd["dvt"].startswith("Válido"))
    return t


def nomes_mun(uf):
    if uf == "ES":
        txt = (RAIZ / "docs" / "data" / "es" / "municipios.js").read_text(encoding="utf-8")
        lista = json.loads(txt[txt.index("["):txt.rindex("]") + 1])
    else:
        lista = json.loads((RAIZ / "docs" / "data" / "uf" / uf.lower() / "municipios.json").read_text(encoding="utf-8"))
    return {m["tse"]: m["nome"] for m in lista}


def somar(destino, tab, num, votos):
    """soma votos em [válidos, esq, centro, dir]; números fora da lista (brancos, nulos, anulados) ficam de fora."""
    g, valido = tab.get(num, (None, False))
    if not valido:
        return
    destino[0] += votos
    if g is not None:
        destino[1 + g] += votos


def presidente():
    """(uf, mun, zona, seção) → [válidos, esq, centro, dir, lula, flávio], para o país todo."""
    tab = numeros("presidente", "ES")   # candidatos e partidos são os mesmos em todas as UFs
    pres = {}
    for r in linhas("votacao_secao_2026_BR.zip", "votacao_secao_2026_BR.csv"):
        if r["CD_CARGO"] != "1" or r["SG_UF"] not in UFS:
            continue
        k = (r["SG_UF"], r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))
        v = pres.setdefault(k, [0, 0, 0, 0, 0, 0])
        n, q = r["NR_VOTAVEL"], int(r["QT_VOTOS"])
        somar(v, tab, n, q)
        if n == LULA:
            v[4] += q
        elif n == FLAVIO:
            v[5] += q
    return pres


def processar(uf, pres):
    tabs = {c: numeros(c, uf) for c in CARGOS[1:]}
    mun = nomes_mun(uf)
    # aptos e comparecimento (linha de governador; DF também tem governador)
    det = {}
    for r in linhas("detalhe_votacao_secao_2026.zip", f"detalhe_votacao_secao_2026_{uf}.csv"):
        if r["CD_CARGO"] != "3":
            continue
        k = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))
        det[k] = (int(r["QT_APTOS"]), int(r["QT_COMPARECIMENTO"]), r["ST_SECAO_INSTALADA"] == "Sim", r["ST_SECAO_ANULADA"] == "Sim")
    # bairro e coordenadas de cada local
    loc_info = {}
    for r in linhas("eleitorado_local_votacao_2026.zip", f"eleitorado_local_votacao_2026_{uf}.csv"):
        k = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_LOCAL_VOTACAO"]))
        if k not in loc_info:
            def coord(s):
                try:
                    return round(float(s.replace(",", ".")), 5)
                except ValueError:
                    return None
            lat, lon = coord(r["NR_LATITUDE"]), coord(r["NR_LONGITUDE"])
            loc_info[k] = (" ".join(r["NM_BAIRRO"].split()), lon if lat else None, lat if lat else None)
    # votos por seção e cargo
    votos, local_de, nome_local = {}, {}, {}
    for r in linhas(f"votacao_secao_2026_{uf}.zip", f"votacao_secao_2026_{uf}.csv"):
        c = COD_CARGO.get(r["CD_CARGO"])
        if not c:
            continue
        k = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))
        v = votos.setdefault(k, {x: [0, 0, 0, 0] for x in CARGOS[1:]})
        somar(v[c], tabs[c], r["NR_VOTAVEL"], int(r["QT_VOTOS"]))
        if k not in local_de:
            kl = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_LOCAL_VOTACAO"]))
            local_de[k] = kl
            nome_local.setdefault(kl, " ".join(r["NM_LOCAL_VOTACAO"].split()))

    locais, idx_local, secoes = [], {}, []
    for k in sorted(votos):
        d = det.get(k)
        p = pres.get((uf,) + k)
        if not d or not p or not d[2] or d[3] or not d[1]:   # só seções instaladas, não anuladas e com votantes
            continue
        kl = local_de[k]
        if kl not in idx_local:
            idx_local[kl] = len(locais)
            bairro, lon, lat = loc_info.get(kl, ("", None, None))
            locais.append([kl[0], kl[1], nome_local[kl], bairro, lon, lat])
        lin = [idx_local[kl], k[1], k[2], d[0], d[1], p[4], p[5]] + p[:4]
        for c in CARGOS[1:]:
            lin += votos[k][c]
        secoes.append(lin)
    saida = {"uf": uf, "grupos": GRUPOS, "partidos": PARTIDOS, "cargos": CARGOS,
             "mun": {t: mun.get(t, t) for t in sorted({l[0] for l in locais})}, "locais": locais, "secoes": secoes}
    (SAIDA / f"{uf.lower()}.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return secoes


def parte(lin, k, g):
    v = lin[7 + 4 * k]
    return lin[8 + 4 * k + g] / v if v else None


def ajustar(todas, g):
    """regressão linear ponderada (comparecimento) do % do campo g para presidente sobre os 4 outros cargos."""
    n = 5
    A = [[0.0] * (n + 1) for _ in range(n)]
    sw = sy = syy = 0.0
    obs = []
    for lin in todas:
        w, y = lin[4], parte(lin, 0, g)
        x = [1.0] + [parte(lin, k, g) for k in range(1, 5)]
        if not w or y is None or None in x:
            continue
        obs.append((w, x, y))
        for i in range(n):
            for j in range(n):
                A[i][j] += w * x[i] * x[j]
            A[i][n] += w * x[i] * y
        sw += w; sy += w * y; syy += w * y * y
    for i in range(n):   # eliminação de Gauss
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i:
                f = A[r][i] / A[i][i]
                for c in range(i, n + 1):
                    A[r][c] -= f * A[i][c]
    b = [A[i][n] / A[i][i] for i in range(n)]
    sr = sum(w * (y - max(0, min(1, sum(bi * xi for bi, xi in zip(b, x))))) ** 2 for w, x, y in obs)
    return {"b": [round(x, 5) for x in b], "r2": round(1 - sr / (syy - sy * sy / sw), 4), "erro": round(math.sqrt(sr / sw), 5)}


def main():
    pedidas = [u.upper() for u in sys.argv[1:]] or UFS
    SAIDA.mkdir(parents=True, exist_ok=True)
    print("presidente (arquivo nacional)...", flush=True)
    pres = presidente()
    todas, ufs = [], {}
    for uf in pedidas:
        sec = processar(uf, pres)
        tot = [sum(l[i] for l in sec) for i in range(3, len(sec[0]))] if sec else []
        ufs[uf] = tot
        todas += sec
        print(f"{uf}: {len(sec)} seções", flush=True)
    if SEM_GRUPO:
        print("partidos sem grupo:", ", ".join(sorted(SEM_GRUPO)))
    if pedidas == UFS:
        modelo = {str(g): ajustar(todas, g) for g in (0, 2)}
        saida = {"grupos": GRUPOS, "cargos": CARGOS, "ufs": ufs, "modelo": modelo}
        (SAIDA / "brasil.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print("brasil.json; modelo:", modelo)


if __name__ == "__main__":
    main()
