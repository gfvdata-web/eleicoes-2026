# Voto cruzado: base estatística e matemática

Referência para interpretar qualquer número de `voto-cruzado.html`. Escrito em 06/10/2026, junto com a construção da página.
Quando o usuário mandar um print ou um número da página, use este documento para dizer **de onde o número vem, como foi calculado e o que ele pode (e não pode) significar**.
Para recalcular, veja a seção 11. Funcionamento da página e formato dos dados: [voto-cruzado.md](voto-cruzado.md).

---

## 1. Pergunta e limite fundamental

**Pergunta:** o voto para presidente acompanha o voto nos outros cargos (governador, Senado, deputado federal e estadual)? Onde ele se descola?
Direção principal combinada com o usuário: **prever o voto para presidente a partir dos outros 4 votos** (não o contrário).

**Limite:** o voto é secreto. Não existe dado individual. Verificado em 06/10: o RDV (Registro Digital do Voto) publicado pelo TSE para cada urna
guarda **uma lista por cargo, ordenada por número**, sem ligação entre os cargos de um mesmo eleitor (145 urnas do ES conferidas).
Logo, toda a análise é **ecológica**: compara **grupos de eleitores** (urnas, locais, municípios, estados), nunca pessoas.

> **Falácia ecológica.** Se uma urna tem 60% de esquerda para presidente e 60% para governador, isso **não prova** que são os mesmos eleitores.
> Toda frase do tipo "os eleitores do Lula votaram em X" é uma inferência sobre agregados, com incerteza. Os únicos números
> **certos** sobre o comportamento de pessoas são os limites matemáticos da seção 6.

---

## 2. Unidades e dados

- **Seção (urna):** unidade básica, média de ~240 votantes (no ES, ~229 votos válidos para presidente). Seções agregadas votam na urna da principal e vêm somadas nela.
  Entram só seções **instaladas, não anuladas e com comparecimento > 0** (Brasil: ~470 mil; ES: 9.844; SP: 103.656).
- **Local de votação** (escola etc.), **município** e **estado** = somas das seções.
- **Exterior não entra** (não há governador nem deputados lá). Por isso o total de Lula na página (53,72 mi) é ~94 mil menor que o oficial (53,82 mi).
- **Votos válidos de um cargo (V):** nominais + legenda de candidatos/partidos com destino "Válido". Brancos, nulos e votos em candidatos **sub judice** ficam fora.
  No **Senado** cada eleitor tem 2 votos, então V ≈ 2 × votantes. No **DF**, "deputado estadual" = deputado distrital.
- **Fontes:** dados abertos do TSE (votação por seção, detalhe por seção, locais de votação), mais a apuração do TSE para partido e destino de cada número. Script: `scripts/voto_cruzado.py`.

## 3. Réguas: como cada voto vira um grupo

Toda a análise usa **3 grupos com índices 0, 1, 2**. O que eles significam depende da **régua** escolhida no topo da página (guardada no navegador):

### Régua B: campo do partido

| Grupo | Partidos |
|---|---|
| 0 Esquerda | PT, PSOL, PCdoB, Rede, PSB, PDT, PV, UP, PSTU, PCB, PCO |
| 1 Centro | MDB, PSD, PSDB, Podemos, Solidariedade, Avante, Cidadania, Agir, Mobiliza |
| 2 Direita | PL, Novo, PP, Republicanos, União, PRD, Missão, DC, PRTB, Democrata |

Base: `camara.html` (uso comum na imprensa), mais os partidos que faltavam (Agir, Mobiliza, PRTB e Democrata foram classificados por Claude; o usuário ainda não confirmou).
Esquerda para presidente ≈ Lula; direita para presidente ≈ Flávio + Renan + Zema + DC + Democrata. Fraqueza: o campo é do *partido*, não da *aliança*
(um governador do MDB ou PSD aliado ao Lula conta como "centro").

### Régua A: aliança presidencial (implementada em 06/10; padrão da página desde então)

