"""
Gera os dados de urnas-zero.html: as seções eleitorais (urnas) em que Flávio Bolsonaro teve até 10 votos no
2º turno de 2026 e como essas mesmas seções votaram no 2º turno de presidente em 2022 e 2018. Só biblioteca padrão.

Entrada (dados abertos do TSE, https://cdn.tse.jus.br/estatistica/sead/odsele/), em apuracao-bruto/urnas-zero/:
  votacao_secao_<ano>_BR.zip          votos de presidente por seção (1º e 2º turnos)
  detalhe_votacao_secao_<ano>.zip     aptos, comparecimento, local, seção instalada/anulada (arquivo _BR.csv)
e apuracao-bruto/secoes-br/eleitorado_local_votacao_2026.zip (tipo do local e coordenadas, de voto_cruzado.py).
Nomes dos municípios: docs/data/uf/<uf>/municipios.json e docs/data/es/municipios.js.

Casamento entre eleições: pela mesma chave (UF, município, zona, seção). O TSE renumera e funde seções, então o
local de votação de cada ano é comparado ao de 2026 (nome normalizado): 1 = mesmo local, 2 = local diferente,
0 = a seção não existia naquele ano.

Saída docs/data/urnas-zero/urnas.json:
  gerado, criterio, tot {ano: [lula/PT, bolsonaro, secoes, secoes com bolsonaro <= criterio]} (país todo, 2º turno),
  ufs {UF: [seções 2026, urnas zero]}, mun {"UF-tse": nome},
  locais [[nome, tipo, lon, lat]] (tipo do TSE: 1 convencional, 2 voto em trânsito, 3 preso provisório, 4 temporário;
          0 = sem cadastro de local, como no exterior),
  secoes [[uf, tse, zona, seção, local, aptos, comp, flávio, lula, brancos+nulos, flávio 1ºt, lula 1ºt,
           casa22, bolsonaro22, lula22, comp22, casa18, bolsonaro18, haddad18, comp18]]
  nomes22 / nomes18 {índice da seção: nome do local naquele ano} (só quando o local é diferente).

Uso: python scripts/urnas_zero.py [--baixar]
"""

import csv
import io
import json
import re
import sys
import unicodedata
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto"
PASTA = BRUTO / "urnas-zero"
SAIDA = RAIZ / "docs" / "data" / "urnas-zero"
CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele/"
ANOS = [2026, 2022, 2018]
CRITERIO = 10
# número do candidato do PT e do candidato da família Bolsonaro no 2º turno de cada ano
PT = {2026: "13", 2022: "13", 2018: "13"}
BOLS = {2026: "22", 2022: "22", 2018: "17"}


def baixar():
    PASTA.mkdir(parents=True, exist_ok=True)
    for a in ANOS:
        for sub, nome in (("votacao_secao", f"votacao_secao_{a}_BR.zip"),
                          ("detalhe_votacao_secao", f"detalhe_votacao_secao_{a}.zip")):
            print("baixando", nome)
            req = urllib.request.Request(CDN + f"{sub}/{nome}", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=600) as r, open(PASTA / nome, "wb") as f:
                while bloco := r.read(1 << 20):
                    f.write(bloco)


def linhas(zip_caminho, csv_nome):
    with zipfile.ZipFile(zip_caminho) as z, z.open(csv_nome) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")


def chave(r):
    return (r["SG_UF"], r["CD_MUNICIPIO"].lstrip("0"), int(r["NR_ZONA"]), int(r["NR_SECAO"]))


def norm(s):
    s = unicodedata.normalize("NFKD", s.upper()).encode("ascii", "ignore").decode()
    return set(re.findall(r"[A-Z0-9]{3,}", s))


