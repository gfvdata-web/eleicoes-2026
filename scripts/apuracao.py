"""
Coleta da apuração do TSE e publicação no site (eleição de 04/10/2026).

A cada minuto, confere cada cargo e cada UF no TSE. Se o dado mudou, baixa,
converte para o formato do site e grava em docs/data/apuracao/<cargo>.json.
Publica (commit + push só desses arquivos) no máximo a cada INTERVALO_PUBLICACAO.

Uso:
  python scripts/apuracao.py --simular        # dados falsos, só local (nunca publica)
  python scripts/apuracao.py                  # coleta real, sem publicar
  python scripts/apuracao.py --publicar       # coleta real e publica no GitHub
  python scripts/apuracao.py --uma-vez        # roda um ciclo e sai
  python scripts/apuracao.py --limpar         # zera os arquivos do site

Só usa a biblioteca padrão do Python. Ctrl+C encerra.
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuração
# ----------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs" / "data" / "apuracao"      # o que o site lê
BRUTO = RAIZ / "apuracao-bruto"                  # cópia do que veio do TSE (fora do site, ignorado pelo git)

INTERVALO_COLETA = 60        # segundos entre conferências no TSE
INTERVALO_PUBLICACAO = 120   # segundos mínimos entre dois pushes
TIMEOUT = 20                 # segundos por requisição
PARALELO = 8                 # downloads simultâneos

UFS = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB",
       "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]

# (id do arquivo, rótulo no terminal, locais). Presidente: BR = Brasil, ZZ = exterior.
CARGOS = [
    ("presidente", "Presidente", ["BR"] + UFS + ["ZZ"]),
    ("governador", "Governador", UFS),
    ("senador", "Senador", UFS),
    ("deputado-federal", "Dep. federal", UFS),
    ("deputado-estadual", "Dep. estadual", UFS),   # no DF, deputado distrital
]

# Endereços do TSE: preencher quando a divulgação abrir. Use {uf} (minúsculo) ou {UF}.
# Enquanto for None, o cargo aparece como "sem endereço" e é pulado.
_BASE = "https://resultados.tse.jus.br/oficial/ele2026"
URLS = {
    "presidente": _BASE + "/6257/dados/{uf}/{uf}-c0001-e006257-u.json",
    "governador": _BASE + "/6259/dados/{uf}/{uf}-c0003-e006259-u.json",
    "senador": _BASE + "/6259/dados/{uf}/{uf}-c0005-e006259-u.json",
    "deputado-federal": _BASE + "/6259/dados/{uf}/{uf}-c0006-e006259-u.json",
    "deputado-estadual": _BASE + "/6259/dados/{uf}/{uf}-c0007-e006259-u.json",   # DF: c0008 (distrital)
}

# Correções manuais de nome: (cargo, UF, nome no TSE) -> nome igual ao de dados.js / senado.js
APELIDOS = {
    # ("governador", "GO", "ZE DA SILVA"): "José da Silva",
}

# Listas de candidatos do site, para casar os nomes do TSE com os nossos
LISTAS = {"governador": RAIZ / "docs" / "data" / "dados.js", "senador": RAIZ / "docs" / "data" / "senado.js"}


def converter(cargo, uf, bruto):
    """Converte o JSON "-u.json" do TSE (2026) para o formato do site (ver apuracao.md).
    Retorna None se o local ainda não tem dado."""
    carg = bruto["carg"][0]
    pct = float(str(bruto.get("s", {}).get("pst", "0")).replace(",", "."))
    res, eleito, turno2 = [], False, False
    for agr in carg.get("agr", []):
        for par in agr.get("par", []):
            for cd in par.get("cand", []):
                vap = int(cd.get("vap") or 0)
                res.append((vap, [cd.get("nmu") or cd["nm"], float(str(cd.get("pvapn") or cd.get("pvap") or 0).replace(",", ".")), par["sg"], vap]))
                eleito |= cd.get("e") == "s"
                turno2 |= "2" in (cd.get("st") or "")
    if not res or pct <= 0:
        return None
    res.sort(key=lambda r: -r[0])
    if cargo.startswith("deputado"):
        res = res[:30]   # só os mais votados, para o arquivo não crescer demais
    return {"pct": pct, "hora": bruto.get("ht") or bruto.get("hg") or "",
            "res": [[n, round(v, 2), p, vap] for vap, (n, v, p, _) in res],
            "situacao": "eleito" if eleito else "2turno" if turno2 else None}


# ----------------------------------------------------------------------------
# Terminal
# ----------------------------------------------------------------------------

os.system("")  # ativa cores ANSI no console do Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COR = {"cinza": "\033[90m", "verde": "\033[32m", "amarelo": "\033[33m", "vermelho": "\033[31m",
       "ciano": "\033[36m", "negrito": "\033[1m", "fim": "\033[0m"}


def c(texto, *cores):
    return "".join(COR[k] for k in cores) + str(texto) + COR["fim"]


def agora():
    return dt.datetime.now().strftime("%H:%M:%S")


def pct_br(v):
    return f"{v:.2f}".replace(".", ",") + "%"


ANTERIOR = {}   # chave -> % apurado no ciclo anterior


def variacao(chave, pct):
    """Texto com o aumento do % apurado desde o ciclo anterior (e guarda o valor atual)."""
    ant = ANTERIOR.get(chave)
    ANTERIOR[chave] = pct
    if ant is None:
        return ""
    d = pct - ant
    if abs(d) < 0.005:
        return c(" (sem mudança)", "cinza")
    return c(f" ({'+' if d > 0 else '−'}{abs(d):.2f}".replace(".", ",") + " p.p.)", "verde" if d > 0 else "vermelho")


def log(msg=""):
    print("\r\033[K" + msg, flush=True)


# ----------------------------------------------------------------------------
# Nomes: casar o nome de urna do TSE com o nome usado no site
# ----------------------------------------------------------------------------

def normalizar(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9 ]", " ", s.upper()).split()


def carregar_listas():
    """{(cargo, UF): [nomes]} lidos de dados.js e senado.js."""
    conhecidos = {}
    for cargo, arq in LISTAS.items():
        texto = arq.read_text(encoding="utf-8")
        blocos = re.split(r'\buf:\s*"', texto)[1:]
        for b in blocos:
            uf = b[:2]
            cand = b.split("candidatos:", 1)
            if len(cand) == 2:
                conhecidos[(cargo, uf)] = re.findall(r'nome:\s*"([^"]+)"', cand[1])
    return conhecidos


def casar(cargo, uf, nome_tse, conhecidos):
    """Devolve (nome do site, encontrado?)."""
    if (cargo, uf, nome_tse) in APELIDOS:
        return APELIDOS[(cargo, uf, nome_tse)], True
    lista = conhecidos.get((cargo, uf))
    if not lista:
        return nome_tse, True   # cargo sem lista no site: usa o nome do TSE
    t = normalizar(nome_tse)
    for n in lista:
        if normalizar(n) == t:
            return n, True
    # um nome contém o outro (ex.: "MAILZA" x "Mailza Assis")
    cands = [n for n in lista if set(normalizar(n)) <= set(t) or set(t) <= set(normalizar(n))]
    if len(cands) == 1:
        return cands[0], True
    return nome_tse, False


# ----------------------------------------------------------------------------
# Coleta
# ----------------------------------------------------------------------------

class Local:
    """Estado de um (cargo, UF) entre ciclos."""
    def __init__(self):
        self.etag = None
        self.modificado = None
        self.hash = None
        self.dado = None      # último dado convertido
        self.status = "—"     # novo | igual | pendente | erro | sem endereço


def baixar(url, loc):
    """Requisição condicional: só baixa de novo se o TSE mudou o arquivo."""
    cab = {"User-Agent": "eleicoes-2026 (site estatico de apuracao)", "Accept": "application/json"}
    if loc.etag:
        cab["If-None-Match"] = loc.etag
    if loc.modificado:
        cab["If-Modified-Since"] = loc.modificado
    req = urllib.request.Request(url, headers=cab)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return 200, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, None, e.headers
    except Exception as e:
        return 0, str(e).encode(), {}


def coletar_real(cargo, uf, loc, conhecidos, avisos):
    modelo = URLS.get(cargo)
    if not modelo:
        loc.status = "sem endereço"
        return False
    url = modelo.format(uf=uf.lower(), UF=uf)
    if cargo == "deputado-estadual" and uf == "DF":
        url = url.replace("c0007", "c0008")
    cod, corpo, cab = baixar(url, loc)
    if cod == 304:
        loc.status = "igual"
        return False
    if cod in (403, 404):
        loc.status = "pendente"
        return False
    if cod != 200:
        loc.status = "erro"
        avisos.append(f"{cargo} {uf}: HTTP {cod or 'falha de rede'} {(corpo or b'')[:80].decode(errors='ignore')}")
        return False
    loc.etag, loc.modificado = cab.get("ETag"), cab.get("Last-Modified")
    h = hashlib.sha1(corpo).hexdigest()
    if h == loc.hash:
        loc.status = "igual"
        return False
    (BRUTO / cargo).mkdir(parents=True, exist_ok=True)
    (BRUTO / cargo / f"{uf}.json").write_bytes(corpo)
    try:
        dado = converter(cargo, uf, json.loads(corpo))
    except NotImplementedError as e:
        loc.status = "erro"
        avisos.append(f"{cargo} {uf}: baixado, mas {e}")
        return False
    except Exception as e:
        loc.status = "erro"
        avisos.append(f"{cargo} {uf}: arquivo inválido ({e})")
        return False
    if dado is None:
        loc.status = "pendente"
        return False
    return aplicar(cargo, uf, loc, dado, h, conhecidos, avisos)


def aplicar(cargo, uf, loc, dado, h, conhecidos, avisos):
    """Confere o dado novo, casa os nomes e guarda. Retorna True se mudou."""
    res = []
    for r in dado["res"]:
        nome, ok = casar(cargo, uf, r[0], conhecidos)
        res.append([nome] + list(r[1:]))
    dado = {**dado, "res": res}
    if loc.dado and dado["pct"] < loc.dado["pct"]:
        avisos.append(f"{cargo} {uf}: % apurado diminuiu ({pct_br(loc.dado['pct'])} → {pct_br(dado['pct'])})")
    loc.hash = h
    if dado == loc.dado:
        loc.status = "igual"
        return False
    loc.dado = dado
    loc.status = "novo"
    return True


# Simulação: dados falsos que avançam a cada ciclo, para testar terminal e página
def coletar_simulado(cargo, uf, loc, conhecidos, avisos):
    ant = loc.dado["pct"] if loc.dado else 0
    if ant == 0 and random.random() < 0.3:
        loc.status = "pendente"
        return False
    if ant >= 100 or random.random() < 0.2:
        loc.status = "igual"
        return False
    pct = min(100.0, round(ant + random.uniform(2, 15), 2))
    nomes = conhecidos.get((cargo, uf)) or [f"Candidato {l}" for l in "ABCDE"]
    base = random.Random(cargo + uf)
    pesos = [base.uniform(5, 50) * random.uniform(0.95, 1.05) for _ in nomes]
    tot = sum(pesos)
    res = sorted(([n, round(p * 100 / tot, 2), None] for n, p in zip(nomes, pesos)), key=lambda r: -r[1])
    res = [[n, v] for n, v, _ in res]
    sit = None
    if pct >= 100:
        sit = "eleito" if cargo == "senador" or res[0][1] > 50 else "2turno" if cargo in ("governador", "presidente") else None
    dado = {"pct": pct, "hora": agora(), "res": res, "situacao": sit}
    return aplicar(cargo, uf, loc, dado, str(pct), conhecidos, avisos)


# ----------------------------------------------------------------------------
# Saída e publicação
# ----------------------------------------------------------------------------

def gravar(cargo, locais, simulacao):
    """Grava docs/data/apuracao/<cargo>.json. Retorna True se o arquivo mudou."""
    ufs = {uf: {k: v for k, v in l.dado.items() if v is not None} for uf, l in locais.items() if l.dado}
    horas = [d["hora"] for d in ufs.values() if d.get("hora")]
    doc = {"cargo": cargo, "simulacao": simulacao, "atualizado": max(horas)[:5] if horas else "", "ufs": ufs}
    if not simulacao:
        doc.pop("simulacao")
    texto = json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n"
    arq = SAIDA / f"{cargo}.json"
    if arq.exists() and arq.read_text(encoding="utf-8") == texto:
        return False
    SAIDA.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8", newline="\n")
    return True


def git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout + r.stderr).strip()


def publicar():
    """Commit e push só de docs/data/apuracao/. Retorna (ok, mensagem)."""
    caminho = "docs/data/apuracao"
    git("add", caminho)
    cod, saida = git("commit", "-m", f"Apuração: atualização {agora()[:5]}", "--", caminho)
    if cod != 0:
        return ("nothing to commit" in saida or "nada a submeter" in saida), "nada novo para commitar"
    _, sha = git("rev-parse", "--short", "HEAD")
    cod, saida = git("push")
    if cod != 0:  # remoto andou (outra sessão publicou): rebase e tenta de novo
        git("pull", "--rebase", "--autostash")
        cod, saida = git("push")
        if cod != 0:
            return False, "push falhou: " + saida.splitlines()[-1]
    return True, f"commit {sha}"


def limpar():
    for cargo, _, _ in CARGOS:
        gravar(cargo, {}, False)
    print("Arquivos zerados em", SAIDA)


def retomar(cargo, locais):
    """Ao reiniciar, parte do que já está gravado (para não apagar o site se o TSE falhar).
    Arquivos de simulação são ignorados."""
    try:
        doc = json.loads((SAIDA / f"{cargo}.json").read_text(encoding="utf-8"))
    except Exception:
        return 0
    if doc.get("simulacao"):
        return 0
    n = 0
    for uf, d in doc.get("ufs", {}).items():
        if uf in locais:
            locais[uf].dado = {"situacao": None, **d}
            n += 1
    return n


# ----------------------------------------------------------------------------
# Ciclo
# ----------------------------------------------------------------------------

def pct_total(locais):
    """% apurado do cargo: o do Brasil (presidente) ou a média dos estados."""
    if "BR" in locais and locais["BR"].dado:
        return locais["BR"].dado["pct"]
    return sum(l.dado["pct"] for l in locais.values() if l.dado) / len(locais)


def resumo(cargo, rotulo, locais):
    st = [l.status for l in locais.values()]
    dados = [l.dado for l in locais.values() if l.dado]
    if st.count("sem endereço") == len(st):
        return f"  {rotulo.lower()}: " + c("sem endereço configurado", "cinza")
    if dados:
        pct = pct_total(locais)
        concl = sum(1 for d in dados if d["pct"] >= 100)
        ultimo = max(d.get("hora", "") for d in dados)
    else:
        pct, concl, ultimo = 0.0, 0, "—"
    texto = (f"  {rotulo.lower()}: {c(st.count('novo'), 'verde')} novos, {st.count('igual')} já lidos, "
             f"{c(pct_br(pct), 'negrito')}{variacao(cargo, pct)}, {concl}/{len(locais)} concluídos, dado das {c(ultimo, 'ciano')}")
    if st.count("pendente"):
        texto += c(f", {st.count('pendente')} sem dado", "cinza")
    if st.count("erro"):
        texto += c(f", {st.count('erro')} erros", "vermelho")
    return texto


def main():
    ap = argparse.ArgumentParser(description="Coleta da apuração do TSE para o site.")
    ap.add_argument("--simular", action="store_true", help="dados falsos, nunca publica")
    ap.add_argument("--publicar", action="store_true", help="faz commit e push dos dados")
    ap.add_argument("--uma-vez", action="store_true", help="roda um ciclo e sai")
    ap.add_argument("--limpar", action="store_true", help="zera os arquivos do site e sai")
    ap.add_argument("--intervalo", type=int, default=INTERVALO_COLETA, help="segundos entre ciclos (padrão 60)")
    ap.add_argument("--cargos", help="só estes cargos, separados por vírgula (ex.: governador,senador)")
    a = ap.parse_args()

    if a.limpar:
        return limpar()
    if a.simular and a.publicar:
        sys.exit("--simular nunca publica. Rode sem --publicar.")

    cargos = [x for x in CARGOS if not a.cargos or x[0] in a.cargos.split(",")]
    estado = {cargo: {uf: Local() for uf in ufs} for cargo, _, ufs in cargos}
    if not a.simular:
        retomados = sum(retomar(cargo, estado[cargo]) for cargo, _, _ in cargos)
        if retomados:
            log(c(f"Retomando {retomados} locais já gravados em {SAIDA.relative_to(RAIZ)}", "cinza"))
    for cargo, _, _ in cargos:
        ANTERIOR[cargo] = pct_total(estado[cargo])   # base da primeira variação
    conhecidos = carregar_listas()
    coletar = coletar_simulado if a.simular else coletar_real
    modo = c("SIMULAÇÃO (só local)", "amarelo", "negrito") if a.simular else (
        c("PUBLICANDO no GitHub", "vermelho", "negrito") if a.publicar else c("coleta sem publicar", "ciano"))
    log(c("Apuração 2026 — coleta do TSE", "negrito") + f" · {modo} · coleta a cada {a.intervalo}s"
        + (f", publicação a cada {INTERVALO_PUBLICACAO}s" if a.publicar else ""))

    ciclo, ultima_pub, pendente_pub = 0, 0.0, False
    while True:
        ciclo += 1
        inicio = time.time()
        log()
        log(c(f"════ {agora()} · ciclo {ciclo} ", "negrito") + "═" * 40)
        avisos, mudou_algo = [], False
        for cargo, rotulo, ufs in cargos:
            print(f"\r\033[K  Tentando ler {c(rotulo.lower(), 'negrito')}...", end="", flush=True)
            with cf.ThreadPoolExecutor(PARALELO) as ex:
                list(ex.map(lambda uf: coletar(cargo, uf, estado[cargo][uf], conhecidos, avisos), ufs))
            if gravar(cargo, estado[cargo], a.simular):
                mudou_algo = True
            log(resumo(cargo, rotulo, estado[cargo]))
        for av in sorted(set(avisos))[:15]:
            log(c("  ⚠ " + av, "amarelo"))
        if len(set(avisos)) > 15:
            log(c(f"  ⚠ … mais {len(set(avisos)) - 15} avisos", "amarelo"))

        pendente_pub = pendente_pub or mudou_algo
        if a.publicar and pendente_pub:
            if time.time() - ultima_pub >= INTERVALO_PUBLICACAO:
                ok, msg = publicar()
                if ok:
                    ultima_pub, pendente_pub = time.time(), False
                    log(c(f"  → publicado {agora()} ({msg})", "verde"))
                else:
                    log(c(f"  ✖ não publicado: {msg}", "vermelho"))
            else:
                prox = dt.datetime.fromtimestamp(ultima_pub + INTERVALO_PUBLICACAO).strftime("%H:%M:%S")
                log(c(f"  → mudanças guardadas; próxima publicação a partir de {prox}", "cinza"))
        elif not mudou_algo:
            log(c("  nada mudou neste ciclo", "cinza"))
        else:
            log(c(f"  → arquivos atualizados em {SAIDA.relative_to(RAIZ)}", "cinza"))

        if a.uma_vez:
            break
        alvo = inicio + a.intervalo
        while time.time() < alvo:  # relógio ao vivo até o próximo ciclo
            print(f"\r\033[K  {c(agora(), 'negrito')} · próximo ciclo em {int(alvo - time.time()):>2}s", end="", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log(c("\nEncerrado.", "cinza"))
