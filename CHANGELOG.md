# Changelog

Formato: data — descrição. Mudanças mais recentes no topo.

## 2026-10-04

- **Nova aba "Bancada Senado" (`senado.html`):** hemiciclo com as 81 cadeiras, somando os 27 senadores com mandato até 2031 aos 54 favoritos nas pesquisas de 2026. O leitor pode trocar os eleitos em cada estado e criar grupos de partidos (linhas de maioria em 41 e de 3/5 em 49). O switch "Substitutos" troca os senadores que disputam o governo pelo 1º suplente (começa com quem lidera a pesquisa para governador; ajustável por estado). Novo arquivo de dados `docs/data/senado-atual.js`.
- **Senado publicado:** seletor Governador/Senado no topo da página. No modo Senado, o mapa é colorido pela disputa da 2ª vaga (2º − 3º colocado), os dois primeiros aparecem em destaque e o rodapé lista as fontes do Senado. O endereço `…/eleicoes-2026/#senado` abre direto nesse modo.

- **Repositório renomeado** de `governadores-2026` para `eleicoes-2026`. Novo endereço do site: https://gfvdata-web.github.io/eleicoes-2026/

- **Documentação:** atualizada para governador e Senado no mesmo repositório e na mesma página (seletor de cargo, `senado.js`, regras para sessões paralelas).
- **Senado (em andamento):** adicionado `docs/data/senado.js` com pesquisas para o Senado nos 27 estados.
- **Documentação:** README revisado; adicionados `CLAUDE.md`, `CHANGELOG.md` e a pasta `documentacao/` (dados, página, roadmap).
- **v1 publicada:** mapa interativo das pesquisas para governador (27 UFs, 3 pesquisas por estado), pop-up por estado e tabela de candidatos com partido, resumo e filtros. Publicada no GitHub Pages (`main` → `/docs`).
