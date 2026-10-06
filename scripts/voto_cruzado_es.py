"""
Gera os dados de voto-cruzado.html: votos de cada seção eleitoral (urna) do Espírito Santo no 1º turno de 2026,
somados por campo político (esquerda / centro / direita, pelo partido do candidato) em cada cargo.
Só biblioteca padrão. Lê o que scripts/secoes_es.py já gerou em docs/data/es/secoes/ (não baixa nada).

Saída: docs/data/voto-cruzado/es.json
  grupos     ["Esquerda", "Centro", "Direita"]
  partidos   {sigla: índice do grupo} (partido fora da lista = sem grupo, não entra em nenhum campo)
  cargos     ordem dos cargos nas seções
  locais     [[código TSE do município, zona, nome do local, bairro, lon, lat]]
  secoes     [[índice do local, zona, nº da seção, aptos, comparecimento, lula, flávio,
               depois, para cada cargo: válidos, esquerda, centro, direita]]
  Válidos = nominais + legenda de candidatos com voto válido (sem sub judice). No Senado, os 2 votos de cada eleitor
  entram na soma (válidos ≈ 2 × votantes).

Uso: python scripts/voto_cruzado_es.py
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "docs" / "data" / "es" / "secoes"
SAIDA = RAIZ / "docs" / "data" / "voto-cruzado"

GRUPOS = ["Esquerda", "Centro", "Direita"]
# Mesma divisão de camara.html (uso comum na imprensa), com os partidos do ES que faltavam lá.
PARTIDOS = {
    "PT": 0, "PSOL": 0, "PCDOB": 0, "REDE": 0, "PSB": 0, "PDT": 0, "PV": 0, "UP": 0, "PSTU": 0, "PCB": 0, "PCO": 0,
    "MDB": 1, "PSD": 1, "PSDB": 1, "PODE": 1, "SOLIDARIEDADE": 1, "AVANTE": 1, "CIDADANIA": 1, "AGIR": 1,
    "PL": 2, "NOVO": 2, "PP": 2, "REPUBLICANOS": 2, "UNIÃO": 2, "PRD": 2, "MISSÃO": 2, "DC": 2, "PRTB": 2, "DEMOCRATA": 2,
}
CARGOS = ["presidente", "governador", "senador", "deputado-federal", "deputado-estadual"]


def main():
    cargos = json.loads((ENTRADA / "cargos.json").read_text(encoding="utf-8"))
    estado = json.loads((ENTRADA / "estado.json").read_text(encoding="utf-8"))
    # grupo de cada candidato (None = sub judice ou partido sem grupo) e de cada partido (votos de legenda)
    gcand = {c: [PARTIDOS.get(x[2]) if x[5] else None for x in cargos[c]["cand"]] for c in CARGOS}
    gpart = {c: [PARTIDOS.get(x[1]) for x in cargos[c]["partidos"]] for c in CARGOS}
    pres = cargos["presidente"]["cand"]
    i_lula = next(i for i, x in enumerate(pres) if x[1] == "LULA")
    i_flavio = next(i for i, x in enumerate(pres) if x[1] == "FLAVIO BOLSONARO")
    sem_grupo = sorted({x[2] for c in CARGOS for x in cargos[c]["cand"] if x[2] not in PARTIDOS}
                       | {x[1] for c in CARGOS for x in cargos[c]["partidos"] if x[1] not in PARTIDOS})
    if sem_grupo:
        print("partidos sem grupo:", ", ".join(sem_grupo))

    locais, secoes = [], []
    for tse in sorted(estado["mun"]):
        m = json.loads((ENTRADA / "m" / f"{tse}.json").read_text(encoding="utf-8"))
        base = len(locais)
        for zona, _num, nome, bairro, _end, lon, lat, _fl in m["locais"]:
            locais.append([tse, zona, nome, bairro, lon, lat])
        for zona, num, loc, apt, comp, _hora, _modelo, flags, _agreg, v in m["secoes"]:
            if not flags & 1 or flags & 2 or not comp:   # só seções instaladas e não anuladas
                continue
            lin = [base + loc, zona, num, apt, comp]
            cand = v["presidente"][2]
            votos = dict(zip(cand[::2], cand[1::2]))
            lin += [votos.get(i_lula, 0), votos.get(i_flavio, 0)]
            for c in CARGOS:
                val, g = 0, [0, 0, 0]
                _b, _n, cv, pv = v[c]
                for idx, n in zip(cv[::2], cv[1::2]):
                    if cargos[c]["cand"][idx][5]:
                        val += n
                        if gcand[c][idx] is not None:
                            g[gcand[c][idx]] += n
                for idx, n in zip(pv[::2], pv[1::2]):
                    val += n
                    if gpart[c][idx] is not None:
                        g[gpart[c][idx]] += n
                lin += [val] + g
            secoes.append(lin)

    SAIDA.mkdir(parents=True, exist_ok=True)
    saida = {"grupos": GRUPOS, "partidos": PARTIDOS, "cargos": CARGOS, "locais": locais, "secoes": secoes}
    (SAIDA / "es.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(secoes)} seções, {len(locais)} locais -> {SAIDA / 'es.json'}")


if __name__ == "__main__":
    main()
