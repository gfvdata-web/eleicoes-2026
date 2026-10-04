# Roadmap

Status: 🟢 feito · 🟡 em andamento / próximo · ⚪ futuro (ainda não detalhado)

## 🟢 v1 — Pesquisas para governador (04/10/2026)

- Mapa com os 27 estados coloridos por margem do líder.
- Pop-up com as 3 pesquisas mais recentes de cada estado.
- Tabela com partido e resumo dos candidatos, com filtro por estado e região.
- Publicado em https://gfvdata-web.github.io/eleicoes-2026/

## 🟢 Senado na mesma página (04/10/2026)

- Seletor Governador/Senado no cabeçalho; `#senado` na URL abre direto no Senado.
- Mapa do Senado colorido pela disputa da 2ª vaga (2º − 3º colocado).
- `docs/data/senado.js` com 27 UFs, 2 vagas e tipos V/T/C.

## 🟢 Aba "Bancada Senado" — `senado.html` (04/10/2026)

- Hemiciclo de 81 cadeiras: 27 com mandato até 2031 + 54 favoritos nas pesquisas de 2026.
- Troca básica dos eleitos por estado (menu com todos os candidatos da pesquisa).
- Grupos de partidos criados pelo leitor, com exemplo pronto e linhas de maioria (41) e de 3/5 (49).
- Switch "Substitutos": senadores que disputam o governo dão lugar ao 1º suplente.
- Aba no seletor do topo (`index.html` → `senado.html`).
- Partido atual dos suplentes conferido na imprensa (04/10/2026); lista de bancadas com %.
- Próximos ajustes (a combinar): apuração.

## 🟡 Ajustes na página atual

- O usuário fará mais alterações. Registrar cada pedido aqui antes de implementar, se for algo grande.
- Pendências de dados já conhecidas estão em [dados.md](dados.md#pendências-conhecidas-nos-dados).

## ⚪ Troca das pesquisas pela apuração

Objetivo: depois da eleição, substituir (ou complementar) as pesquisas pelos resultados oficiais, **para governador e Senado**. **Ainda não iniciado; será planejado quando a apuração começar.** Pontos a decidir na hora:

- **Fonte:** provavelmente os dados de divulgação do TSE (resultados por UF). Confirmar formato e disponibilidade.
- **Atualização:** manual (editar `dados.js`) ou automática (script + GitHub Actions publicando um JSON). Os outros projetos da conta já usam coleta automática versionada, o que pode servir de referência.
- **Modelo de dados:** provável novo campo por estado, por exemplo `apuracao: { pctUrnas, atualizadoEm, res: [[nome, %válidos], ...], situacao: "eleito" | "2º turno" }`, mantendo `pesquisas` para comparação.
- **Senado:** não tem 2º turno; são eleitos os 2 mais votados de cada estado.
- **Exibição:** cor do mapa pelo vencedor ou pela situação (eleito no 1º turno / 2º turno); pop-up com apuração versus última pesquisa; coluna extra na tabela.
- **2º turno:** estados com 2º turno em 25/10/2026 (data a confirmar) podem precisar de uma nova rodada de pesquisas.