0 = aliança de Lula, 1 = neutros e outros, 2 = aliança de Flávio. Classificação **feita sem olhar o resultado das urnas** (evita circularidade), por `scripts/alinhamento.py`:
1. **Presidente:** Lula = 0, Flávio = 2, os outros 10 candidatos = 1 ("outros", incluindo Caiado, Zema e Renan).
2. **Governador e senador:** coligação registrada no TSE (`consulta_cand_2026`). Coligação, federação ou partido com o **PT** → 0; com o **PL** → 2; com os dois → 1 (conflito; não ocorreu).
3. Se a coligação não decide: **apoio declarado**, com fonte, em `docs/data/voto-cruzado/apoios-declarados.json`. Pesquisado em 06/10 para os 70 neutros com ≥ 10% dos votos;
   só vale **declaração explícita do próprio candidato** (ou apoio público de Lula a ele). "Quer o apoio" ou "o pai apoia" não contam.
   Resultado: 7 → Lula (Casagrande, Fufuca, Weverton, Veneziano, Celso Sabino, Zenaide Maia, Mônica Benício), 5 → Flávio (Lahesio Bonfim, Alan Rick, Wilson Lima, Cleitinho,
   Cristina Graeml), 4 neutros declarados (Ferraço, Braide, Daniel Vilela e Gracinha Caiado; os dois últimos apoiam Caiado). As fontes vieram de buscas na web e convém conferir.
4. Sem nenhum dos dois: **neutro**.
5. **Deputados (por partido):** partido da coligação presidencial de Lula (PT, PCdoB, PV, PSB, PDT, PSOL, Rede) → 0; da de Flávio (só o PL) → 2; os outros → 1.

Totais (governador + senador, candidatos com voto): 83 aliança de Lula, 326 neutros, 76 aliança de Flávio.
Consequência importante: o grupo 2 da régua A é **bem menor** que a direita da régua B, porque Republicanos, PP, União etc. não estão na coligação do Flávio
(nos deputados do ES: aliança de Flávio 25% contra direita 57%).

### Reclassificação pelo leitor

Na subaba **Classificação** (`#classificacao`) o leitor muda o grupo de qualquer candidato ou partido. As mudanças ficam em `localStorage` (`vc-reclass`), **só naquele navegador**,
e todas as abas passam a usá-las. Chaves: `B|SIGLA` (régua B), `P|número` (presidente), `UF|1|número` e `UF|2|número` (governador e senador), `D|SIGLA` (deputados, todos os estados)
e `UF|D|SIGLA` (deputados num estado). Dá para exportar e importar um JSON com as mudanças. **Ao interpretar um print, pergunte se havia reclassificações**: elas mudam todos os números.

## 4. Notação

Para uma unidade *i* (urna, local, município ou estado), um cargo *k* e um campo *g*:

- k = 0 presidente, 1 governador, 2 Senado, 3 deputado federal, 4 deputado estadual
- **V_ik** = votos válidos do cargo k na unidade i
- **N_ikg** = votos válidos do campo g no cargo k
- **p_ikg = N_ikg / V_ik**: proporção do campo g no cargo k (o "%" de todas as barras e eixos)
- **w_i** = comparecimento (votantes) da unidade: é o **peso** de cada unidade nas regressões e o **tamanho** dos pontos

Para unidades agregadas, somam-se primeiro os votos (N e V) e só depois se divide. A proporção de um município **não** é a média simples das proporções das urnas.

## 5. O modelo "presidente previsto pelos outros votos"

### 5.1 Equação

Para um campo g (esquerda **ou** direita; cada um tem o seu modelo):

```
p̂_i0 = b0 + b1·p_i1 + b2·p_i2 + b3·p_i3 + b4·p_i4        (todos do mesmo campo g)
previsto_i = min(1, max(0, p̂_i0))                          (cortado em 0–100%)
```

Em palavras: o % do campo para presidente é estimado como uma combinação linear do % do mesmo campo nos 4 outros cargos.

### 5.2 Ajuste (mínimos quadrados ponderados)

Os coeficientes b = (b0…b4) minimizam

```
Σ_i  w_i · (p_i0 − p̂_i0)²
```

somando sobre **todas as urnas** do recorte (estado ou país). Solução pelas equações normais `(XᵀWX) b = XᵀWy`, resolvidas por eliminação de Gauss
(função `ajustar` no navegador e no script). O peso w_i (comparecimento) faz uma urna de 400 votantes contar o dobro de uma de 200.
Urnas com V = 0 em algum cargo ficam fora do ajuste.

