# Apuração (`apuracao.html` + `scripts/apuracao.py`)

Réplica de `index.html` preparada para a apuração do 1º turno (04/10/2026), criada a pedido do usuário. **Não substitui** `index.html`: as duas páginas convivem. Mudanças de layout feitas em `index.html` depois de 04/10 não são copiadas automaticamente para cá.

## Arquitetura

```
TSE (JSON de divulgação)  →  scripts/apuracao.py (neste computador, a cada 60 s)
                          →  docs/data/apuracao/<cargo>.json  →  git push (no máximo a cada 120 s)
                          →  GitHub Actions publica docs/ no Pages (~1 min)
                          →  apuracao.html relê o JSON a cada 60 s
```

Atraso esperado para o leitor: cerca de 2 a 4 minutos depois do TSE.

### Publicação pelo GitHub Actions

O workflow [.github/workflows/pages.yml](../.github/workflows/pages.yml) publica `docs/` a cada push em `main`. Para ele valer, em **Settings → Pages → Build and deployment → Source**, escolha **GitHub Actions** (antes: "Deploy from a branch", `main` `/docs`). O motivo é o limite de cerca de 10 publicações por hora do modo "Deploy from a branch", que não vale para o Actions.

Para voltar ao modo antigo, basta trocar a opção de novo; o workflow pode ficar no repositório.

## Página

- **Faixa "Apuração oficial"** no topo: média do % de urnas apuradas nos 27 estados (do cargo selecionado), estados com apuração, estados concluídos, hora do dado do TSE e barra de progresso. Antes dos dados: "Aguardando o início da apuração". Com dados simulados, mostra o aviso "Dados simulados, não oficiais".
- **% apurado no mapa:** abaixo de cada sigla (arredondado para baixo; `<1%` entre 0 e 1; `100%` só quando completo).
- **Apuração como pesquisa principal:** com `pct > 0`, a apuração vira a "pesquisa principal" (`apuracao(e)` dentro de `principal(e)`). Cor, líder, margem, pop-up e tabela passam a usá-la, com selo "TSE"/"oficial". Com 0%, o estado segue com a pesquisa. As pesquisas continuam no pop-up para comparação.
- Lê `data/apuracao/governador.json` e `data/apuracao/senador.json` com `?t=<timestamp>` (evita o cache do Pages) e repinta só se algo mudou.

## Formato de `docs/data/apuracao/<cargo>.json`

Um arquivo por cargo: `presidente`, `governador`, `senador`, `deputado-federal`, `deputado-estadual`.

```json
{
  "cargo": "governador",
  "atualizado": "19:42",
  "ufs": {
    "SP": { "pct": 45.31, "hora": "19:41:30", "res": [["Nome A", 52.1], ["Nome B", 30.4], ["NOME C", 0.8, "PCO"]], "situacao": "2turno" }
  }
}
```

- `pct`: % de seções/urnas totalizadas no local (0–100). Presidente usa também `BR` (Brasil) e `ZZ` (exterior).
- `hora`: hora em que o TSE gerou o dado daquele local. `atualizado` = a mais recente (HH:MM).
- `res`: `[nome, % de votos válidos, partido?]`, do mais para o menos votado. Para governador e Senado, o script troca o nome de urna pelo nome de `candidatos[]` (`dados.js`/`senado.js`); o partido (3º elemento) só é preciso para quem não está na lista.
- `situacao` (opcional): `"eleito"` ou `"2turno"`.
- `simulacao: true` só aparece em dados gerados por `--simular`.
- Local ausente = 0% apurado.

## Script `scripts/apuracao.py`

Só biblioteca padrão do Python. Comandos:

| Comando | O que faz |
|---|---|
| `python scripts/apuracao.py --simular` | Dados falsos que avançam a cada minuto, para testar terminal e página localmente. **Nunca publica.** |
| `python scripts/apuracao.py` | Coleta real, grava os arquivos, não publica. |
| `python scripts/apuracao.py --publicar` | Coleta real e publica (commit + push só de `docs/data/apuracao/`). |
| `--uma-vez` | Roda um ciclo e sai. |
| `--cargos governador,senador` | Limita os cargos. |
| `--limpar` | Zera os arquivos do site. Rodar antes de commitar se tiver usado `--simular`. |

O terminal mostra, a cada ciclo, a hora atual e, por cargo: novos / iguais / pendentes / erros, andamento (média ou BR), concluídos e a hora do último dado do TSE. Entre ciclos, um relógio conta até o próximo. Avisos em amarelo: nome sem correspondência na lista do site, % apurado que diminuiu, erro de rede ou arquivo inválido.

Comportamento:
- Requisição condicional (`ETag` / `If-Modified-Since`): só baixa de novo se o TSE mudou o arquivo. Local que ainda não existe (403/404) fica como "pendente".
- A cópia bruta do TSE fica em `apuracao-bruto/` (ignorada pelo git).
- Ao reiniciar, parte dos arquivos já gravados, para não apagar o site se o TSE falhar.
- O commit inclui só `docs/data/apuracao/`, sem mexer no que outras sessões estiverem editando. Se o push falhar porque o remoto andou, faz `pull --rebase --autostash` e tenta de novo.

### A fazer quando a divulgação abrir (17h)

1. Preencher `URLS` no topo do script com os endereços de 2026 (`{uf}` ou `{UF}`).
2. Escrever `converter(cargo, uf, bruto)` conforme o formato real do TSE.
3. Testar com `--uma-vez`, conferir os avisos de nomes (corrigir em `APELIDOS`) e então rodar com `--publicar`.
4. Deputados: decidir o que a página vai mostrar (eleitos, quociente); o formato atual já guarda todos os candidatos.
