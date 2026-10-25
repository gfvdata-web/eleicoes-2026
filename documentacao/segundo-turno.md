# 2º turno (`2turno.html`, `2turno-es.html`) e domínio eleicoes2026.gfvdata.com

Páginas do 2º turno de 25/10/2026, criadas a pedido do usuário "começando do zero": só o que foi escolhido para espelhar do 1º turno. As páginas do 1º turno continuam como estão e ganharam o item **2º turno** no switch de seções.

## Endereços

- **Principal:** https://eleicoes2026.gfvdata.com/ (Cloudflare, Worker de estáticos `eleicoes2026`, config em [worker/wrangler.jsonc](../worker/wrangler.jsonc)).
- **Reserva:** https://gfvdata-web.github.io/eleicoes-2026/ (GitHub Pages, mesma pasta `docs/`). Desligar só com OK do usuário.
- Os dois são publicados pelo mesmo workflow ([.github/workflows/pages.yml](../.github/workflows/pages.yml)) a cada push em `main`: job `deploy` (Pages) e job `cloudflare` (`wrangler deploy` via `cloudflare/wrangler-action`).
- O job `cloudflare` precisa dos secrets do repositório `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID`. Sem eles, só avisa e o Pages segue publicando.
  - Token: Cloudflare → My Profile → API Tokens → modelo "Edit Cloudflare Workers", conta gfvdata, zona gfvdata.com. O usuário cria e cadastra (`gh secret set CLOUDFLARE_API_TOKEN`); nunca digitar token por ele.
  - O primeiro deploy cria o domínio personalizado e o DNS (`custom_domain: true`).
- `docs/_headers` (só a Cloudflare lê): `Cache-Control: no-cache` nos JSONs da apuração.

## Estrutura das páginas

Switch próprio do 2º turno (igual nas duas): **Nacional e bancadas** (`2turno.html`) | **Estados** (`2turno-es.html`) | **← 1º turno**.

### `2turno.html` (Nacional e bancadas)
- **Card do topo "Apuração do 2º turno":** % apurado por cargo. Presidente = `BR` do TSE; Governador = média do % nos 6 estados com 2º turno, com quantos já têm apuração e quantos terminaram.
- **Subabas** Presidente (`#presidente`, padrão) e Governador (`#governador`).
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
| `docs/data/apuracao2t/presidente.json`, `governador.json` | apuração por UF (mesmo formato de [apuracao.md](apuracao.md)); `"ufs": {}` = 0% | `python scripts/apuracao.py --turno 2` |
| `docs/data/es/apuracao2t/<cargo>.json` e `<UF>/<cargo>.json` | apuração por município (mesmo formato de [es.md](es.md)) | `python scripts/apuracao_es.py --turno 2` |

UFs com 2º turno de governador: as que têm arquivo na eleição 6260 do TSE (lista `UFS_GOV_2T` em `scripts/apuracao.py`, conferida em 25/10).

## Coleta no dia (`--turno 2`)

Eleições do TSE no 2º turno: **6258** (federal: presidente) e **6260** (estadual: governador). A lista de municípios vem do config da 6258 (a 6260 só traz os 6 estados com 2º turno).

```
python scripts/apuracao.py --turno 2 --publicar
python scripts/apuracao_es.py --turno 2 --publicar --ufs ES
python scripts/apuracao_es.py --turno 2 --publicar --exceto ES
```

- `--simular --turno 2` simula só os dois finalistas; nunca publica. Depois de simular, rode `--limpar --turno 2` (nacional) e uma coleta real `--uma-vez` (por município) antes de commitar.
- Cada processo commita só a própria pasta (`docs/data/apuracao2t/` ou `docs/data/es/apuracao2t/...`).
- Correção feita junto: o TSE marca `e="s"` também em quem vai ao 2º turno (`st = "2º turno"`); `converter` agora grava `situacao: "2turno"` nesses casos (antes saía "eleito"). Os JSONs do 1º turno foram regravados com o resultado final.

## Pendências

### Feito em 25/10 no computador oficial
- Job `cloudflare` aplicado em `.github/workflows/pages.yml`; secret `CLOUDFLARE_ACCOUNT_ID` cadastrado.
- Primeiro deploy feito à mão (`npx --yes wrangler@4.150.0 deploy --config worker/wrangler.jsonc`, login OAuth local): Worker, domínio e DNS criados.
- **Limite de 25 MiB por arquivo do Worker:** `docs/data/voto-cruzado/sp.json` (30 MiB) fica de fora pelo `docs/.assetsignore` e o `docs/_redirects` manda esse caminho para a cópia do GitHub Pages (CORS liberado). Se outro arquivo passar de 25 MiB, o deploy falha com "Asset too large": repita o par `.assetsignore` + `_redirects`. Por isso o GitHub Pages não pode sair do ar enquanto o redirecionamento existir.
- A Cloudflare responde `/2turno.html` com 307 para `/2turno` (padrão do Worker de estáticos); links e `?uf=` continuam funcionando.

### 1. Secret `CLOUDFLARE_API_TOKEN` (falta)
Sem ele o job `cloudflare` só avisa e o domínio fica parado no último deploy manual. O usuário cria o token (Cloudflare → My Profile → API Tokens → "Edit Cloudflare Workers") e cadastra: `gh secret set CLOUDFLARE_API_TOKEN --repo gfvdata-web/eleicoes-2026`. Enquanto isso, publicar à mão com o comando acima.

### 2. Demais

- Atualizar `Cloudfare/CLAUDE.md` (inventário: Worker `eleicoes2026`, domínio eleicoes2026.gfvdata.com, sem D1/KV/Cron).
- Atualizar o mapa do `~/.claude/CLAUDE.md` (eleicoes-2026 passa a ter domínio próprio) e, se fizer sentido, o painel-status (`src/config.py`).
- Depois da apuração: decidir se o GitHub Pages sai do ar (com OK do usuário).