### 5.3 Qual modelo é usado onde

| Onde | Ajustado em | Calculado |
|---|---|---|
| Aba "Análise por campo", unidades Urnas / Locais / Municípios | todas as urnas do **ES** | no navegador |
| Aba "Análise por campo", unidade **Estados** | os **5.570 municípios** do Brasil (pesos = comparecimento) | no navegador |
| Subaba "Comparativo estados", cada gráfico | todas as urnas **daquele estado** | no navegador |
| Subaba "Urna esperada × anômala" | urnas do **ES** | no navegador |

Consequências:
- O **filtro de município não muda o modelo**. O padrão é sempre o do estado inteiro, e o filtro só escolhe quais unidades aparecem.
- Todos os modelos são recalculados no navegador para a **régua** e as **reclassificações** atuais.
- O modelo nacional é ajustado em **municípios**, não em urnas (o navegador não carrega as 470 mil urnas do país). Municípios têm menos ruído, então o R² nacional não é comparável
  ao de um estado ajustado por urna. Até 06/10 cedo ele era ajustado por urna em Python (R² esquerda 0,31, direita 0,70; ver 5.6).
- Um estado no gráfico "Estados" é comparado ao **padrão nacional**. No comparativo, cada estado é comparado ao **próprio padrão**.
  O "+27,6 p.p." do Piauí na unidade Estados quer dizer "o Piauí deu ao Lula 27,6 p.p. a mais do que o padrão nacional preveria pelos outros cargos do Piauí".
- Para unidades agregadas, o previsto é calculado **sobre as proporções agregadas** da unidade (soma os votos e depois aplica a equação).

### 5.4 Leitura do card

- **"X% da variação entre urnas explicada pelos outros cargos"** = R² ponderado:
  `R² = 1 − Σ w_i (y_i − previsto_i)² / Σ w_i (y_i − ȳ_w)²`, com y = p_i0 e ȳ_w a média ponderada.
  Usa o previsto **já cortado** em 0–100%. R² = 1 seria previsão perfeita; R² = 0 seria o mesmo que chutar a média do estado para toda urna.
- **"Diferença típica entre real e previsto, por urna"** = raiz do erro quadrático médio ponderado, `sqrt(Σ w_i (y_i − previsto_i)² / Σ w_i)`, em p.p.
  Cerca de 2/3 das urnas ficam dentro de ± esse valor.
- **Peso de um cargo (b_k):** quanto o previsto para presidente sobe, em p.p., para cada 1 p.p. a mais do campo **naquele** cargo, **com os outros 3 parados**.
  Ex.: ES, esquerda, Senado = 0,86 → duas urnas iguais em tudo menos em +10 p.p. de esquerda no Senado diferem em +8,6 p.p. no previsto para presidente.

### 5.5 Cuidados ao interpretar os pesos

1. **Os cargos se sobrepõem (colinearidade).** Os 4 regressores andam juntos (onde a esquerda vai bem no Senado, costuma ir bem nos deputados).
   A regressão divide o crédito entre eles. Um peso ≈ 0 quer dizer "não acrescenta informação **depois** dos outros", e não "não tem relação".
   Pesos negativos pequenos (ex.: −0,03) são ruído dessa divisão.
2. **Regressor quase constante → peso absurdo.** Quando o campo quase não teve candidato num cargo, a coluna é ~0 em todas as urnas e o coeficiente explode.
   Em 06/10 isso acontece com a esquerda para governador em AL (0,4%), AM, AP, MT, PA, PB, SE e TO, com pesos como −5,7 (AL), −6,8 (PB) e −7,4 (TO).
   Esses pesos **não têm interpretação**. Leia o R² e o erro, não o peso.
   **Desde 06/10 a página tira esse cargo do ajuste** (peso 0, "fora" no card) quando o grupo tem média < 3% ou desvio-padrão entre urnas < 2 p.p.
   O R² cai pouco (régua B: AL 0,20 → 0,15; régua A: RR 0,51 → 0,49) e os pesos absurdos somem. Os números das tabelas da 5.6 são do ajuste com os 4 cargos.