def mesmo_local(a, b):
    ta, tb = norm(a), norm(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.5


def votos(ano, so=None):
    """chave → {turno: {número: votos}} (só presidente); com `so`, só as chaves desse conjunto."""
    v = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for r in linhas(PASTA / f"votacao_secao_{ano}_BR.zip", f"votacao_secao_{ano}_BR.csv"):
        if r["CD_CARGO"] != "1":
            continue
        k = chave(r)
        if so is not None and k not in so:
            continue
        v[k][r["NR_TURNO"]][r["NR_VOTAVEL"]] += int(r["QT_VOTOS"])
    return v


def detalhe(ano, so):
    """chave → (aptos, comparecimento, nome do local) no 2º turno, só seções não anuladas."""
    d = {}
    for r in linhas(PASTA / f"detalhe_votacao_secao_{ano}.zip", f"detalhe_votacao_secao_{ano}_BR.csv"):
        if r["CD_CARGO"] != "1" or r["NR_TURNO"] != "2":
            continue
        k = chave(r)
        if k in so and r["ST_SECAO_ANULADA"] not in ("Sim", "S"):
            d[k] = (int(r["QT_APTOS"]), int(r["QT_COMPARECIMENTO"]), r["NM_LOCAL_VOTACAO"])
    return d


def nomes_mun():
    t = {}
    for uf_dir in (RAIZ / "docs" / "data" / "uf").iterdir():
        f = uf_dir / "municipios.json"
        if f.exists():
            for m in json.loads(f.read_text(encoding="utf-8")):
                t[(uf_dir.name.upper(), m["tse"].lstrip("0"))] = m["nome"]
    txt = (RAIZ / "docs" / "data" / "es" / "municipios.js").read_text(encoding="utf-8")
    for m in json.loads(txt[txt.index("["):txt.rindex("]") + 1]):
        t[("ES", m["tse"].lstrip("0"))] = m["nome"]
    return t


def locais_2026(so):
    """chave → (nome do local, tipo, lon, lat), de eleitorado_local_votacao_2026."""
    z = zipfile.ZipFile(BRUTO / "secoes-br" / "eleitorado_local_votacao_2026.zip")
    t = {}
    for nome in z.namelist():
        if not nome.endswith(".csv"):
            continue
        for r in csv.DictReader(io.TextIOWrapper(z.open(nome), encoding="latin-1"), delimiter=";"):
            k = chave(r)
            if k not in so:
                continue
            tipo = int(r["CD_TIPO_LOCAL"])
            try:
                lon = round(float(r["NR_LONGITUDE"].replace(",", ".")), 5)
                lat = round(float(r["NR_LATITUDE"].replace(",", ".")), 5)
                if lon == -1 or lat == -1:
                    lon = lat = None
            except ValueError:
                lon = lat = None
            t[k] = (r["NM_LOCAL_VOTACAO"], tipo, lon, lat)
    return t


def main():
    if "--baixar" in sys.argv:
        baixar()

    tot = {}
    print("2026 …")
    v26 = votos(2026)
    t2 = {k: x["2"] for k, x in v26.items() if "2" in x}
    tot[2026] = [sum(x.get(PT[2026], 0) for x in t2.values()), sum(x.get(BOLS[2026], 0) for x in t2.values()),
                 len(t2), sum(1 for x in t2.values() if x.get(BOLS[2026], 0) <= CRITERIO)]
    ufs = defaultdict(lambda: [0, 0])
    for k in t2:
        ufs[k[0]][0] += 1
    zero = {k for k, x in t2.items() if x.get(BOLS[2026], 0) <= CRITERIO and sum(x.values()) > 0}
    for k in zero:
        ufs[k[0]][1] += 1
    print(f"  {len(t2)} seções, {len(zero)} urnas zero")

    det = {2026: detalhe(2026, zero)}
    hist = {}
    for a in (2022, 2018):
        print(a, "…")
        va = votos(a)
        ta = {k: x["2"] for k, x in va.items() if "2" in x}
        tot[a] = [sum(x.get(PT[a], 0) for x in ta.values()), sum(x.get(BOLS[a], 0) for x in ta.values()),
                  len(ta), sum(1 for x in ta.values() if x.get(BOLS[a], 0) <= CRITERIO)]
        hist[a] = {k: ta[k] for k in zero if k in ta}
        det[a] = detalhe(a, set(hist[a]))
        del va, ta

    loc = locais_2026(zero)
    mun = nomes_mun()
    locais, idx_local, secoes, nomes = [], {}, [], {2022: {}, 2018: {}}
    for k in sorted(zero):
        uf, tse, zona, sec = k
        x2, x1 = v26[k]["2"], v26[k].get("1", {})
        aptos, comp, nome26 = det[2026].get(k, (0, 0, ""))
        nl, tipo, lon, lat = loc.get(k, (nome26, 0, None, None))
        chave_l = (uf, tse, nl, lon, lat)
        if chave_l not in idx_local:
            idx_local[chave_l] = len(locais)
            locais.append([nl, tipo, lon, lat])
        linha = [uf, tse, zona, sec, idx_local[chave_l], aptos, comp, x2.get("22", 0), x2.get("13", 0),
                 x2.get("95", 0) + x2.get("96", 0), x1.get("22", 0), x1.get("13", 0)]
        for a in (2022, 2018):
            if k not in hist[a]:
                linha += [0, 0, 0, 0]
                continue
            ap, cp, na = det[a].get(k, (0, 0, ""))
            casa = 1 if mesmo_local(nl or nome26, na) else 2
            if casa == 2:
                nomes[a][len(secoes)] = na
            linha += [casa, hist[a][k].get(BOLS[a], 0), hist[a][k].get(PT[a], 0), cp]
        secoes.append(linha)

    nomes_tse = {(k[0], k[1]) for k in zero}
    # nomes que faltam (exterior e municípios sem arquivo): do próprio CSV do detalhe de 2026
    if any(mun.get(k) is None for k in nomes_tse):
        for r in linhas(PASTA / "detalhe_votacao_secao_2026.zip", "detalhe_votacao_secao_2026_BR.csv"):
            k = (r["SG_UF"], r["CD_MUNICIPIO"].lstrip("0"))
            if k in nomes_tse and mun.get(k) is None:
                mun[k] = r["NM_MUNICIPIO"].title()
    saida = {
        "gerado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "criterio": CRITERIO,
        "tot": {str(a): t for a, t in tot.items()},
        "ufs": {u: c for u, c in sorted(ufs.items())},
        "mun": {f"{u}-{t}": mun.get((u, t)) for (u, t) in sorted(nomes_tse)},
        "locais": locais,
        "secoes": secoes,
        "nomes22": nomes[2022],
        "nomes18": nomes[2018],
    }
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "urnas.json").write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("totais 2º turno (PT, Bolsonaro, seções, seções com Bolsonaro <= critério):", tot)
    for a, i in ((2022, 12), (2018, 16)):
        c = [s[i] for s in secoes]
        print(f"  {a}: mesmo local {c.count(1)}, local diferente {c.count(2)}, não existia {c.count(0)}")
    print(f"gravado {SAIDA / 'urnas.json'} ({(SAIDA / 'urnas.json').stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
