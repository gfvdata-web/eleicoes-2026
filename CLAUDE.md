# CLAUDE.md — instruções para alterar este projeto

Leia este arquivo antes de qualquer mudança. Para detalhes, consulte:
- [documentacao/dados.md](documentacao/dados.md): formato dos dados e como atualizar
- [documentacao/pagina.md](documentacao/pagina.md): funcionamento da página
- [documentacao/roadmap.md](documentacao/roadmap.md): o que está planejado

## Contexto

- Site estático publicado no GitHub Pages (`main` → `/docs`), conta **gfvdata-web**, repositório público `governadores-2026`.
- Projeto irmão: uma página equivalente para **senadores** está sendo criada em outro projeto/sessão. Mantenha as convenções visuais e de dados compatíveis (ver "Convenções" abaixo), para que as duas páginas possam ser ligadas ou unificadas no futuro.
- Público: leitores em geral, em português do Brasil. Todo texto visível na página fica em pt-BR.

## Regras do projeto

1. **Sem build, sem framework, sem testes automatizados.** O site é só `docs/index.html` + `docs/data/`. Não adicione npm, bundler, CI de testes nem subagentes.
2. **Fonte única dos dados:** `docs/data/dados.js`. Não coloque números de pesquisa dentro do HTML.
3. **Uma única página/aba.** Novas seções entram em `index.html`; não crie páginas novas sem pedido explícito.
4. **Dependências externas só via CDN confiável** (cdnjs para D3; Google Fonts para a fonte Inter).
5. **Verifique localmente antes do push**: `python -m http.server 8765 --directory docs` e confira que o mapa mostra 27 estados, que o pop-up abre e que o filtro funciona.
6. **Commits** em português, descrevendo o que mudou. Atualize o [CHANGELOG.md](CHANGELOG.md) a cada mudança visível.
7. **Push em `main` publica o site.** Só faça push quando o usuário pedir ou concordar.

## Convenções de dados (resumo)

- Cada estado tem `uf`, `nome`, `regiao`, `pesquisas[]` (a mais recente primeiro) e `candidatos[]`.
- `pesquisas[0]` define a cor do estado no mapa e o percentual mostrado na tabela.
- `tipo: "V"` = votos válidos; `tipo: "T"` = votos totais (estimulada). Sempre indique qual.
- Nomes em `pesquisas[].res` devem ser **idênticos** aos de `candidatos[].nome`, senão a tabela mostra "—".
- Partido desconhecido: use `"—"` em vez de chutar.

## Cuidados editoriais

- Os resumos dos candidatos são texto editorial. Devem ser **neutros, factuais e curtos** (1 a 2 frases), sem adjetivos de valor.
- Prefeitos que concorrem a governador renunciam 6 meses antes da eleição: chame-os de **ex-prefeitos**.
- Vices que assumiram o governo em 2026 (porque o titular saiu para concorrer a outro cargo) são governadores no cargo; descreva assim.
- Na dúvida sobre um fato, prefira omitir ou usar uma descrição genérica. O rodapé da página avisa que os resumos podem conter imprecisões; mantenha esse aviso.
