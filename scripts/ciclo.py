"""Roda as três coletas do TSE em sequência, uma de cada vez, para não estourar o limite (HTTP 429).

Ordem de cada rodada:
  1. geral        (scripts/apuracao.py)
  2. Espírito Santo (scripts/apuracao_es.py --ufs ES)
  3. outros estados (scripts/apuracao_es.py --exceto ES), só se já passaram 10 min desde o fim da última vez

Geral + ES se repetem a cada INTERVALO_RODADA segundos (contados do início da rodada; se a rodada demorar mais, a próxima começa logo).
Cada etapa roda com --uma-vez --publicar (commit + push só dos arquivos dela).

Uso: python scripts/ciclo.py            (Ctrl+C encerra)
     python scripts/ciclo.py --sem-publicar
"""
import argparse
import datetime as dt
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INTERVALO_RODADA = 120    # segundos entre rodadas de geral + ES
INTERVALO_OUTROS = 600    # segundos entre duas coletas dos outros estados (contados do fim da anterior)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def hora():
    return dt.datetime.now().strftime("%H:%M:%S")


def etapa(nome, script, *args, publicar=True):
    print(f"\n[{hora()}] ▶ {nome}", flush=True)
    t0 = time.time()
    cmd = [sys.executable, str(RAIZ / "scripts" / script), "--uma-vez", *args] + (["--publicar"] if publicar else [])
    cod = subprocess.run(cmd, cwd=RAIZ).returncode
    print(f"[{hora()}] ■ {nome} terminou em {int(time.time() - t0)}s" + ("" if cod == 0 else f" (código {cod})"), flush=True)


def main():
    ap = argparse.ArgumentParser(description="Coleta geral, ES e outros estados em sequência.")
    ap.add_argument("--sem-publicar", action="store_true", help="só grava os arquivos, sem commit/push")
    a = ap.parse_args()
    pub = not a.sem_publicar
    fim_outros = 0.0
    while True:
        inicio = time.time()
        etapa("Geral", "apuracao.py", publicar=pub)
        etapa("Espírito Santo", "apuracao_es.py", "--ufs", "ES", publicar=pub)
        if time.time() - fim_outros >= INTERVALO_OUTROS:
            etapa("Outros estados", "apuracao_es.py", "--exceto", "ES", publicar=pub)
            fim_outros = time.time()
        alvo = inicio + INTERVALO_RODADA
        while time.time() < alvo:
            print(f"\r\033[K  próxima rodada em {int(alvo - time.time()):>3}s", end="", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrado.")
