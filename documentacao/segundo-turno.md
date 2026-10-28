# 2º turno (`index.html`, `2turno-es.html`) e domínio eleicoes2026.gfvdata.com

Páginas do 2º turno de 25/10/2026, criadas a pedido do usuário "começando do zero": só o que foi escolhido para espelhar do 1º turno. As páginas do 1º turno continuam como estão e ganharam o item **2º turno** no switch de seções.

## Endereços

- **Principal:** https://eleicoes2026.gfvdata.com/ (Cloudflare, Worker de estáticos `eleicoes2026`, config em [worker/wrangler.jsonc](../worker/wrangler.jsonc)).
- **Reserva:** https://gfvdata-web.github.io/eleicoes-2026/ (GitHub Pages, mesma pasta `docs/`). Desligar só com OK do usuário.
- Os dois são publicados pelo mesmo workflow ([.github/workflows/pages.yml](../.github/workflows/pages.yml)) a cada push em `main`: job `deploy` (Pages) e job `cloudflare` (`npx --yes wrangler@4.150.0 deploy`; o `cloudflare/wrangler-action` instala o wrangler 3, que não aceita Worker só de assets).
- O job `cloudflare` precisa dos secrets do repositório `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID`. Sem eles, só avisa e o Pages segue publicando.
  - Token: Cloudflare → My Profile → API Tokens → modelo "Edit Cloudflare Workers", conta gfvdata, zona gfvdata.com. O usuário cria e cadastra (`gh secret set CLOUDFLARE_API_TOKEN`); nunca digitar token por ele.
  - O primeiro deploy cria o domínio personalizado e o DNS (`custom_domain: true`).
- `docs/_headers` (só a Cloudflare lê): `Cache-Control: no-cache` nos JSONs da apuração.

## Estrutura das páginas

Switch próprio do 2º turno (igual nas três): **Brasil** (`index.html`, raiz do site; antes `2turno.html` e "Nacional e bancadas") | **Estados** (`2turno-es.html`) | **Urnas até 19h** (`2turno-urnas.html`, desde 28/10; ver [urnas-19h.md](urnas-19h.md)) | **← 1º turno** (abre `apuracao.html`, "Nacional e bancadas").

### `index.html` (Brasil)
- **Card do topo "Apuração do 2º turno":** % apurado por cargo. Presidente = `BR` do TSE; Governador = média do % nos 6 estados com 2º turno, com quantos já têm apuração e quantos terminaram.
  - Switch **Cargos | No tempo** no canto superior direito (escolha guardada no navegador, chave `apuVista2t`). "No tempo" troca os dois subcards por um gráfico do % apurado das 17h até a última atualização, com a `serie` dos JSONs (ver Dados). Se o JSON não tiver `serie`, usa os pontos vistos desde que a página foi aberta.
- **Subabas** Presidente (`#presidente`, padrão), Governador (`#governador`) e Previsão simples (`#previsao`, sem mapa).
- **Previsão simples:** por município, `previsão = votos do 2º turno + (1 − % apurado do município) × votos do 1º turno`, só com os dois finalistas (casados pela sigla em `cand[]`; `v[]` segue a ordem de `cand[]`). Soma por estado e, no presidente, pelo Brasil. Com 0% apurado repete o 1º turno entre os dois (Flávio 51,0 × Lula 49,0); com 100% é o resultado oficial. Não considera para onde vão os votos dos eliminados, mudança de comparecimento nem o exterior (ZZ). Lê `data/es/apuracao/<UF>/<cargo>.json` (1º turno, uma vez) e `data/es/apuracao2t/<UF>/<cargo>.json` (a cada minuto, só com a aba aberta); ES fica na raiz das pastas. Mostra o título "Como funciona: URNAS APURADAS + URNAS DO 1º TURNO", o placar do Brasil, as 6 disputas de governador e o mapa do Brasil da aba Presidente (mesmo `#mapa`): cor de quem lidera a previsão em cada UF, com `fill-opacity` de 0,4 (0% apurado) a 1 (100%); rótulos com % apurado e previsão Flávio / Lula; tooltip com 1º turno entre os dois × previsão.
- **Presidente:** placar nacional Flávio × Lula (barra com linha de 50%), mapa dos 27 estados na cor do partido de quem lidera (cinza sem apuração), rótulo com % de urnas e % de Flávio / Lula, pop-up com o % do 1º turno e o atual.
- **Governador:** o mapa mostra as duas situações:
  - **2º turno hoje** (AC, AM, DF, ES, RN, TO): contorno grosso; âmbar (`--disputa`) até a apuração começar, depois a cor do partido de quem lidera; % de urnas no rótulo.
  - **Definido no 1º turno** (os outros 21): listrado e claro, na cor do partido do eleito, sem número; pop-up com o eleito e o % de 4/10.
  - Lista lateral das 6 disputas (clique destaca no mapa) e tabela dos 21 definidos.
