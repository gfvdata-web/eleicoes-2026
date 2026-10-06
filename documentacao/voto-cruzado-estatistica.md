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

## 3. Campos políticos (opção B, atual)

Cada voto conta para o **campo do partido** do candidato (para legenda, o do partido):

| Campo | Partidos |
|---|---|
| Esquerda (g = 0) | PT, PSOL, PCdoB, Rede, PSB, PDT, PV, UP, PSTU, PCB, PCO |
| Centro (g = 1) | MDB, PSD, PSDB, Podemos, Solidariedade, Avante, Cidadania, Agir, Mobiliza |
| Direita (g = 2) | PL, Novo, PP, Republicanos, União, PRD, Missão, DC, PRTB, Democrata |

Base: `camara.html` (uso comum na imprensa), mais os partidos que faltavam. Agir, Mobiliza, PRTB e Democrata foram classificados por Claude e o usuário ainda não confirmou.
Na prática, **esquerda para presidente ≈ Lula** (no ES, 37,9% contra 37,8% do Lula) e **direita para presidente ≈ Flávio + Renan + Zema + DC + Democrata**.
O centro para presidente é pequeno (Cury, Caiado).

**Fraqueza conhecida:** o campo é do *partido*, não da *aliança*. Um governador do MDB ou do PSD aliado ao Lula conta como "centro". Isso é o que a opção A (seção 10) resolve.

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
| Aba "Análise por campo", unidade **Estados** | todas as urnas do **Brasil** (~470 mil) | no script → `brasil.json` |
| Subaba "Comparativo estados", cada gráfico | todas as urnas **daquele estado** | no navegador |
| Subaba "Urna esperada × anômala" | urnas do **ES** | no navegador |

Consequências:
- O **filtro de município não muda o modelo**. O padrão é sempre o do estado inteiro, e o filtro só escolhe quais unidades aparecem.
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
3. **Não é causal.** O peso descreve associação entre urnas, não "o efeito" de um cargo sobre o outro.
4. **Intercepto (b0)** não aparece no card. É o previsto quando os 4 cargos têm 0% do campo, normalmente fora da faixa dos dados.

### 5.6 Resultados de referência (06/10/2026)

ES (b para governador, Senado, dep. federal, dep. estadual):
- Esquerda: b0 = 0,005; 0,18 / 0,86 / 0,08 / −0,03; R² 0,74; erro 5,2 p.p.
- Direita: b0 = 0,096; 0,18 / 0,79 / 0,09 / −0,05; R² 0,82; erro 4,3 p.p.

Brasil (modelo nacional, `brasil.json`):
- Esquerda: b0 = 0,275; 0,09 / 0,30 / 0,02 / 0,19; **R² 0,31**; erro 14,4 p.p.
- Direita: b0 = 0,023; 0,11 / 0,64 / 0,12 / 0,06; R² 0,70; erro 9,0 p.p.

O R² nacional baixo da esquerda vem do Nordeste: Lula muito acima do que a esquerda nos outros cargos indicaria. Na unidade Estados: PI +27,6, AL +24,9, MA +23,9 e SE +21,4 p.p.
A causa provável são governadores e senadores de partidos de "centro" aliados ao Lula, mais estados sem candidato de esquerda a governador.

Por estado (R² e erro em p.p.; mediana e percentil 90 do índice de anomalia da seção 7):

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

## 10. Opção A: alinhamento com os presidenciáveis (proposta de 06/10, ainda não implementada)

**Ideia:** trocar o campo do *partido* pelo **alinhamento na eleição presidencial**. Cada candidato a governador e senador é classificado como
aliado de Lula (L), aliado de Flávio (F) ou outro/neutro (O). Nos deputados, cada partido é classificado **por estado**.
O modelo da seção 5 continua igual; muda só o que é "o campo" em cada cargo.

**Por que deve funcionar melhor:** os estados de R² baixo (tabela 5.6) são justamente aqueles em que a régua esquerda/centro/direita
não descreve as alianças (governadores e senadores de MDB, PSD, PP etc. aliados ao Lula no Nordeste e no Norte) ou em que um campo não teve candidato a governador.

### 10.1 Classificação (sem olhar o resultado)

1. **Fonte objetiva:** a composição da coligação de cada candidato a governador e senador no registro do TSE
   (arquivo de candidatos `consulta_cand_2026`, campo de composição da coligação). Coligação com o PT ou com a federação PT/PCdoB/PV → L; com o PL → F.
2. **Apoio declarado** (para quem não está na mesma coligação): só com fonte verificável (site oficial, TSE, imprensa), anotada numa planilha de dados (`docs/data/`), com a fonte de cada linha.
3. **Na dúvida → O** (neutro). Seguir a regra editorial do projeto: não chutar.
4. **Deputados:** partido da coligação do governador aliado em cada estado, ou partido da coligação presidencial. Testar as duas regras.
5. **Congelar a classificação antes de rodar o modelo.** Assim o critério não é ajustado para melhorar o resultado.

