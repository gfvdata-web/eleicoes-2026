"""
Apuração do Espírito Santo por município (eleição de 04/10/2026), para es.html.

A cada minuto, confere no TSE o arquivo do estado e dos 78 municípios de cada cargo
(presidente, governador, senador, deputado federal e estadual). Se algo mudou, grava
docs/data/es/apuracao/<cargo>.json. Publica (commit + push só dessa pasta) no máximo
a cada INTERVALO_PUBLICACAO.

Uso:
  python scripts/apuracao_es.py --simular     # dados falsos com os candidatos reais, só local (nunca publica)
  python scripts/apuracao_es.py               # coleta real, sem publicar
  python scripts/apuracao_es.py --publicar    # coleta real e publica no GitHub
  python scripts/apuracao_es.py --uma-vez     # roda um ciclo e sai
  python scripts/apuracao_es.py --limpar      # zera os arquivos do site

Usa as funções de terminal e git de apuracao.py. Só biblioteca padrão. Ctrl+C encerra.
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apuracao import RAIZ, UFS, Local, agora, baixar, c, git, log, pct_br, variacao, ANTERIOR  # noqa: E402

SAIDA = RAIZ / "docs" / "data" / "es" / "apuracao"   # o que es.html lê
BRUTO = RAIZ / "apuracao-bruto" / "es"               # cópia do TSE (ignorada pelo git)
MUNICIPIOS = RAIZ / "docs" / "data" / "es" / "municipios.js"
CONFIG_MUN = "https://resultados.tse.jus.br/oficial/ele2026/6259/config/mun-e006259-cm.json"

INTERVALO_COLETA = 60
INTERVALO_PUBLICACAO = 120
PARALELO = 24   # são ~28 mil arquivos por ciclo (5 cargos × ~5.570 municípios + estados)

# Divulgação do TSE de 2026. Eleição 6257 = federal (presidente); 6259 = estadual.
BASE = "https://resultados.tse.jus.br/oficial/ele2026"
# (id do arquivo, rótulo no terminal, código da eleição, código do cargo)
CARGOS = [
    ("presidente", "Presidente", 6257, 1),
    ("governador", "Governador", 6259, 3),
    ("senador", "Senador", 6259, 5),
    ("deputado-federal", "Dep. federal", 6259, 6),
    ("deputado-estadual", "Dep. estadual", 6259, 7),
]


def url(ele, cargo, local, uf="ES"):
    """local = "" para o estado ou o código TSE do município."""
    u = uf.lower()
    if cargo == 7 and uf == "DF":
        cargo = 8   # deputado distrital
    return f"{BASE}/{ele}/dados/{u}/{u}{local}-c{cargo:04d}-e{ele:06d}-u.json"


def pasta_bruta(uf, cargo):
    return BRUTO / cargo if uf == "ES" else BRUTO / "outros" / uf / cargo


def arq_saida(uf, cargo):
    """ES continua em <cargo>.json (es.html lê daí); os demais estados em <UF>/<cargo>.json."""
    return SAIDA / f"{cargo}.json" if uf == "ES" else SAIDA / uf / f"{cargo}.json"


def carregar_municipios(todos):
    """{UF: [códigos TSE dos municípios]}. Com todos=False, só o ES (arquivo local)."""
    if not todos:
        return {"ES": re.findall(r'"tse":\s*"(\d+)"', MUNICIPIOS.read_text(encoding="utf-8"))}
    cache = BRUTO / "municipios-todos.json"
    try:
        cod, corpo, _ = baixar(CONFIG_MUN, Local())
        if cod != 200:
            raise RuntimeError(f"HTTP {cod}")
        cfg = json.loads(corpo.decode("utf-8-sig"))
        res = {a["cd"].upper(): [m["cd"] for m in a["mu"]] for a in cfg["abr"]}
        BRUTO.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(res), encoding="utf-8")
    except Exception as ex:
        if not cache.exists():
            sys.exit(f"Não consegui a lista de municípios do TSE ({ex}) e não há cópia local.")
        log(c(f"Lista de municípios do TSE indisponível ({ex}); usando a cópia local", "amarelo"))
        res = json.loads(cache.read_text(encoding="utf-8"))
    return {uf: res[uf] for uf in UFS if uf in res}


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return 0.0


def inteiro(v):
    return int(num(v))


# ----------------------------------------------------------------------------
# Conversão do arquivo do TSE (formato "-u.json" de 2026)
# ----------------------------------------------------------------------------

def converter(bruto):
    """Devolve um dict com os totais do local e, por candidato, metadados e votos.
    Proporcionais: cada "agr" é uma lista (partido isolado ou federação)."""
    carg = bruto["carg"][0]
    s, e, v = bruto.get("s", {}), bruto.get("e", {}), bruto.get("v", {})
    feds = {f["n"]: f["sg"] for f in carg.get("fed", [])}
    listas, cands, leg = {}, {}, {}
    for agr in carg.get("agr", []):
        for par in agr.get("par", []):
            if agr.get("tp") == "f":
                nome_lista = "Federação " + feds.get(par.get("nfed"), agr.get("com", agr["nm"]))
            elif agr.get("tp") == "c":
                nome_lista = agr.get("com") or agr["nm"]
            else:
                nome_lista = par["sg"]
            listas[agr["n"]] = (nome_lista, agr.get("tp", ""), inteiro(agr.get("vag", 0)))
            leg[par["sg"]] = (agr["n"], inteiro(par.get("tvtl", 0)))
            for cd in par.get("cand", []):
                cands[cd["n"]] = {"nome": cd.get("nmu") or cd["nm"], "partido": par["sg"], "lista": agr["n"],
                                  "st": cd.get("st", ""), "e": cd.get("e") == "s", "votos": inteiro(cd.get("vap", 0))}
    hora = (bruto.get("ht") or bruto.get("hg") or "")
    return {
        "pct": num(s.get("pst", 0)), "hora": hora, "el": inteiro(e.get("te", 0)), "comp": inteiro(e.get("c", 0)),
        "abst": inteiro(e.get("a", 0)), "vv": inteiro(v.get("vv", 0)), "vb": inteiro(v.get("vb", 0)),
        "vn": inteiro(v.get("tvn", 0)), "vl": inteiro(v.get("vl", 0)),
        "vagas": inteiro(carg.get("nv", 1)), "qe": inteiro(carg.get("qe", 0)),
        "listas": listas, "cands": cands, "leg": leg,
    }


# ----------------------------------------------------------------------------
# Coleta
# ----------------------------------------------------------------------------

PULAR_CONCLUIDOS = True   # município com 100% apurado não é mais consultado (--tudo desliga)


def coletar_real(uf, cargo, ele, cd, local, loc, avisos):
    if PULAR_CONCLUIDOS and loc.dado and loc.dado["pct"] >= 100:
        loc.status = "igual"
        return False
    cod, corpo, cab = baixar(url(ele, cd, local, uf), loc)
    nome = f"{cargo} {uf} {local}".strip()
    if cod == 304:
        loc.status = "igual"
        return False
    if cod in (403, 404):
        loc.status = "pendente"
        return False
    if cod in (429, 503):   # limite do TSE: mantém o dado anterior e tenta no próximo ciclo
        loc.status = "limitado"
        return False
    if cod != 200:
        loc.status = "erro"
        avisos.append(f"{nome}: HTTP {cod or 'falha de rede'} {(corpo or b'')[:80].decode(errors='ignore')}")
        return False
    loc.etag, loc.modificado = cab.get("ETag"), cab.get("Last-Modified")
    h = hashlib.sha1(corpo).hexdigest()
    if h == loc.hash:
        loc.status = "igual"
        return False
    try:
        dado = converter(json.loads(corpo))
    except Exception as ex:
        loc.status = "erro"
        avisos.append(f"{nome}: arquivo inválido ({ex})")
        return False
    pasta = pasta_bruta(uf, cargo)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / f"{local or uf}.json").write_bytes(corpo)
    if loc.dado and dado["pct"] < loc.dado["pct"]:
        avisos.append(f"{nome}: % apurado diminuiu ({pct_br(loc.dado['pct'])} → {pct_br(dado['pct'])})")
    if dado["vl"] and sum(x[1] for x in dado["leg"].values()) != dado["vl"]:
        avisos.append(f"{nome}: votos de legenda por partido não batem com o total (conferir campo tvtl)")
    loc.hash, loc.dado, loc.status = h, dado, "novo"
    return True


def retomar(uf, cargo, locais):
    """Ao reiniciar, relê a última cópia do TSE guardada em apuracao-bruto/es/."""
    n = 0
    for local, loc in locais.items():
        arq = pasta_bruta(uf, cargo) / f"{local or uf}.json"
        if arq.exists():
            try:
                corpo = arq.read_bytes()
                loc.dado, loc.hash = converter(json.loads(corpo)), hashlib.sha1(corpo).hexdigest()
                n += 1
            except Exception:
                pass
    return n


# Simulação: parte dos candidatos reais (arquivos do TSE com 0 voto) e inventa votos por município
class Simulador:
    def __init__(self, cargo, ele, cd, muns, avisos):
        self.cargo, self.muns = cargo, muns
        arq = BRUTO / cargo / "ES.json"
        base = None
        try:
            cod, corpo, _ = baixar(url(ele, cd, ""), Local())
            if cod == 200:
                base = converter(json.loads(corpo))
        except Exception:
            pass
        if base is None and arq.exists():
            base = converter(json.loads(arq.read_bytes()))
        if base is None:
            avisos.append(f"{cargo}: sem a lista do TSE, simulando com candidatos fictícios")
            base = {"vagas": 1, "qe": 0, "listas": {"1": ("Partido A", "i", 0)}, "leg": {"PA": ("1", 0)},
                    "cands": {str(i): {"nome": f"Candidato {i}", "partido": "PA", "lista": "1", "st": "", "e": False, "votos": 0}
                              for i in range(10, 15)}}
        self.base = base
        r = random.Random(cargo)
        # força de cada candidato no estado e uma "região de origem" (município) com mais votos
        self.forca = {n: r.paretovariate(1.3) for n in base["cands"]}
        self.casa = {n: r.choice(muns) for n in base["cands"]}
        self.eleitores = {m: int(r.lognormvariate(9.5, 1.0)) + 3000 for m in muns}
        self.pct = {m: 0.0 for m in muns}

    def passo(self, local, loc):
        if local == "":
            return False
        ant = self.pct[local]
        if ant >= 100 or (ant == 0 and random.random() < 0.3) or random.random() < 0.2:
            loc.status = "igual" if loc.dado else "pendente"
            return False
        pct = min(100.0, round(ant + random.uniform(4, 20), 2))
        self.pct[local] = pct
        r = random.Random(self.cargo + local)
        el = self.eleitores[local]
        comp = int(el * 0.8 * pct / 100)
        vb, vn = int(comp * 0.03), int(comp * 0.05)
        vv = comp - vb - vn
        proporcional = self.base["vagas"] > 1 and self.cargo.startswith("deputado")
        pesos = {n: f * r.uniform(0.4, 1.6) * (25 if self.casa[n] == local else 1) for n, f in self.forca.items()}
        vl = int(vv * 0.06) if proporcional else 0
        tot = sum(pesos.values()) or 1
        cands = {n: {**m, "votos": int((vv - vl) * pesos[n] / tot)} for n, m in self.base["cands"].items()}
        partidos = list(self.base["leg"])
        leg = {p: (self.base["leg"][p][0], 0) for p in partidos}
        for _ in range(min(vl, 200)):
            p = r.choice(partidos)
            leg[p] = (leg[p][0], leg[p][1] + vl // 200)
        loc.dado = {"pct": pct, "hora": agora(), "el": el, "comp": comp, "abst": el - int(el * 0.8),
                    "vv": vv, "vb": vb, "vn": vn, "vl": sum(x[1] for x in leg.values()),
                    "vagas": self.base["vagas"], "qe": 0, "listas": self.base["listas"], "cands": cands, "leg": leg}
        loc.status = "novo"
        return True


def somar_estado(cargo_locais, base):
    """Simulação: o total do estado é a soma dos municípios."""
    muns = [l.dado for k, l in cargo_locais.items() if k and l.dado]
    if not muns:
        return None
    el = sum(d["el"] for d in muns)
    tot = {k: sum(d[k] for d in muns) for k in ("comp", "abst", "vv", "vb", "vn", "vl")}
    cands = {n: {**m, "votos": sum(d["cands"].get(n, {}).get("votos", 0) for d in muns)} for n, m in base["cands"].items()}
    leg = {p: (base["leg"][p][0], sum(d["leg"].get(p, (0, 0))[1] for d in muns)) for p in base["leg"]}
    pct = sum(d["pct"] * d["el"] for d in muns) / el if el else 0
    return {"pct": round(pct, 2), "hora": max(d["hora"] for d in muns), "el": el, **tot,
            "vagas": base["vagas"], "qe": 0, "listas": base["listas"], "cands": cands, "leg": leg}


# ----------------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------------

def gravar(cargo, locais, simulacao, uf="ES"):
    """Grava docs/data/es/apuracao/<cargo>.json no formato descrito em documentacao/es.md.
    Retorna True se o arquivo mudou."""
    est = locais[""].dado
    dados = [l.dado for l in locais.values() if l.dado]
    if not dados:
        doc = {"cargo": cargo, "atualizado": "", "es": None, "mun": {}}
    else:
        # lista mestre de candidatos, listas e partidos (do estado; completa com o que aparecer nos municípios)
        cands, listas, partidos = {}, {}, {}
        for d in [est] + dados if est else dados:
            for n, m in d["cands"].items():
                cands.setdefault(n, m)
            for k, v in d["listas"].items():
                listas.setdefault(k, v)
            for p, (k, _) in d["leg"].items():
                partidos.setdefault(p, k)
        lid = {k: i for i, k in enumerate(listas)}
        nums = sorted(cands, key=lambda n: (-(est["cands"].get(n, {}).get("votos", 0) if est else 0), n))
        sgs = sorted(partidos)
        ref = est or dados[0]

        def bloco(d):
            return {"pct": d["pct"], "hora": d["hora"], "el": d["el"], "comp": d["comp"], "abst": d["abst"],
                    "vv": d["vv"], "vb": d["vb"], "vn": d["vn"], "vl": d["vl"],
                    "v": [d["cands"].get(n, {}).get("votos", 0) for n in nums],
                    "leg": [d["leg"].get(p, (0, 0))[1] for p in sgs]}

        doc = {
            "cargo": cargo,
            "atualizado": max(d["hora"] for d in dados)[:5],
            "vagas": ref["vagas"], "qe": ref["qe"],
            "listas": [[v[0], v[1], v[2]] for v in listas.values()],
            "cand": [[n, cands[n]["nome"], cands[n]["partido"], lid[cands[n]["lista"]], cands[n]["st"], 1 if cands[n]["e"] else 0]
                     for n in nums],
            "partidos": [[p, lid[partidos[p]]] for p in sgs],
            "es": bloco(est) if est else None,
            "mun": {k: bloco(l.dado) for k, l in locais.items() if k and l.dado},
        }
    if simulacao:
        doc["simulacao"] = True
    texto = json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n"
    arq = arq_saida(uf, cargo)
    if arq.exists() and arq.read_text(encoding="utf-8") == texto:
        return False
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8", newline="\n")
    return True


def publicar(caminhos, rotulo):
    """Commit e push só dos caminhos deste processo (assim dois processos não se atropelam)."""
    git("add", *caminhos)
    cod, saida = git("commit", "-m", f"Apuração {rotulo}: atualização {agora()[:5]}", "--", *caminhos)
    if cod != 0:
        return ("nothing to commit" in saida or "nada a submeter" in saida), "nada novo para commitar"
    _, sha = git("rev-parse", "--short", "HEAD")
    cod, saida = git("push")
    if cod != 0:  # remoto andou (outra sessão ou apuracao.py publicou): rebase e tenta de novo
        git("pull", "--rebase", "--autostash")
        cod, saida = git("push")
        if cod != 0:
            return False, "push falhou: " + saida.splitlines()[-1]
    return True, f"commit {sha}"


def limpar():
    for cargo, _, _, _ in CARGOS:
        for uf in UFS:
            if uf == "ES" or arq_saida(uf, cargo).exists():
                gravar(cargo, {"": Local()}, False, uf)
    print("Arquivos zerados em", SAIDA)


def pct_estados(por_uf):
    """% apurado do cargo no país: média dos estados (arquivo do estado de cada UF)."""
    return sum((l[""].dado["pct"] if l[""].dado else 0.0) for l in por_uf.values()) / len(por_uf)


def resumo(rotulo, por_uf):
    """Uma linha por cargo: arquivos de todos os estados, % apurado e variação; ES detalhado."""
    todos = [l for locais in por_uf.values() for l in locais.values()]
    st = [l.status for l in todos]
    partes = [f"{c(st.count('novo'), 'verde')} novos", f"{st.count('igual')} iguais"]
    if st.count("pendente"):
        partes.append(c(f"{st.count('pendente')} pendentes", "cinza"))
    if st.count("limitado"):
        partes.append(c(f"{st.count('limitado')} limitados pelo TSE", "cinza"))
    if st.count("erro"):
        partes.append(c(f"{st.count('erro')} erros", "vermelho"))
    pct = pct_estados(por_uf)
    linhas = [f"  {rotulo:<14}{len(todos):>5} arquivos | " + "  ".join(partes)
              + f" | apurado {c(pct_br(pct), 'negrito')}{variacao(rotulo, pct)}"]
    if "ES" in por_uf and len(por_uf) > 1:
        locais = por_uf["ES"]
        est = locais[""].dado
        muns = [l.dado for k, l in locais.items() if k and l.dado]
        concl = sum(1 for d in muns if d["pct"] >= 100)
        ultimo = max((d["hora"] for d in muns + ([est] if est else [])), default="—")
        pe = est["pct"] if est else 0.0
        linhas.append(f"  {'':<14}  ES {pct_br(pe)}{variacao(rotulo + '/ES', pe)} · {concl}/{len(locais) - 1} municípios concluídos"
                      f" | último dado {c(ultimo, 'ciano')}")
    elif "ES" in por_uf:
        locais = por_uf["ES"]
        muns = [l.dado for k, l in locais.items() if k and l.dado]
        concl = sum(1 for d in muns if d["pct"] >= 100)
        linhas[0] += f" · {concl}/{len(locais) - 1} municípios concluídos"
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser(description="Apuração do ES por município, para es.html.")
    ap.add_argument("--simular", action="store_true", help="dados falsos, nunca publica")
    ap.add_argument("--publicar", action="store_true", help="faz commit e push dos dados")
    ap.add_argument("--uma-vez", action="store_true", help="roda um ciclo e sai")
    ap.add_argument("--limpar", action="store_true", help="zera os arquivos do site e sai")
    ap.add_argument("--intervalo", type=int, default=INTERVALO_COLETA, help="segundos entre ciclos (padrão 60)")
    ap.add_argument("--tudo", action="store_true", help="consulta também os municípios já com 100% apurado")
    ap.add_argument("--ufs", help="só estes estados, separados por vírgula (ex.: ES ou SP,RJ)")
    ap.add_argument("--exceto", help="todos os estados menos estes (ex.: ES)")
    ap.add_argument("--cargos", help="só estes cargos, separados por vírgula (ex.: deputado-federal,deputado-estadual)")
    a = ap.parse_args()
    global PULAR_CONCLUIDOS
    PULAR_CONCLUIDOS = not a.tudo

    if a.limpar:
        return limpar()
    if a.simular and a.publicar:
        sys.exit("--simular nunca publica. Rode sem --publicar.")

    log(c("Iniciando: buscando a lista de municípios no TSE...", "cinza"))
    muns = carregar_municipios(todos=not a.simular)   # a simulação é só do ES
    if a.ufs:
        muns = {uf: m for uf, m in muns.items() if uf in a.ufs.upper().split(",")}
    if a.exceto and not a.simular:
        muns = {uf: m for uf, m in muns.items() if uf not in a.exceto.upper().split(",")}
    if not muns:
        sys.exit("Nenhum estado selecionado (confira --ufs / --exceto).")
    rotulo_pub = "ES" if list(muns) == ["ES"] else "demais estados" if "ES" not in muns else "estados"
    cargos = [x for x in CARGOS if not a.cargos or x[0] in a.cargos.split(",")]
    # estado[cargo][UF] = {"" (estado) ou código do município: Local}
    estado = {cargo: {uf: {loc: Local() for loc in [""] + lista} for uf, lista in muns.items()}
              for cargo, _, _, _ in cargos}
    avisos = []
    sims = {}
    if a.simular:
        sims = {cargo: Simulador(cargo, ele, cd, muns["ES"], avisos) for cargo, _, ele, cd in cargos}
    else:
        log(c("Relendo os arquivos já baixados (pode levar 1 a 2 minutos)...", "cinza"))
        n = sum(retomar(uf, cargo, estado[cargo][uf]) for cargo, _, _, _ in cargos for uf in muns)
        if n:
            log(c(f"Retomando {n} arquivos já baixados em {BRUTO.relative_to(RAIZ)}", "cinza"))
    for cargo, rotulo, _, _ in cargos:
        ANTERIOR[rotulo] = pct_estados(estado[cargo])   # base da primeira variação
        if "ES" in estado[cargo] and len(muns) > 1:
            ANTERIOR[rotulo + "/ES"] = estado[cargo]["ES"][""].dado["pct"] if estado[cargo]["ES"][""].dado else 0.0
    modo = c("SIMULAÇÃO (só local)", "amarelo", "negrito") if a.simular else (
        c("PUBLICANDO no GitHub", "vermelho", "negrito") if a.publicar else c("coleta sem publicar", "ciano"))
    log(c("Apuração ES 2026 — por município", "negrito") + f" · {modo} · coleta a cada {a.intervalo}s")

    ciclo, ultima_pub, pendente_pub = 0, 0.0, False
    while True:
        ciclo += 1
        inicio = time.time()
        log()
        log(c(f"════ {agora()} · {rotulo_pub} · ciclo {ciclo} ", "negrito") + "═" * 36)
        mudou_algo = False
        if a.simular:
            for cargo, _, _, _ in cargos:
                locais = estado[cargo]["ES"]
                for loc_id, loc in locais.items():
                    sims[cargo].passo(loc_id, loc)
                locais[""].dado = somar_estado(locais, sims[cargo].base)
                locais[""].status = "novo"
        else:
            tarefas = [(uf, cargo, ele, cd, loc_id) for cargo, _, ele, cd in cargos
                       for uf in estado[cargo] for loc_id in estado[cargo][uf]]
            feitos = 0
            with cf.ThreadPoolExecutor(PARALELO) as ex:
                for _ in ex.map(lambda t: coletar_real(t[0], t[1], t[2], t[3], t[4], estado[t[1]][t[0]][t[4]], avisos), tarefas):
                    feitos += 1
                    if feitos % 100 == 0 or feitos == len(tarefas):
                        print(f"\r\033[K  Baixando do TSE... {feitos}/{len(tarefas)} arquivos", end="", flush=True)
        for cargo, rotulo, _, _ in cargos:
            for uf, locais in estado[cargo].items():
                if gravar(cargo, locais, a.simular, uf):
                    mudou_algo = True
            log(resumo(rotulo, estado[cargo]))
        for av in sorted(set(avisos))[:15]:
            log(c("  ⚠ " + av, "amarelo"))
        if len(set(avisos)) > 15:
            log(c(f"  ⚠ … mais {len(set(avisos)) - 15} avisos", "amarelo"))
        avisos.clear()

        pendente_pub = pendente_pub or mudou_algo
        if a.publicar and pendente_pub:
            if time.time() - ultima_pub >= INTERVALO_PUBLICACAO:
                caminhos = [f"docs/data/es/apuracao/{uf}" for uf in muns if uf != "ES"]
                if "ES" in muns:
                    caminhos += [f"docs/data/es/apuracao/{cargo}.json" for cargo, _, _, _ in cargos]
                ok, msg = publicar(caminhos, rotulo_pub)
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
        while time.time() < alvo:
            print(f"\r\033[K  {c(agora(), 'negrito')} · próximo ciclo em {int(alvo - time.time()):>2}s", end="", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log(c("\nEncerrado.", "cinza"))
