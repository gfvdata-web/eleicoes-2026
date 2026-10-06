"""
Gera docs/data/voto-cruzado/classificacao.json: as duas réguas de voto-cruzado.html.

Régua B (campo do partido): sigla → 0 esquerda, 1 centro, 2 direita (mesma divisão de camara.html).
Régua A (aliança presidencial): 0 = aliado de Lula, 1 = neutro/outro, 2 = aliado de Flávio. Critérios, nesta ordem:
  1. Presidente: Lula = 0, Flávio = 2, outros = 1.
  2. Governador e senador: coligação registrada no TSE (consulta_cand_2026). Coligação, federação ou partido com o PT → 0;
     com o PL → 2 (com os dois: neutro, marcado como conflito).
  3. Se a coligação não decide: apoio declarado, de docs/data/voto-cruzado/apoios-declarados.json (com fonte).
  4. Senão: neutro.
  5. Deputados (por partido): partido da coligação presidencial de Lula → 0; da de Flávio → 2; outros → 1.
A classificação é feita SEM olhar os resultados das urnas (evita circularidade). O leitor pode reclassificar na página.

Entrada: apuracao-bruto/candidatos/consulta_cand_2026.zip (https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/),
         apuracao-bruto/<cargo>/<UF>.json (votos, só para ordenar a lista na página).
Uso: python scripts/alinhamento.py
"""

import csv
import io
import json
import re
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto"
SAIDA = RAIZ / "docs" / "data" / "voto-cruzado"
UFS = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
       "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
PARTIDOS_B = {
    "PT": 0, "PSOL": 0, "PCDOB": 0, "REDE": 0, "PSB": 0, "PDT": 0, "PV": 0, "UP": 0, "PSTU": 0, "PCB": 0, "PCO": 0,
    "MDB": 1, "PSD": 1, "PSDB": 1, "PODE": 1, "SOLIDARIEDADE": 1, "AVANTE": 1, "CIDADANIA": 1, "AGIR": 1, "MOBILIZA": 1,
    "PL": 2, "NOVO": 2, "PP": 2, "REPUBLICANOS": 2, "UNIÃO": 2, "PRD": 2, "MISSÃO": 2, "DC": 2, "PRTB": 2, "DEMOCRATA": 2,
}
LULA, FLAVIO = "13", "22"


def sigla(s):
    return s.upper().replace(" ", "")


def partidos_de(texto):
    """siglas citadas numa composição de coligação/federação do TSE."""
    texto = texto.replace("PC do B", "PCDOB")
    return {sigla(p) for p in re.findall(r"[A-ZÀ-Ú][A-ZÀ-Ú]+", texto.upper())}


def votos(cargo, uf):
    d = json.loads((BRUTO / cargo / f"{uf}.json").read_text(encoding="utf-8"))
    v = {}
    for c in d["carg"]:
        for a in c["agr"]:
            for p in a["par"]:
                for cd in p["cand"]:
                    v[cd["n"]] = int(cd.get("vap", "0") or 0)
    return v


def main():
    z = zipfile.ZipFile(BRUTO / "candidatos" / "consulta_cand_2026.zip")

    def rows(nome):
        return csv.DictReader(io.TextIOWrapper(z.open(nome), encoding="latin-1"), delimiter=";")

    # coligações presidenciais
    pres, col_pres = {}, {}
    for r in rows("consulta_cand_2026_BR.csv"):
        if r["CD_CARGO"] == "1":
            n = r["NR_CANDIDATO"]
            pres[n] = 0 if n == LULA else 2 if n == FLAVIO else 1
            col_pres[n] = partidos_de(r["DS_COMPOSICAO_COLIGACAO"] + " " + r["SG_PARTIDO"])
    dep = {}
    for p in PARTIDOS_B:
        dep[p] = 0 if p in col_pres[LULA] else 2 if p in col_pres[FLAVIO] else 1

    apoios = {}
    arq = SAIDA / "apoios-declarados.json"
    if arq.exists():
        for a in json.loads(arq.read_text(encoding="utf-8")):
            apoios[(a["uf"], a["cargo"], a["numero"])] = a

    cand = {}
    for uf in UFS:
        lista, vistos = [], set()
        v = {1: votos("governador", uf), 2: votos("senador", uf)}
        for r in rows(f"consulta_cand_2026_{uf}.csv"):
            k = {"3": 1, "5": 2}.get(r["CD_CARGO"])
            if not k or (k, r["NR_CANDIDATO"]) in vistos or not v[k].get(r["NR_CANDIDATO"]):
                continue
            vistos.add((k, r["NR_CANDIDATO"]))
            col = r["DS_COMPOSICAO_COLIGACAO"] if r["DS_COMPOSICAO_COLIGACAO"] not in ("#NULO", "#NULO#") else r["SG_PARTIDO"]
            ps = partidos_de(col + " " + r["SG_PARTIDO"] + " " + r["DS_COMPOSICAO_FEDERACAO"])
            pt, pl = "PT" in ps, "PL" in ps
            if pt and pl:
                g, crit, fonte = 1, "Conflito: coligação com PT e PL", ""
            elif pt:
                g, crit, fonte = 0, "Coligação com o PT", "TSE, registro de candidatura"
            elif pl:
                g, crit, fonte = 2, "Coligação com o PL", "TSE, registro de candidatura"
            else:
                a = apoios.get((uf, k, r["NR_CANDIDATO"]))
                if a:
                    rot = "Neutro declarado" if a["g"] == 1 else "Apoio declarado"
                    g, crit, fonte = a["g"], rot + (": " + a["nota"] if a.get("nota") else ""), a["fonte"]
                else:
                    g, crit, fonte = 1, "Neutro: sem coligação com PT ou PL nem apoio declarado encontrado", ""
            lista.append([k, r["NR_CANDIDATO"], r["NM_URNA_CANDIDATO"], sigla(r["SG_PARTIDO"]), col, v[k][r["NR_CANDIDATO"]], g, crit, fonte])
        lista.sort(key=lambda x: (x[0], -x[5]))
        cand[uf] = lista

    saida = {
        "b": PARTIDOS_B,
        "a": {"pres": pres, "dep": dep, "cand": cand,
              "coligacao_lula": sorted(col_pres[LULA]), "coligacao_flavio": sorted(col_pres[FLAVIO])},
    }
    (SAIDA / "classificacao.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    cont = [0, 0, 0]
    for l in cand.values():
        for c in l:
            cont[c[6]] += 1
    print(f"governador/senador: {cont[0]} Lula, {cont[1]} neutros, {cont[2]} Flávio; deputados: {dep}")


if __name__ == "__main__":
    main()
