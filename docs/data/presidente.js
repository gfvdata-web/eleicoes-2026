// Pesquisas de intenção de voto para presidente — eleição 2026, 1º turno (04/10/2026).
// Usadas só na aba "Comparativo presidente" de index.html (pesquisa nacional × resultado oficial do Brasil).
// tipo "V" = votos válidos; tipo "T" = votos totais (estimulada).
// Só pesquisas nacionais (uf "BR"); a aba não tem mapa.
// Os nomes são casados com os do TSE ignorando acentos e maiúsculas ("Augusto Cury" = "ESCRITOR AUGUSTO CURY").
//
// Fonte: Wikipédia "Opinion polling for the 2026 Brazilian presidential election" (votos totais).
window.ATUALIZADO_EM_PRESIDENTE = "04/10/2026";

window.PRESIDENTE = [
  {
    uf: "BR", nome: "Brasil",
    pesquisas: [
      { inst: "Datafolha", campo: "03/10", tipo: "T", res: [["Lula", 42], ["Flávio Bolsonaro", 40], ["Ronaldo Caiado", 4], ["Renan Santos", 3], ["Augusto Cury", 3], ["Romeu Zema", 0]] },
      { inst: "Quaest", campo: "02–03/10", tipo: "T", res: [["Lula", 40], ["Flávio Bolsonaro", 38], ["Ronaldo Caiado", 3], ["Renan Santos", 3], ["Augusto Cury", 3], ["Romeu Zema", 0]] },
      { inst: "Futura", campo: "02–03/10", tipo: "T", res: [["Flávio Bolsonaro", 42.5], ["Lula", 40.5], ["Augusto Cury", 3.9], ["Ronaldo Caiado", 3.7], ["Renan Santos", 2.6], ["Romeu Zema", 0.8]] },
      { inst: "Palver", campo: "30/09–03/10", tipo: "T", res: [["Flávio Bolsonaro", 47], ["Lula", 43], ["Renan Santos", 7], ["Ronaldo Caiado", 1], ["Augusto Cury", 1], ["Romeu Zema", 0]] },
      { inst: "PoderData", campo: "30/09–02/10", tipo: "T", res: [["Lula", 42], ["Flávio Bolsonaro", 41], ["Renan Santos", 3], ["Augusto Cury", 3], ["Ronaldo Caiado", 2], ["Romeu Zema", 1]] },
      { inst: "MDA", campo: "29/09–02/10", tipo: "T", res: [["Lula", 43.1], ["Flávio Bolsonaro", 38], ["Augusto Cury", 3.2], ["Ronaldo Caiado", 3], ["Renan Santos", 1.5], ["Romeu Zema", 0.8]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "T", res: [["Lula", 46.7], ["Flávio Bolsonaro", 43.8], ["Renan Santos", 4.6], ["Augusto Cury", 2.1], ["Ronaldo Caiado", 1.4], ["Romeu Zema", 0.3]] },
      { inst: "Vox Brasil", campo: "29/09–01/10", tipo: "T", res: [["Flávio Bolsonaro", 41.2], ["Lula", 40.4], ["Ronaldo Caiado", 3.3], ["Renan Santos", 2.2], ["Romeu Zema", 1.3], ["Augusto Cury", 1.2]] }
    ]
  }
];

// Nomes de pesquisa que não batem com o nome de urna do TSE nem por aproximação: "UF|nome da pesquisa" → nome no TSE
window.APELIDOS_TSE = {
  "AP|João Capiberibe": "CAPI",
  "SE|Alessandro Vieira": "DELEGADO ALESSANDRO"
};
