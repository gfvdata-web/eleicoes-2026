# Urnas até 19h (`2turno-urnas.html`)

Página do 2º turno, criada a pedido do usuário em 28/10/2026, que fica no switch do 2º turno como **Urnas até 19h**. Ela mostra as urnas que ficaram abertas depois do horário normal com a prorrogação da votação.

## O que aconteceu
Em 25/10/2026, às 17h03, o ministro Zanin (STF) prorrogou a votação do 2º turno até as 19h (horário de Brasília). A prorrogação valeu só nas seções que ainda não tinham encerrado. As urnas já fechadas não podiam ser reabertas.

O TSE **não publicou lista** das seções que usaram a prorrogação. A Gazeta do Povo, com base em apuração do G1 nos logs de urna, contou 35,5 mil votos para presidente depois das 17h, sem divisão por estado nem por candidato.

## Critério (nosso, não oficial)
- **Urna postergada:** urna cujo encerramento, convertido para o horário de Brasília, foi **depois das 17h30**.
  - O limite fica na constante `LIMITE` de `scripts/urnas_19h.py`.
  - Foi escolhido com o usuário para excluir as urnas que só fecharam alguns minutos depois das 17h por causa da fila normal.
- **Fonte do horário:** o horário vem de `DT_ENCERRAMENTO` no boletim de urna e está em **hora local**.
  - O fuso de cada urna é deduzido de `DT_ABERTURA`, porque todas abriram às 8h de Brasília: `fuso = round(8h − abertura local)`.
  - Isso cobre AC, oeste do AM, MT, MS, RO e RR sem precisar de tabela.
  - Urna com abertura fora do padrão (mais de 20 min de diferença) herda o fuso mais comum do município.
  - Urna sem horário de encerramento conta como não postergada e entra em `sem_horario`.
- **Exterior (ZZ):** fica de fora, porque cada país tem seu fuso.
- **Limite do critério:** urna postergada não quer dizer que todos os votos dela foram dados depois das 17h. A maior parte foi dada durante o dia.

## Dados
Os dados são gerados por `python scripts/urnas_19h.py [--baixar] [--manter]`, que usa só a biblioteca padrão.
- **Download:** os `bweb_2t_<UF>_*.zip` dos dados abertos do TSE (dataset `resultados-2026-boletim-de-urna`, links lidos pela API CKAN) vão para `apuracao-bruto/urnas19h/`. Ao todo são cerca de 150 MB.
- **Leitura:** o script lê só o cargo Presidente (`CD_CARGO_PERGUNTA = 1`). Os votos de Lula são os do número 13 e os de Flávio, os do 22.
- **Limpeza:** no fim, apaga os zips, a menos que receba `--manter`.
- **Pegadinha do portal:** o recurso de RR aponta para o `.sha512`, e o script tira o sufixo.

`docs/data/urnas19h/resumo.json`:
- `criterio`, `fonte`, `gerado_em`, `candidatos`.
- `br` e `ufs.<UF>` têm a forma `{nao_post: G, post: G, sem_horario}`, com `G = {urnas, aptos, comparecimento, lula, flavio, brancos, nulos}`.
  - Nas UFs há também `fusos` (os encontrados) e `municipios` (os 8 com mais urnas postergadas, no formato `[nome, n]`).
- `histograma`: urnas por faixa de 15 min do horário de encerramento (Brasília), de 16h30 a 19h30. Mais `antes` e `depois`.

`docs/data/urnas19h/secoes.json`:
- `colunas` e `secoes`, uma linha por urna postergada: `[uf, municipio, zona, secao, local, encerramento, aptos, comparecimento, flavio, lula, brancos, nulos]`.

## Página
- **Mapa e resumo (`#mapa`):**
  - mapa do Brasil colorido pelo número de urnas postergadas, ou pelo % das urnas da UF;
  - pop-up por UF;
  - cards com o total e Flávio × Lula nessas urnas;
  - histograma dos horários de encerramento, com marcas em 17h03 (decisão) e 17h30 (critério).
- **Comparativo (`#comparativo`):**
  - seletor Brasil / UF;
  - tabela "Urnas não postergadas × Urnas postergadas" com votos e % válidos de Flávio e Lula, brancos, nulos e comparecimento;
  - barras empilhadas;
  - lista filtrável das urnas postergadas, que carrega `secoes.json` só nessa aba.