### 10.2 Validação

- **Comparar A e B nas mesmas urnas:** R², erro típico e índice de anomalia por estado. A deve melhorar justamente nos estados problemáticos
  (AL, MA, PA, PB, SE, TO etc.) e quase não mudar onde B já funciona (SP, RS, DF).
- **Validação fora da amostra** (contra sobreajuste): ajustar o modelo com metade dos **municípios** e medir o erro na outra metade, repetindo várias vezes
  (validação cruzada por blocos). Dividir por município, e não por urna, porque urnas vizinhas são parecidas (autocorrelação espacial),
  e isso tornaria o teste otimista demais.
- **Teste de sensibilidade:** refazer com cada candidato duvidoso trocado de grupo (O→L, O→F). Uma conclusão que muda com uma única troca não é robusta.
- **Resíduo espacial:** em B, o resíduo forma blocos regionais (Nordeste inteiro acima). Em A, ele deve ficar mais "salpicado".
  Isso pode ser medido com a correlação do resíduo entre municípios vizinhos (I de Moran).
- **Âncora externa (validação contra dados individuais):** pesquisas com cruzamento "voto para governador × voto para presidente" (Quaest, Datafolha, AtlasIntel)
  são dados **individuais**. Por inferência ecológica (regressão de Goodman ou método de King), dá para estimar "% dos eleitores de Lula que votaram no governador X"
  e comparar com o cruzamento da pesquisa. Se A chegar perto das pesquisas e B não, temos evidência independente.
- **Teto de previsibilidade (modelo C, só para comparação):** regredir o % de Lula diretamente sobre o % de **cada candidato**, estado por estado, sem nenhuma classificação.
  É o máximo de R² alcançável com esses dados; A deve chegar perto desse teto. Os coeficientes de C também sugerem alinhamentos,
  mas **não** podem ser usados para classificar em A (seria circular: o resultado definiria a régua que depois o avalia).

## 11. Como recalcular qualquer número

```python
import json, numpy as np
d = json.load(open('docs/data/voto-cruzado/es.json', encoding='utf-8'))   # ou sp.json, ba.json...
S = np.array(d['secoes'], dtype=float)
# colunas: 0 local, 1 zona, 2 seção, 3 aptos, 4 comparecimento, 5 lula, 6 flávio,
#          depois para k = 0..4: 7+4k válidos, 8+4k esquerda, 9+4k centro, 10+4k direita
p = lambda k, g: S[:, 8 + 4*k + g] / np.maximum(S[:, 7 + 4*k], 1)
w = S[:, 4]
g = 0                                                     # 0 esquerda, 2 direita
y = p(0, g); X = np.column_stack([np.ones(len(S))] + [p(k, g) for k in range(1, 5)])
b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
prev = np.clip(X @ b, 0, 1); r = y - prev
R2 = 1 - np.sum(w * r**2) / np.sum(w * (y - np.average(y, weights=w))**2)
erro = np.sqrt(np.average(r**2, weights=w))
```

- Achar uma urna: linha com `S[:,1] == zona` e `S[:,2] == seção`; o município está em `d['locais'][int(S[i,0])][0]` e o nome em `d['mun']`.
- Unidade agregada: some as colunas 3 em diante das urnas da unidade **antes** de dividir.
- Modelo nacional: `docs/data/voto-cruzado/brasil.json` → `modelo["0"]` / `modelo["2"]` (`b` = [b0, gov, Senado, dep. fed., dep. est.]); totais por UF em `ufs`.
- Votos completos de uma urna do ES (candidato a candidato): `docs/data/es/secoes/m/<tse>.json` + `cargos.json` (ver [es-secoes.md](es-secoes.md)).

## 12. Roteiro para responder perguntas sobre um print

1. Identifique **a aba, o campo (esquerda/direita), a comparação (previsto/cargo) e a unidade**. Cada combinação muda o número.
2. Identifique **qual modelo** está por trás (tabela 5.3): ES, Brasil ou o do próprio estado.
3. Diferença = real − previsto (ou − cargo), em p.p.; positivo = presidente acima.
4. Antes de chamar algo de anomalia, compare com o ruído (seção 8) e com a mediana/p90 do índice no estado (tabela 5.6).
5. Se o número parecer estranho, verifique: estado sem candidato do campo a governador (5.5, item 2); centro grande para governador (classificação por partido);
   Senado com 2 votos; urna pequena.
6. Lembre a falácia ecológica (seção 1): descreva o que os agregados mostram, sem afirmar o voto de indivíduos.