3. **Não é causal.** O peso descreve associação entre urnas, não "o efeito" de um cargo sobre o outro.
4. **Intercepto (b0)** não aparece no card. É o previsto quando os 4 cargos têm 0% do campo, normalmente fora da faixa dos dados.
5. **Selo de encaixe** no card: bom (R² ≥ 0,6), moderado (0,4–0,6), fraco (< 0,4). Com encaixe fraco, os desvios dizem que o padrão não se aplica, não que há anomalia.

### 5.6 Resultados de referência (06/10/2026)

ES (b para governador, Senado, dep. federal, dep. estadual):
- Esquerda: b0 = 0,005; 0,18 / 0,86 / 0,08 / −0,03; R² 0,74; erro 5,2 p.p.
- Direita: b0 = 0,096; 0,18 / 0,79 / 0,09 / −0,05; R² 0,82; erro 4,3 p.p.

Brasil, modelo **por urna** (Python, antes da mudança para municípios; régua B):
- Esquerda: b0 = 0,275; 0,09 / 0,30 / 0,02 / 0,19; **R² 0,31**; erro 14,4 p.p.
- Direita: b0 = 0,023; 0,11 / 0,64 / 0,12 / 0,06; R² 0,70; erro 9,0 p.p.

O R² nacional baixo da esquerda vem do Nordeste: Lula muito acima do que a esquerda nos outros cargos indicaria. Na unidade Estados: PI +27,6, AL +24,9, MA +23,9 e SE +21,4 p.p.
A causa provável são governadores e senadores de partidos de "centro" aliados ao Lula, mais estados sem candidato de esquerda a governador.

Brasil, modelo **por município** (o que a página mostra hoje na unidade Estados): régua B esquerda R² 0,28 (erro 13,3 p.p.); régua A Lula **R² 0,70** (8,6 p.p.); régua A Flávio R² 0,57 (9,4 p.p.).
Na régua B, os estados mais acima do previsto são PI (+26,2), MA (+23,5), AL (+22,9) e SE (+21,4). Na régua A, TO (+21,8), SE (+18,3), PB (−13,2), AL (+13,0) e MA (+11,2).

**Régua B × régua A por estado** (modelo por urna; R² e erro em p.p.):

| UF | B esq. R² | B erro | A Lula R² | A erro | B dir. R² | A Flávio R² |
|---|---|---|---|---|---|---|
| AC | 0,62 | 6,1 | 0,63 | 6,0 | 0,38 | 0,34 |
| AL | 0,20 | 12,6 | **0,63** | 8,5 | 0,18 | **0,66** |
| AM | 0,37 | 13,3 | **0,78** | 7,9 | 0,68 | 0,80 |
| AP | 0,36 | 8,3 | 0,33 | 8,4 | 0,19 | 0,32 |
| BA | 0,77 | 5,8 | 0,76 | 5,9 | 0,74 | 0,75 |
| CE | 0,85 | 4,5 | 0,86 | 4,5 | 0,84 | 0,87 |
| DF | 0,87 | 2,2 | 0,88 | 2,2 | 0,85 | 0,88 |
| ES | 0,74 | 5,2 | 0,76 | 5,0 | 0,82 | 0,81 |
| GO | 0,39 | 6,3 | 0,41 | 6,3 | 0,57 | 0,65 |
| MA | 0,19 | 13,2 | 0,28 | 12,4 | 0,53 | **0,78** |
| MG | 0,51 | 8,3 | 0,56 | 7,9 | 0,61 | 0,75 |
| MS | 0,82 | 4,8 | 0,83 | 4,8 | 0,80 | 0,74 |
| MT | 0,52 | 8,6 | **0,78** | 5,8 | 0,77 | 0,54 |
| PA | 0,22 | 14,7 | **0,87** | 5,9 | 0,46 | **0,89** |
| PB | 0,27 | 11,1 | **0,81** | 5,7 | 0,36 | **0,87** |
| PE | 0,49 | 8,1 | 0,50 | 8,1 | 0,65 | 0,66 |
| PI | 0,63 | 6,9 | 0,67 | 6,6 | 0,63 | 0,71 |
| PR | 0,77 | 4,5 | 0,77 | 4,5 | 0,82 | 0,79 |
| RJ | 0,80 | 4,1 | 0,88 | 3,1 | 0,89 | 0,86 |
| RN | 0,36 | 9,3 | **0,63** | 7,1 | 0,60 | 0,66 |
| RO | 0,66 | 5,2 | 0,56 | 6,0 | 0,66 | 0,80 |
| RR | 0,65 | 8,1 | 0,51 | 9,6 | 0,77 | 0,69 |
| RS | 0,94 | 3,2 | 0,94 | 3,2 | 0,94 | 0,93 |
| SC | 0,84 | 3,7 | 0,84 | 3,7 | 0,80 | 0,67 |
| SE | 0,12 | 9,4 | **0,57** | 6,6 | 0,18 | 0,48 |
| SP | 0,95 | 2,4 | 0,95 | 2,4 | 0,95 | 0,95 |
| TO | 0,22 | 12,1 | 0,08 | 13,2 | 0,16 | 0,22 |

