// Pesquisas de intenção de voto para governador — eleição 2026, 1º turno (04/10/2026).
// tipo "V" = votos válidos; "T" = votos totais (estimulada).
// Fontes: O Povo (resultados Quaest/Datafolha 02–03/10), Gazeta do Povo, O Hoje
// e páginas "Pesquisas eleitorais para a eleição estadual de 2026" da Wikipédia.
window.ATUALIZADO_EM = "04/10/2026";

window.ESTADOS = [
  // ---------------- NORTE ----------------
  {
    uf: "AC", nome: "Acre", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Mailza Assis", 41], ["Alan Rick", 37], ["Tião Bocalom", 16], ["Thor Dantas", 5]] },
      { inst: "Veritá", campo: "26/09–01/10", tipo: "T", res: [["Mailza Assis", 34.6], ["Alan Rick", 32.9], ["Tião Bocalom", 12.3]] },
      { inst: "Delta", campo: "23–29/09", tipo: "T", res: [["Mailza Assis", 40.6], ["Alan Rick", 30.5], ["Tião Bocalom", 12.4]] }
    ],
    candidatos: [
      { nome: "Mailza Assis", partido: "PP", resumo: "Era vice e assumiu o governo do Acre em 2026, quando Gladson Cameli deixou o cargo para disputar o Senado. Concorre à reeleição no cargo." },
      { nome: "Alan Rick", partido: "Republicanos", resumo: "Senador pelo Acre desde 2023, antes deputado federal. Jornalista, ligado à bancada evangélica e de perfil conservador." },
      { nome: "Tião Bocalom", partido: "PSDB", resumo: "Ex-prefeito de Rio Branco: foi reeleito em 2024 e deixou o cargo em 2026 para concorrer. Antes, foi prefeito de Acrelândia e disputou o governo outras vezes." },
      { nome: "Thor Dantas", partido: "PSB", resumo: "Candidato do PSB, representa o campo de centro-esquerda na disputa." }
    ]
  },
  {
    uf: "AP", nome: "Amapá", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Dr. Furlan", 53], ["Clécio Luís", 47]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Dr. Furlan", 59], ["Clécio Luís", 38]] },
      { inst: "Paraná Pesquisas", campo: "25–27/09", tipo: "T", res: [["Dr. Furlan", 59.2], ["Clécio Luís", 39.7]] }
    ],
    candidatos: [
      { nome: "Dr. Furlan", partido: "PSD", resumo: "Médico, foi prefeito de Macapá por dois mandatos (reeleito em 2024 com votação expressiva). Deixou a prefeitura para disputar o governo." },
      { nome: "Clécio Luís", partido: "União Brasil", resumo: "Governador do Amapá desde 2023, busca a reeleição. Foi prefeito de Macapá por dois mandatos antes de Furlan." }
    ]
  },
  {
    uf: "AM", nome: "Amazonas", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Omar Aziz", 40], ["Maria do Carmo", 25], ["David Almeida", 11]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Omar Aziz", 36], ["Roberto Cidade", 24], ["Maria do Carmo", 24], ["David Almeida", 9]] },
      { inst: "Pontual", campo: "23–29/09", tipo: "T", res: [["Omar Aziz", 29.5], ["Roberto Cidade", 26.9], ["Maria do Carmo", 18], ["David Almeida", 14.5]] }
    ],
    candidatos: [
      { nome: "Omar Aziz", partido: "PSD", resumo: "Senador e ex-governador do Amazonas (2010–2014). Ganhou projeção nacional ao presidir a CPI da Covid no Senado." },
      { nome: "Maria do Carmo", partido: "PL", resumo: "Professora Maria do Carmo Seffair, empresária da educação. Foi candidata a prefeita de Manaus e é a aposta do bolsonarismo no estado." },
      { nome: "Roberto Cidade", partido: "União Brasil", resumo: "Deputado estadual e presidente da Assembleia Legislativa do Amazonas. Candidato apoiado pelo grupo do governador Wilson Lima." },
      { nome: "David Almeida", partido: "Avante", resumo: "Ex-prefeito de Manaus: foi reeleito em 2024 e deixou o cargo em 2026 para concorrer. Já governou o estado interinamente em 2017." }
    ]
  },
  {
    uf: "PA", nome: "Pará", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Dr. Daniel", 57], ["Hana Ghassan", 40]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "T", res: [["Hana Ghassan", 50.4], ["Dr. Daniel", 44.4]] },
      { inst: "Doxa", campo: "27–30/09", tipo: "T", res: [["Hana Ghassan", 43.9], ["Dr. Daniel", 38.7]] }
    ],
    candidatos: [
      { nome: "Dr. Daniel", partido: "Podemos", resumo: "Daniel Santos, médico e ex-prefeito de Ananindeua, na região metropolitana de Belém, por dois mandatos. Lidera a oposição ao grupo de Helder Barbalho." },
      { nome: "Hana Ghassan", partido: "MDB", resumo: "Era vice e assumiu o governo em 2026, quando Helder Barbalho saiu para disputar o Senado. Foi secretária de Planejamento. É a candidata da continuidade." }
    ]
  },
  {
    uf: "RO", nome: "Rondônia", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Marcos Rogério", 53], ["Adailton Fúria", 24], ["Hildon Chaves", 15], ["Expedito Netto", 7]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Marcos Rogério", 45], ["Adailton Fúria", 32], ["Hildon Chaves", 11], ["Expedito Netto", 9]] },
      { inst: "Veritá", campo: "21–25/09", tipo: "T", res: [["Marcos Rogério", 49.2], ["Adailton Fúria", 19.6], ["Expedito Netto", 15]] }
    ],
    candidatos: [
      { nome: "Marcos Rogério", partido: "PL", resumo: "Senador por Rondônia e aliado de Bolsonaro. Disputou o governo em 2022 e perdeu no 2º turno para Marcos Rocha." },
      { nome: "Adailton Fúria", partido: "PSD", resumo: "Ex-prefeito de Cacoal por dois mandatos, cidade do interior do estado." },
      { nome: "Hildon Chaves", partido: "União Brasil", resumo: "Ex-prefeito de Porto Velho por dois mandatos (2017–2024). Advogado e empresário." },
      { nome: "Expedito Netto", partido: "PT", resumo: "Ex-deputado federal, de família tradicional na política de Rondônia. Candidato do campo governista federal." }
    ]
  },
  {
    uf: "RR", nome: "Roraima", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Arthur Henrique", 64], ["Soldado Sampaio", 34]] },
      { inst: "Eficaz", campo: "14–19/09", tipo: "T", res: [["Arthur Henrique", 63], ["Soldado Sampaio", 22.9]] },
      { inst: "Census", campo: "08–13/09", tipo: "T", res: [["Arthur Henrique", 50.0], ["Soldado Sampaio", 38.1]] }
    ],
    candidatos: [
      { nome: "Arthur Henrique", partido: "PL", resumo: "Ex-prefeito de Boa Vista. Venceu a eleição suplementar de junho de 2026 para o governo e agora tenta um mandato completo." },
      { nome: "Soldado Sampaio", partido: "Republicanos", resumo: "Deputado estadual, policial militar e presidente da Assembleia Legislativa de Roraima." }
    ]
  },
  {
    uf: "TO", nome: "Tocantins", regiao: "Norte",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Professora Dorinha", 46], ["Vicentinho Júnior", 41], ["Laurez Moreira", 11]] },
      { inst: "Paraná Pesquisas", campo: "29/09–01/10", tipo: "T", res: [["Professora Dorinha", 42.3], ["Vicentinho Júnior", 35.9], ["Laurez Moreira", 7.2]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Professora Dorinha", 42], ["Vicentinho Júnior", 36], ["Laurez Moreira", 6]] }
    ],
    candidatos: [
      { nome: "Professora Dorinha", partido: "União Brasil", resumo: "Senadora pelo Tocantins desde 2023, antes deputada federal por vários mandatos. Atua na área de educação." },
      { nome: "Vicentinho Júnior", partido: "PSDB", resumo: "Deputado federal pelo Tocantins, filho do ex-senador Vicentinho Alves." },
      { nome: "Laurez Moreira", partido: "PSD", resumo: "Ex-vice-governador do Tocantins e ex-prefeito de Gurupi." }
    ]
  },

  // ---------------- NORDESTE ----------------
  {
    uf: "AL", nome: "Alagoas", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Renan Filho", 50], ["JHC", 49]] },
      { inst: "Paraná Pesquisas", campo: "26–29/09", tipo: "T", res: [["JHC", 52.4], ["Renan Filho", 46.3]] },
      { inst: "DataTrends", campo: "26–28/09", tipo: "T", res: [["Renan Filho", 46], ["JHC", 45]] }
    ],
    candidatos: [
      { nome: "Renan Filho", partido: "MDB", resumo: "Ex-governador de Alagoas (2015–2022), senador e ministro dos Transportes no governo Lula. Filho do senador Renan Calheiros." },
      { nome: "JHC", partido: "PSDB", resumo: "João Henrique Caldas, ex-prefeito de Maceió: foi reeleito em 2024 com folga e deixou o cargo em 2026 para concorrer. Principal adversário do grupo Calheiros." }
    ]
  },
  {
    uf: "BA", nome: "Bahia", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Jerônimo Rodrigues", 52], ["ACM Neto", 48]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "T", res: [["Jerônimo Rodrigues", 51.5], ["ACM Neto", 47.4]] },
      { inst: "Paraná Pesquisas", campo: "29/09–02/10", tipo: "T", res: [["ACM Neto", 46.4], ["Jerônimo Rodrigues", 44.6]] }
    ],
    candidatos: [
      { nome: "Jerônimo Rodrigues", partido: "PT", resumo: "Governador da Bahia desde 2023, busca a reeleição. Professor e ex-secretário de Educação. O PT governa o estado desde 2007." },
      { nome: "ACM Neto", partido: "União Brasil", resumo: "Ex-prefeito de Salvador (2013–2020), neto de Antônio Carlos Magalhães. Perdeu para Jerônimo no 2º turno de 2022 e agora busca a revanche." }
    ]
  },
  {
    uf: "CE", nome: "Ceará", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Elmano de Freitas", 50], ["Ciro Gomes", 49]] },
      { inst: "AtlasIntel", campo: "23–28/09", tipo: "T", res: [["Elmano de Freitas", 49], ["Ciro Gomes", 47.6]] },
      { inst: "Datafolha", campo: "22–24/09", tipo: "T", res: [["Ciro Gomes", 44], ["Elmano de Freitas", 43]] }
    ],
    candidatos: [
      { nome: "Elmano de Freitas", partido: "PT", resumo: "Governador do Ceará desde 2023, busca a reeleição. Aliado do ex-governador Camilo Santana." },
      { nome: "Ciro Gomes", partido: "PSDB", resumo: "Ex-governador do Ceará (1991–1994), ex-ministro da Fazenda e quatro vezes candidato a presidente. Rompido com o PT, tenta voltar ao governo." }
    ]
  },
  {
    uf: "MA", nome: "Maranhão", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Eduardo Braide", 52], ["Orleans Brandão", 35], ["Felipe Camarão", 10]] },
      { inst: "Ranking", campo: "17–21/09", tipo: "T", res: [["Eduardo Braide", 40.8], ["Orleans Brandão", 37.2], ["Felipe Camarão", 8.7]] },
      { inst: "Viva Voz", campo: "15–20/09", tipo: "T", res: [["Eduardo Braide", 49.3], ["Orleans Brandão", 26.1], ["Felipe Camarão", 6.4]] }
    ],
    candidatos: [
      { nome: "Eduardo Braide", partido: "PSD", resumo: "Ex-prefeito de São Luís: foi reeleito em 2024 no 1º turno e deixou o cargo em 2026 para concorrer. Advogado e ex-deputado federal." },
      { nome: "Orleans Brandão", partido: "MDB", resumo: "Ex-secretário estadual e sobrinho do governador Carlos Brandão, de quem é o candidato." },
      { nome: "Felipe Camarão", partido: "PT", resumo: "Vice-governador do Maranhão e ex-secretário de Educação. Aliado de Flávio Dino." }
    ]
  },
  {
    uf: "PB", nome: "Paraíba", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Lucas Ribeiro", 61], ["Efraim Filho", 23], ["Cícero Lucena", 16]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Lucas Ribeiro", 45], ["Efraim Filho", 24], ["Cícero Lucena", 18]] },
      { inst: "TDL", campo: "23–27/09", tipo: "T", res: [["Lucas Ribeiro", 48], ["Efraim Filho", 15], ["Cícero Lucena", 14]] }
    ],
    candidatos: [
      { nome: "Lucas Ribeiro", partido: "PP", resumo: "Era vice e assumiu o governo da Paraíba em 2026, quando João Azevêdo saiu para disputar o Senado. É o candidato da continuidade." },
      { nome: "Efraim Filho", partido: "PL", resumo: "Senador pela Paraíba desde 2023, antes deputado federal por vários mandatos. Representa a oposição de direita." },
      { nome: "Cícero Lucena", partido: "MDB", resumo: "Ex-prefeito de João Pessoa: foi reeleito em 2024 e deixou o cargo em 2026 para concorrer. Já foi governador interino, senador e prefeito da capital em outros mandatos." }
    ]
  },
  {
    uf: "PE", nome: "Pernambuco", regiao: "Nordeste",
    pesquisas: [
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Raquel Lyra", 49], ["João Campos", 48]] },
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Raquel Lyra", 52], ["João Campos", 47]] },
      { inst: "DataTrends", campo: "28–30/09", tipo: "T", res: [["Raquel Lyra", 47], ["João Campos", 41]] }
    ],
    candidatos: [
      { nome: "Raquel Lyra", partido: "PSD", resumo: "Governadora de Pernambuco desde 2023, busca a reeleição. Ex-prefeita de Caruaru. Trocou o PSDB pelo PSD." },
      { nome: "João Campos", partido: "PSB", resumo: "Ex-prefeito do Recife: foi reeleito em 2024 com cerca de 78% dos votos e deixou o cargo em 2026 para concorrer. Filho de Eduardo Campos e presidente nacional do PSB." }
    ]
  },
  {
    uf: "PI", nome: "Piauí", regiao: "Nordeste",
    pesquisas: [
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Rafael Fonteles", 67], ["Joel Rodrigues", 28]] },
      { inst: "AtlasIntel", campo: "23–28/09", tipo: "T", res: [["Rafael Fonteles", 64.5], ["Joel Rodrigues", 24.4]] },
      { inst: "Datamax", campo: "14–19/09", tipo: "T", res: [["Rafael Fonteles", 73], ["Joel Rodrigues", 21.8]] }
    ],
    candidatos: [
      { nome: "Rafael Fonteles", partido: "PT", resumo: "Governador do Piauí desde 2023, busca a reeleição. Economista e ex-secretário da Fazenda nos governos de Wellington Dias." },
      { nome: "Joel Rodrigues", partido: "PP", resumo: "Ex-prefeito de Floriano, no sul do estado. Principal nome da oposição." }
    ]
  },
  {
    uf: "RN", nome: "Rio Grande do Norte", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Allyson Bezerra", 37], ["Cadu de Lula", 32], ["Álvaro Dias", 29]] },
      { inst: "Exatus", campo: "28–30/09", tipo: "T", res: [["Allyson Bezerra", 43.3], ["Cadu de Lula", 24.4], ["Álvaro Dias", 22.2]] },
      { inst: "AtlasIntel", campo: "23–28/09", tipo: "T", res: [["Cadu de Lula", 37.1], ["Álvaro Dias", 27.3], ["Allyson Bezerra", 27.1]] }
    ],
    candidatos: [
      { nome: "Allyson Bezerra", partido: "União Brasil", resumo: "Ex-prefeito de Mossoró, a segunda maior cidade do estado, reeleito em 2024 com ampla votação." },
      { nome: "Cadu de Lula", partido: "PT", resumo: "Carlos Eduardo Xavier, ex-secretário da Fazenda no governo Fátima Bezerra. Candidato do PT, usa o nome de urna associado ao presidente." },
      { nome: "Álvaro Dias", partido: "PL", resumo: "Ex-prefeito de Natal por dois mandatos (2018–2024). Médico. Representa a direita bolsonarista no estado." }
    ]
  },
  {
    uf: "SE", nome: "Sergipe", regiao: "Nordeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Fábio Mitidieri", 55], ["Valmir de Francisquinho", 44]] },
      { inst: "IFP", campo: "24–26/09", tipo: "T", res: [["Fábio Mitidieri", 42.2], ["Valmir de Francisquinho", 26.7], ["Ricardo Marques", 4.8]] },
      { inst: "Real Time Big Data", campo: "17–21/09", tipo: "T", res: [["Fábio Mitidieri", 43], ["Valmir de Francisquinho", 38], ["Ricardo Marques", 10]] }
    ],
    candidatos: [
      { nome: "Fábio Mitidieri", partido: "PSD", resumo: "Governador de Sergipe desde 2023, busca a reeleição. Ex-deputado federal." },
      { nome: "Valmir de Francisquinho", partido: "Republicanos", resumo: "Ex-prefeito de Itabaiana. Em 2022 liderava as pesquisas, mas teve a candidatura barrada pela Justiça Eleitoral." },
      { nome: "Ricardo Marques", partido: "—", resumo: "Ex-vereador de Aracaju. Candidato com desempenho de um dígito nas pesquisas." }
    ]
  },

  // ---------------- CENTRO-OESTE ----------------
  {
    uf: "DF", nome: "Distrito Federal", regiao: "Centro-Oeste",
    pesquisas: [
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Celina Leão", 55], ["Leandro Grass", 27], ["Paula Belmonte", 10]] },
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Celina Leão", 53], ["Leandro Grass", 32], ["Paula Belmonte", 10]] },
      { inst: "Exata OP", campo: "30/09–02/10", tipo: "V", res: [["Celina Leão", 54], ["Leandro Grass", 30]] }
    ],
    candidatos: [
      { nome: "Celina Leão", partido: "PP", resumo: "Era vice e assumiu o governo do DF em 2026, quando Ibaneis Rocha saiu para disputar o Senado. Ex-deputada federal e distrital." },
      { nome: "Leandro Grass", partido: "PT", resumo: "Ex-deputado distrital e ex-presidente do Iphan. Foi candidato ao governo em 2022 e representa o campo de esquerda." },
      { nome: "Paula Belmonte", partido: "PSDB", resumo: "Ex-deputada federal pelo DF e deputada distrital. Atua em pautas de fiscalização e da infância." }
    ]
  },
  {
    uf: "GO", nome: "Goiás", regiao: "Centro-Oeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Daniel Vilela", 57], ["Wilder Morais", 20], ["Marconi Perillo", 18]] },
      { inst: "Paraná Pesquisas", campo: "25–27/09", tipo: "T", res: [["Daniel Vilela", 45.6], ["Wilder Morais", 18.5], ["Marconi Perillo", 18.4], ["Luis Cesar Bueno", 6.1]] },
      { inst: "Goiás Pesquisas", campo: "24–25/09", tipo: "T", res: [["Daniel Vilela", 44.6], ["Wilder Morais", 18.2], ["Marconi Perillo", 13.8], ["Luis Cesar Bueno", 5.7]] }
    ],
    candidatos: [
      { nome: "Daniel Vilela", partido: "MDB", resumo: "Era vice e assumiu o governo de Goiás em 2026, quando Ronaldo Caiado saiu para disputar a Presidência. Filho do ex-governador Maguito Vilela." },
      { nome: "Wilder Morais", partido: "PL", resumo: "Senador por Goiás e empresário. É o candidato do bolsonarismo no estado." },
      { nome: "Marconi Perillo", partido: "PSDB", resumo: "Governou Goiás por quatro mandatos (1999–2006 e 2011–2018). Presidente nacional do PSDB, tenta voltar ao cargo." },
      { nome: "Luis Cesar Bueno", partido: "PT", resumo: "Deputado estadual por vários mandatos. Candidato do PT em Goiás." }
    ]
  },
  {
    uf: "MT", nome: "Mato Grosso", regiao: "Centro-Oeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Otaviano Pivetta", 54], ["Wellington Fagundes", 28], ["Doutora Natasha", 13]] },
      { inst: "MT Dados", campo: "25–30/09", tipo: "T", res: [["Otaviano Pivetta", 42], ["Wellington Fagundes", 23], ["Doutora Natasha", 14]] },
      { inst: "Paraná Pesquisas", campo: "27–29/09", tipo: "T", res: [["Otaviano Pivetta", 46.4], ["Wellington Fagundes", 27.1], ["Doutora Natasha", 15.5]] }
    ],
    candidatos: [
      { nome: "Otaviano Pivetta", partido: "Republicanos", resumo: "Era vice e assumiu o governo de Mato Grosso em 2026, com a saída de Mauro Mendes. Empresário do agronegócio e ex-prefeito de Lucas do Rio Verde." },
      { nome: "Wellington Fagundes", partido: "PL", resumo: "Senador por Mato Grosso desde 2015, antes deputado federal por vários mandatos." },
      { nome: "Doutora Natasha", partido: "PSD", resumo: "Natasha Slhessarenko, médica pediatra conhecida em Cuiabá. Estreante em disputas majoritárias de destaque." }
    ]
  },
  {
    uf: "MS", nome: "Mato Grosso do Sul", regiao: "Centro-Oeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Eduardo Riedel", 67], ["Fábio Trad", 23]] },
      { inst: "Ranking Brasil", campo: "21–25/09", tipo: "T", res: [["Eduardo Riedel", 50], ["Fábio Trad", 18], ["Catan", 3]] },
      { inst: "Quaest", campo: "21–24/09", tipo: "T", res: [["Eduardo Riedel", 51], ["Fábio Trad", 12], ["Catan", 3]] }
    ],
    candidatos: [
      { nome: "Eduardo Riedel", partido: "PP", resumo: "Governador de Mato Grosso do Sul desde 2023, busca a reeleição. Ex-secretário de Infraestrutura e ligado ao agronegócio." },
      { nome: "Fábio Trad", partido: "PT", resumo: "Advogado e ex-deputado federal por Mato Grosso do Sul. De família tradicional na política de Campo Grande." },
      { nome: "Catan", partido: "—", resumo: "João Henrique Catan, deputado estadual de perfil conservador. Aparece com um dígito nas pesquisas." }
    ]
  },

  // ---------------- SUDESTE ----------------
  {
    uf: "ES", nome: "Espírito Santo", regiao: "Sudeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Lorenzo Pazolini", 45], ["Ricardo Ferraço", 41], ["Helder Salomão", 12]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Ricardo Ferraço", 45], ["Lorenzo Pazolini", 37], ["Helder Salomão", 14]] },
      { inst: "Perfil/ES Hoje", campo: "21–24/09", tipo: "T", res: [["Lorenzo Pazolini", 36.9], ["Ricardo Ferraço", 33.9], ["Helder Salomão", 8.1]] }
    ],
    candidatos: [
      { nome: "Lorenzo Pazolini", partido: "Republicanos", resumo: "Ex-prefeito de Vitória (reeleito em 2024 no 1º turno). Delegado da Polícia Civil." },
      { nome: "Ricardo Ferraço", partido: "MDB", resumo: "Era vice e assumiu o governo do ES em 2026, quando Renato Casagrande saiu para disputar o Senado. Ex-senador." },
      { nome: "Helder Salomão", partido: "PT", resumo: "Deputado federal e ex-prefeito de Cariacica. Candidato do PT no estado." }
    ]
  },
  {
    uf: "MG", nome: "Minas Gerais", regiao: "Sudeste",
    pesquisas: [
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Cleitinho", 53], ["Patrus Ananias", 21], ["Alexandre Kalil", 9]] },
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Cleitinho", 54], ["Patrus Ananias", 23], ["Alexandre Kalil", 10]] },
      { inst: "Real Time Big Data", campo: "28/09–02/10", tipo: "T", res: [["Cleitinho", 45], ["Patrus Ananias", 22], ["Alexandre Kalil", 6], ["Mateus Simões", 6]] }
    ],
    candidatos: [
      { nome: "Cleitinho", partido: "Republicanos", resumo: "Cleitinho Azevedo, senador por Minas desde 2023, eleito com discurso antipolítico e forte presença nas redes sociais." },
      { nome: "Patrus Ananias", partido: "PT", resumo: "Ex-prefeito de Belo Horizonte e ex-ministro do Desenvolvimento Social, responsável pelo Bolsa Família no governo Lula. Deputado federal." },
      { nome: "Alexandre Kalil", partido: "PDT", resumo: "Ex-prefeito de Belo Horizonte (2017–2022) e ex-presidente do Atlético-MG. Foi candidato ao governo em 2022." },
      { nome: "Mateus Simões", partido: "—", resumo: "Era vice e assumiu o governo de Minas em 2026, com a saída de Romeu Zema para disputar a Presidência." }
    ]
  },
  {
    uf: "RJ", nome: "Rio de Janeiro", regiao: "Sudeste",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Eduardo Paes", 49], ["Douglas Ruas", 40], ["Anthony Garotinho", 6]] },
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Eduardo Paes", 46], ["Douglas Ruas", 38], ["Anthony Garotinho", 7]] },
      { inst: "Paraná Pesquisas", campo: "29/09–01/10", tipo: "T", res: [["Eduardo Paes", 47.9], ["Douglas Ruas", 34.4], ["Anthony Garotinho", 9.4]] }
    ],
    candidatos: [
      { nome: "Eduardo Paes", partido: "PSD", resumo: "Prefeito do Rio por quatro mandatos, o último iniciado em 2025. Deixou o cargo para disputar o governo, que já tentou em 2018." },
      { nome: "Douglas Ruas", partido: "PL", resumo: "Deputado estadual de São Gonçalo, filho do ex-prefeito Capitão Nelson. É o candidato do bolsonarismo no estado." },
      { nome: "Anthony Garotinho", partido: "Republicanos", resumo: "Ex-governador do RJ (1999–2002) e candidato a presidente em 2002. Ex-deputado federal." }
    ]
  },
  {
    uf: "SP", nome: "São Paulo", regiao: "Sudeste",
    pesquisas: [
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Tarcísio de Freitas", 60], ["Fernando Haddad", 35]] },
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Tarcísio de Freitas", 60], ["Fernando Haddad", 36]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "T", res: [["Tarcísio de Freitas", 55.6], ["Fernando Haddad", 40.3]] }
    ],
    candidatos: [
      { nome: "Tarcísio de Freitas", partido: "Republicanos", resumo: "Governador de São Paulo desde 2023, busca a reeleição. Foi ministro da Infraestrutura no governo Bolsonaro. Engenheiro e militar da reserva." },
      { nome: "Fernando Haddad", partido: "PT", resumo: "Ministro da Fazenda no governo Lula até 2026. Ex-prefeito de São Paulo, candidato a presidente em 2018 e ao governo de SP em 2022, quando perdeu para Tarcísio." }
    ]
  },

  // ---------------- SUL ----------------
  {
    uf: "PR", nome: "Paraná", regiao: "Sul",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Sergio Moro", 43], ["Sandro Alex", 29], ["Requião Filho", 27]] },
      { inst: "IRG", campo: "29/09–01/10", tipo: "T", res: [["Sergio Moro", 40.6], ["Sandro Alex", 28.4], ["Requião Filho", 23]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Sergio Moro", 37], ["Sandro Alex", 29], ["Requião Filho", 24]] }
    ],
    candidatos: [
      { nome: "Sergio Moro", partido: "PL", resumo: "Senador pelo Paraná desde 2023. Ex-juiz da Lava Jato e ex-ministro da Justiça de Bolsonaro." },
      { nome: "Sandro Alex", partido: "PSD", resumo: "Ex-secretário de Infraestrutura e ex-deputado federal. É o candidato do governador Ratinho Junior." },
      { nome: "Requião Filho", partido: "PDT", resumo: "Deputado estadual, filho do ex-governador Roberto Requião. Representa o campo de centro-esquerda." }
    ]
  },
  {
    uf: "RS", nome: "Rio Grande do Sul", regiao: "Sul",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Luciano Zucco", 52], ["Juliana Brizola", 35], ["Gabriel Souza", 12]] },
      { inst: "Real Time Big Data", campo: "24–28/09", tipo: "T", res: [["Luciano Zucco", 40], ["Juliana Brizola", 35], ["Gabriel Souza", 19]] },
      { inst: "Neokemp", campo: "23–24/09", tipo: "T", res: [["Luciano Zucco", 44.9], ["Juliana Brizola", 28.8], ["Gabriel Souza", 15.7]] }
    ],
    candidatos: [
      { nome: "Luciano Zucco", partido: "PL", resumo: "Deputado federal, militar da reserva do Exército, e foi líder da oposição na Câmara. Candidato do bolsonarismo." },
      { nome: "Juliana Brizola", partido: "PDT", resumo: "Ex-deputada estadual e neta de Leonel Brizola. Disputou a prefeitura de Porto Alegre em 2024 e reúne apoio da centro-esquerda." },
      { nome: "Gabriel Souza", partido: "MDB", resumo: "Vice-governador do RS no governo de Eduardo Leite e candidato da continuidade. Ex-presidente da Assembleia Legislativa." }
    ]
  },
  {
    uf: "SC", nome: "Santa Catarina", regiao: "Sul",
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Jorginho Mello", 71], ["João Rodrigues", 14], ["Gelson Merísio", 12]] },
      { inst: "Neokemp", campo: "30/09", tipo: "T", res: [["Jorginho Mello", 58.2], ["Gelson Merísio", 18.3], ["João Rodrigues", 16.7]] },
      { inst: "Paraná Pesquisas", campo: "20–22/09", tipo: "T", res: [["Jorginho Mello", 58.6], ["João Rodrigues", 16.5], ["Gelson Merísio", 11.3]] }
    ],
    candidatos: [
      { nome: "Jorginho Mello", partido: "PL", resumo: "Governador de Santa Catarina desde 2023, busca a reeleição. Ex-senador e aliado de Bolsonaro." },
      { nome: "João Rodrigues", partido: "PSD", resumo: "Ex-prefeito de Chapecó por dois mandatos e ex-deputado federal." },
      { nome: "Gelson Merísio", partido: "PSB", resumo: "Ex-deputado estadual e ex-presidente da Assembleia Legislativa de SC. Foi candidato ao governo em 2018." }
    ]
  }
];
