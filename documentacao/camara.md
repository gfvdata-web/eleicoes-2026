# Página de bancadas da Câmara (`docs/camara.html`)

Mostra como fica a Câmara dos Deputados a partir de 01/02/2027 (513 cadeiras), pela apuração do TSE. Criada a pedido do usuário em 04/10/2026, no modelo da [Bancada Senado](senado.md). Aparece como a aba **Bancada Câmara** em `apuracao.html` e em `senado.html?apuracao`. Não há versão de pesquisas (não há pesquisas de deputado no site).

## Dados

- Lê `data/apuracao/deputado-federal.json` (gerado por `scripts/apuracao.py`) a cada 60 s, com `?t=` para evitar cache.
- Cadeiras = campo `eleitos` de cada UF: `[nome, % válidos, sigla, votos, conf]`. `conf = 1`: o TSE marcou como eleito (confirmado); `conf = 0`: vaga provisória que o TSE distribui à lista/federação com os votos apurados, dada aos mais votados dela (projetado).
- Vagas por UF fixas em `VAGAS` (distribuição de 2022, total 513). UF sem `eleitos` aparece como vagas "sem apuração".
- Siglas do TSE viram os nomes do site em `SIGLAS` (ex.: `UNIÃO` → `União Brasil`, `PODE` → `Podemos`). Cores em `CORES_PARTIDOS` (`senado-atual.js`); partido sem cor fica cinza. Partido novo: acrescente sigla e cor.

## Visual e controles

- Hemiciclo de 14 fileiras, preenchido da esquerda para a direita na ordem dos grupos e, dentro deles, pelo tamanho da bancada. Círculo cheio = confirmado; com miolo vazado = projetado; só contorno = sem apuração.
- "Todos / Confirmados / Projetados" esmaece as outras cadeiras.
- Barra empilhada com marcas em 257 (maioria absoluta), 308 (3/5, PEC) e 342 (2/3).
- Grupos iguais aos da Bancada Senado (`GRUPOS_PADRAO`, esquerda / centro / direita; Missão em Direita), salvos no navegador com chaves `camara27:grupos` e `camara27:partidoGrupo`.
- Tabela por estado: vagas, % de urnas, cadeiras por partido e lista dos deputados (mais votados primeiro).

## Assembleias (`camara.html?uf=SP`)

Aba **Assembleias**, a pedido do usuário. Mesma página e mesmo código, com o parâmetro `uf`:

- Lê `data/apuracao/deputado-estadual.json` e mostra só a UF escolhida no seletor "Estado" (a troca atualiza a URL sem recarregar). `?uf=` vazio ou inválido usa o último estado escolhido (`camara27:uf`) ou SP.
- Cadeiras por estado: `vagasEst(uf)` = 3 × deputados federais até 36; acima disso, 24 + deputados federais (CF, art. 27). DF = 24 (Câmara Legislativa). Bate com os eleitos do TSE em 2026.
- O hemiciclo ajusta fileiras e tamanho dos círculos ao total (`geometria()`). As marcas da barra são calculadas para a casa: maioria absoluta, 3/5 e 2/3 (`marcas()`).
- O card de baixo vira a lista dos deputados do estado (posição, partido, votos, % válidos, eleito/projetado).
- Grupos são os mesmos da Câmara (mesmas chaves no navegador). DC entra em Direita; Agir, Mobiliza e Democrata ficam sem grupo.
