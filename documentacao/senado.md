# Página de bancadas do Senado (`docs/senado.html`)

Simula a composição do Senado a partir de 01/02/2027. É uma página separada, criada a pedido do usuário, e aparece como a aba **Bancada Senado** no seletor do topo (Governador | Senado | Bancada Senado). No `index.html` a aba é um link (`<a>`) dentro de `.modo`; no `senado.html` as abas Governador e Senado apontam para `./` e `./#senado`.

## Dados

| Arquivo | Conteúdo |
|---|---|
| `data/senado.js` | `window.SENADO`: pesquisas e candidatos de 2026 por UF (2 vagas por estado). O mesmo arquivo do mapa. |
| `data/senado-atual.js` | `window.SENADO_ATUAL`: os 27 eleitos em 2022 (`uf`, `nome`, `partido`, `nota`). `window.CORES_PARTIDOS`: cor de cada partido. |

- O partido de um senador atual é a filiação atual conhecida. Se mudar, edite `senado-atual.js`.
- Partido sem cor em `CORES_PARTIDOS` aparece em cinza. Adicione a cor lá.
- Nove senadores com mandato até 2031 concorrem a governador. Eles têm `governador` (nome igual ao de `dados.js`) e `suplente: { nome, partido }` (1º suplente; nomes da Wikipédia, partidos conferidos na imprensa em 04/10/2026; fontes no comentário do arquivo).

## Como a simulação funciona

- Ponto de partida: os 2 primeiros de `pesquisas[0]` em cada UF. Em caso de empate, vale a ordem do array `res`.
- O leitor troca os eleitos em cada linha da tabela. Escolher na vaga 1 quem estava na vaga 2 faz os dois trocarem de lugar.
- **Substitutos** (switch): troca o titular pelo 1º suplente quando ele é marcado como "eleito governador". O ponto de partida marca quem lidera `pesquisas[0]` em `dados.js` (por isso a página carrega `dados.js`). O leitor marca/desmarca cada um na tabela. Cadeira de suplente tem contorno tracejado.
- Grupos: até 6. Cada partido pertence a no máximo um grupo. Na primeira visita, os partidos vêm em **Esquerda / Centro / Direita** (`GRUPOS_PADRAO` em `senado.html`; classificação aproximada, editorial — revise com cuidado). O leitor muda o grupo de qualquer partido pelo menu da lista de bancadas; "Restaurar esquerda / centro / direita" volta ao padrão. Partidos fora da lista (ex.: "Sem partido") ficam em "Sem grupo".
- Escolhas e grupos ficam salvos no `localStorage` do navegador (chaves `senado27:*`: `escolha`, `grupos`, `partidoGrupo`, `subs`, `eleitoGov`). "Voltar às pesquisas" restaura as vagas.

## Visual

- Hemiciclo: 5 fileiras e 81 círculos, preenchidos da esquerda para a direita na ordem dos grupos e, dentro de cada grupo, pelo tamanho da bancada. Círculo com miolo vazado = eleito em 2026.
- Barra empilhada com marcas em 41 (maioria absoluta) e 49 (3/5, quórum de PEC).
- A lista de bancadas mostra cadeiras e % sobre 81.
- Os botões "Todos / Mandato até 2031 / Eleitos em 2026" esmaecem as outras cadeiras.
