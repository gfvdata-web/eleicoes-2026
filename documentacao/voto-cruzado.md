# Voto cruzado (`voto-cruzado.html` + `scripts/voto_cruzado.py`)

Página criada a pedido do usuário em 06/10/2026. Desde 06/10 é a seção **"Voto cruzado"** do switch de seções no topo do site. As subabas "Análise por campo" e "Urna esperada × urna anômala" têm seletor de **estado** (os 27; padrão ES; lembrado no navegador em `vc-uf`; endereço `#uf=sp` e `#urnas=sp`). A unidade "Estados" mostra o Brasil. A subaba "Comparativo estados" mostra vários estados lado a lado.

Base estatística, fórmulas, resultados de referência e plano da opção A: [voto-cruzado-estatistica.md](voto-cruzado-estatistica.md).

## Objetivo

Medir se o voto para presidente acompanha os outros cargos do 1º turno (governador, Senado, deputado federal e estadual) e achar onde ele se descola. Direção principal combinada com o usuário: **prever o voto para presidente a partir dos outros votos** (ex.: urna com muito voto de esquerda para deputado, Senado e governador, mas pouco para o Lula).

## Limite: o voto é secreto

Não há dado por eleitor. Testado em 06/10: o RDV (Registro Digital do Voto) de cada urna, publicado em
`https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/...` (pleito 3220; índice das seções em `config/es/es-p003220-cs.json`, arquivos de cada seção em `dados/es/<mun>/<zona>/<seção>/p003220-es-m<mun>-z<zona>-s<seção>-aux.json`), guarda **uma lista por cargo, em ordem de número**, sem ligação entre os cargos de um mesmo eleitor. Amostra de 145 urnas: todas assim; ~15 KB por urna (ES inteiro ≈ 150 MB, ~1h40 em sequência), sem limite 429. Algumas seções (agregadas) dão 404. Conclusão: o RDV não acrescenta nada à votação por seção e não foi baixado inteiro. A unidade da análise é a urna (~240 votantes).

## Réguas

Duas réguas, escolhidas no topo da página (guardadas em `localStorage` `vc-regua`): **A, aliança presidencial** (padrão desde 06/10, por explicar melhor o voto para presidente) e **B, campo do partido** (esquerda / centro / direita, como em `camara.html`).
A régua A agrupa em aliança de Lula / neutros / aliança de Flávio: coligação no TSE → apoio declarado com fonte → neutro; deputados pelo partido da coligação presidencial.
Critérios, resultados e comparação em [voto-cruzado-estatistica.md](voto-cruzado-estatistica.md) (seções 3 e 5.6).

## Dados

1. `python scripts/voto_cruzado.py [UF ...]` (sem UF: os 27, ~12 min) lê os arquivos do TSE em `apuracao-bruto/secoes-br/` e o partido/destino de cada número em
   `apuracao-bruto/<cargo>/<UF>.json`. Grava `docs/data/voto-cruzado/<uf>.json` (`uf`, `mun`, `locais`, `ent` = [cargo, número, nome, sigla], uma por candidato a presidente,
   governador e senador e uma por partido nos deputados; `secoes` = [local, zona, seção, aptos, comparecimento, entidade, votos, ...], só pares com voto) e `brasil.json`
   (por UF: `ent`, `tot` e `mun` no mesmo formato de pares). Só seções instaladas e não anuladas; só votos válidos (sem brancos, nulos e sub judice). ~141 MB no total (SP: 31 MB).
2. `python scripts/alinhamento.py` lê `apuracao-bruto/candidatos/consulta_cand_2026.zip` (TSE, `consulta_cand/`) e `docs/data/voto-cruzado/apoios-declarados.json`
   (editado à mão: `uf`, `cargo` 1 ou 2, `numero`, `nome`, `g` 0/1/2, `fonte`, `nota`) e grava `classificacao.json`: `b` {sigla: grupo} e `a` {`pres`, `dep`, `cand` {UF: [[cargo, número, nome, sigla,
   coligação, votos, grupo, critério, fonte]]}, `coligacao_lula`, `coligacao_flavio`}.

Ao gravar no Windows com o servidor local aberto, a escrita pode falhar ("Invalid argument"): pare o servidor e rode de novo.

## Página

- Seletor de **régua** no topo (vale para todas as subabas). Todas as somas por grupo e os modelos são recalculados no navegador a partir dos votos por entidade.
- Controles: campo (esquerda / direita, ou Lula / Flávio na régua A), comparação (previsto, governador, Senado, dep. federal, dep. estadual), unidade (urnas, locais de votação, municípios do ES; **Estados** = Brasil, com o modelo nacional, mapa dos estados e tabela por UF) e filtro de município (clique no mapa).
- Barras: cada cargo por campo no estado ou no município.
- Modelo: regressão linear ponderada pelo comparecimento, nas urnas do estado inteiro, do % do campo para presidente sobre o % do mesmo campo nos 4 outros cargos (calculada no navegador). Em 06/10: R² 0,74 (esquerda) e 0,82 (direita); o Senado tem o maior peso.
  **Cargo vazio:** se o grupo tem menos de 3% dos votos num cargo ou desvio-padrão entre urnas abaixo de 2 p.p. (`VAZIO_MED`, `VAZIO_DP`), o cargo sai do ajuste (peso 0, "fora" no card, com aviso).
  **Selo de encaixe** (`confianca`): bom com R² ≥ 0,6, moderado de 0,4 a 0,6, fraco abaixo de 0,4; com encaixe fraco os pesos ficam esmaecidos e marcados como sem interpretação. Vale também para o comparativo.