- Candidatos casados com a apuração pela sigla do partido (os finalistas são sempre de partidos diferentes) e, se falhar, pelo nome sem acentos.

### `2turno-es.html` (Estados)
- Cópia transformada de `es.html` (mesmo layout por município e região, `?uf=XX`), só com Presidente e Governador, lendo `data/es/apuracao2t/`.
- Card do topo com os dois cargos no estado escolhido. Nos 21 estados sem 2º turno de governador, a aba Governador fica desativada e um aviso mostra o eleito no 1º turno.
- Mudanças feitas em `es.html` depois de 25/10 não passam para cá automaticamente.

## Dados

| Arquivo | O que é | Gerado por |
|---|---|---|
| `docs/data/2turno/disputas.js` (`window.SEGUNDO_TURNO`) | finalistas de presidente (com % do 1º turno por UF) e, por UF, governador `definido` (eleito) ou `2turno` (os dois candidatos) | resultado final do 1º turno (`docs/data/apuracao/*.json`), gerado uma vez em 25/10 |
| `docs/data/apuracao2t/presidente.json`, `governador.json` | apuração por UF (mesmo formato de [apuracao.md](apuracao.md)); `"ufs": {}` = 0%. Só no 2º turno: `serie: [["HH:MM", %], ...]` com o histórico do % apurado (presidente = BR; governador = média das 6 UFs; em presidente cada ponto tem um 3º elemento `[[nome, % válidos], ...]` do BR, usado pelo card "Como a apuração andou"), um ponto por mudança, preservado entre reinícios do coletor (função `serie()`); `--limpar` zera | `python scripts/apuracao.py --turno 2` |
| `docs/data/es/apuracao2t/<cargo>.json` e `<UF>/<cargo>.json` | apuração por município (mesmo formato de [es.md](es.md)) | `python scripts/apuracao_es.py --turno 2` |

UFs com 2º turno de governador: as que têm arquivo na eleição 6260 do TSE (lista `UFS_GOV_2T` em `scripts/apuracao.py`, conferida em 25/10).

## Coleta no dia (`--turno 2`)

Eleições do TSE no 2º turno: **6258** (federal: presidente) e **6260** (estadual: governador). A lista de municípios vem do config da 6258 (a 6260 só traz os 6 estados com 2º turno).

Dois terminais, dois processos contínuos (coleta a cada 60 s; **não** usar `ciclo.py` nem `--uma-vez`, que reiniciam o processo, perdem os ETags e releem `apuracao-bruto/` a cada rodada):

```
python scripts/apuracao.py --turno 2 --publicar
python scripts/apuracao_es.py --turno 2 --publicar
```

