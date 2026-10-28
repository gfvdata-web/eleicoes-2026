# Urnas até 19h (`2turno-urnas.html`)

Página do 2º turno, criada a pedido do usuário em 28/10/2026, que fica no switch do 2º turno como **Urnas até 19h**. Ela mostra as urnas que ficaram abertas depois do horário normal com a prorrogação da votação.

## O que aconteceu
Em 25/10/2026, às 17h03, o ministro Zanin (STF) prorrogou a votação do 2º turno até as 19h (horário de Brasília). A prorrogação valeu só nas seções que ainda não tinham encerrado. As urnas já fechadas não podiam ser reabertas.

O TSE **não publicou lista** das seções que usaram a prorrogação. A Gazeta do Povo, com base em apuração do G1 nos logs de urna, contou 35,5 mil votos para presidente depois das 17h, sem divisão por estado nem por candidato.

## Critério (nosso, não oficial)
- **Urna postergada:** urna cujo encerramento, convertido para o horário de Brasília, foi **a partir das 18h45** (minuto cheio: 18:45:00 em diante).
  - O limite fica na constante `LIMITE` de `scripts/urnas_19h.py`; vale para o mapa, os cartões e o histograma.
  - Histórico: em 28/10 o corte era 17h30; o usuário passou para 18h45 depois de ver a dispersão por minuto. A fila normal acaba por volta das 17h40, há um patamar de 5 a 30 urnas por minuto até ~18h55 e um pico entre 19h00 e 19h10 (as urnas que ficaram até o fim da prorrogação).
  - Na subaba Comparativo, o leitor muda o corte com um controle deslizante (17h15 a 19h15).
- **Fonte do horário:** o horário vem de `DT_ENCERRAMENTO` no boletim de urna e está em **hora local**.
  - O fuso de cada urna é deduzido de `DT_ABERTURA`, porque todas abriram às 8h de Brasília: `fuso = round(8h − abertura local)`.
  - Isso cobre AC, oeste do AM, MT, MS, RO e RR sem precisar de tabela.
  - Um município tem um fuso só: toda urna usa o fuso mais comum do município (só entram na conta as aberturas a até 10 min de uma hora cheia), o que corrige urnas que abriram atrasadas.
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

`docs/data/urnas19h/minutos.json` (lido só no Comparativo):
- `controle` (`min`, `max`, `padrao` do controle deslizante), `colunas` e, para `br` e cada UF em `ufs`, uma linha por minuto de encerramento (Brasília): `[minuto, urnas, flavio, lula, brancos, nulos, aptos, comparecimento]`, com `minuto` em minutos desde 0h.
- Encerramentos antes de 17h00 ficam no balde 1019 (16:59) e de 20h00 em diante no 1200. A página soma as linhas com `minuto >= corte` (postergadas) e o resto (não postergadas).

`docs/data/urnas19h/secoes.json`:
- `colunas` e `secoes`, uma linha por urna que encerrou a partir de `SECOES_DESDE` (17h15, o mínimo do controle): `[uf, municipio, zona, secao, local, encerramento, aptos, comparecimento, flavio, lula, brancos, nulos]`. O encerramento vem em minuto cheio (HH:MM), e a página filtra pelo corte escolhido.

## Página
- **Mapa e resumo (`#mapa`):**
  - mapa do Brasil colorido pelo número de urnas postergadas, ou pelo % das urnas da UF;
  - pop-up por UF;
  - cards com o total e Flávio × Lula nessas urnas;
  - histograma dos horários de encerramento, com marcas em 17h03 (decisão) e 18h45 (critério).
- **Comparativo (`#comparativo`):**
  - seletor Brasil / UF;
  - controle deslizante do corte (padrão 18h45) e duas dispersões por minuto de encerramento: nº de urnas (escala log) e % de Lula nos válidos (ponto do tamanho do nº de urnas), com os minutos depois do corte em destaque;
  - tabela "Urnas não postergadas × Urnas postergadas", recalculada pelo corte, com votos e % válidos de Flávio e Lula, brancos, nulos e comparecimento;
  - barras empilhadas;
  - lista filtrável das urnas postergadas pelo corte escolhido, que carrega `secoes.json` só nessa aba.