- Dispersão (presidente × comparação, linha de igualdade), mapa dos municípios pela diferença (±10 p.p.) e tabela das unidades com maior diferença, ordenável.
- Limites matemáticos para comparação com um cargo de 1 voto (não Senado): voto dividido mínimo = metade da soma das diferenças entre os 3 campos; núcleo mínimo do campo = máx(0, a + b − 1).

## Estado escolhido (análise e urnas)

O seletor carrega `docs/data/voto-cruzado/<uf>.json` e a malha `docs/data/uf/<uf>/municipios.geojson` + `municipios.json` (ES: `docs/data/es/municipios.geojson` e `municipios.js`);
o código TSE da malha vem com zero à esquerda e é normalizado. Com mais de 6 mil pontos (urnas de estados grandes), a dispersão da análise é desenhada em canvas, sem clique para destacar.
Nada precisou ser baixado: os dados por urna dos 27 estados já estavam processados.

## Subaba "Urna esperada × urna anômala" (`voto-cruzado.html#urnas=es`)

- **Índice de anomalia** de uma urna = raiz da média dos quadrados dos dois erros da previsão (% da esquerda e % da direita para presidente, real − previsto), em p.p. Zero = votou para presidente exatamente como o padrão do estado indica dado o voto nos outros 4 cargos. No ES (06/10): mediana 3,6 p.p.; 90% abaixo de 7,5.
- Começa com a urna de menor e a de maior índice entre as com 200+ votantes. Cada lado tem um atalho (as 15 mais esperadas / as 15 mais anômalas) e a escolha de **qualquer urna** do ES por município e seção (todas, inclusive as pequenas). Selo pelo índice: "Esperada" = 25% menores; "Anômala" = 10% maiores; "Intermediária" = o resto; a frase diz o percentil e avisa urna com menos de 200 votantes. Em 06/10: esperada = Vitória, zona 52, seção 407 (0,0); anômala = Pinheiros, zona 39, seção 111 (26,1: Lula 74%, previsto 49%; a anomalia vem de votos locais, como 84% em um deputado federal do PSB e 79% no centro para deputado estadual, e do governador do MDB contado como centro).
- Lado a lado: resumo (índice, real × previsto, campos em cada cargo) e, por cargo, os votos da urna. **No ES**: lista completa (deputados por partido e cada candidato em "Todos os candidatos", brancos e nulos), de `docs/data/es/secoes/cargos.json` e `m/<tse>.json`. **Outros estados**: votos por entidade do `<uf>.json` (candidatos a presidente, governador e senador; deputados por partido, nominais + legenda), sem brancos e nulos. Ter a lista por candidato a deputado no Brasil exigiria só processar os arquivos já baixados em `apuracao-bruto/secoes-br/`, mas somaria centenas de MB ao site.

## Subaba "Classificação" (`voto-cruzado.html#classificacao`)

Tabela de todos os candidatos e partidos com o grupo de cada um (régua A: presidente, governador e senador por estado, deputados por partido, nacional ou por estado; régua B: partidos),
o critério e a fonte. Filtros por busca, estado, cargo e "só os que mudei / só neutros". O menu da linha muda o grupo; as mudanças valem em todas as abas e ficam em
`localStorage` (`vc-reclass`), só naquele navegador. "Exportar minhas mudanças" baixa um JSON (`{tipo, data, mudancas: {chave: grupo}}`); "Importar" lê esse JSON. Para tornar uma mudança padrão
do site, grave-a em `apoios-declarados.json` (governador/senador) ou no script `alinhamento.py` (deputados, presidente, régua B) e rode `alinhamento.py`.

## Subaba "Comparativo estados" (`voto-cruzado.html#estados=es,sp`)

Um gráfico "Presidente × previsto" por estado escolhido (padrão ES e SP; o endereço guarda a lista), lado a lado, com a mesma escala. A previsão de cada estado usa o modelo ajustado nas urnas **dele** (calculado no navegador ao carregar `<uf>.json`). Controles: campo, unidade (urnas, locais, municípios) e "Adicionar estado"; × remove. O gráfico é em canvas (SP tem ~100 mil urnas), com tooltip pelo ponto mais próximo. Abaixo de cada gráfico, **conclusões geradas dos números** (função `conclusoes`): onde a nuvem está na diagonal (% do campo no estado × Brasil, ±3 p.p.), espalhamento (faixas de 50% e 80% dos votantes; >30 p.p. = "comprida", <15 = "curta"), encaixe (R² ≥ 0,85 "estreita", ≥ 0,6 "moderada", senão "larga"), acima × abaixo (% dos votantes em unidades além de ±10 p.p. para urnas, ±5 para locais, ±3 para municípios; equilíbrio se nenhum lado tem mais que o dobro do outro; "quase nada" se os dois somam menos de 3%) e os municípios com 2 mil votantes ou mais que mais fogem do previsto.

## Dados do Brasil (baixados em 06/10)

`apuracao-bruto/secoes-br/` (fora do git, 2,6 GB compactados, ~20 GB descompactados): `votacao_secao_2026_<UF>.zip` dos 27 estados, `votacao_secao_2026_BR.zip` (presidente), `detalhe_votacao_secao_2026.zip` e `eleitorado_local_votacao_2026.zip`, de `https://cdn.tse.jus.br/estatistica/sead/odsele/`. O zip do ES baixado agora é maior que o de 05/10 (319 MB × 274 MB descompactados) porque o TSE preencheu o nome e o endereço do local de votação; os votos são idênticos seção por seção, então `es-secoes` não precisou ser refeito.