Leitura: A melhora muito onde B falhava (AL, AM, PA, PB, SE, RN, MT para Lula; MA, PA, PB, AL para Flávio) e quase não muda onde B já funcionava (SP, RS, DF, CE, BA).
Piora em alguns casos (RO e RR para Lula; MT e SC para Flávio): provavelmente porque a aliança de Flávio na régua A é só o PL, deixando de fora partidos de direita que apoiam
Flávio informalmente. TO e MA (Lula) seguem mal explicados (candidatos relevantes neutros).

Tabela da régua B (R² e erro em p.p.; mediana e percentil 90 do índice de anomalia da seção 7):

| UF | R² esq | erro esq | R² dir | erro dir | % esq. gov. | índice med / p90 |
|---|---|---|---|---|---|---|
| AC | 0,62 | 6,1 | 0,38 | 7,7 | 7,7 | 4,1 / 10,7 |
| AL | 0,20 | 12,6 | 0,18 | 12,2 | 0,4 | 9,8 / 19,7 |
| AM | 0,37 | 13,3 | 0,68 | 8,7 | 0,7 | 7,3 / 19,4 |
| AP | 0,36 | 8,3 | 0,19 | 8,6 | 0,2 | 5,0 / 13,4 |
| BA | 0,77 | 5,8 | 0,74 | 5,9 | 56,2 | 4,1 / 9,1 |
| CE | 0,85 | 4,5 | 0,84 | 4,3 | 53,3 | 2,7 / 7,0 |
| DF | 0,87 | 2,2 | 0,85 | 2,3 | 37,1 | 1,7 / 3,5 |
| ES | 0,74 | 5,2 | 0,82 | 4,3 | 15,4 | 3,6 / 7,5 |
| GO | 0,39 | 6,3 | 0,57 | 5,8 | 10,2 | 4,7 / 9,3 |
| MA | 0,19 | 13,2 | 0,53 | 9,4 | 9,9 | 8,4 / 18,9 |
| MG | 0,51 | 8,3 | 0,61 | 7,1 | 30,2 | 5,2 / 12,1 |
| MS | 0,82 | 4,8 | 0,80 | 5,0 | 24,2 | 3,3 / 7,7 |
| MT | 0,52 | 8,6 | 0,77 | 6,1 | 0,0 | 5,2 / 11,3 |
| PA | 0,22 | 14,7 | 0,46 | 11,9 | 2,1 | 9,8 / 22,7 |
| PB | 0,27 | 11,1 | 0,36 | 9,6 | 0,5 | 8,3 / 16,0 |
| PE | 0,49 | 8,1 | 0,65 | 6,3 | 46,4 | 5,0 / 11,1 |
| PI | 0,63 | 6,9 | 0,63 | 6,4 | 71,7 | 4,4 / 10,9 |
| PR | 0,77 | 4,5 | 0,82 | 3,9 | 23,7 | 3,1 / 6,5 |
| RJ | 0,80 | 4,1 | 0,89 | 3,1 | 3,4 | 2,7 / 5,5 |
| RN | 0,36 | 9,3 | 0,60 | 7,0 | 36,3 | 5,9 / 13,1 |
| RO | 0,66 | 5,2 | 0,66 | 5,7 | 8,2 | 3,6 / 7,7 |
| RR | 0,65 | 8,1 | 0,77 | 6,3 | 1,5 | 3,8 / 9,6 |
| RS | 0,94 | 3,2 | 0,94 | 3,1 | 31,8 | 2,2 / 5,0 |
| SC | 0,84 | 3,7 | 0,80 | 4,3 | 16,4 | 2,8 / 6,4 |
| SE | 0,12 | 9,4 | 0,18 | 8,4 | 0,0 | 6,9 / 14,1 |
| SP | 0,95 | 2,4 | 0,95 | 2,5 | 37,3 | 1,8 / 3,8 |
| TO | 0,22 | 12,1 | 0,16 | 12,2 | 0,6 | 9,1 / 19,2 |

