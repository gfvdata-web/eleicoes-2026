# Roadmap

Status: 🟢 feito · 🟡 em andamento / próximo · ⚪ futuro (ainda não detalhado)

## 🟢 v1 — Pesquisas para governador (04/10/2026)

- Mapa com os 27 estados coloridos por margem do líder.
- Pop-up com as 3 pesquisas mais recentes de cada estado.
- Tabela com partido e resumo dos candidatos, com filtro por estado e região.
- Publicado em https://gfvdata-web.github.io/eleicoes-2026/

## 🟡 Senado na mesma página

- Em andamento em sessão paralela, **neste mesmo repositório e no mesmo `index.html`**.
- Já existe: `docs/data/senado.js` (27 UFs, 2 vagas) e o seletor Governador/Senado no cabeçalho.
- Ao concluir: atualizar [pagina.md](pagina.md) (seção "Seletor de cargo"), o [CHANGELOG](../CHANGELOG.md) e as pendências de dados do Senado em [dados.md](dados.md).

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
