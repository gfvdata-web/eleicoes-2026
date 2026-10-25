# App Android "Apuração 2026"

App nativo (Kotlin + Jetpack Compose, molde do `painel-status/android`) em `android/`, para acompanhar o 2º turno no celular.

## O que faz
- Lê os JSON do TSE **direto** (não usa `docs/data/`), a cada 60 s **enquanto o app está na tela**. Fechado ou em segundo plano, não atualiza.
  - Presidente: `https://resultados.tse.jus.br/oficial/ele2026/6258/dados/{uf}/{uf}-c0001-e006258-u.json` (`br`, 27 UFs, `zz` = exterior).
  - Governador: `.../6260/dados/{uf}/{uf}-c0003-e006260-u.json` (AC, AM, DF, ES, RN, TO).
- Usa ETag (`If-None-Match`) e no máximo 8 downloads ao mesmo tempo, como os scripts. Em 429/503, a espera dobra até 300 s.
- A leitura do JSON (`data/Conversor.kt`) segue `converter()` de `scripts/apuracao.py`. Quem foi ao 2º turno não conta como eleito.

## Como instalar
1. Push em `main` que mexa em `android/**` (ou "Run workflow" em Actions → **Android — app**).
2. Na run, em **Artifacts**, baixe `eleicoes2026-debug-buildN.apk` (já é o `.apk`, sem zip).
3. No celular, abra o arquivo e permita "instalar apps desconhecidos". Para atualizar, instale o APK novo por cima.

Não há assinatura de release, KV/D1 nem aviso de versão: é só APK de debug.

## Testes
`./gradlew testDebugUnitTest` (no Actions). As fixtures reais do TSE ficam em `android/app/src/test/resources/tse/`.