Padrão: R² baixo ⇔ estado onde as alianças locais não seguem a régua esquerda/centro/direita (muitos no Nordeste e no Norte) ou onde um campo não teve candidato a governador.

## 6. Comparação com um cargo e limites matemáticos

Quando "Comparar presidente com" é um cargo k (e não "Previsto"), o eixo X é p_ikg em vez do previsto, e **diferença = p_i0g − p_ikg**.

Para comparações com cargos de **1 voto** (governador, dep. federal, dep. estadual) há dois **limites exatos**, não estimativas:

- **Voto dividido mínimo** = ½ · Σ_h |p_i0h − p_ikh| (soma sobre os 3 campos h).
  É a distância de variação total entre as duas distribuições: a menor fração de eleitores que **necessariamente** votou em campos diferentes nos dois cargos.
  Ex.: presidente 60/10/30 e governador 40/30/30 (esq/cen/dir) → ½(20 + 20 + 0) = 20%.
- **Núcleo mínimo** do campo g = max(0, p_i0g + p_ikg − 1) (limite inferior de Fréchet): a menor fração que **necessariamente** votou no campo g nos dois cargos.
  O máximo possível é min(p_i0g, p_ikg) (não aparece na página).
  Ex.: 60% e 40% → núcleo mínimo 0% e máximo 40%; 70% e 65% → mínimo 35%.

Ressalvas: (a) os dois cargos têm denominadores um pouco diferentes (brancos e nulos variam por cargo), então os limites são exatos sobre os **votos válidos**, e aproximados sobre os eleitores;
(b) **não valem para o Senado** (2 votos por eleitor: a mesma pessoa pode dar um voto à esquerda e outro à direita). Por isso a página mostra "—" nesse caso.

## 7. Índice de anomalia (subaba "Urna esperada × urna anômala")

Para cada urna, com o modelo do ES:

```
rE = p_i0,esq − previsto_esq(i)      rD = p_i0,dir − previsto_dir(i)
índice_i = sqrt( (rE² + rD²) / 2 )                 (em p.p.)
```

É a média quadrática dos dois erros. Zero significa que a urna votou para presidente exatamente como o padrão do estado prevê pelos outros cargos.
Na escolha das urnas extremas, só entram as que têm **≥ 200 votantes** (`MIN_VOT`).
Referência ES: mediana 3,6 p.p. e 90% abaixo de 7,5 p.p. (outros estados na tabela 5.6).

O índice mede desvio em relação **ao modelo**, não "estranheza" absoluta. A urna mais anômala do ES em 06/10 (Pinheiros, zona 39, seção 111) é na verdade coerente
e local: Lula 74%, Ferraço (MDB, "centro") 75%, um deputado federal do PSB com 71% e um estadual do Agir com 63%. Ela fica longe do modelo porque o modelo
dá peso ~0 aos deputados e trata o MDB como centro.

## 8. Ruído de amostragem: o que é sinal e o que é acaso

Mesmo um eleitorado com "tendência" fixa varia de urna para urna por acaso. Tratando os V votos de uma urna como sorteios com probabilidade p:

```
desvio-padrão do % ≈ sqrt( p (1 − p) / V )
```

