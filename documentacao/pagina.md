# Página

Tudo está em [`docs/index.html`](../docs/index.html): HTML, CSS e JavaScript inline, sem build.

## Dependências

| Recurso | Origem |
|---|---|
| D3.js 7.9.0 | `cdnjs.cloudflare.com` |
| Fonte Inter | Google Fonts |
| Dados | `data/dados.js` (governador) e `data/senado.js` (Senado), como script |
| Malha | `data/brasil-estados.geojson` (via `fetch`, por isso exige servidor HTTP) |

## Switch de seções (todas as páginas)

`<nav class="secoes" id="secoes">` no topo de cada página, com 3 links: **Pesquisas e análises** (`index.html`), **Nacional e bancadas** (`apuracao.html`) e **Estados** (`es.html`). O item da página atual tem `aria-current="page"` (em `senado.html?apuracao` o script troca para "Nacional e bancadas"). O HTML e o CSS (`.secoes`) são copiados iguais nas 5 páginas; ao mudar, mude em todas.

## Seletor de cargo

No cabeçalho, um grupo de botões (`.modo`, `data-modo="gov"` | `"sen"`) alterna entre **Governador** (dados de `ESTADOS`) e **Senado** (dados de `SENADO`). A troca atualiza título, legenda, cores do mapa, pop-up, tabela e fontes do rodapé. Elementos visíveis só no modo Senado usam a classe `so-sen`.

- O modo inicial vem da URL: `#senado` abre direto no Senado; sem hash, abre em Governador. Clicar no seletor atualiza a URL (`history.replaceState`).
- Cada modo tem sua configuração no objeto `MODOS` (dados, data de atualização, título, textos da legenda e título da aba). `setModo(m)` aplica tudo e repinta o mapa.
- `vagas()` vale 1 (governador) ou 2 (Senado): define a margem usada no mapa e quantos nomes ficam em negrito na tabela e no pop-up (classes `lead` e `.row.eleito`).

## Seções

### 1. Mapa (`<svg id="mapa">`)

- Projeção `d3.geoMercator().fitExtent(...)` num `viewBox` de 800×780. O SVG é responsivo pela largura.
- As siglas são desenhadas no centróide de cada estado. Estados pequenos do litoral têm deslocamento manual no objeto `pequenos` (DF, SE, AL, PB, RN, PE, ES, RJ).
- **Cor = margem** na pesquisa principal, em pontos (governador: AtlasIntel quando houver, senão `pesquisas[0]`; Senado: `pesquisas[0]`). O pop-up lista a pesquisa principal primeiro. Governador: 1º − 2º colocado. Senado: 2º − 3º (disputa pela 2ª vaga); se `pesquisas[0]` for do tipo `C`, a margem é dividida por 2. As mesmas faixas valem para os dois cargos.

| Faixa | Margem | Variável CSS |
|---|---|---|
| Empate técnico | até 4 pts | `--empate` |
| Apertada | 4 a 10 pts | `--apertada` |
| Vantagem | 10 a 20 pts | `--competitiva` |
| Folgada | mais de 20 pts | `--folgada` |

  As faixas ficam no array `FAIXAS`. A cor é neutra quanto a partido de propósito: mostra competitividade, não ideologia.
- **Colorir por partido** (seletor `.seg`, `data-colorir="folga"` | `"partido"`): no modo Partido a cor vem de `CORES_PARTIDOS` (em `data/senado-atual.js`) para o partido do 1º colocado (governador) ou dos dois primeiros (Senado). Se as duas vagas do Senado têm cores diferentes, o estado é dividido ao meio (1º colocado à esquerda, 2º à direita) por um `<linearGradient>` com corte seco, criado em `metades()`. A legenda (`legenda()`) conta estados ou vagas por partido/grupo.
- **Grupos políticos** (`#grupos`): o leitor cria grupos com nome, cor e partidos; um partido pertence a um só grupo. Os grupos substituem a cor e o nome do partido no modo Partido. Ficam em `localStorage` (`grupos`, `colorir`), só naquele navegador; a página funciona sem isso.

### 2. Pop-up (`#tip`)

- Abre em `mouseenter` e acompanha o cursor (`moveTip`, que evita sair da tela). No celular, abre ao tocar e fecha ao tocar fora do mapa.
- Mostra: nome do estado, líder e margem (no Senado: os dois à frente e a disputa pela 2ª vaga), e as pesquisas com barras horizontais, instituto, selo V/T/C e período de campo.

### 3. Tabela (`#tbody`)

- Uma linha por candidato, agrupada por estado (ordem alfabética do nome do estado). Dentro do estado, a ordem segue o percentual na pesquisa principal.
- Colunas: UF, Candidato, Partido, Última pesquisa (com instituto, tipo e data na primeira linha), Resumo.
- Filtros: **Estado** e **Região**, que são mutuamente exclusivos (escolher um limpa o outro), e o botão "Limpar filtros". Clicar no mapa seleciona o estado e destaca o contorno (`path.sel`).

## Abas Comparativo (pesquisa × resultado)

Três botões no seletor de cargo (`data-modo="cpres" | "cgov" | "csen"`, URLs `#comparativo-presidente`, `#comparativo-governador`, `#comparativo-senado`) escondem `#secPesq` e mostram `#secComp`. O código fica no bloco `<script>` próprio que define `window.Comparativo.abrir(m)`; a troca é feita por `trocar(m)` no script principal.

- **Dados:** pesquisas de `presidente.js`, `dados.js` e `senado.js`; resultado de `data/apuracao/<cargo>.json` (relido se tiver mais de 2 min). Sem resultado (`pct` 0) o estado fica cinza.
- **Presidente (`cpres`):** sem mapa, sem ranking e sem filtros. O seletor lista as pesquisas nacionais (`PRESIDENTE[0].pesquisas`, com o erro médio de cada uma) e a tabela mostra uma por vez contra o total `BR`.
- **Seletor "Pesquisa comparada"** (`#cPesq`), em governo e Senado: "Última pesquisa de cada estado" (`pesquisas[0]`) ou um instituto (a pesquisa mais recente dele em cada estado). Vale para mapa, resumo e tabela.
- **Conversão:** tudo em % de votos válidos. `V` fica como está; `T` e `C` são reescaladas para os candidatos listados somarem 100%.
- **Métricas** (`comparar()`): erro médio = média de |pesquisa − urna| dos candidatos da pesquisa que tiveram votos; acerto = os `vagas` primeiros da pesquisa são os `vagas` primeiros da urna; erro na margem = margem da pesquisa − margem da urna entre os colocados reais (1º − 2º; Senado 2º − 3º).
- **Mapa:** cor por erro médio (até 2 / 2–4 / 4–7 / mais de 7 pts, reaproveitando as variáveis das faixas de folga) ou por acerto; o número abaixo da sigla é o erro médio.
- **Cards (governo e Senado), nesta ordem:** mapa, tabela pesquisa × urna por estado com filtros próprios (`#cEstado`, `#cRegiao`) e "Institutos" (ranking; clicar seleciona o instituto).

## Tema

- Cores definidas como variáveis em `:root`, com versão escura em `@media (prefers-color-scheme: dark)`.
- Layout: duas colunas (mapa + legenda) acima de 820px; uma coluna abaixo disso. Margem lateral de 16px.

## Pontos de extensão previstos

- Trocar a fonte do percentual (pesquisa → apuração): ver [roadmap.md](roadmap.md).
- Novos cargos (se houver): seguir o mesmo padrão do Senado — novo arquivo em `docs/data/`, novo botão no seletor de cargo, mesmo GeoJSON e mesmas variáveis CSS.
