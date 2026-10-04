# Espírito Santo (`es.html` + `scripts/apuracao_es.py`)

Página dedicada ao Espírito Santo, criada a pedido do usuário em 04/10/2026. **Só usa a apuração oficial do TSE** (sem pesquisas), com detalhe por município e região. Convive com `index.html` e `apuracao.html`; o link fica na barra de cargos da `apuracao.html`.

## Arquitetura

```
TSE (um arquivo por cargo × estado e por cargo × município)
  →  scripts/apuracao_es.py (neste computador, a cada 60 s; 5 cargos × 79 arquivos)
  →  docs/data/es/apuracao/<cargo>.json  →  git push (no máximo a cada 120 s)
  →  es.html relê o cargo aberto a cada 60 s
```

Pode rodar ao mesmo tempo que `scripts/apuracao.py`: cada script só commita a própria pasta.

## Endereços do TSE (divulgação 2026, conferidos em 04/10)

- Lista de eleições: `https://resultados.tse.jus.br/oficial/comum/config/ele-c.json`
- Eleição **6257** = federal (presidente, cargo 1). Eleição **6259** = estadual (governador 3, senador 5, dep. federal 6, dep. estadual 7, distrital 8).
- Estado: `…/oficial/ele2026/{ele}/dados/es/es-c{cargo:04}-e{ele:06}-u.json`
- Município: `…/oficial/ele2026/{ele}/dados/es/es{cód. TSE}-c{cargo:04}-e{ele:06}-u.json`
- Municípios (código TSE ↔ IBGE): `…/oficial/ele2026/6259/config/mun-e006259-cm.json`

Os mesmos endereços (trocando `es` pela UF) servem para o `scripts/apuracao.py`.

Campos usados do arquivo `-u.json`: `s.pst` (% de seções totalizadas), `e.te` / `e.c` / `e.a` (eleitorado, comparecimento, abstenção), `v.vv` / `v.vb` / `v.tvn` / `v.vl` (válidos, brancos, nulos, legenda), `carg[0].nv` (vagas), `carg[0].qe` (quociente do TSE), `carg[0].agr[]` (coligação, federação ou partido isolado; nos proporcionais, cada `agr` é uma lista), `par[].tvtl` (votos de legenda do partido, a conferir quando chegarem votos: o script avisa se a soma não bater com `v.vl`), `cand[].nmu` / `n` / `vap` / `st` / `e`.

## Formato de `docs/data/es/apuracao/<cargo>.json`

```json
{
  "cargo": "deputado-federal", "atualizado": "19:42", "vagas": 10, "qe": 0,
  "listas": [["PSB", "i", 0], ["Federação PT/PC do B/PV", "f", 0]],
  "cand": [["4010", "FREITAS", "PSB", 0, "", 0]],
  "partidos": [["PSB", 0]],
  "es":  { "pct": 45.31, "hora": "19:41:30", "el": 0, "comp": 0, "abst": 0, "vv": 0, "vb": 0, "vn": 0, "vl": 0, "v": [0], "leg": [0] },
  "mun": { "57053": { "...": "mesmos campos de es" } }
}
```

- `listas`: `[nome, tipo, vagas do TSE]`; tipo `i` = partido isolado, `f` = federação, `c` = coligação (majoritários).
- `cand`: `[número, nome de urna, partido, índice em listas, situação do TSE, eleito 0/1]`, do mais para o menos votado no estado.
- `partidos`: `[sigla, índice em listas]`, na ordem de `leg`.
- `es` e cada `mun[código TSE]`: totais do local; `v` = votos de cada candidato na ordem de `cand`; `leg` = votos de legenda na ordem de `partidos`.
- `simulacao: true` só em dados de `--simular`.

Arquivos estáticos (gerados uma vez, não mudam durante a apuração):
- `docs/data/es/municipios.js` (`window.ES_MUNICIPIOS`): código TSE, código IBGE, nome, microrregião e macrorregião de planejamento (Lei estadual 9.768/2011; Jerônimo Monteiro no Caparaó pela Lei 11.174/2020).
- `docs/data/es/municipios.geojson`: malha do IBGE (qualidade intermediária), propriedade `ibge`. As ilhas de Trindade e Martim Vaz (parte de Vitória) foram retiradas para o mapa caber.

## Script `scripts/apuracao_es.py`

| Comando | O que faz |
|---|---|
| `python scripts/apuracao_es.py --simular` | Dados falsos com os candidatos reais do TSE, só local. **Nunca publica.** |
| `python scripts/apuracao_es.py` | Coleta real, grava os arquivos, não publica. |
| `python scripts/apuracao_es.py --publicar` | Coleta real e publica (commit + push só de `docs/data/es/apuracao/`). |
| `--uma-vez`, `--intervalo N`, `--cargos a,b`, `--limpar` | Como em `apuracao.py`. |

- Requisições condicionais (ETag): a cada minuto só baixa o que mudou.
- A cópia do TSE fica em `apuracao-bruto/es/<cargo>/<município>.json` (ignorada pelo git). Ao reiniciar, parte dela.
- Depois de usar `--simular`, rode uma coleta real (`--uma-vez`) antes de commitar, para os arquivos voltarem aos dados oficiais.

## Página

- **Abas de cargo** no topo (presidente, governador, Senado, dep. federal, dep. estadual); o endereço `es.html#deputado-federal` abre direto na aba.
- **Área**: estado inteiro, macrorregião, microrregião ou município (também clicando no mapa ou numa linha da tabela "Por região"). Estado inteiro usa o total do TSE; as demais áreas somam os municípios.
- **Números da área**: % de urnas apuradas (média ponderada pelo eleitorado), eleitores, comparecimento, válidos, brancos e nulos. Nos majoritários, uma frase com a situação no estado ("haverá 2º turno entre…"; no fim, a situação oficial do TSE).
- **Mapa** colorido pelo mais votado (cor do partido), por um candidato (clique no nome dele: % dos válidos em cada município) ou pelo % apurado.
- **Quem está passando** (só deputados): projeção das vagas com os votos já apurados no estado inteiro, pelas regras do Código Eleitoral (QE com fração até 0,5 desprezada; QP com mínimo de 10% do QE; sobras pela maior média entre listas com 80% do QE e candidatos com 20%; depois, maior média entre todas, conforme o STF nas ADIs 7228/7263/7325). Mostra eleitos, o 1º fora de cada lista e os votos por lista. A situação oficial do TSE (`st`) aparece ao lado quando divulgada.
- **Candidatos**: ranking da área, com busca e filtro de partido nos deputados (40 primeiros, botão para todos). ★ fixa o candidato: ele vai para o topo e ganha coluna na tabela "Por região". Fixados, cor do mapa e recorte ficam salvos só no navegador do leitor (`localStorage`).
- **Por região**: macrorregiões, microrregiões ou municípios da área, com eleitores, % apurado, mais votado, vantagem sobre o 2º e o % de cada fixado; colunas ordenáveis.
