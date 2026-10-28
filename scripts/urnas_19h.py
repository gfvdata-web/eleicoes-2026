"""
Gera os dados de 2turno-urnas.html: urnas do 2º turno (25/10/2026) que ficaram abertas depois das 17h, quando o
STF prorrogou a votação até as 19h (horário de Brasília) nas seções que ainda não tinham encerrado. O TSE não
publicou lista dessas seções; a página usa o horário de encerramento gravado no boletim de urna (BU).

Critério: urna "postergada" = encerrou depois de LIMITE (17h30) no horário de Brasília. O BU traz o horário local;
o fuso de cada urna sai da abertura (todas abriram às 8h de Brasília): fuso = round(hora local de abertura − 8h).
Urna com abertura fora do padrão herda o fuso mais comum do município. O exterior (ZZ) fica de fora.

Fonte: dados abertos do TSE, "Boletim de urna" do 2º turno (bweb_2t_<UF>_<data>.zip, um por UF); só o cargo
Presidente é lido. Os links saem da API do portal (package resultados-2026-boletim-de-urna).

Saída em docs/data/urnas19h/:
  resumo.json   critério, totais do Brasil e de cada UF por grupo (não postergadas × postergadas), histograma
                dos horários de encerramento e municípios com mais urnas postergadas
  secoes.json   uma linha por urna postergada, com município, zona, seção, encerramento e votos

Uso: python scripts/urnas_19h.py [--baixar] [--manter]
  --baixar   baixa de novo os zips para apuracao-bruto/urnas19h/ (senão usa os que já estão lá)
  --manter   não apaga os zips no fim
"""

import csv
import io
import json
import sys
import urllib.request
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "apuracao-bruto" / "urnas19h"
SAIDA = RAIZ / "docs" / "data" / "urnas19h"
API = "https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-2026-boletim-de-urna"
UFS = ("AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO").split()
LIMITE = 17 * 60 + 30            # minutos desde 0h, horário de Brasília
DECISAO = "17h03"
HIST_INI, HIST_FIM, HIST_PASSO = 16 * 60 + 30, 19 * 60 + 30, 15   # faixas do histograma (Brasília)
NUMEROS = {"13": "lula", "22": "flavio"}


def baixar():
    BRUTO.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        recursos = json.load(r)["result"]["resources"]
    urls = {}
    for rec in recursos:
        u = rec["url"].removesuffix(".sha512")      # o portal às vezes aponta o recurso para o hash
        nome = u.rsplit("/", 1)[-1]
        if nome.startswith("bweb_2t_") and nome.endswith(".zip"):
            urls[nome.split("_")[2]] = u
    faltam = [uf for uf in UFS if uf not in urls]
    if faltam:
        sys.exit("sem BU do 2º turno para: " + ", ".join(faltam))

    def um(uf):
        req = urllib.request.Request(urls[uf], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=900) as r, open(BRUTO / f"bweb_2t_{uf}.zip", "wb") as f:
            while bloco := r.read(1 << 20):
                f.write(bloco)
        print("  baixado", uf, flush=True)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(um, UFS))


def linhas(uf):
    with zipfile.ZipFile(BRUTO / f"bweb_2t_{uf}.zip") as z:
        nome = next(n for n in z.namelist() if n.endswith(".csv"))
        with z.open(nome) as f:
            yield from csv.DictReader(io.TextIOWrapper(f, encoding="latin-1", newline=""), delimiter=";")


def minutos(dt):
    """'2026-10-25 15:00:48' → minutos desde 0h do dia 25 (pode passar de 1440 se for no dia seguinte)."""
    try:
        t = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return (t.day - 25) * 1440 + t.hour * 60 + t.minute + t.second / 60


def hhmm(m):
    m = int(m)
    return f"{m // 60:02d}:{m % 60:02d}"


def ler_uf(uf):
    """Uma entrada por urna (seção principal), só o cargo Presidente."""
    urnas = {}
    for ln in linhas(uf):
        if ln["CD_CARGO_PERGUNTA"] != "1":
            continue
        chave = (ln["CD_MUNICIPIO"], ln["NR_ZONA"], ln["NR_SECAO"])
        u = urnas.get(chave)
        if u is None:
            u = urnas[chave] = {
                "mun": ln["CD_MUNICIPIO"], "nome": ln["NM_MUNICIPIO"], "zona": int(ln["NR_ZONA"]),
                "secao": int(ln["NR_SECAO"]), "local": int(ln["NR_LOCAL_VOTACAO"]),
                "aptos": int(ln["QT_APTOS"]), "comp": int(ln["QT_COMPARECIMENTO"]),
                "abre": minutos(ln["DT_ABERTURA"]), "fecha": minutos(ln["DT_ENCERRAMENTO"]),
                "tipo": ln["DS_TIPO_URNA"], "lula": 0, "flavio": 0, "brancos": 0, "nulos": 0,
            }
        tipo = ln["DS_TIPO_VOTAVEL"].lower()
        q = int(ln["QT_VOTOS"])
        if tipo.startswith("nominal") and ln["NR_VOTAVEL"] in NUMEROS:
            u[NUMEROS[ln["NR_VOTAVEL"]]] += q
        elif tipo.startswith("branco"):
            u["brancos"] += q
        elif tipo.startswith("nulo"):
            u["nulos"] += q
    # fuso pela abertura (8h de Brasília); um município tem um fuso só, então toda urna usa o mais comum
    # do município (corrige urnas que abriram atrasadas, por substituição)
    por_mun = defaultdict(Counter)
    for u in urnas.values():
        if u["abre"] is not None:
            f = round((8 * 60 - u["abre"]) / 60)
            if 0 <= f <= 2 and abs(u["abre"] + f * 60 - 8 * 60) <= 10:
                por_mun[u["mun"]][f] += 1
    for u in urnas.values():
        u["fuso"] = por_mun[u["mun"]].most_common(1)[0][0] if por_mun[u["mun"]] else 0
        u["fecha_bsb"] = None if u["fecha"] is None else u["fecha"] + u["fuso"] * 60
    return list(urnas.values())


