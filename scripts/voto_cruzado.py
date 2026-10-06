"""
Gera os dados de voto-cruzado.html para os 27 estados: votos de cada seção eleitoral (urna) no 1º turno de 2026,
por candidato (presidente, governador, senador) e por partido (deputados federal e estadual, nominais + legenda).
A soma por grupo (régua B = campo do partido; régua A = aliança presidencial) é feita no navegador, para que o
leitor possa reclassificar candidatos e partidos. Só biblioteca padrão.

Entrada (dados abertos do TSE em apuracao-bruto/secoes-br/, de https://cdn.tse.jus.br/estatistica/sead/odsele/):
  votacao_secao_2026_<UF>.zip         votos por seção: governador, senador, dep. federal e estadual/distrital
  votacao_secao_2026_BR.zip           idem, presidente (todas as UFs)
  detalhe_votacao_secao_2026.zip      aptos, comparecimento, seção instalada/anulada
  eleitorado_local_votacao_2026.zip   bairro e coordenadas dos locais de votação
Partido, nome e destino do voto (válido ou sub judice) de cada número: apuracao-bruto/<cargo>/<UF>.json
(de scripts/apuracao.py). Nomes dos municípios: docs/data/uf/<uf>/municipios.json e docs/data/es/municipios.js.

Saída em docs/data/voto-cruzado/:
  <uf>.json   uf, mun {tse: nome}, locais [[tse, zona, nome, bairro, lon, lat]],
              ent [[cargo 0-4, número, nome, sigla do partido]]  (cargos 3 e 4: uma entidade por partido),
              secoes [[local, zona, seção, aptos, comparecimento, entidade, votos, entidade, votos, ...]]
              (só pares com votos > 0; só votos válidos: brancos, nulos e sub judice ficam de fora)
  brasil.json ufs {UF: {ent, tot: [aptos, comp, pares...], mun: {tse: [aptos, comp, pares...]}}}
              (para a unidade "Estados" e o modelo nacional, ajustado por município no navegador)

Uso: python scripts/voto_cruzado.py [UF ...]   (sem UF: todas; brasil.json só é gravado quando roda todas)
"""

import csv
import io
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto"
SECOES = BRUTO / "secoes-br"
SAIDA = RAIZ / "docs" / "data" / "voto-cruzado"

UFS = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
       "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
CARGOS = ["presidente", "governador", "senador", "deputado-federal", "deputado-estadual"]
COD_CARGO = {"3": 1, "5": 2, "6": 3, "7": 4, "8": 4}   # código TSE → índice do cargo (8 = distrital, no DF)


def linhas(zip_nome, csv_nome):
    with zipfile.ZipFile(SECOES / zip_nome) as z, z.open(csv_nome) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")


def sigla(s):
    return s.upper().replace(" ", "")


def numeros(k, uf):
    """número votável → (chave da entidade, nome, sigla) para votos válidos do cargo k.
    Presidente, governador e senador: o candidato. Deputados: o partido (nominal e legenda)."""
    d = json.loads((BRUTO / CARGOS[k] / f"{uf}.json").read_text(encoding="utf-8"))
    t = {}
    for c in d["carg"]:
        for a in c["agr"]:
            for p in a["par"]:
                sg = sigla(p["sg"])
                if k >= 3 and p.get("dvt", "").startswith("Válido"):
                    t[p["n"]] = (p["n"], sg, sg)
                for cd in p["cand"]:
                    if cd["dvt"].startswith("Válido"):
                        t[cd["n"]] = ((p["n"], sg, sg) if k >= 3 else (cd["n"], cd.get("nmu") or cd["nm"], sg))
    return t


def nomes_mun(uf):
    if uf == "ES":
        txt = (RAIZ / "docs" / "data" / "es" / "municipios.js").read_text(encoding="utf-8")
        lista = json.loads(txt[txt.index("["):txt.rindex("]") + 1])
    else:
        lista = json.loads((RAIZ / "docs" / "data" / "uf" / uf.lower() / "municipios.json").read_text(encoding="utf-8"))
    return {m["tse"]: m["nome"] for m in lista}


def presidente():
    """(uf, mun, zona, seção) → {número: votos} (só candidatos com voto válido), para o país todo."""
    tab = numeros(0, "ES")   # candidatos a presidente são os mesmos em todas as UFs
    pres = defaultdict(lambda: defaultdict(int))
    for r in linhas("votacao_secao_2026_BR.zip", "votacao_secao_2026_BR.csv"):
        if r["CD_CARGO"] != "1" or r["SG_UF"] not in UFS or r["NR_VOTAVEL"] not in tab:
            continue
        pres[(r["SG_UF"], r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))][r["NR_VOTAVEL"]] += int(r["QT_VOTOS"])
    return tab, pres


