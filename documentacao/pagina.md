# Página

Tudo está em [`docs/index.html`](../docs/index.html): HTML, CSS e JavaScript inline, sem build.

## Dependências

| Recurso | Origem |
|---|---|
| D3.js 7.9.0 | `cdnjs.cloudflare.com` |
| Fonte Inter | Google Fonts |
| Dados | `data/dados.js` (script) |
| Malha | `data/brasil-estados.geojson` (via `fetch`, por isso exige servidor HTTP) |

## Seções

### 1. Mapa (`<svg id="mapa">`)

- Projeção `d3.geoMercator().fitExtent(...)` num `viewBox` de 800×780. O SVG é responsivo pela largura.
- As siglas são desenhadas no centróide de cada estado. Estados pequenos do litoral têm deslocamento manual no objeto `pequenos` (DF, SE, AL, PB, RN, PE, ES, RJ).
- **Cor = margem do líder** em `pesquisas[0]` (1º menos 2º colocado, em pontos):

| Faixa | Margem | Variável CSS |
|---|---|---|
| Empate técnico | até 4 pts | `--empate` |
| Apertada | 4 a 10 pts | `--apertada` |
| Vantagem | 10 a 20 pts | `--competitiva` |
| Folgada | mais de 20 pts | `--folgada` |

  As faixas ficam no array `FAIXAS`. A cor é neutra quanto a partido de propósito: mostra competitividade, não ideologia.

### 2. Pop-up (`#tip`)

- Abre em `mouseenter` e acompanha o cursor (`moveTip`, que evita sair da tela). No celular, abre ao tocar e fecha ao tocar fora do mapa.
- Mostra: nome do estado, líder e margem, e as 3 pesquisas com barras horizontais, instituto, selo V/T e período de campo.

### 3. Tabela (`#tbody`)

- Uma linha por candidato, agrupada por estado (ordem alfabética do nome do estado). Dentro do estado, a ordem segue o percentual em `pesquisas[0]`.
- Colunas: UF, Candidato, Partido, Última pesquisa (com instituto, tipo e data na primeira linha), Resumo.
- Filtros: **Estado** e **Região**, que são mutuamente exclusivos (escolher um limpa o outro), e o botão "Limpar filtros". Clicar no mapa seleciona o estado e destaca o contorno (`path.sel`).

## Tema

- Cores definidas como variáveis em `:root`, com versão escura em `@media (prefers-color-scheme: dark)`.
- Layout: duas colunas (mapa + legenda) acima de 820px; uma coluna abaixo disso. Margem lateral de 16px.

## Pontos de extensão previstos

- Trocar a fonte do percentual (pesquisa → apuração): ver [roadmap.md](roadmap.md).
- Integração com a página de senadores: manter os mesmos nomes de variáveis CSS, a mesma estrutura de `ESTADOS` e o mesmo GeoJSON facilita reaproveitar o código.