def grupo():
    return {"urnas": 0, "aptos": 0, "comparecimento": 0, "lula": 0, "flavio": 0, "brancos": 0, "nulos": 0}


def somar(g, u):
    g["urnas"] += 1
    g["aptos"] += u["aptos"]
    g["comparecimento"] += u["comp"]
    for k in ("lula", "flavio", "brancos", "nulos"):
        g[k] += u[k]


def main():
    args = sys.argv[1:]
    if "--baixar" in args or not all((BRUTO / f"bweb_2t_{uf}.zip").exists() for uf in UFS):
        print("baixando os boletins de urna do 2º turno...")
        baixar()

    br = {"nao_post": grupo(), "post": grupo(), "sem_horario": 0}
    ufs, secoes = {}, []
    nbin = (HIST_FIM - HIST_INI) // HIST_PASSO
    hist = {"antes": 0, "faixas": [0] * nbin, "depois": 0}
    for uf in UFS:
        urnas = ler_uf(uf)
        r = {"nao_post": grupo(), "post": grupo(), "sem_horario": 0, "fusos": sorted({u["fuso"] for u in urnas})}
        muns = Counter()
        for u in urnas:
            fb = u["fecha_bsb"]
            if fb is None:
                r["sem_horario"] += 1
            if fb is not None and fb > LIMITE:
                somar(r["post"], u)
                muns[u["nome"]] += 1
                secoes.append([uf, u["nome"], u["zona"], u["secao"], u["local"], hhmm(fb),
                               u["aptos"], u["comp"], u["flavio"], u["lula"], u["brancos"], u["nulos"]])
            else:
                somar(r["nao_post"], u)
            if fb is not None:
                if fb < HIST_INI:
                    hist["antes"] += 1
                elif fb >= HIST_FIM:
                    hist["depois"] += 1
                else:
                    hist["faixas"][int((fb - HIST_INI) // HIST_PASSO)] += 1
        r["municipios"] = muns.most_common(8)
        ufs[uf] = r
        for g in ("nao_post", "post"):
            for k, v in r[g].items():
                br[g][k] += v
        br["sem_horario"] += r["sem_horario"]
        print(f"  {uf}: {r['post']['urnas']:>6} postergadas de {r['post']['urnas'] + r['nao_post']['urnas']:>7}"
              f"  fusos {r['fusos']}", flush=True)

    secoes.sort(key=lambda s: (s[0], s[1], s[2], s[3]))
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    resumo = {
        "gerado_em": agora,
        "criterio": {"limite": hhmm(LIMITE), "decisao": DECISAO, "fuso": "horário de Brasília",
                     "texto": "urna que encerrou depois das 17h30 (horário de Brasília), pelo horário gravado no boletim de urna"},
        "fonte": "TSE, dados abertos: Boletim de urna, 2º turno (arquivos de 26/10/2026), cargo Presidente",
        "candidatos": {"flavio": {"nome": "Flávio Bolsonaro", "partido": "PL"}, "lula": {"nome": "Lula", "partido": "PT"}},
        "br": br,
        "ufs": ufs,
        "histograma": {"inicio": hhmm(HIST_INI), "passo": HIST_PASSO, **hist},
    }
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (SAIDA / "secoes.json").write_text(json.dumps({
        "gerado_em": agora,
        "colunas": ["uf", "municipio", "zona", "secao", "local", "encerramento", "aptos", "comparecimento",
                    "flavio", "lula", "brancos", "nulos"],
        "secoes": secoes}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    p, n = br["post"], br["nao_post"]
    print(f"Brasil: {p['urnas']} urnas postergadas de {p['urnas'] + n['urnas']} ({br['sem_horario']} sem horário)")
    print(f"  total BU: Lula {p['lula'] + n['lula']}, Flávio {p['flavio'] + n['flavio']}")
    if "--manter" not in args:
        for uf in UFS:
            (BRUTO / f"bweb_2t_{uf}.zip").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