def processar(uf, tab_pres, pres):
    tabs = {k: numeros(k, uf) for k in range(1, 5)}
    tabs[0] = tab_pres
    mun = nomes_mun(uf)
    det = {}
    for r in linhas("detalhe_votacao_secao_2026.zip", f"detalhe_votacao_secao_2026_{uf}.csv"):
        if r["CD_CARGO"] != "3":
            continue
        k = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))
        det[k] = (int(r["QT_APTOS"]), int(r["QT_COMPARECIMENTO"]), r["ST_SECAO_INSTALADA"] == "Sim", r["ST_SECAO_ANULADA"] == "Sim")
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
    # votos por seção e entidade (cargo, chave)
    votos = defaultdict(lambda: defaultdict(int))
    local_de, nome_local = {}, {}
    for r in linhas(f"votacao_secao_2026_{uf}.zip", f"votacao_secao_2026_{uf}.csv"):
        kc = COD_CARGO.get(r["CD_CARGO"])
        if kc is None:
            continue
        k = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_SECAO"]))
        e = tabs[kc].get(r["NR_VOTAVEL"])
        if e:
            votos[k][(kc, e[0])] += int(r["QT_VOTOS"])
        if k not in local_de:
            kl = (r["CD_MUNICIPIO"], int(r["NR_ZONA"]), int(r["NR_LOCAL_VOTACAO"]))
            local_de[k] = kl
            nome_local.setdefault(kl, " ".join(r["NM_LOCAL_VOTACAO"].split()))

    validas = []
    for k in sorted(votos):
        d, p = det.get(k), pres.get((uf,) + k)
        if d and p and d[2] and not d[3] and d[1]:   # só seções instaladas, não anuladas e com votantes
            for n, q in p.items():
                votos[k][(0, n)] += q
            validas.append(k)
    # entidades: por cargo, da mais para a menos votada no estado
    total = defaultdict(int)
    for k in validas:
        for e, q in votos[k].items():
            total[e] += q
    ent_info = {}
    for kc in range(5):
        for num, (chave, nome, sg) in tabs[kc].items():
            ent_info.setdefault((kc, chave), (nome, sg))
    ents = sorted(total, key=lambda e: (e[0], -total[e]))
    idx = {e: i for i, e in enumerate(ents)}
    ent = [[e[0], e[1], ent_info[e][0], ent_info[e][1]] for e in ents]

    locais, idx_local, secoes = [], {}, []
    por_mun = defaultdict(lambda: defaultdict(int))
    apt_mun = defaultdict(lambda: [0, 0])
    for k in validas:
        d = det[k]
        kl = local_de[k]
        if kl not in idx_local:
            idx_local[kl] = len(locais)
            bairro, lon, lat = loc_info.get(kl, ("", None, None))
            locais.append([kl[0], kl[1], nome_local[kl], bairro, lon, lat])
        lin = [idx_local[kl], k[1], k[2], d[0], d[1]]
        for e, q in sorted(votos[k].items(), key=lambda x: idx[x[0]]):
            if q:
                lin += [idx[e], q]
                por_mun[k[0]][idx[e]] += q
        apt_mun[k[0]][0] += d[0]; apt_mun[k[0]][1] += d[1]
        secoes.append(lin)
    saida = {"uf": uf, "mun": {t: mun.get(t, t) for t in sorted({l[0] for l in locais})}, "locais": locais, "ent": ent, "secoes": secoes}
    (SAIDA / f"{uf.lower()}.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    def linha(ap, pm):
        out = list(ap)
        for i in sorted(pm):
            out += [i, pm[i]]
        return out
    tot_ent = defaultdict(int)
    for pm in por_mun.values():
        for i, q in pm.items():
            tot_ent[i] += q
    resumo = {"ent": ent,
              "tot": linha([sum(a[0] for a in apt_mun.values()), sum(a[1] for a in apt_mun.values())], tot_ent),
              "mun": {t: linha(apt_mun[t], por_mun[t]) for t in sorted(por_mun)}}
    return len(secoes), resumo


def main():
    pedidas = [u.upper() for u in sys.argv[1:]] or UFS
    SAIDA.mkdir(parents=True, exist_ok=True)
    print("presidente (arquivo nacional)...", flush=True)
    tab_pres, pres = presidente()
    ufs = {}
    for uf in pedidas:
        n, resumo = processar(uf, tab_pres, pres)
        ufs[uf] = resumo
        print(f"{uf}: {n} seções, {len(resumo['ent'])} entidades", flush=True)
    if pedidas == UFS:
        (SAIDA / "brasil.json").write_text(json.dumps({"ufs": ufs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print("brasil.json gravado")


if __name__ == "__main__":
    main()
