# Dados

Há dois arquivos de dados, ambos carregados pela página como script comum (definem variáveis globais em `window`):

| Arquivo | Cargo | Variáveis |
|---|---|---|
| [`docs/data/dados.js`](../docs/data/dados.js) | Governador | `window.ESTADOS`, `window.ATUALIZADO_EM` |
| [`docs/data/senado.js`](../docs/data/senado.js) | Senado | `window.SENADO`, `window.ATUALIZADO_EM_SENADO` |

Os dois seguem o mesmo formato por estado; as diferenças do Senado estão na seção [Senado](#senado-senadojs).

# Governador (`dados.js`)

## Variáveis globais

| Variável | Tipo | Uso |
|---|---|---|
| `window.ATUALIZADO_EM` | string (`"DD/MM/AAAA"`) | Data mostrada no rodapé |
| `window.ESTADOS` | array com 27 objetos | Um objeto por UF (26 estados + DF) |

## Formato de um estado

```js
{
  uf: "SP",                       // sigla; precisa bater com `sigla` no GeoJSON
  nome: "São Paulo",
  regiao: "Sudeste",              // Norte | Nordeste | Centro-Oeste | Sudeste | Sul
  pesquisas: [                    // ordem: mais recente primeiro (máx. 3 hoje)
    {
      inst: "Datafolha",          // instituto
      campo: "02–03/10",          // período de campo, texto livre
      tipo: "V",                  // "V" = votos válidos | "T" = votos totais
      res: [["Tarcísio de Freitas", 60], ["Fernando Haddad", 35]]  // [nome, %]
    }
  ],
  candidatos: [
    { nome: "Tarcísio de Freitas", partido: "Republicanos", resumo: "..." }
  ]
}
```

### Regras de consistência

- `pesquisas[0]` é a referência: define a **cor do estado** (margem entre 1º e 2º) e a coluna **"Última pesquisa"** da tabela.
- Os nomes em `res` devem ser idênticos aos de `candidatos[].nome`.
- Um candidato pode aparecer em `candidatos` sem estar em `pesquisas[0]` (aparece com "—" na tabela).
- Percentuais com decimal usam ponto no JS (`45.6`); a página formata com vírgula.
- Partido desconhecido: `"—"`.

## Critério de escolha das pesquisas (versão atual)

- As 3 pesquisas **mais recentes** de cada estado, com prioridade para institutos de maior alcance (Quaest, Datafolha, AtlasIntel) e preferindo institutos diferentes entre si.
- As rodadas finais da Quaest e do Datafolha (campo em 02–03/10/2026) foram registradas em **votos válidos** (`V`), como divulgado pela imprensa. As demais estão em **votos totais**, cenário estimulado (`T`).

## Fontes usadas (coleta de 04/10/2026)

- [O Povo — resultados Datafolha e Quaest para governador](https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/04/resultados-das-pesquisas-datafolha-e-quaest-para-governador.html) (rodadas finais, votos válidos)
- [Gazeta do Povo — pesquisas eleitorais 2026](https://www.gazetadopovo.com.br/eleicoes/2026/pesquisa-eleitoral-2026/)
- [O Hoje — Exata OP no DF](https://ohoje.com/2026/10/02/pesquisa-mostra-celina-leao-com-54-das-intencoes-de-votos-validos-no-df/)
- Wikipédia: páginas "Pesquisas eleitorais para a eleição estadual de 2026 em/no/na {estado}" (demais pesquisas). A página do DF não existe com esse nome.

## Pendências conhecidas nos dados

| UF | Pendência |
|---|---|
| AM | A Quaest final, como foi publicada, não mostra Roberto Cidade (que tinha ~24% em outras pesquisas). |
| MG | Partido de Mateus Simões não confirmado (`"—"`). |
| MS | Partido de Catan não confirmado (`"—"`). |
| SE | Partido de Ricardo Marques não confirmado (`"—"`). |
| AC, CE, RJ, RS | A AtlasIntel divulgou rodadas em outubro, mas os números não foram obtidos; foram usadas as rodadas anteriores disponíveis. |
| Todos | Resumos escritos com base em conhecimento até meados de 2026. Revisar sobretudo quem assumiu governos em 2026. |
| DF | O resumo de governador diz que Ibaneis Rocha saiu para disputar o Senado, mas ele não aparece nas pesquisas de Senado do DF (Quaest 02–03/10: Michelle, Leila, Bia Kicis e Erika somam 99%). Confirmar. |
| Senado | Resumos genéricos a completar: Chicão (PA), Bruno Bolsonaro Scheid (RO), Coronel Hélio e Samanda de Lula (RN), Alliny Serrão (AP), Iran Barbosa (SE). |

# Senado (`senado.js`)

Mesmo formato de estado, com estas diferenças:

- Campo extra `vagas` (2 em 2026: cada estado elege 2 senadores e cada eleitor dá 2 votos).
- Os percentuais somam os dois votos. A **margem que importa é a da 2ª vaga: 2º colocado − 3º colocado**.
- Tipos de número:
  - `"V"`: votos válidos, os dois votos somados e reduzidos a 100%.
  - `"T"`: votos totais, os dois votos somados e reduzidos a 100% (brancos, nulos e indecisos na base).
  - `"C"`: % de eleitores que citam o candidato em qualquer dos dois votos. A soma passa de 100% (até ~200%).
- As fontes e observações de coleta estão no cabeçalho do próprio `senado.js`. Números de institutos secundários vindos da Wikipédia devem ser conferidos antes de publicar.

# Comum aos dois

## Malha geográfica

`docs/data/brasil-estados.geojson` vem do [click_that_hood](https://github.com/codeforamerica/click_that_hood), com estas transformações:

- Propriedades reduzidas a `sigla` e `nome`.
- Coordenadas arredondadas para 2 casas decimais (~1 km) e pontos repetidos removidos.
- Anéis com menos de 4 pontos removidos (causavam erro no D3).
- Orientação dos anéis ajustada para o padrão do D3 (anel externo no sentido horário). **Se trocar a malha, refaça esse ajuste**, ou o D3 desenha o "globo inteiro" em vez do estado.

## Como atualizar uma pesquisa

1. Edite o estado em `dados.js` (ou `senado.js`): insira a nova pesquisa **no início** de `pesquisas` e remova a mais antiga, para manter 3.
2. Se surgir um candidato novo, adicione-o em `candidatos` com partido e resumo.
3. Atualize `window.ATUALIZADO_EM` (ou `window.ATUALIZADO_EM_SENADO`).
4. Teste localmente e registre a mudança no [CHANGELOG.md](../CHANGELOG.md).
