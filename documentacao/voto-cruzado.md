# Voto cruzado (`voto-cruzado.html` + `scripts/voto_cruzado_es.py`)

Página criada a pedido do usuário em 06/10/2026. **Não tem link no menu** (endereço próprio: `voto-cruzado.html`). Protótipo só com o Espírito Santo; o Brasil fica para depois.

## Objetivo

Medir se o voto para presidente acompanha os outros cargos do 1º turno (governador, Senado, deputado federal e estadual) e achar onde ele se descola. Direção principal combinada com o usuário: **prever o voto para presidente a partir dos outros votos** (ex.: urna com muito voto de esquerda para deputado, Senado e governador, mas pouco para o Lula).

## Limite: o voto é secreto

Não há dado por eleitor. Testado em 06/10: o RDV (Registro Digital do Voto) de cada urna, publicado em
`https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/...` (pleito 3220; índice das seções em `config/es/es-p003220-cs.json`, arquivos de cada seção em `dados/es/<mun>/<zona>/<seção>/p003220-es-m<mun>-z<zona>-s<seção>-aux.json`), guarda **uma lista por cargo, em ordem de número**, sem ligação entre os cargos de um mesmo eleitor. Amostra de 145 urnas: todas assim; ~15 KB por urna (ES inteiro ≈ 150 MB, ~1h40 em sequência), sem limite 429. Algumas seções (agregadas) dão 404. Conclusão: o RDV não acrescenta nada à votação por seção e não foi baixado inteiro. A unidade da análise é a urna (~240 votantes).

## Campos (opção B, combinada com o usuário)

Esquerda / centro / direita pelo partido do candidato, como em `camara.html`, mais os partidos do ES que faltavam lá (UP, PSTU, PCB, PCO na esquerda; Agir no centro; PRTB e Democrata na direita). A lista fica em `PARTIDOS` no script. Opção A guardada para depois: campo pelo alinhamento com os presidenciáveis (apoios e coligações em cada estado).

## Dados

`python scripts/voto_cruzado_es.py` lê `docs/data/es/secoes/` (de `scripts/secoes_es.py`; não baixa nada) e grava `docs/data/voto-cruzado/es.json`:
- `grupos`, `partidos` ({sigla: grupo}), `cargos`, `locais` ([tse, zona, nome, bairro, lon, lat]);
- `secoes`: [local, zona, seção, aptos, comparecimento, Lula, Flávio, e para cada cargo: válidos, esquerda, centro, direita]. Só seções instaladas e não anuladas; válidos = nominais + legenda sem sub judice; no Senado os 2 votos somam.

## Página

- Controles: campo (esquerda / direita), comparação (previsto, governador, Senado, dep. federal, dep. estadual), unidade (urnas, locais de votação, municípios) e filtro de município (clique no mapa).
- Barras: cada cargo por campo no estado ou no município.
- Modelo: regressão linear ponderada pelo comparecimento, nas urnas do estado inteiro, do % do campo para presidente sobre o % do mesmo campo nos 4 outros cargos (calculada no navegador). Em 06/10: R² 0,74 (esquerda) e 0,82 (direita); o Senado tem o maior peso.
- Dispersão (presidente × comparação, linha de igualdade), mapa dos municípios pela diferença (±10 p.p.) e tabela das unidades com maior diferença, ordenável.
- Limites matemáticos para comparação com um cargo de 1 voto (não Senado): voto dividido mínimo = metade da soma das diferenças entre os 3 campos; núcleo mínimo do campo = máx(0, a + b − 1).

## Subaba "Urna esperada × urna anômala" (`voto-cruzado.html#urnas`)

- **Índice de anomalia** de uma urna = raiz da média dos quadrados dos dois erros da previsão (% da esquerda e % da direita para presidente, real − previsto), em p.p. Zero = votou para presidente exatamente como o padrão do estado indica dado o voto nos outros 4 cargos. No ES (06/10): mediana 3,6 p.p.; 90% abaixo de 7,5.
- Escolhe a urna de menor e a de maior índice entre as com 200+ votantes (menus com as 15 de cada ponta). Em 06/10: esperada = Vitória, zona 52, seção 407 (0,0); anômala = Pinheiros, zona 39, seção 111 (26,1: Lula 74%, previsto 49%; a anomalia vem de votos locais, como 84% em um deputado federal do PSB e 79% no centro para deputado estadual, e do governador do MDB contado como centro).
- Lado a lado: resumo (índice, real × previsto, campos em cada cargo) e, por cargo, todos os votos da urna (deputados: por partido, com a lista completa de candidatos em "Todos os candidatos"). Lê `docs/data/es/secoes/cargos.json` e `m/<tse>.json`.

## Dados do Brasil (baixados em 06/10, ainda não processados)

`apuracao-bruto/secoes-br/` (fora do git, 2,6 GB compactados, ~20 GB descompactados): `votacao_secao_2026_<UF>.zip` dos 27 estados, `votacao_secao_2026_BR.zip` (presidente), `detalhe_votacao_secao_2026.zip` e `eleitorado_local_votacao_2026.zip`, de `https://cdn.tse.jus.br/estatistica/sead/odsele/`. O zip do ES baixado agora é maior que o de 05/10 (319 MB × 274 MB descompactados): conferir se o TSE republicou antes de reprocessar.
