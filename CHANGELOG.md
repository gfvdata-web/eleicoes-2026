# Changelog

Formato: data — descrição. Mudanças mais recentes no topo.

## 2026-10-04

- **Nova página de apuração (`apuracao.html`):** réplica da página principal com a faixa "Apuração oficial" no topo (média de urnas apuradas, estados concluídos, horário) e o % de urnas apuradas abaixo de cada sigla no mapa. Quando um estado tem urnas apuradas, cor, pop-up e tabela passam a usar o resultado do TSE; sem apuração, segue a pesquisa. Os dados vêm de `docs/data/apuracao/<cargo>.json` (um arquivo por cargo: presidente, governador, senador, deputado federal e estadual), relidos a cada minuto. A página atual (`index.html`) não muda.
- **Coleta da apuração:** novo script `scripts/apuracao.py`, que roda neste computador, confere o TSE a cada minuto, mostra no terminal o andamento de cada cargo e publica só os arquivos de apuração. Novo workflow `.github/workflows/pages.yml` para publicar o site pelo GitHub Actions (sem o limite de ~10 publicações por hora).
- **Pop-up do mapa:** cada candidato listado nas pesquisas (Governador e Senado) agora mostra o partido entre parênteses ao lado do nome.
- **Senado no modo Partido:** quando as duas vagas ficam com partidos diferentes, o estado agora aparece dividido ao meio (1º colocado à esquerda, 2º à direita) em vez de listrado.
- **Bancada Senado:** grupos iniciais esquerda / centro / direita (o leitor muda qualquer partido de grupo pelo menu; botão para restaurar). Lista de bancadas e grupos com % (sobre 81 cadeiras). Partido atual dos suplentes conferido na imprensa; Mauro Carvalho Júnior (suplente de Wellington Fagundes) passa a constar sem partido.
- **Governador: AtlasIntel como pesquisa principal.** Nos estados com pesquisa AtlasIntel (BA, CE, PA, PI, RN, SP), ela passa a definir a cor do mapa, o líder e os percentuais da tabela, e aparece primeiro no pop-up. Nos demais estados e no Senado, segue valendo a pesquisa mais recente.
- **Mapa colorido por partido:** novo seletor "Folga | Partido" ao lado da legenda, nos modos Governador e Senado. No modo Partido, o estado recebe a cor do partido do líder (Senado: listras quando as duas vagas ficam com partidos diferentes), e a legenda conta estados/vagas por partido. O botão "Grupos políticos" permite juntar partidos sob um nome e uma cor; os grupos ficam salvos só no navegador do leitor. O pop-up passa a mostrar o partido dos líderes.
- **Nova aba "Bancada Senado" (`senado.html`):** hemiciclo com as 81 cadeiras, somando os 27 senadores com mandato até 2031 aos 54 favoritos nas pesquisas de 2026. O leitor pode trocar os eleitos em cada estado e criar grupos de partidos (linhas de maioria em 41 e de 3/5 em 49). O switch "Substitutos" troca os senadores que disputam o governo pelo 1º suplente (começa com quem lidera a pesquisa para governador; ajustável por estado). Novo arquivo de dados `docs/data/senado-atual.js`.
- **Senado publicado:** seletor Governador/Senado no topo da página. No modo Senado, o mapa é colorido pela disputa da 2ª vaga (2º − 3º colocado), os dois primeiros aparecem em destaque e o rodapé lista as fontes do Senado. O endereço `…/eleicoes-2026/#senado` abre direto nesse modo.
- **Repositório renomeado** de `governadores-2026` para `eleicoes-2026`. Novo endereço do site: https://gfvdata-web.github.io/eleicoes-2026/

- **Documentação:** atualizada para governador e Senado no mesmo repositório e na mesma página (seletor de cargo, `senado.js`, regras para sessões paralelas).
- **Senado (em andamento):** adicionado `docs/data/senado.js` com pesquisas para o Senado nos 27 estados.
- **Documentação:** README revisado; adicionados `CLAUDE.md`, `CHANGELOG.md` e a pasta `documentacao/` (dados, página, roadmap).
- **v1 publicada:** mapa interativo das pesquisas para governador (27 UFs, 3 pesquisas por estado), pop-up por estado e tabela de candidatos com partido, resumo e filtros. Publicada no GitHub Pages (`main` → `/docs`).
