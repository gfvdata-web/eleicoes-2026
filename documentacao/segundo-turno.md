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

## Pendências para o computador oficial

### 1. Job da Cloudflare no workflow (não foi enviado em 25/10)

O push de 25/10 foi recusado para `.github/workflows/pages.yml` porque a credencial do outro computador não tinha a permissão `workflow`. Aplique a mudança abaixo no computador oficial (salve o bloco em `cf.patch` e rode `git apply cf.patch`, ou cole o job à mão), cadastre os secrets e faça push. Se o push recusar de novo: `gh auth refresh -h github.com -s workflow`.

```bash
gh secret set CLOUDFLARE_API_TOKEN --repo gfvdata-web/eleicoes-2026
gh secret set CLOUDFLARE_ACCOUNT_ID --repo gfvdata-web/eleicoes-2026
```

```diff
diff --git a/.github/workflows/pages.yml b/.github/workflows/pages.yml
index 484fae1..e087fb9 100644
--- a/.github/workflows/pages.yml
+++ b/.github/workflows/pages.yml
@@ -1,4 +1,8 @@
-# Publica a pasta docs/ no GitHub Pages a cada push em main.
+# Publica a pasta docs/ a cada push em main, em dois lugares:
+#  - Cloudflare (eleicoes2026.gfvdata.com), Worker de estáticos em worker/wrangler.jsonc — endereço principal;
+#  - GitHub Pages (gfvdata-web.github.io/eleicoes-2026) — reserva.
+# A Cloudflare precisa dos secrets CLOUDFLARE_API_TOKEN e CLOUDFLARE_ACCOUNT_ID no repositório;
+# sem eles o job só avisa e o Pages segue publicando.
 # Requer Settings → Pages → Source: "GitHub Actions". Sem o limite de ~10 publicações/hora
 # do modo "Deploy from a branch", o que permite atualizar a apuração a cada 1–2 minutos.
 name: Publicar site
@@ -32,3 +36,28 @@ jobs:
           path: docs
       - id: deployment
         uses: actions/deploy-pages@v4
+
+  cloudflare:
+    runs-on: ubuntu-latest
+    env:
+      CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
+      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
+    steps:
+      - name: Conferir secrets
+        id: conf
+        run: |
+          if [ -z "$CLOUDFLARE_API_TOKEN" ] || [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
+            echo "::warning::Secrets CLOUDFLARE_API_TOKEN/CLOUDFLARE_ACCOUNT_ID ausentes: Cloudflare não publicada."
+            echo "ok=false" >> "$GITHUB_OUTPUT"
+          else
+            echo "ok=true" >> "$GITHUB_OUTPUT"
+          fi
+      - uses: actions/checkout@v4
+        if: steps.conf.outputs.ok == 'true'
+      - uses: cloudflare/wrangler-action@v3
+        if: steps.conf.outputs.ok == 'true'
+        with:
+          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
+          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
+          workingDirectory: worker
+          command: deploy
```

Depois do push: conferir no Actions que o job `cloudflare` passou e abrir https://eleicoes2026.gfvdata.com/2turno.html.

### 2. Demais

- Atualizar `Cloudfare/CLAUDE.md` (inventário: Worker `eleicoes2026`, domínio eleicoes2026.gfvdata.com, sem D1/KV/Cron).
- Atualizar o mapa do `~/.claude/CLAUDE.md` (eleicoes-2026 passa a ter domínio próprio) e, se fizer sentido, o painel-status (`src/config.py`).
- Depois da apuração: decidir se o GitHub Pages sai do ar (com OK do usuário).
