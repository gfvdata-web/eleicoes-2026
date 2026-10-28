# Urnas zero (`urnas-zero.html` + `scripts/urnas_zero.py`)

Página do 2º turno criada a pedido do usuário em 28/10/2026; no switch do 2º turno, é o item **Urnas zero**. Ela mostra as seções eleitorais (urnas) em que Flávio Bolsonaro teve **até 10 votos** no 2º turno de presidente de 2026 e onde elas ficam. Mostra também como essas mesmas seções votaram em todos os 2º turnos de presidente com dados por seção:

| Ano | Candidato do PT | Adversário |
|---|---|---|
| 2022 | Lula | Jair Bolsonaro |
| 2018 | Haddad | Jair Bolsonaro |
| 2014 | Dilma | Aécio |
| 2010 | Dilma | Serra |
| 2006 | Lula | Alckmin |
| 2002 | Lula | Serra |

Em 1998 e 1994 não houve 2º turno de presidente, e o TSE não publica votos por seção antes de 1998. "Urna" e "seção" são usadas como sinônimos.

## Fontes (dados abertos do TSE)

`https://cdn.tse.jus.br/estatistica/sead/odsele/`, baixados para `apuracao-bruto/urnas-zero/` (ignorado pelo git, ~2,2 GB):
- `votacao_secao/votacao_secao_<ano>_BR.zip`: votos de presidente por seção, nos dois turnos, de 2002 a 2026. O de 2026 foi republicado com o 2º turno em 26/10.
- `detalhe_votacao_secao/detalhe_votacao_secao_<ano>.zip`: aptos, comparecimento e local. Só se usa o `_BR.csv`, que traz presidente em todas as UFs e no exterior. O nome do local só vem a partir de 2018; antes disso, só o número.
- `eleitorado_locais_votacao/eleitorado_local_votacao_{2014,2010}.zip`: nome do local nesses anos. Não existe para 2006 e 2002.
- Tipo do local e coordenadas: `apuracao-bruto/secoes-br/eleitorado_local_votacao_2026.zip`, o mesmo do `voto_cruzado.py`.

Não use o `apuracao-bruto/secoes-br/votacao_secao_2026_BR.zip` do 1º turno: o `voto_cruzado.py` não filtra `NR_TURNO` e passaria a somar os dois turnos.

## Script

```bash
python scripts/urnas_zero.py            # usa os arquivos já baixados (~8 min)
python scripts/urnas_zero.py --baixar   # baixa de novo do TSE
```

Conferência em 28/10: a soma das seções bate com o resultado oficial do 2º turno nos sete anos.

| Ano | Candidato do PT | Adversário |
|---|---|---|
| 2026 | 64.256.232 | 59.826.041 |
| 2022 | 60.345.999 | 58.206.354 |
| 2018 | 47.040.906 | 57.797.847 |
| 2014 | 54.501.118 | 51.041.155 |
| 2010 | 55.752.529 | 43.711.388 |
| 2006 | 58.295.042 | 37.543.178 |
| 2002 | 52.793.364 | 33.370.739 |

## Casamento entre eleições

As seções são casadas pela mesma chave (UF, município, zona, seção). Como o TSE renumera e funde seções entre eleições, o nome do local de votação de cada ano é comparado com o de 2026 (palavras com 3 letras ou mais, sem acento, Jaccard ≥ 0,5):
- `1` = mesmo local, que entra no comparativo;
- `2` = mesmo número, mas local diferente;
- `0` = a seção não existia naquele ano.

Em 2006 e 2002 não há nome do local. Nesses anos, a seção conta como mesmo local quando o número do local é igual ao do ano seguinte (2010, depois 2006) e ela já era o mesmo local nesse ano. Esse critério é mais frágil que o dos outros anos.

Seções casadas no mesmo local, das 3.042 urnas zero (28/10):

| Ano | Mesmo local | Local diferente | Não existia |
|---|---|---|---|
| 2022 | 1.990 | 324 | 728 |
| 2018 | 1.815 | 270 | 957 |
| 2014 | 1.153 | 490 | 1.399 |
| 2010 | 954 | 486 | 1.602 |
| 2006 | 724 | 413 | 1.905 |
| 2002 | 554 | 331 | 2.157 |

Nos seis anos ao mesmo tempo, casam 529 seções.

## Formato de `docs/data/urnas-zero/urnas.json`

Detalhes na docstring de `scripts/urnas_zero.py`.
- `anos`: `[ano, candidato do PT, adversário]`.
- `tot`: totais do país por ano.
- `ufs`, `mun` e `locais` (`[nome, tipo TSE, lon, lat]`).
- `secoes`: 12 colunas de 2026, mais 4 por ano anterior (`casa, adversário, PT, comparecimento`; índice `12 + 4·n`).
- `nomes {ano: {linha: nome}}`: o nome do local naquele ano, quando é diferente do de 2026.

## Números de 28/10 (para conferir a página)

- 3.042 urnas zero (0,6% das 499.205 seções), com 526.654 aptos e 423.454 votantes. Flávio teve 18.868 votos nelas e Lula, 395.215.
- Tipo do local: 2.853 convencionais, 167 de preso provisório e 22 temporários.
- Por UF: MA 788, BA 466, PI 312, PA 283, AM 260, CE 235, MG 175. No exterior, 13.
- % do candidato do PT (sobre PT + adversário):

| Recorte | 2002 | 2006 | 2010 | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|---|---|
| Seções casadas em cada ano | 54,8 | 88,7 | 89,9 | 90,1 | 96,4 | 95,3 | 95,4 |
| Mesmas 529 seções em todos os anos | 54,3 | 88,1 | 89,8 | 90,8 | 96,0 | 95,2 | 95,3 |
| País | 61,3 | 60,8 | 56,1 | 51,6 | 44,9 | 50,9 | 51,8 |

- No país, seções com o adversário do PT com até 10 votos:

| 2002 | 2006 | 2010 | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|---|
| 1.300 | 6.296 | 5.975 | 6.330 | 7.620 | 4.118 | 3.042 |
