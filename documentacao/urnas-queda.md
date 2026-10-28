# Votos a menos (`urnas-queda.html` + `scripts/queda_votos.py`)

Página do 2º turno criada a pedido do usuário em 28/10/2026. No switch do 2º turno, fica no item **Votos a menos**. Ela procura anomalias: municípios e seções eleitorais (urnas) em que **Lula (13) ou Flávio Bolsonaro (22) tiveram menos votos no 2º turno (25/10) do que no 1º turno (04/10)**, para presidente. Critério combinado com o usuário: **qualquer queda** (1 voto ou mais), nos níveis município e seção. A queda não indica irregularidade por si só (abstenção maior na seção, eleitor que mudou de voto, agregação de seções); por isso a página mostra o comparecimento dos dois turnos ao lado.

## Fontes

Os mesmos arquivos do TSE baixados para as urnas zero ([urnas-zero.md](urnas-zero.md)), em `apuracao-bruto/urnas-zero/`:
- `votacao_secao_2026_BR.zip`: votos de presidente por seção, nos dois turnos (`NR_TURNO`);
- `detalhe_votacao_secao_2026.zip` (`_BR.csv`): comparecimento por turno e nome do local (seções anuladas ficam de fora).

A seção é a mesma nos dois turnos da mesma eleição: o casamento é exato por (UF, município, zona, seção).

## Script

```bash
python scripts/queda_votos.py   # ~1,5 min; importa as funções de scripts/urnas_zero.py
```

Para baixar os arquivos de novo, use `python scripts/urnas_zero.py --baixar`.

## Formato (`docs/data/queda-votos/`)

Ver a docstring de `scripts/queda_votos.py`:
- `resumo.json`: totais do país, faixas de queda (1–5, 6–10, 11–25, 26–50, mais de 50 votos), `ufs` e `mun` (todos os municípios, com os votos dos dois turnos e o número de seções com queda);
- `secoes/<UF>.json`: só as seções com queda de pelo menos um dos dois, carregadas pela página quando o leitor escolhe o estado (ZZ = exterior). Total ~5 MB; o maior é MA (~570 KB).

## Números de 28/10 (para conferir a página)

- Somas batem com o resultado oficial nos dois turnos: Lula 53.879.538 → 64.256.232; Flávio 56.104.503 → 59.826.041. Comparecimento 125.275.835 → 128.236.074.
- 499.205 seções com votos nos dois turnos. Queda de Flávio em 82.180 (16,5%), de Lula em 9.590 (1,9%), dos dois em 5.458. Votos perdidos somados nessas seções: Flávio 383.008, Lula 58.933 (86.888 nas seções em que os dois caíram).
- Faixas de queda (seções): Flávio 58.466 / 17.175 / 6.077 / 436 / 26; Lula 5.976 / 2.021 / 1.378 / 205 / 10.
- Municípios com queda: Flávio 950, Lula 88.