Com V ≈ 230 e p ≈ 0,4, isso dá ≈ **3,2 p.p.** (média ponderada no ES: 3,1 p.p.). Consequências:
- Boa parte do "erro típico" de 5,2 p.p. do ES por urna é **puro acaso**. A parte sistemática (que o modelo não explica) é da ordem de sqrt(5,2² − 3,1²) ≈ 4 p.p.
- Uma diferença de ±5 p.p. numa urna **não é anomalia**. Acima de ~3 desvios (±10 p.p. numa urna média) começa a ser difícil atribuir ao acaso.
- Em unidades maiores o ruído cai com 1/sqrt(V): num local com ~1.000 votos, ~1,5 p.p.; num município com 50 mil, ~0,2 p.p.
  Por isso locais e municípios dão um quadro mais estável e a tabela avisa que "urnas com poucos votantes oscilam mais".
- O mesmo vale para o índice de anomalia: em urnas pequenas, ele é inflado pelo acaso. Por isso o corte de 200 votantes.

## 9. Elementos visuais

- **Dispersão:** X = previsto (ou % do campo no cargo escolhido), Y = % do campo para presidente, ambos de 0 a 100%. Tamanho do ponto ∝ sqrt(votantes).
  **Diagonal tracejada** = X igual a Y. **Acima** (roxo) = presidente teve mais do campo do que o previsto ou do que o outro cargo; **abaixo** (verde) = menos.
  Distância vertical até a diagonal = diferença.
  Num modelo bem ajustado, a nuvem fica **em volta** da diagonal; uma nuvem inteira deslocada só acontece na comparação com um cargo.
- **Cor:** escala divergente verde → cinza → roxo, de −10 a +10 p.p., cortada nas pontas (valores além de ±10 ficam com a cor máxima).
- **Mapa:** mesma diferença da dispersão, por município (ES) ou por estado (unidade Estados).
- **Barras "Cada cargo por campo":** p_kg agregado do recorte (estado, município ou Brasil). No Senado, sobre os 2 votos.
- **Comparativo estados:** um gráfico por UF, cada um com o modelo próprio (5.3); mesmo eixo 0–100% em todos. R², erro e pesos acima de cada gráfico.

### 9.1 Conclusões automáticas do comparativo

Cada gráfico do comparativo tem frases geradas dos números (ver [voto-cruzado.md](voto-cruzado.md), subaba "Comparativo estados"). Como ler:
- **Posição na diagonal** = quanto o estado vota no campo. Nuvem mais acima e à direita = estado mais favorável ao campo que o Brasil.
- **Comprimento da nuvem** ao longo da diagonal = diferenças regionais dentro do estado.
- **Largura da nuvem** em volta da diagonal = o quanto os outros cargos explicam o presidente (R²).
- **Acima × abaixo:** o modelo tem intercepto, então a diferença média ponderada é ~0 **por construção**. Uma nuvem simétrica é o esperado; o informativo é
  quanta gente está além do limiar de acaso (±10 p.p. por urna, ±5 por local, ±3 por município, cerca de 3 desvios do ruído da seção 8) e se um lado tem muito mais que o outro
  (bolsões onde o presidenciável teve mais ou menos voto que o resto da chapa do seu lado).

## 10. Opção A: decisões do usuário e pendências (06/10)

- **Implementada** como "régua A" (seção 3), com a subaba Classificação para recategorizar.
- **Comparar A e B** nas mesmas urnas é parte natural da análise (o seletor de régua faz isso), e não um "teste" à parte.
- **Não fazer:** validação cruzada por blocos de municípios e teste de sensibilidade trocando candidatos duvidosos de lado (itens 3 e 4 da proposta).
- **Não fazer:** comparação com cruzamentos de pesquisas (não há acesso a pesquisas com cruzamento).
- **Para retomar depois (o usuário quer questionar):**
  - *Mapa dos resíduos.* O usuário não entendeu a proposta. Explicação a dar: o "resíduo" é a diferença real − previsto de cada município. Na régua B ele forma manchas
    regionais (o Nordeste inteiro acima do previsto), sinal de que falta uma variável sistemática no modelo. Se a régua A captar a causa certa (alianças locais),
    as manchas devem sumir, e o mapa da aba "Análise por campo" com "Previsto" fica sem blocos de uma cor só. É só olhar o mapa nas duas réguas; dá para medir com o I de Moran.
  - *Teto de previsibilidade (modelo C):* regredir o % de Lula sobre o % de cada candidato, estado por estado, sem classificação. Serve só para medir quanto A ainda pode melhorar;
    nunca para classificar (seria circular).
  - *Urnas com mais de 10 p.p. de diferença:* analisar o que elas têm em comum (pedido do usuário para depois).