- **Filtro por município** (`apuracao_es.py`): cada ciclo baixa os 33 arquivos de estado (27 de presidente + 6 de governador) e os 33 de **abrangência** do TSE (`{uf}-e{eleição}-ab.json`, um por estado e eleição, com o % apurado de cada município, sem votos; o de SP tem ~490 KB). Só pede o `-u.json` do município cujo % na abrangência difere do último guardado; se o arquivo do município ainda vier atrasado (cache do TSE de 58 s), é pedido de novo no ciclo seguinte. Município com 100% não é mais consultado.
  - Se o TSE servir uma cópia mais velha (% menor que o guardado), o dado mais novo é mantido e aparece o aviso "% apurado diminuiu …; mantido o anterior".
  - Sem a abrangência de um estado (erro ou 429), aquele estado volta ao **portão por estado**: municípios só se o arquivo do estado mudou, ou a cada 10 min (`REVARRER`) enquanto não chegou a 100%.
- **Recuo** (nos dois scripts): se o TSE responder 429/503, o próximo ciclo espera o dobro (até 300 s, `INTERVALO_MAX`); um ciclo sem limite volta para 60 s. `PARALELO` = 8 nos dois (no 1º turno, 24 levou a bloqueio).
- Log por ciclo: `N pedidos (X municípios) · novos · iguais · limitados · segundos`.
- O TSE manda os arquivos com `Cache-Control: max-age=58`: coletar mais rápido que ~60 s devolve o mesmo arquivo.
- Cada processo publica no máximo a cada 120 s e cada push dispara o workflow (~1–2 min): o site anda a cada ~2–4 min.
- Ensaio em 25/10 às 16h (TSE com 0%): 1º ciclo com 6.073 arquivos, os seguintes com 33, nenhum 429. Durante a apuração o portão por estado abria tudo (todos os estados mudam a cada minuto) e o ciclo levava minutos.
- Ensaio do filtro por município em 25/10 às 19h15 (~7% apurado): 450 a 700 pedidos por ciclo, 4 a 7 s, nenhum 429.

- `--simular --turno 2` simula só os dois finalistas; nunca publica. Depois de simular, rode `--limpar --turno 2` (nacional) e uma coleta real `--uma-vez` (por município) antes de commitar.
- Cada processo commita só a própria pasta (`docs/data/apuracao2t/` ou `docs/data/es/apuracao2t/...`).
- Correção feita junto: o TSE marca `e="s"` também em quem vai ao 2º turno (`st = "2º turno"`); `converter` agora grava `situacao: "2turno"` nesses casos (antes saía "eleito"). Os JSONs do 1º turno foram regravados com o resultado final.

## Pendências

### Feito em 25/10 no computador oficial
- Job `cloudflare` aplicado em `.github/workflows/pages.yml`; secrets `CLOUDFLARE_ACCOUNT_ID` e `CLOUDFLARE_API_TOKEN` cadastrados; o job publica a cada push em `main`.
- Primeiro deploy feito à mão (`npx --yes wrangler@4.150.0 deploy --config worker/wrangler.jsonc`, login OAuth local): Worker, domínio e DNS criados.
- **Limite de 25 MiB por arquivo do Worker:** `docs/data/voto-cruzado/sp.json` (30 MiB) fica de fora pelo `docs/.assetsignore` e o `docs/_redirects` manda esse caminho para a cópia do GitHub Pages (CORS liberado). Se outro arquivo passar de 25 MiB, o deploy falha com "Asset too large": repita o par `.assetsignore` + `_redirects`. Por isso o GitHub Pages não pode sair do ar enquanto o redirecionamento existir.
- Desde 25/10/2026 o 2º turno é a **raiz** do site e o 1º turno fica em `/primeiro-turno` (`primeiro-turno.html`; a Cloudflare responde `.html` com 307 para o endereço sem extensão). O endereço antigo `/2turno.html` redireciona para `/`: na Cloudflare por `docs/_redirects` (301) e no GitHub Pages pelo próprio `docs/2turno.html`, que só tem o redirecionamento (preserva `?` e `#`).

### Ainda pendente

- painel-status (`src/config.py`) ainda monitora o endereço do GitHub Pages; trocar para o domínio só se o Pages sair do ar. (`Cloudfare/CLAUDE.md` e o mapa do `~/.claude/CLAUDE.md` já foram atualizados em 25/10.)
- Depois da apuração: decidir se o GitHub Pages sai do ar (com OK do usuário).
