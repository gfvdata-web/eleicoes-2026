# Urnas zero (`urnas-zero.html` + `scripts/urnas_zero.py`)

Página do 2º turno criada a pedido do usuário em 28/10/2026. No switch do 2º turno, fica no item **Urnas zero**. Ela mostra as seções eleitorais (urnas) em que Flávio Bolsonaro teve **até 10 votos** no 2º turno de presidente de 2026, onde elas ficam e como essas mesmas seções votaram no 2º turno de 2022 (Lula × Jair Bolsonaro) e de 2018 (Jair Bolsonaro × Haddad). "Urna" e "seção" são usadas como sinônimos.

## Fontes (dados abertos do TSE)

`https://cdn.tse.jus.br/estatistica/sead/odsele/`, baixados para `apuracao-bruto/urnas-zero/` (ignorado pelo git, ~1,5 GB):
- `votacao_secao/votacao_secao_{2026,2022,2018}_BR.zip`: votos de presidente por seção, nos dois turnos. O de 2026 foi republicado com o 2º turno em 26/10.
- `detalhe_votacao_secao/detalhe_votacao_secao_{2026,2022,2018}.zip`: aptos, comparecimento e local. Só se usa o `_BR.csv`, que traz presidente em todas as UFs e no exterior.
- Tipo do local e coordenadas: `apuracao-bruto/secoes-br/eleitorado_local_votacao_2026.zip`, o mesmo do `voto_cruzado.py`.

Não use o `apuracao-bruto/secoes-br/votacao_secao_2026_BR.zip` do 1º turno: o `voto_cruzado.py` não filtra `NR_TURNO` e passaria a somar os dois turnos.

## Script

```bash
python scripts/urnas_zero.py            # usa os arquivos já baixados (~5 min)
python scripts/urnas_zero.py --baixar   # baixa de novo do TSE
```

Conferência em 28/10: a soma das seções bate com o resultado oficial nos três anos. 2026: Lula 64.256.232 × Flávio 59.826.041. 2022: Lula 60.345.999 × Bolsonaro 58.206.354. 2018: Bolsonaro 57.797.847 × Haddad 47.040.906.

## Casamento entre eleições

As seções são casadas pela mesma chave (UF, município, zona, seção). Como o TSE renumera e funde seções entre eleições, o nome do local de votação de cada ano é comparado com o de 2026 (palavras com 3 letras ou mais, sem acento, Jaccard ≥ 0,5):
- `1` = mesmo local, que entra no comparativo;
- `2` = mesmo número, mas local diferente;
- `0` = a seção não existia naquele ano.

Em 28/10, das 3.042 urnas zero:
- 2022: 1.990 no mesmo local, 324 em local diferente e 728 que não existiam;
- 2018: 1.815 no mesmo local, 270 em local diferente e 957 que não existiam;
- 1.724 casam nos dois anos.

## Formato de `docs/data/urnas-zero/urnas.json`

Ver a docstring de `scripts/urnas_zero.py`:
- `tot`: totais do país por ano;
- `ufs`, `mun` e `locais` (`[nome, tipo TSE, lon, lat]`);
- `secoes`: 20 colunas por seção, para 2026, 2022 e 2018;
- `nomes22` / `nomes18`: o nome do local naquele ano, quando é diferente do de 2026.

## Números de 28/10 (para conferir a página)

- 3.042 urnas zero (0,6% das 499.205 seções), com 526.654 aptos e 423.454 votantes. Flávio teve 18.868 votos nelas e Lula, 395.215.
- Tipo do local: 2.853 convencionais, 167 de preso provisório e 22 temporários.
- Por UF: MA 788, BA 466, PI 312, PA 283, AM 260, CE 235, MG 175. No exterior, 13.
- Nas 1.724 seções casadas nos dois anos, o candidato Bolsonaro teve 3,6% em 2018, 4,6% em 2022 e 4,3% em 2026.
- No país, seções com Bolsonaro ≤ 10 votos: 7.620 em 2018, 4.118 em 2022 e 3.042 em 2026.
