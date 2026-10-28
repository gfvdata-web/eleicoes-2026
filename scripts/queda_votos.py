"""
Gera os dados de urnas-queda.html: municípios e seções eleitorais em que Lula (13) ou Flávio Bolsonaro (22)
tiveram MENOS votos no 2º turno de 2026 (25/10) do que no 1º turno (04/10). Qualquer queda (1 voto ou mais) entra.
Só biblioteca padrão.

Entrada (dados abertos do TSE, já baixados por scripts/urnas_zero.py) em apuracao-bruto/urnas-zero/:
  votacao_secao_2026_BR.zip          votos de presidente por seção, nos dois turnos (NR_TURNO)
  detalhe_votacao_secao_2026.zip     comparecimento por turno e nome do local (arquivo _BR.csv)
A seção é a mesma nos dois turnos da mesma eleição: casamento exato por (UF, município, zona, seção).

Saída em docs/data/queda-votos/:
  resumo.json
    gerado, tot {lula1, lula2, flavio1, flavio2, comp1, comp2, secoes, ql, qf, qa, pl, pf, pa} (país; ql/qf/qa =
        seções com queda de Lula / de Flávio / dos dois; pl/pf = votos perdidos somados nessas seções; pa = soma das
        duas quedas nas seções em que os dois caíram),
    faixas: limites das faixas de queda; dist {l: [...], f: [...]} = seções por faixa de queda (votos perdidos),
    ufs {UF: [seções, ql, qf, qa, lula1, lula2, flavio1, flavio2, comp1, comp2]},
    mun [[uf, tse, nome, lula1, lula2, flavio1, flavio2, comp1, comp2, seções, ql, qf]] (todos os municípios)
  secoes/<UF>.json  {locais: [nome], secoes: [[tse, zona, seção, local, comp1, comp2, lula1, lula2, flavio1,
        flavio2]]} só as seções com queda de pelo menos um dos dois.

Uso: python scripts/queda_votos.py
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from urnas_zero import PASTA, RAIZ, chave, linhas, nomes_mun  # noqa: E402

SAIDA = RAIZ / "docs" / "data" / "queda-votos"
FAIXAS = [5, 10, 25, 50]  # 1–5, 6–10, 11–25, 26–50, mais de 50


def faixa(q):
    for i, lim in enumerate(FAIXAS):
        if q <= lim:
            return i
    return len(FAIXAS)


def main():
    print("votos por seção …")
    v = defaultdict(lambda: [0, 0, 0, 0])  # lula1, lula2, flavio1, flavio2
    turnos = defaultdict(set)
    for r in linhas(PASTA / "votacao_secao_2026_BR.zip", "votacao_secao_2026_BR.csv"):
        if r["CD_CARGO"] != "1":
            continue
        k, t = chave(r), r["NR_TURNO"]
        turnos[k].add(t)
        n = r["NR_VOTAVEL"]
        if n == "13":
            v[k][0 if t == "1" else 1] += int(r["QT_VOTOS"])
        elif n == "22":
            v[k][2 if t == "1" else 3] += int(r["QT_VOTOS"])
    dois = {k for k, ts in turnos.items() if ts >= {"1", "2"}}
    print(f"  {len(turnos)} seções, {len(dois)} com votos nos dois turnos")

    print("comparecimento …")
    comp = defaultdict(lambda: [0, 0])
    local = {}
    for r in linhas(PASTA / "detalhe_votacao_secao_2026.zip", "detalhe_votacao_secao_2026_BR.csv"):
        if r["CD_CARGO"] != "1" or r["ST_SECAO_ANULADA"] in ("Sim", "S"):
            continue
        k = chave(r)
        comp[k][0 if r["NR_TURNO"] == "1" else 1] += int(r["QT_COMPARECIMENTO"])
        local.setdefault(k, r["NM_LOCAL_VOTACAO"])
        if (k[0], k[1]) not in nomes_tse_extra:
            nomes_tse_extra[(k[0], k[1])] = r["NM_MUNICIPIO"].title()

    tot = dict(lula1=0, lula2=0, flavio1=0, flavio2=0, comp1=0, comp2=0, secoes=0, ql=0, qf=0, qa=0, pl=0, pf=0, pa=0)
    dist = {"l": [0] * (len(FAIXAS) + 1), "f": [0] * (len(FAIXAS) + 1)}
    ufs = defaultdict(lambda: [0] * 10)
    mun = defaultdict(lambda: [0] * 9)  # lula1, lula2, flavio1, flavio2, comp1, comp2, seções, ql, qf
    por_uf = defaultdict(lambda: {"locais": [], "idx": {}, "secoes": []})
    for k in sorted(v):
        l1, l2, f1, f2 = v[k]
        c1, c2 = comp.get(k, (0, 0))
        tot["lula1"] += l1; tot["lula2"] += l2; tot["flavio1"] += f1; tot["flavio2"] += f2
        tot["comp1"] += c1; tot["comp2"] += c2
        if k not in dois:
            continue
        ql, qf = l2 < l1, f2 < f1
        tot["secoes"] += 1
        tot["ql"] += ql; tot["qf"] += qf; tot["qa"] += ql and qf
        if ql and qf:
            tot["pa"] += l1 - l2 + f1 - f2
        if ql:
            tot["pl"] += l1 - l2
            dist["l"][faixa(l1 - l2)] += 1
        if qf:
            tot["pf"] += f1 - f2
            dist["f"][faixa(f1 - f2)] += 1
        u = ufs[k[0]]
        for i, x in enumerate((1, ql, qf, ql and qf, l1, l2, f1, f2, c1, c2)):
            u[i] += x
        m = mun[(k[0], k[1])]
        for i, x in enumerate((l1, l2, f1, f2, c1, c2, 1, ql, qf)):
            m[i] += x
        if ql or qf:
            p = por_uf[k[0]]
            nl = local.get(k, "")
            if nl not in p["idx"]:
                p["idx"][nl] = len(p["locais"])
                p["locais"].append(nl)
            p["secoes"].append([k[1], k[2], k[3], p["idx"][nl], c1, c2, l1, l2, f1, f2])

    nm = nomes_mun()
    linhas_mun = [[u, t, nm.get((u, t)) or nomes_tse_extra.get((u, t), t)] + x for (u, t), x in sorted(mun.items())]
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "secoes").mkdir(exist_ok=True)
    resumo = {
        "gerado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tot": tot, "faixas": FAIXAS, "dist": dist,
        "ufs": {u: x for u, x in sorted(ufs.items())},
        "mun": linhas_mun,
    }
    (SAIDA / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for u, p in por_uf.items():
        (SAIDA / "secoes" / f"{u}.json").write_text(
            json.dumps({"locais": p["locais"], "secoes": p["secoes"]}, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    print("totais:", tot)
    print("faixas Lula:", dist["l"], "Flávio:", dist["f"])
    print("municípios com queda: Lula", sum(1 for x in mun.values() if x[1] < x[0]),
          "Flávio", sum(1 for x in mun.values() if x[3] < x[2]))
    tam = sum(f.stat().st_size for f in (SAIDA / "secoes").iterdir()) // 1024
    print(f"gravado {SAIDA} (resumo {(SAIDA / 'resumo.json').stat().st_size // 1024} KB, seções {tam} KB)")


nomes_tse_extra = {}

if __name__ == "__main__":
    main()
