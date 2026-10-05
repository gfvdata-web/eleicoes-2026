# Espírito Santo: votos por urna (`es-secoes.html` + `scripts/secoes_es.py`)

Página criada a pedido do usuário em 05/10/2026. Mostra o 1º turno no ES com o maior detalhe que o TSE publica: estado → município → zona eleitoral → local de votação → seção (urna), nos 5 cargos. **Não tem link no menu** (endereço próprio: `es-secoes.html`); só um link de volta para `es.html`. Só ES; não baixar dados de outros estados para ela.

## Nomenclatura do TSE

- **Zona eleitoral**: área de um cartório eleitoral. Pode atender vários municípios, e um município grande tem várias (Vitória: 1 e 52).
- **Local de votação**: o prédio (escola etc.), com número próprio dentro da zona.
- **Seção**: a urna. Seções **agregadas** votam na mesma urna da principal; os votos vêm somados na principal.

## Fontes (dados abertos do TSE, publicados em 05/10)

`https://cdn.tse.jus.br/estatistica/sead/odsele/`
- `votacao_secao/votacao_secao_2026_ES.zip`: votos por seção e candidato (governador, senador, deputados).
- `votacao_secao/votacao_secao_2026_BR.zip`: presidente (o script guarda só as linhas do ES e apaga o zip).
- `detalhe_votacao_secao/detalhe_votacao_secao_2026.zip`: aptos, comparecimento, brancos, nulos, hora do boletim e modelo da urna (`_ES` e as linhas do ES de `_BR`).
- `eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip`: local de cada seção, com endereço, bairro, latitude e longitude (`_ES`).

Os arquivos ficam em `apuracao-bruto/es-secoes/` (ignorado pelo git). Nome de urna, partido, situação e **destino do voto** (`dvt`: "Anulado sub judice" não é válido) vêm de `docs/data/es/apuracao/<cargo>.json` e da cópia bruta `apuracao-bruto/es/<cargo>/ES.json` (de `scripts/apuracao_es.py`), que também traz partidos sem candidato (ex.: legenda do Cidadania).

Conferência (05/10): votos válidos e de legenda do estado batem com a divulgação oficial nos 5 cargos. Votos em números que não estão na lista do TSE (poucas centenas) são ignorados (o TSE os conta como nulos/anulados).

## Script

```bash
python scripts/secoes_es.py            # usa os arquivos já baixados
python scripts/secoes_es.py --baixar   # baixa de novo do TSE
```

Locais com coordenada fora do município (22 em 05/10) vão para perto dos outros locais da mesma zona e ficam marcados como "posição aproximada"; locais com a mesma coordenada são afastados um pouco.

## Formato de `docs/data/es/secoes/`

- `cargos.json`: `{cargo: {vagas, cand: [[número, nome de urna, partido, situação, eleito 0/1, válido 0/1]], partidos: [[número, sigla]]}}`.
- `estado.json`: `{es: totais, mun: {tse: {apt, comp, n, zonas, locais, v}}}`.
- `m/<tse>.json`: `{tse, nome, zonas, locais: [[zona, nº local, nome, bairro, endereço, lon, lat, flags]], secoes: [[zona, nº, índice do local, aptos, comparecimento, hora do BU, modelo da urna, flags, [agregadas], v]]}`.
  - flags do local: 1 = posição aproximada, 2 = não convencional (unidade prisional). Flags da seção: 1 = instalada, 2 = anulada.
- `v` = `{cargo: [brancos, nulos, [índice do candidato, votos, ...], [índice do partido, votos de legenda, ...]]}`, do mais para o menos votado.

## Página

- Abas de cargo; trilha clicável (Espírito Santo › município › zona › local › seção); endereço com o nível (`#c=senador&m=57053&z=1&l=12&s=1-34`, `l` = índice do local no arquivo do município, `s` = zona-seção).
- Mapa dos municípios (clique abre o município) e mapa do município: um ponto por local (tamanho = eleitores), áreas de Voronoi recortadas pelo limite do município (aproximação: o TSE não publica limites de zona) e linhas grossas onde as áreas vizinhas são de zonas diferentes. Zoom com roda do mouse, dois dedos ou botões; ao escolher um local, o mapa aproxima nele.
- Cor: mais votado (mais forte quanto maior o % dele: 25% → 75% dos válidos; no Senado vale o dobro do %), zona eleitoral ou candidato em foco (clique no nome no ranking).
- Card do nível: eleitores, comparecimento, abstenção, válidos, brancos, nulos (com os sub judice); ranking de candidatos (deputados: 30 primeiros, busca e "mostrar todos") e, em deputados, partidos com nominais + legenda. Na seção: hora do boletim, modelo da urna e agregadas.
- Tabela de detalhamento: filhos do nível (municípios; zonas / locais / seções), com mais votado, %, vantagem sobre o 2º e % do candidato em foco; ordenável; clique na linha desce de nível.
