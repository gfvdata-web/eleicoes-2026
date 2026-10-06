# CLAUDE.md — instruções para alterar este projeto

Leia este arquivo antes de qualquer mudança. Para detalhes, consulte:
- [documentacao/dados.md](documentacao/dados.md): formato dos dados e como atualizar
- [documentacao/pagina.md](documentacao/pagina.md): funcionamento da página
- [documentacao/roadmap.md](documentacao/roadmap.md): o que está planejado
- [documentacao/senado.md](documentacao/senado.md): página de bancadas do Senado (`senado.html`)
- [documentacao/camara.md](documentacao/camara.md): página de bancadas da Câmara e das Assembleias (`camara.html` e `camara.html?uf=XX`, só apuração, lê `deputado-federal.json` / `deputado-estadual.json` em `docs/data/apuracao/`)
- [documentacao/apuracao.md](documentacao/apuracao.md): página de apuração (`apuracao.html`, dados em `docs/data/apuracao/`, coleta em `scripts/apuracao.py`)
- [documentacao/es.md](documentacao/es.md): página do Espírito Santo (`es.html`, só apuração do TSE por município, dados em `docs/data/es/`, coleta em `scripts/apuracao_es.py`)
- [documentacao/es-secoes.md](documentacao/es-secoes.md): votos por urna no ES (`es-secoes.html`, seção "Urnas ES" do menu; município → zona → local de votação → seção; dados em `docs/data/es/secoes/`, gerados por `scripts/secoes_es.py`)
- [documentacao/voto-cruzado.md](documentacao/voto-cruzado.md): análise de voto cruzado entre cargos; base estatística e matemática (para explicar números da página) em [documentacao/voto-cruzado-estatistica.md](documentacao/voto-cruzado-estatistica.md) (`voto-cruzado.html`, seção "Voto cruzado" do menu, análise do ES, unidade Estados e comparativo entre estados; dados dos 27 estados em `docs/data/voto-cruzado/`, gerados por `scripts/voto_cruzado.py`; classificação das réguas em `classificacao.json`, por `scripts/alinhamento.py`)

## Contexto

- Site estático publicado no GitHub Pages (`main` → `/docs`), conta **gfvdata-web**, repositório público `eleicoes-2026`.
- O site cobre **dois cargos na mesma página**: governador e Senado, alternados por um seletor no topo (`data-modo="gov"` / `"sen"`). Mesmo repositório, mesma pasta, mesmo `index.html`, mesmo GeoJSON.
- O trabalho pode acontecer em sessões paralelas (uma para governador, outra para Senado) **no mesmo diretório**. Antes de commitar, rode `git status` e adicione **apenas os arquivos que você alterou** (nada de `git add -A`). Não reverta nem reescreva mudanças de outra sessão em `index.html`; se houver conflito, pergunte ao usuário.
- Público: leitores em geral, em português do Brasil. Todo texto visível na página fica em pt-BR.

## Regras do projeto

1. **Sem build, sem framework, sem testes automatizados.** O site é só `docs/index.html` + `docs/data/`. Não adicione npm, bundler, CI de testes nem subagentes. Exceções combinadas para a apuração: `scripts/apuracao.py`, `scripts/apuracao_es.py`, `scripts/secoes_es.py`, `scripts/voto_cruzado.py`, `scripts/alinhamento.py` e `scripts/metricas_estados.py` (Python, só biblioteca padrão, roda no computador do usuário) e `.github/workflows/pages.yml` (só publica `docs/`).
2. **Dados só nos arquivos de dados:** governador em `docs/data/dados.js` (`window.ESTADOS`), Senado em `docs/data/senado.js` (`window.SENADO`); senadores com mandato até 2031 e cores dos partidos em `docs/data/senado-atual.js`; pesquisas de presidente (só para as abas Comparativo) em `docs/data/presidente.js` (`window.PRESIDENTE`). Não coloque números de pesquisa dentro do HTML.
3. **Uma única página.** Governador e Senado convivem em `index.html` via seletor de cargo; a exceção é `senado.html` (simulação das bancadas do Senado, criada a pedido do usuário; ver [documentacao/senado.md](documentacao/senado.md)) `apuracao.html` (réplica de `index.html` para a apuração; ver [documentacao/apuracao.md](documentacao/apuracao.md)) e `es.html` (apuração do Espírito Santo por município, sem pesquisas; ver [documentacao/es.md](documentacao/es.md)) e `camara.html` (bancadas da Câmara pela apuração; ver [documentacao/camara.md](documentacao/camara.md)) e `es-secoes.html` (votos por urna no ES; ver [documentacao/es-secoes.md](documentacao/es-secoes.md)) e `voto-cruzado.html` (relação entre os votos nos cargos; ver [documentacao/voto-cruzado.md](documentacao/voto-cruzado.md)). O switch de seções no topo de todas as páginas tem 5 itens: Pesquisas e análises, Nacional e bancadas, Estados, Urnas ES, Voto cruzado (mesmo HTML e CSS em todas; ao mudar, mude em todas). Não crie outras páginas sem pedido explícito.
4. **Dependências externas só via CDN confiável** (cdnjs para D3; Google Fonts para a fonte Inter).
5. **Verifique localmente antes do push**: `python -m http.server 8765 --directory docs` e confira, **nos dois modos** (Governador e Senado), que o mapa mostra 27 estados, que o pop-up abre e que o filtro funciona.
6. **Commits** em português, descrevendo o que mudou. Atualize o [CHANGELOG.md](CHANGELOG.md) a cada mudança visível.
7. **Push em `main` publica o site.** Só faça push quando o usuário pedir ou concordar.

## Convenções de dados (resumo)

Valem para `ESTADOS` (governador) e `SENADO`. Diferenças do Senado estão em [documentacao/dados.md](documentacao/dados.md#senado-senadojs).

- Cada estado tem `uf`, `nome`, `regiao`, `pesquisas[]` (a mais recente primeiro) e `candidatos[]`.
- A **pesquisa principal** define a cor do estado no mapa e o percentual mostrado na tabela: no governador, a AtlasIntel quando o estado tiver uma; senão (e sempre no Senado), `pesquisas[0]`.
- `tipo: "V"` = votos válidos; `tipo: "T"` = votos totais (estimulada); no Senado também `tipo: "C"` = % de eleitores que citam o nome em um dos 2 votos. Sempre indique qual.
- Margem que colore o mapa: governador = 1º − 2º; Senado = 2º − 3º (disputa pela 2ª vaga).
- Nomes em `pesquisas[].res` devem ser **idênticos** aos de `candidatos[].nome`, senão a tabela mostra "—".
- Partido desconhecido: use `"—"` em vez de chutar.

## Cuidados editoriais

- Os resumos dos candidatos são texto editorial. Devem ser **neutros, factuais e curtos** (1 a 2 frases), sem adjetivos de valor.
- Prefeitos que concorrem a governador ou senador renunciam 6 meses antes da eleição: chame-os de **ex-prefeitos**.
- Vices que assumiram o governo em 2026 (porque o titular saiu para concorrer a outro cargo) são governadores no cargo; descreva assim.
- Na dúvida sobre um fato, prefira omitir ou usar uma descrição genérica. O rodapé da página avisa que os resumos podem conter imprecisões; mantenha esse aviso.