## 11. Como recalcular qualquer número

Formato atual (desde 06/10): `docs/data/voto-cruzado/<uf>.json` traz votos **por entidade** (candidato a presidente, governador e senador; partido nos deputados),
e a soma por grupo é feita na hora, conforme a régua. Exemplo em Python (régua A, sem reclassificações):

```python
import json, numpy as np
cls = json.load(open('docs/data/voto-cruzado/classificacao.json', encoding='utf-8'))
d = json.load(open('docs/data/voto-cruzado/es.json', encoding='utf-8'))
uf = d['uf']; cand = {(r[0], r[1]): r[6] for r in cls['a']['cand'][uf]}
def grupo(e, regua='a'):                  # e = [cargo, número, nome, sigla]
    k, num, _, sg = e
    if regua == 'b': return cls['b'].get(sg)
    if k == 0: return cls['a']['pres'].get(num, 1)
    if k <= 2: return cand.get((k, num), 1)
    return cls['a']['dep'].get(sg, 1)
gs = [grupo(e) for e in d['ent']]; ks = [e[0] for e in d['ent']]
# S: colunas 0 aptos, 1 comparecimento, depois para k = 0..4: 2+4k válidos, 3+4k grupo 0, 4+4k grupo 1, 5+4k grupo 2
S = np.zeros((len(d['secoes']), 22))
for i, r in enumerate(d['secoes']):           # r = [local, zona, seção, aptos, comp, entidade, votos, ...]
    S[i, 0], S[i, 1] = r[3], r[4]
    for j in range(5, len(r), 2):
        e, q = r[j], r[j + 1]; S[i, 2 + 4*ks[e]] += q
        if gs[e] is not None: S[i, 3 + 4*ks[e] + gs[e]] += q
g = 0; w = S[:, 1]; p = lambda k: S[:, 3 + 4*k + g] / np.maximum(S[:, 2 + 4*k], 1)
y = p(0); X = np.column_stack([np.ones(len(S))] + [p(k) for k in range(1, 5)])
b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
r = y - np.clip(X @ b, 0, 1)
R2 = 1 - np.sum(w * r**2) / np.sum(w * (y - np.average(y, weights=w))**2); erro = np.sqrt(np.average(r**2, weights=w))
```

- Achar uma urna: `d['secoes'][i][1]` = zona, `[2]` = seção; município em `d['locais'][r[0]][0]`, nome em `d['mun']`.
- Unidade agregada: some os votos das urnas da unidade **antes** de dividir.
- Brasil: `brasil.json` → `ufs[UF]` = `{ent, tot: [aptos, comp, entidade, votos, ...], mun: {tse: [aptos, comp, pares...]}}`; o modelo nacional é ajustado nas linhas de `mun`.
- Votos completos de uma urna do ES, candidato a candidato: `docs/data/es/secoes/m/<tse>.json` + `cargos.json` (ver [es-secoes.md](es-secoes.md)).

## 12. Roteiro para responder perguntas sobre um print

1. Identifique **a régua (campo do partido ou aliança presidencial), se há reclassificações do leitor, a aba, o campo, a comparação (previsto/cargo) e a unidade**. Cada combinação muda o número.
2. Identifique **qual modelo** está por trás (tabela 5.3): ES, Brasil (por município) ou o do próprio estado.
3. Diferença = real − previsto (ou − cargo), em p.p.; positivo = presidente acima.
4. Antes de chamar algo de anomalia, compare com o ruído (seção 8) e com a mediana/p90 do índice no estado (tabela 5.6).
5. Se o número parecer estranho, verifique: estado sem candidato do campo a governador (5.5, item 2); centro grande para governador (classificação por partido);
   Senado com 2 votos; urna pequena.
6. Lembre a falácia ecológica (seção 1): descreva o que os agregados mostram, sem afirmar o voto de indivíduos.
