"""
Gera docs/data/voto-cruzado/estados-metricas.json: métricas por estado para a subaba "Tabela de estados" de voto-cruzado.html.
Usa a classificação PADRÃO (classificacao.json), sem as reclassificações que o leitor faz no navegador.
O modelo é o mesmo da página (função ajustar): regressão ponderada pelo comparecimento do % do grupo para presidente sobre o
% do mesmo grupo nos outros 4 cargos, por urna; cargo com média < 3% ou desvio-padrão < 2 p.p. sai do ajuste (peso 0).
Só biblioteca padrão. Rode depois de scripts/voto_cruzado.py e scripts/alinhamento.py.

Saída: {gerado, limiar, regua: {"a"|"b": {UF|"BR": {n, votantes, ind: {med, p90, n10},
         g: {"0"|"2": {y, r2, erro, b, fora, acima, abaixo, p10, p90}}}}}}
  y = % do grupo para presidente; acima/abaixo = nº de urnas com diferença (real − previsto) > +10 p.p. / < −10 p.p.;
  p10/p90 = faixa do % do grupo para presidente que contém 80% dos votantes; ind = índice de anomalia (raiz da média dos
  quadrados dos erros dos dois lados), mediana, percentil 90 e nº de urnas acima de 10 p.p.
  "BR" = todas as urnas do país num modelo só (na página, a unidade "Estados" ajusta por município).

Uso: python scripts/metricas_estados.py
"""

import json
import math
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "docs" / "data" / "voto-cruzado"
UFS = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
       "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
VAZIO_MED, VAZIO_DP, LIMIAR = 0.03, 0.02, 0.10


def grupo(cls, cand, reg, uf, e):
    k, num, _nome, sg = e
    if reg == "b":
        return cls["b"].get(sg)
    if k == 0:
        return cls["a"]["pres"].get(num, 1)
    if k <= 2:
        return cand[uf].get((k, num), 1)
    return cls["a"]["dep"].get(sg, 1)


def linhas(d, gs):
    """[comparecimento, (válidos, g0, g1, g2) × 5] por urna."""
    ks = [e[0] for e in d["ent"]]
    out = []
    for r in d["secoes"]:
        o = [r[4]] + [0] * 20
        for j in range(5, len(r), 2):
            e, q = r[j], r[j + 1]
            k = ks[e]
            o[1 + 4 * k] += q
            if gs[e] is not None:
                o[2 + 4 * k + gs[e]] += q
        out.append(o)
    return out


def parte(o, k, g):
    v = o[1 + 4 * k]
    return o[2 + 4 * k + g] / v if v else None


def ajustar(rows, g):
    xs = []
    for o in rows:
        w, y = o[0], parte(o, 0, g)
        x = [1.0] + [parte(o, k, g) for k in range(1, 5)]
        if w and y is not None and None not in x:
            xs.append((w, x, y))
    W = sum(w for w, _, _ in xs)
    fora = []
    for k in range(1, 5):
        med = sum(w * x[k] for w, x, _ in xs) / W
        dp = math.sqrt(sum(w * (x[k] - med) ** 2 for w, x, _ in xs) / W)
        if med < VAZIO_MED or dp < VAZIO_DP:
            fora.append([k, round(med, 4)])
    usa = [k for k in range(5) if k not in {f[0] for f in fora}]
    n = len(usa)
    A = [[0.0] * (n + 1) for _ in range(n)]
    sw = sy = syy = 0.0
    for w, xx, y in xs:
        x = [xx[k] for k in usa]
        for i in range(n):
            xi = w * x[i]
            for j in range(n):
                A[i][j] += xi * x[j]
            A[i][n] += xi * y
        sw += w; sy += w * y; syy += w * y * y
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i:
                f = A[r][i] / A[i][i]
                for c in range(i, n + 1):
                    A[r][c] -= f * A[i][c]
    b = [0.0] * 5
    for i, k in enumerate(usa):
        b[k] = A[i][n] / A[i][i]
    return b, fora, (sw, sy, syy)


def prever(o, g, b):
    y = b[0]
    for k in range(1, 5):
        if b[k]:
            p = parte(o, k, g)
            if p is None:
                return None
            y += b[k] * p
    return max(0.0, min(1.0, y))


def quantil(v, q):
    v = sorted(v)
    if not v:
        return None
    i = (len(v) - 1) * q
    lo, hi = math.floor(i), math.ceil(i)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def metricas(rows):
    res = {"n": len(rows), "votantes": sum(o[0] for o in rows), "g": {}}
    resid = {}
    for g in (0, 2):
        b, fora, (sw, sy, syy) = ajustar(rows, g)
        sr = 0.0; acima = abaixo = 0; difs = []; ys = []
        for o in rows:
            y = parte(o, 0, g)
            if y is None:
                difs.append(None); continue
            ys.append((y, o[0]))
            p = prever(o, g, b)
            if p is None or not o[0]:
                difs.append(None); continue
            d = y - p
            difs.append(d)
            sr += o[0] * d * d
            acima += d > LIMIAR; abaixo += d < -LIMIAR
        resid[g] = difs
        tv = sum(o[1 + 0] for o in rows)
        y_tot = sum(o[2 + g] for o in rows) / tv if tv else None
        ys.sort(); tot = sum(w for _, w in ys); acc = 0; p10 = p90 = None
        for y, w in ys:
            acc += w
            if p10 is None and acc >= .1 * tot: p10 = y
            if p90 is None and acc >= .9 * tot: p90 = y; break
        res["g"][str(g)] = {"y": round(y_tot, 4), "r2": round(1 - sr / (syy - sy * sy / sw), 4), "erro": round(math.sqrt(sr / sw), 4),
                            "b": [round(x, 4) for x in b], "fora": fora, "acima": acima, "abaixo": abaixo,
                            "p10": round(p10, 4), "p90": round(p90, 4)}
    ind = [math.sqrt((a * a + c * c) / 2) for a, c in zip(resid[0], resid[2]) if a is not None and c is not None]
    res["ind"] = {"med": round(quantil(ind, .5), 4), "p90": round(quantil(ind, .9), 4), "n10": sum(x > LIMIAR for x in ind)}
    return res


def main():
    cls = json.loads((DADOS / "classificacao.json").read_text(encoding="utf-8"))
    cand = {uf: {(r[0], r[1]): r[6] for r in l} for uf, l in cls["a"]["cand"].items()}
    saida = {"gerado": datetime.now().strftime("%d/%m/%Y %H:%M"), "limiar": LIMIAR, "regua": {"a": {}, "b": {}}}
    todas = {"a": [], "b": []}
    for uf in UFS:
        d = json.loads((DADOS / f"{uf.lower()}.json").read_text(encoding="utf-8"))
        for reg in ("a", "b"):
            rows = linhas(d, [grupo(cls, cand, reg, uf, e) for e in d["ent"]])
            saida["regua"][reg][uf] = metricas(rows)
            todas[reg] += rows
        print(uf, flush=True)
    for reg in ("a", "b"):
        saida["regua"][reg]["BR"] = metricas(todas[reg])
    (DADOS / "estados-metricas.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("estados-metricas.json gravado")


if __name__ == "__main__":
    main()
