# Eleições 2026 — Governadores e Senado

Mapa interativo com as últimas pesquisas de intenção de voto para **governador** e **Senado** nas eleições de 2026 (1º turno em 04/10/2026), estado por estado.

- **Site:** https://gfvdata-web.github.io/eleicoes-2026/
- **Repositório:** https://github.com/gfvdata-web/eleicoes-2026 (público)

## O que a página mostra

Uma única página, com um seletor de cargo no topo (**Governador** | **Senado**) e duas seções:

1. **Mapa do Brasil:** cada estado é colorido pela margem da disputa na pesquisa mais recente (governador: 1º × 2º; Senado: 2º × 3º, porque há 2 vagas). Ao passar o mouse (ou tocar), um pop-up mostra as 3 pesquisas mais recentes daquele estado. Clicar num estado filtra a tabela.
2. **Tabela:** UF, candidato, partido, percentual na última pesquisa e um resumo curto de cada candidato, com filtro por estado e por região.

## Estrutura

```
.
├── README.md              ← este arquivo (visão geral)
├── CLAUDE.md              ← instruções para quem (humano ou IA) for alterar o projeto
├── CHANGELOG.md           ← histórico de mudanças
├── documentacao/
│   ├── dados.md           ← formato dos dados, fontes e como atualizar
│   ├── pagina.md          ← como a página funciona (mapa, pop-up, tabela, cores)
│   └── roadmap.md         ← próximos passos (senadores, apuração, ajustes)
└── docs/                  ← pasta publicada pelo GitHub Pages
    ├── index.html         ← página única (HTML + CSS + JS inline), com seletor Governador/Senado
    └── data/
        ├── dados.js           ← pesquisas e candidatos a governador
        ├── senado.js          ← pesquisas e candidatos ao Senado
        └── brasil-estados.geojson ← malha simplificada dos 27 estados
```

> Importante: a pasta `docs/` é **o site** (é o que o GitHub Pages publica), não documentação. A documentação fica em `documentacao/`.

## Rodar localmente

A página usa `fetch` para carregar o GeoJSON, então precisa de um servidor (abrir o `index.html` direto do disco não funciona):

```bash
python -m http.server 8765 --directory docs
```

Depois acesse http://localhost:8765.

## Publicação

O GitHub Pages está configurado para servir `main` → `/docs`. Basta dar push em `main`: o site atualiza sozinho em cerca de 1 minuto.

## Créditos

- Pesquisas (governador e Senado): Quaest, Datafolha, AtlasIntel, Paraná Pesquisas, Real Time Big Data e outros institutos, compilados de O Povo, Gazeta do Povo e Wikipédia (detalhes em [documentacao/dados.md](documentacao/dados.md)).
- Malha dos estados: [codeforamerica/click_that_hood](https://github.com/codeforamerica/click_that_hood), simplificada.
- Mapa renderizado com [D3.js](https://d3js.org/) v7 (via cdnjs).
