// Pesquisas de intenção de voto para o Senado — eleição 2026, 1º turno (04/10/2026).
// Em 2026 cada estado elege 2 senadores e cada eleitor dá 2 votos.
// Por isso a disputa relevante é pela 2ª vaga: margem = 2º colocado − 3º colocado.
//
// tipo "V" = votos válidos, os dois votos somados e reduzidos a 100% (sem brancos, nulos e indecisos).
// tipo "T" = votos totais, os dois votos somados e reduzidos a 100% (brancos, nulos e indecisos na base).
// tipo "C" = % de eleitores que citam o candidato em qualquer dos dois votos (a soma passa de 100%, até ~200%).
//
// Fontes: Gazeta do Povo (Quaest, Datafolha, AtlasIntel, Neokemp, 02–03/10), CartaCapital (Quaest 25–28/09),
// DGABC / CNN Brasil (SP e DF), Brasil de Fato (Datafolha DF) e páginas
// "Pesquisas eleitorais para a eleição estadual de 2026" da Wikipédia (demais institutos).
// Os números de institutos secundários vindos da Wikipédia devem ser conferidos antes da publicação.
window.ATUALIZADO_EM_SENADO = "04/10/2026";

window.SENADO = [
  // ---------------- NORTE ----------------
  {
    uf: "AC", nome: "Acre", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Gladson Cameli", 24], ["Márcio Bittar", 22], ["Mara Rocha", 19], ["Jorge Viana", 16], ["Sérgio Petecão", 9], ["Eduardo Velloso", 7], ["Dr. Júnior Feitosa", 2], ["Inácio Moreira", 1]] },
      { inst: "Real Time Big Data", campo: "19/09", tipo: "T", res: [["Gladson Cameli", 24], ["Márcio Bittar", 21], ["Jorge Viana", 15], ["Mara Rocha", 15], ["Eduardo Velloso", 6], ["Sérgio Petecão", 5]] }
    ],
    candidatos: [
      { nome: "Gladson Cameli", partido: "PP", resumo: "Governador do Acre de 2019 a 2026, deixou o cargo para disputar o Senado. Já foi senador e deputado federal." },
      { nome: "Márcio Bittar", partido: "PL", resumo: "Senador desde 2019, busca a reeleição. Foi relator do Orçamento e é aliado de Bolsonaro." },
      { nome: "Mara Rocha", partido: "Republicanos", resumo: "Ex-deputada federal e candidata ao governo do Acre em 2022." },
      { nome: "Jorge Viana", partido: "PT", resumo: "Ex-governador do Acre (1999–2006) e ex-senador. Presidiu a ApexBrasil no governo Lula." },
      { nome: "Sérgio Petecão", partido: "PSD", resumo: "Senador desde 2011, busca o terceiro mandato. Disputou o governo em 2022." },
      { nome: "Eduardo Velloso", partido: "Solidariedade", resumo: "Deputado federal pelo Acre." }
    ]
  },
  {
    uf: "AP", nome: "Amapá", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Rayssa Furlan", 30], ["Randolfe Rodrigues", 21], ["Lucas Barreto", 21], ["Acácio Favacho", 20], ["Alliny Serrão", 8]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Rayssa Furlan", 30], ["Randolfe Rodrigues", 20], ["Lucas Barreto", 20], ["Alliny Serrão", 13], ["Acácio Favacho", 11], ["João Capiberibe", 1]] },
      { inst: "Paraná Pesquisas", campo: "25–27/09", tipo: "C", res: [["Rayssa Furlan", 54], ["Randolfe Rodrigues", 36.7], ["Lucas Barreto", 36.1], ["Acácio Favacho", 21.4], ["Alliny Serrão", 20], ["João Capiberibe", 6.1]] }
    ],
    candidatos: [
      { nome: "Rayssa Furlan", partido: "Podemos", resumo: "Esposa do ex-prefeito de Macapá Dr. Furlan, que disputa o governo. Pode ser a primeira mulher eleita senadora pelo Amapá." },
      { nome: "Randolfe Rodrigues", partido: "PT", resumo: "Senador desde 2011, busca o terceiro mandato. Foi líder do governo Lula no Congresso." },
      { nome: "Lucas Barreto", partido: "PSD", resumo: "Senador desde 2019, busca a reeleição." },
      { nome: "Acácio Favacho", partido: "MDB", resumo: "Deputado federal pelo Amapá." },
      { nome: "Alliny Serrão", partido: "União Brasil", resumo: "Candidata do União Brasil." }
    ]
  },
  {
    uf: "AM", nome: "Amazonas", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "T", res: [["Eduardo Braga", 27], ["Capitão Alberto Neto", 18], ["Plínio Valério", 16], ["Wilson Lima", 12], ["Ismael Munduruku", 1], ["Professora Evany", 1]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Capitão Alberto Neto", 25], ["Eduardo Braga", 19], ["Wilson Lima", 19], ["Plínio Valério", 19]] },
      { inst: "Viva Voz", campo: "22–27/09", tipo: "T", res: [["Eduardo Braga", 24.4], ["Capitão Alberto Neto", 21.8], ["Plínio Valério", 15.5], ["Wilson Lima", 14.1]] }
    ],
    candidatos: [
      { nome: "Eduardo Braga", partido: "MDB", resumo: "Senador desde 2011 e ex-governador do Amazonas (2003–2010). Líder do MDB no Senado, busca o terceiro mandato." },
      { nome: "Capitão Alberto Neto", partido: "PL", resumo: "Deputado federal desde 2019, militar da reserva. Disputou a prefeitura de Manaus em 2024." },
      { nome: "Plínio Valério", partido: "PSDB", resumo: "Senador desde 2019, busca a reeleição." },
      { nome: "Wilson Lima", partido: "União Brasil", resumo: "Governador do Amazonas de 2019 a 2026, deixou o cargo para disputar o Senado. Ex-apresentador de TV." }
    ]
  },
  {
    uf: "PA", nome: "Pará", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Helder Barbalho", 28], ["Delegado Éder Mauro", 24], ["Chicão", 20], ["Zequinha Marinho", 17], ["Celso Sabino", 8], ["Gizelle Freitas", 1], ["Lívia Noronha", 1], ["Coronel Jonildo", 1]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "V", res: [["Helder Barbalho", 27.1], ["Delegado Éder Mauro", 21.2], ["Chicão", 18.9], ["Zequinha Marinho", 18.2], ["Celso Sabino", 9.9]] },
      { inst: "Doxa", campo: "27–30/09", tipo: "T", res: [["Helder Barbalho", 23.8], ["Delegado Éder Mauro", 16.6], ["Chicão", 16.1], ["Zequinha Marinho", 10.3], ["Celso Sabino", 8.9]] }
    ],
    candidatos: [
      { nome: "Helder Barbalho", partido: "MDB", resumo: "Governador do Pará de 2019 a 2026, deixou o cargo para disputar o Senado. Ex-ministro da Integração Nacional." },
      { nome: "Delegado Éder Mauro", partido: "PL", resumo: "Deputado federal desde 2015 e delegado da Polícia Civil. Aliado de Bolsonaro, disputou a prefeitura de Belém em 2024." },
      { nome: "Chicão", partido: "União Brasil", resumo: "Candidato do União Brasil." },
      { nome: "Zequinha Marinho", partido: "Podemos", resumo: "Senador desde 2019, busca a reeleição. Ex-vice-governador do Pará." },
      { nome: "Celso Sabino", partido: "PDT", resumo: "Deputado federal e ex-ministro do Turismo do governo Lula." }
    ]
  },
  {
    uf: "RO", nome: "Rondônia", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "T", res: [["Dr. Fernando Máximo", 20], ["Bruno Bolsonaro Scheid", 16], ["Sílvia Cristina", 15], ["Mariana Carvalho", 12], ["Luciana Oliveira", 4], ["Acir Gurgacz", 3], ["Neidinha", 2], ["Luis Fernando", 2]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Dr. Fernando Máximo", 22], ["Sílvia Cristina", 17], ["Bruno Bolsonaro Scheid", 14], ["Mariana Carvalho", 14], ["Acir Gurgacz", 5]] },
      { inst: "Veritá", campo: "21–25/09", tipo: "C", res: [["Dr. Fernando Máximo", 49.1], ["Bruno Bolsonaro Scheid", 47.1], ["Sílvia Cristina", 17.1], ["Mariana Carvalho", 15.8], ["Acir Gurgacz", 15.1]] }
    ],
    candidatos: [
      { nome: "Dr. Fernando Máximo", partido: "PL", resumo: "Médico, deputado federal e ex-secretário estadual de Saúde de Rondônia." },
      { nome: "Bruno Bolsonaro Scheid", partido: "PL", resumo: "Candidato do PL, ligado ao bolsonarismo." },
      { nome: "Sílvia Cristina", partido: "PP", resumo: "Deputada federal por Rondônia desde 2019." },
      { nome: "Mariana Carvalho", partido: "Republicanos", resumo: "Médica e ex-deputada federal. Chegou ao 2º turno da prefeitura de Porto Velho em 2024." },
      { nome: "Acir Gurgacz", partido: "PDT", resumo: "Ex-senador por Rondônia (2009–2023)." }
    ]
  },
  {
    uf: "RR", nome: "Roraima", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Nicoletti", 26], ["Teresa Surita", 25], ["Helena da Asatur", 19], ["Chico Rodrigues", 15], ["Hélio Lopes", 9], ["Regina Tio Ivo", 4], ["Pastor Isamar", 1], ["Hilton Xavier", 1]] },
      { inst: "Eficaz", campo: "14–19/09", tipo: "T", res: [["Teresa Surita", 21.9], ["Nicoletti", 20.8], ["Helena da Asatur", 14.9], ["Chico Rodrigues", 12.4], ["Hélio Lopes", 6.2]] },
      { inst: "Real Time Big Data", campo: "05–09/09", tipo: "T", res: [["Teresa Surita", 25], ["Nicoletti", 17], ["Chico Rodrigues", 16], ["Helena da Asatur", 15], ["Hélio Lopes", 9]] }
    ],
    candidatos: [
      { nome: "Nicoletti", partido: "PL", resumo: "Deputado federal por Roraima, aliado de Bolsonaro." },
      { nome: "Teresa Surita", partido: "MDB", resumo: "Ex-prefeita de Boa Vista por vários mandatos e ex-deputada federal." },
      { nome: "Helena da Asatur", partido: "PSD", resumo: "Deputada federal por Roraima." },
      { nome: "Chico Rodrigues", partido: "PSB", resumo: "Senador desde 2019, busca a reeleição. Ex-governador de Roraima." },
      { nome: "Hélio Lopes", partido: "PL", resumo: "Deputado federal eleito pelo Rio de Janeiro e aliado próximo de Bolsonaro. Concorre por Roraima." }
    ]
  },
  {
    uf: "TO", nome: "Tocantins", regiao: "Norte", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Eduardo Gomes", 25], ["Carlos Gaguim", 21], ["Alexandre Guimarães", 17], ["Eli Borges", 11], ["Paulo Mourão", 10], ["Ronaldo Dimas", 7], ["Vanderlei Luxemburgo", 5]] },
      { inst: "Paraná Pesquisas", campo: "29/09–01/10", tipo: "C", res: [["Eduardo Gomes", 37], ["Alexandre Guimarães", 26.1], ["Carlos Gaguim", 24.4], ["Eli Borges", 21.4], ["Paulo Mourão", 16.8], ["Ronaldo Dimas", 13], ["Vanderlei Luxemburgo", 12.6]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Eduardo Gomes", 24], ["Carlos Gaguim", 17], ["Alexandre Guimarães", 17], ["Paulo Mourão", 11], ["Eli Borges", 10], ["Ronaldo Dimas", 8], ["Vanderlei Luxemburgo", 8]] }
    ],
    candidatos: [
      { nome: "Eduardo Gomes", partido: "PL", resumo: "Senador desde 2019, busca a reeleição. Foi líder do governo Bolsonaro no Congresso." },
      { nome: "Carlos Gaguim", partido: "União Brasil", resumo: "Ex-governador do Tocantins e deputado federal." },
      { nome: "Alexandre Guimarães", partido: "MDB", resumo: "Deputado federal pelo Tocantins." },
      { nome: "Eli Borges", partido: "Republicanos", resumo: "Deputado federal pelo Tocantins, ligado à bancada evangélica." },
      { nome: "Paulo Mourão", partido: "PT", resumo: "Candidato do PT, representa o campo governista." },
      { nome: "Ronaldo Dimas", partido: "Podemos", resumo: "Ex-prefeito de Araguaína e candidato ao governo em 2022." },
      { nome: "Vanderlei Luxemburgo", partido: "Podemos", resumo: "Ex-técnico de futebol, estreia em eleições." }
    ]
  },

  // ---------------- NORDESTE ----------------
  {
    uf: "AL", nome: "Alagoas", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Marina JHC", 29], ["Arthur Lira", 27], ["Renan Calheiros", 25], ["Davi Davino Filho", 9], ["Dr. Wanderley", 9], ["Mariedson", 1]] },
      { inst: "Paraná Pesquisas", campo: "26–29/09", tipo: "C", res: [["Marina JHC", 45.6], ["Arthur Lira", 41.6], ["Renan Calheiros", 36.9], ["Davi Davino Filho", 22.9], ["Dr. Wanderley", 15.2]] },
      { inst: "DataTrends", campo: "26–28/09", tipo: "C", res: [["Marina JHC", 42], ["Arthur Lira", 41], ["Renan Calheiros", 41], ["Davi Davino Filho", 21], ["Dr. Wanderley", 14]] }
    ],
    candidatos: [
      { nome: "Marina JHC", partido: "PSDB", resumo: "Esposa do prefeito de Maceió, JHC, que desistiu de concorrer. Lidera numericamente a disputa." },
      { nome: "Arthur Lira", partido: "PP", resumo: "Deputado federal desde 2011 e presidente da Câmara de 2021 a 2025." },
      { nome: "Renan Calheiros", partido: "MDB", resumo: "Senador desde 1995 e quatro vezes presidente do Senado. Busca mais um mandato." },
      { nome: "Davi Davino Filho", partido: "Republicanos", resumo: "Ex-deputado federal por Alagoas." },
      { nome: "Dr. Wanderley", partido: "MDB", resumo: "Candidato do MDB." }
    ]
  },
  {
    uf: "BA", nome: "Bahia", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Rui Costa", 33], ["Jaques Wagner", 30], ["Angelo Coronel", 18], ["João Roma", 17], ["Professora Delliana", 1]] },
      { inst: "AtlasIntel", campo: "24–28/09", tipo: "V", res: [["Rui Costa", 28.2], ["Jaques Wagner", 24.4], ["João Roma", 21], ["Angelo Coronel", 20.9]] },
      { inst: "Real Time Big Data", campo: "23–26/09", tipo: "T", res: [["Rui Costa", 28], ["Jaques Wagner", 20], ["João Roma", 17], ["Angelo Coronel", 15]] }
    ],
    candidatos: [
      { nome: "Rui Costa", partido: "PT", resumo: "Ex-governador da Bahia (2015–2022) e ministro da Casa Civil do governo Lula até deixar o cargo para concorrer." },
      { nome: "Jaques Wagner", partido: "PT", resumo: "Senador desde 2019 e ex-governador da Bahia (2007–2014). Líder do governo Lula no Senado, busca a reeleição." },
      { nome: "Angelo Coronel", partido: "Republicanos", resumo: "Senador desde 2019, eleito na chapa de Wagner. Agora disputa a reeleição no campo adversário ao PT." },
      { nome: "João Roma", partido: "PL", resumo: "Ex-ministro da Cidadania de Bolsonaro e candidato ao governo da Bahia em 2022." }
    ]
  },
  {
    uf: "CE", nome: "Ceará", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Cid Gomes", 32], ["Luizianne Lins", 27], ["Capitão Wagner", 26], ["Alcides Fernandes", 13], ["Catarina Matos", 1], ["Guilherme Theophilo", 1]] },
      { inst: "AtlasIntel", campo: "23–28/09", tipo: "V", res: [["Cid Gomes", 26.3], ["Luizianne Lins", 25.7], ["Capitão Wagner", 21.7], ["Alcides Fernandes", 18.5]] },
      { inst: "Datafolha", campo: "22–24/09", tipo: "T", res: [["Cid Gomes", 23], ["Capitão Wagner", 20], ["Luizianne Lins", 19], ["Alcides Fernandes", 9]] }
    ],
    candidatos: [
      { nome: "Cid Gomes", partido: "PSB", resumo: "Senador desde 2019 e ex-governador do Ceará (2007–2014). Busca a reeleição na chapa de Elmano de Freitas, enquanto o irmão Ciro disputa o governo pela oposição." },
      { nome: "Luizianne Lins", partido: "Rede", resumo: "Ex-prefeita de Fortaleza (2005–2012) e deputada federal." },
      { nome: "Capitão Wagner", partido: "União Brasil", resumo: "Ex-deputado federal e candidato ao governo em 2022. Principal nome da oposição." },
      { nome: "Alcides Fernandes", partido: "PL", resumo: "Deputado estadual, pai do deputado federal André Fernandes. Candidato do bolsonarismo." }
    ]
  },
  {
    uf: "MA", nome: "Maranhão", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Roseana Sarney", 25], ["André Fufuca", 23], ["Lahesio Bonfim", 18], ["Eliziane Gama", 16], ["Weverton Rocha", 12], ["Cidônio Gonçalves", 4], ["Dr. Hilton Gonçalo", 2]] },
      { inst: "Ranking", campo: "17–21/09", tipo: "T", res: [["Roseana Sarney", 21.4], ["André Fufuca", 18.45], ["Weverton Rocha", 12.95], ["Lahesio Bonfim", 11.55], ["Eliziane Gama", 9.05]] },
      { inst: "Viva Voz", campo: "15–20/09", tipo: "T", res: [["Roseana Sarney", 17.3], ["André Fufuca", 16.2], ["Lahesio Bonfim", 11.7], ["Weverton Rocha", 9.8], ["Eliziane Gama", 8]] }
    ],
    candidatos: [
      { nome: "Roseana Sarney", partido: "MDB", resumo: "Ex-governadora do Maranhão por quatro mandatos e deputada federal. Filha de José Sarney." },
      { nome: "André Fufuca", partido: "PP", resumo: "Deputado federal e ex-ministro do Esporte do governo Lula." },
      { nome: "Lahesio Bonfim", partido: "Novo", resumo: "Ex-prefeito de São Pedro dos Crentes e candidato ao governo em 2022. Nome da direita no estado." },
      { nome: "Eliziane Gama", partido: "PT", resumo: "Senadora desde 2019, busca a reeleição." },
      { nome: "Weverton Rocha", partido: "PDT", resumo: "Senador desde 2019, busca a reeleição. Foi candidato ao governo em 2022." }
    ]
  },
  {
    uf: "PB", nome: "Paraíba", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["João Azevêdo", 35], ["Veneziano", 25], ["Nabor Wanderley", 20], ["Marcelo Queiroga", 15], ["Major Fábio", 3], ["André Gadelha", 1], ["João Batista", 1]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["João Azevêdo", 31], ["Veneziano", 24], ["Nabor Wanderley", 16], ["Marcelo Queiroga", 16], ["Major Fábio", 5]] },
      { inst: "Anova", campo: "20–22/09", tipo: "C", res: [["João Azevêdo", 54.5], ["Veneziano", 35.8], ["Nabor Wanderley", 23.1], ["Marcelo Queiroga", 11.6], ["Major Fábio", 6.2]] }
    ],
    candidatos: [
      { nome: "João Azevêdo", partido: "PSB", resumo: "Governador da Paraíba de 2019 a 2026, deixou o cargo para disputar o Senado. Tem apoio de Lula." },
      { nome: "Veneziano", partido: "MDB", resumo: "Senador desde 2019, busca a reeleição. Ex-prefeito de Campina Grande, também apoiado por Lula, mas em outra chapa." },
      { nome: "Nabor Wanderley", partido: "Republicanos", resumo: "Ex-prefeito de Patos." },
      { nome: "Marcelo Queiroga", partido: "PL", resumo: "Ex-ministro da Saúde do governo Bolsonaro. Disputou a prefeitura de João Pessoa em 2024." }
    ]
  },
  {
    uf: "PE", nome: "Pernambuco", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "T", res: [["Marília Arraes", 19], ["Humberto Costa", 19], ["Mendonça Filho", 12], ["Eduardo da Fonte", 10], ["Túlio Gadêlha", 5], ["Carlos Sant'anna", 2]] },
      { inst: "DataTrends", campo: "28–30/09", tipo: "T", res: [["Marília Arraes", 19], ["Humberto Costa", 16], ["Mendonça Filho", 11], ["Eduardo da Fonte", 11], ["Túlio Gadêlha", 4]] },
      { inst: "Quaest", campo: "25–28/09", tipo: "T", res: [["Marília Arraes", 19], ["Humberto Costa", 17], ["Mendonça Filho", 10], ["Eduardo da Fonte", 7], ["Túlio Gadêlha", 3]] }
    ],
    candidatos: [
      { nome: "Marília Arraes", partido: "PDT", resumo: "Ex-deputada federal e neta de Miguel Arraes. Chegou ao 2º turno do governo em 2022." },
      { nome: "Humberto Costa", partido: "PT", resumo: "Senador desde 2011, busca o terceiro mandato. Ex-ministro da Saúde." },
      { nome: "Mendonça Filho", partido: "PL", resumo: "Deputado federal, ex-governador de Pernambuco e ex-ministro da Educação." },
      { nome: "Eduardo da Fonte", partido: "PP", resumo: "Deputado federal por Pernambuco desde 2007." },
      { nome: "Túlio Gadêlha", partido: "PSD", resumo: "Deputado federal por Pernambuco." }
    ]
  },
  {
    uf: "PI", nome: "Piauí", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Datafolha", campo: "01–03/10", tipo: "V", res: [["Marcelo Castro", 28], ["Ciro Nogueira", 26], ["Júlio César", 25], ["Tiago Junqueira", 9]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "V", res: [["Marcelo Castro", 32.7], ["Júlio César", 28.2], ["Ciro Nogueira", 19.1], ["Tiago Junqueira", 13.8]] },
      { inst: "Amostragem", campo: "29/08–02/09", tipo: "T", res: [["Marcelo Castro", 29.68], ["Ciro Nogueira", 29.32], ["Júlio César", 20.98], ["Tiago Junqueira", 4.83]] }
    ],
    candidatos: [
      { nome: "Marcelo Castro", partido: "MDB", resumo: "Senador desde 2019, busca a reeleição. Ex-ministro da Saúde." },
      { nome: "Ciro Nogueira", partido: "PP", resumo: "Senador desde 2011, presidente nacional do PP e ex-ministro da Casa Civil de Bolsonaro." },
      { nome: "Júlio César", partido: "PSD", resumo: "Deputado federal pelo Piauí há vários mandatos." },
      { nome: "Tiago Junqueira", partido: "PL", resumo: "Candidato do PL, representa o bolsonarismo no estado." }
    ]
  },
  {
    uf: "RN", nome: "Rio Grande do Norte", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Styvenson Valentim", 27], ["Coronel Hélio", 20], ["Samanda de Lula", 18], ["Zenaide Maia", 17], ["Rafael Motta", 12], ["Sandro Pimentel", 2], ["Tércio Tinôco", 2]] },
      { inst: "Exatus", campo: "28–30/09", tipo: "C", res: [["Styvenson Valentim", 47.2], ["Zenaide Maia", 35.47], ["Samanda de Lula", 19.99], ["Rafael Motta", 19.3], ["Coronel Hélio", 17.29]] },
      { inst: "TN/Consult", campo: "24–26/09", tipo: "T", res: [["Styvenson Valentim", 23.8], ["Zenaide Maia", 15.41], ["Coronel Hélio", 9.91], ["Samanda de Lula", 9.08], ["Rafael Motta", 7.53]] }
    ],
    candidatos: [
      { nome: "Styvenson Valentim", partido: "Podemos", resumo: "Senador desde 2019, busca a reeleição. Ex-policial militar conhecido pelas blitze da Lei Seca em Natal." },
      { nome: "Coronel Hélio", partido: "PL", resumo: "Coronel da Polícia Militar, candidato do PL." },
      { nome: "Samanda de Lula", partido: "PT", resumo: "Candidata do PT." },
      { nome: "Zenaide Maia", partido: "PSD", resumo: "Senadora desde 2019, médica e ex-deputada federal. Busca a reeleição." },
      { nome: "Rafael Motta", partido: "PDT", resumo: "Ex-deputado federal pelo Rio Grande do Norte." }
    ]
  },
  {
    uf: "SE", nome: "Sergipe", regiao: "Nordeste", vagas: 2,
    pesquisas: [
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "V", res: [["Rogério Carvalho", 23.7], ["Delegado André David", 15.7], ["Alessandro Vieira", 13.2], ["Edvaldo Nogueira", 11.2], ["Rodrigo Valadares", 9], ["Eduardo Amorim", 8.9], ["André Moura", 7.4], ["Iran Barbosa", 5.9], ["Coronel Rocha", 4.6]] },
      { inst: "Quaest", campo: "20–23/09", tipo: "T", res: [["André Moura", 12], ["Delegado André David", 11], ["Alessandro Vieira", 10], ["Rogério Carvalho", 10], ["Eduardo Amorim", 8], ["Edvaldo Nogueira", 5], ["Rodrigo Valadares", 5], ["Coronel Rocha", 2]] },
      { inst: "Real Time Big Data", campo: "17–21/09", tipo: "T", res: [["Delegado André David", 18], ["Alessandro Vieira", 14], ["Rogério Carvalho", 12], ["André Moura", 10], ["Eduardo Amorim", 9], ["Edvaldo Nogueira", 9], ["Rodrigo Valadares", 9], ["Coronel Rocha", 8]] }
    ],
    candidatos: [
      { nome: "Rogério Carvalho", partido: "PT", resumo: "Senador desde 2019, busca a reeleição. Candidato ao governo em 2022." },
      { nome: "Delegado André David", partido: "Republicanos", resumo: "Delegado de polícia, candidato do Republicanos." },
      { nome: "Alessandro Vieira", partido: "MDB", resumo: "Senador desde 2019 e delegado da Polícia Civil. Busca a reeleição." },
      { nome: "Edvaldo Nogueira", partido: "PDT", resumo: "Ex-prefeito de Aracaju por vários mandatos." },
      { nome: "Rodrigo Valadares", partido: "PL", resumo: "Deputado federal por Sergipe." },
      { nome: "Eduardo Amorim", partido: "Republicanos", resumo: "Ex-senador por Sergipe (2011–2019)." },
      { nome: "André Moura", partido: "União Brasil", resumo: "Ex-deputado federal e ex-líder do governo Temer na Câmara." },
      { nome: "Iran Barbosa", partido: "PSOL", resumo: "Candidato do PSOL." }
    ]
  },

  // ---------------- CENTRO-OESTE ----------------
  {
    uf: "DF", nome: "Distrito Federal", regiao: "Centro-Oeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Michelle Bolsonaro", 31], ["Leila do Vôlei", 27], ["Bia Kicis", 24], ["Erika Kokay", 17]] },
      { inst: "Datafolha", campo: "28/09–01/10", tipo: "T", res: [["Michelle Bolsonaro", 23], ["Leila do Vôlei", 18], ["Bia Kicis", 18], ["Erika Kokay", 13], ["Sebastião Coelho", 2], ["Guilherme Amorim", 2], ["Ronaldo Fonseca", 1]] },
      { inst: "Quaest", campo: "25–28/09", tipo: "T", res: [["Michelle Bolsonaro", 26], ["Leila do Vôlei", 20], ["Bia Kicis", 18], ["Erika Kokay", 16]] }
    ],
    candidatos: [
      { nome: "Michelle Bolsonaro", partido: "PL", resumo: "Ex-primeira-dama e presidente do PL Mulher. Estreia como candidata." },
      { nome: "Leila do Vôlei", partido: "PDT", resumo: "Senadora desde 2019 e ex-jogadora da seleção brasileira de vôlei. Busca a reeleição." },
      { nome: "Bia Kicis", partido: "PL", resumo: "Deputada federal desde 2019, procuradora aposentada e aliada de Bolsonaro." },
      { nome: "Erika Kokay", partido: "PT", resumo: "Deputada federal desde 2011, ex-bancária e sindicalista." }
    ]
  },
  {
    uf: "GO", nome: "Goiás", regiao: "Centro-Oeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Gracinha Caiado", 30], ["Gustavo Gayer", 21], ["Zacharias Calil", 18], ["Vanderlan Cardoso", 10], ["Gustavo Mendanha", 9], ["Oséias Varão", 7], ["Isaura Lemos", 3], ["Cíntia Dias", 1], ["Ernesto Roller", 1]] },
      { inst: "Goiás Pesquisas", campo: "24–25/09", tipo: "T", res: [["Gracinha Caiado", 21.6], ["Gustavo Gayer", 21.1], ["Zacharias Calil", 18.2], ["Gustavo Mendanha", 8.4], ["Isaura Lemos", 4.9], ["Vanderlan Cardoso", 4.4], ["Cíntia Dias", 4.4], ["Oséias Varão", 4.2]] },
      { inst: "Real Time Big Data", campo: "17–21/09", tipo: "T", res: [["Gracinha Caiado", 23], ["Gustavo Gayer", 20], ["Zacharias Calil", 13], ["Vanderlan Cardoso", 12], ["Gustavo Mendanha", 8], ["Cíntia Dias", 5], ["Isaura Lemos", 5], ["Oséias Varão", 5]] }
    ],
    candidatos: [
      { nome: "Gracinha Caiado", partido: "União Brasil", resumo: "Esposa do ex-governador Ronaldo Caiado. Presidiu a Organização das Voluntárias de Goiás." },
      { nome: "Gustavo Gayer", partido: "PL", resumo: "Deputado federal desde 2023, influenciador digital bolsonarista." },
      { nome: "Zacharias Calil", partido: "MDB", resumo: "Médico cirurgião pediátrico e deputado federal." },
      { nome: "Vanderlan Cardoso", partido: "PSD", resumo: "Senador desde 2019, busca a reeleição. Ex-prefeito de Senador Canedo." },
      { nome: "Gustavo Mendanha", partido: "PRD", resumo: "Ex-prefeito de Aparecida de Goiânia e candidato ao governo em 2022." },
      { nome: "Oséias Varão", partido: "PL", resumo: "Segundo candidato do PL ao Senado em Goiás." }
    ]
  },
  {
    uf: "MT", nome: "Mato Grosso", regiao: "Centro-Oeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Mauro Mendes", 37], ["Janaína Riva", 23], ["Zé Medeiros", 17], ["Pedro Taques", 9], ["Carlos Fávaro", 9], ["Galvan", 2], ["Margareth Buzetti", 2], ["Coronel Darwin", 1]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "V", res: [["Zé Medeiros", 26.8], ["Mauro Mendes", 25.3], ["Carlos Fávaro", 14], ["Janaína Riva", 10.2], ["Pedro Taques", 9.3], ["Galvan", 7.3]] }
    ],
    candidatos: [
      { nome: "Mauro Mendes", partido: "União Brasil", resumo: "Governador de Mato Grosso de 2019 a 2026, deixou o cargo para disputar o Senado. Ex-prefeito de Cuiabá." },
      { nome: "Janaína Riva", partido: "MDB", resumo: "Deputada estadual em vários mandatos." },
      { nome: "Zé Medeiros", partido: "PL", resumo: "Deputado federal e ex-senador. Candidato do bolsonarismo." },
      { nome: "Carlos Fávaro", partido: "PSD", resumo: "Senador desde 2020 e ministro da Agricultura do governo Lula." },
      { nome: "Pedro Taques", partido: "PSB", resumo: "Ex-governador de Mato Grosso (2015–2018) e ex-senador." }
    ]
  },
  {
    uf: "MS", nome: "Mato Grosso do Sul", regiao: "Centro-Oeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Capitão Contar", 35], ["Reinaldo Azambuja", 32], ["Soraya Thronicke", 16], ["Vander Loubet", 10], ["Roberto Oshiro", 3], ["Beto do Movimento", 3], ["Daniel Junior", 1]] },
      { inst: "Novo Ibrape", campo: "23–28/09", tipo: "T", res: [["Reinaldo Azambuja", 26.1], ["Capitão Contar", 24.8], ["Soraya Thronicke", 9.5], ["Vander Loubet", 9.2]] },
      { inst: "IPEMS", campo: "22–27/09", tipo: "T", res: [["Reinaldo Azambuja", 29.43], ["Capitão Contar", 27.59], ["Soraya Thronicke", 14.21], ["Vander Loubet", 7.19]] }
    ],
    candidatos: [
      { nome: "Capitão Contar", partido: "PL", resumo: "Ex-deputado estadual e militar da reserva. Chegou ao 2º turno do governo em 2022." },
      { nome: "Reinaldo Azambuja", partido: "PL", resumo: "Ex-governador de Mato Grosso do Sul (2015–2022)." },
      { nome: "Soraya Thronicke", partido: "PSB", resumo: "Senadora desde 2019 e candidata à Presidência em 2022. Busca a reeleição." },
      { nome: "Vander Loubet", partido: "PT", resumo: "Deputado federal por Mato Grosso do Sul desde 2003." }
    ]
  },

  // ---------------- SUDESTE ----------------
  {
    uf: "ES", nome: "Espírito Santo", regiao: "Sudeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Renato Casagrande", 31], ["Evair de Melo", 18], ["Maguinha Malta", 18], ["Fabiano Contarato", 10], ["Rose de Freitas", 8], ["Sergio Meneguelli", 8], ["Marcos do Val", 5], ["Callegari", 1], ["Professor Fabian", 1]] },
      { inst: "Real Time Big Data", campo: "25–29/09", tipo: "T", res: [["Renato Casagrande", 28], ["Sergio Meneguelli", 13], ["Fabiano Contarato", 12], ["Maguinha Malta", 12], ["Evair de Melo", 12], ["Rose de Freitas", 9], ["Marcos do Val", 4], ["Leonardo Monjardim", 2]] },
      { inst: "Perfil/ES Hoje", campo: "21–24/09", tipo: "T", res: [["Renato Casagrande", 30.69], ["Fabiano Contarato", 11.29], ["Maguinha Malta", 8.88], ["Sergio Meneguelli", 8.42], ["Evair de Melo", 7.41], ["Marcos do Val", 5.78], ["Rose de Freitas", 4.98]] }
    ],
    candidatos: [
      { nome: "Renato Casagrande", partido: "PSB", resumo: "Governador do Espírito Santo por três mandatos, deixou o cargo em 2026 para disputar o Senado. Já foi senador." },
      { nome: "Evair de Melo", partido: "Republicanos", resumo: "Deputado federal pelo Espírito Santo." },
      { nome: "Maguinha Malta", partido: "PL", resumo: "Candidata do PL, da família do senador Magno Malta." },
      { nome: "Fabiano Contarato", partido: "PT", resumo: "Senador desde 2019 e delegado da Polícia Civil. Busca a reeleição." },
      { nome: "Rose de Freitas", partido: "MDB", resumo: "Ex-senadora (2015–2023) e ex-deputada federal." },
      { nome: "Sergio Meneguelli", partido: "PSD", resumo: "Ex-prefeito de Colatina." },
      { nome: "Marcos do Val", partido: "Avante", resumo: "Senador desde 2019, busca a reeleição." }
    ]
  },
  {
    uf: "MG", nome: "Minas Gerais", regiao: "Sudeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Domingos Sávio", 22], ["Marília Campos", 18], ["Carlos Viana", 18], ["Aécio Neves", 17], ["Marcelo Aro", 10], ["Marco Antônio Superman", 9]] },
      { inst: "Real Time Big Data", campo: "28/09–02/10", tipo: "T", res: [["Domingos Sávio", 20], ["Carlos Viana", 20], ["Marília Campos", 19], ["Aécio Neves", 9], ["Marcelo Aro", 9], ["Marco Antônio Superman", 8], ["Áurea Carolina", 7]] },
      { inst: "Datafolha", campo: "28/09–01/10", tipo: "T", res: [["Marília Campos", 13], ["Aécio Neves", 11], ["Carlos Viana", 11], ["Domingos Sávio", 9], ["Marcelo Aro", 6], ["Áurea Carolina", 5], ["Marco Antônio Superman", 2]] }
    ],
    candidatos: [
      { nome: "Domingos Sávio", partido: "PL", resumo: "Deputado federal por vários mandatos, candidato do bolsonarismo." },
      { nome: "Marília Campos", partido: "PT", resumo: "Prefeita de Contagem por vários mandatos, deixou o cargo para disputar o Senado." },
      { nome: "Carlos Viana", partido: "PSD", resumo: "Senador desde 2019 e jornalista. Busca a reeleição." },
      { nome: "Aécio Neves", partido: "PSDB", resumo: "Ex-governador de Minas, ex-senador e candidato à Presidência em 2014. Deputado federal." },
      { nome: "Marcelo Aro", partido: "PP", resumo: "Ex-deputado federal e ex-secretário de Estado em Minas Gerais." },
      { nome: "Marco Antônio Superman", partido: "Novo", resumo: "Candidato do Novo." },
      { nome: "Áurea Carolina", partido: "PSOL", resumo: "Ex-deputada federal e ex-vereadora de Belo Horizonte." }
    ]
  },
  {
    uf: "RJ", nome: "Rio de Janeiro", regiao: "Sudeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "T", res: [["Benedita da Silva", 26], ["Carlos Jordy", 22], ["Carlos Portinho", 14], ["Marcelo Crivella", 9], ["Pedro Paulo", 7], ["Monica Benicio", 3], ["Michelly Xavier", 1]] },
      { inst: "Quaest", campo: "25–28/09", tipo: "T", res: [["Carlos Portinho", 15], ["Benedita da Silva", 15], ["Carlos Jordy", 15], ["Marcelo Crivella", 7], ["Pedro Paulo", 7], ["Monica Benicio", 6]] }
    ],
    candidatos: [
      { nome: "Benedita da Silva", partido: "PT", resumo: "Deputada federal, ex-governadora do Rio e ex-senadora." },
      { nome: "Carlos Jordy", partido: "PL", resumo: "Deputado federal desde 2019 e ex-vereador de Niterói. Aliado de Bolsonaro." },
      { nome: "Carlos Portinho", partido: "PL", resumo: "Senador desde 2021, busca a reeleição." },
      { nome: "Marcelo Crivella", partido: "Republicanos", resumo: "Ex-prefeito do Rio, ex-senador e deputado federal." },
      { nome: "Pedro Paulo", partido: "PSD", resumo: "Deputado federal, aliado do prefeito Eduardo Paes." },
      { nome: "Monica Benicio", partido: "PSOL", resumo: "Vereadora do Rio e viúva de Marielle Franco." }
    ]
  },
  {
    uf: "SP", nome: "São Paulo", regiao: "Sudeste", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Guilherme Derrite", 25], ["André do Prado", 23], ["Marina Silva", 22], ["Simone Tebet", 22]] },
      { inst: "Datafolha", campo: "02–03/10", tipo: "V", res: [["Guilherme Derrite", 22], ["André do Prado", 22], ["Marina Silva", 21], ["Simone Tebet", 20]] },
      { inst: "Datafolha", campo: "28–30/09", tipo: "T", res: [["Marina Silva", 16], ["André do Prado", 15], ["Simone Tebet", 15], ["Guilherme Derrite", 14]] }
    ],
    candidatos: [
      { nome: "Guilherme Derrite", partido: "PP", resumo: "Ex-secretário da Segurança Pública de SP no governo Tarcísio, deputado federal e capitão da reserva da PM." },
      { nome: "André do Prado", partido: "PL", resumo: "Presidente da Assembleia Legislativa de São Paulo." },
      { nome: "Marina Silva", partido: "Rede", resumo: "Ministra do Meio Ambiente do governo Lula até deixar o cargo para concorrer. Ex-senadora pelo Acre e três vezes candidata à Presidência." },
      { nome: "Simone Tebet", partido: "PSB", resumo: "Ministra do Planejamento do governo Lula até deixar o cargo para concorrer. Ex-senadora por MS e candidata à Presidência em 2022." }
    ]
  },

  // ---------------- SUL ----------------
  {
    uf: "PR", nome: "Paraná", regiao: "Sul", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Filipe Barros", 25], ["Alexandre Curi", 21], ["Deltan Dallagnol", 21], ["Gleisi Hoffmann", 15], ["Dr. Rosinha", 10], ["Cristina Graeml", 7], ["Karen Guerreiro", 1]] },
      { inst: "Neokemp", campo: "29/09–01/10", tipo: "V", res: [["Deltan Dallagnol", 24.9], ["Filipe Barros", 23], ["Gleisi Hoffmann", 15.7], ["Alexandre Curi", 12.1], ["Dr. Rosinha", 9.7], ["Cristina Graeml", 8.9]] },
      { inst: "Real Time Big Data", campo: "28/09–01/10", tipo: "T", res: [["Deltan Dallagnol", 21], ["Filipe Barros", 19], ["Alexandre Curi", 19], ["Gleisi Hoffmann", 16], ["Cristina Graeml", 12], ["Dr. Rosinha", 7]] }
    ],
    candidatos: [
      { nome: "Filipe Barros", partido: "PL", resumo: "Deputado federal desde 2019, aliado de Bolsonaro." },
      { nome: "Alexandre Curi", partido: "Republicanos", resumo: "Presidente da Assembleia Legislativa do Paraná." },
      { nome: "Deltan Dallagnol", partido: "Novo", resumo: "Ex-procurador e coordenador da Lava Jato. Teve o mandato de deputado federal cassado em 2023." },
      { nome: "Gleisi Hoffmann", partido: "PT", resumo: "Ex-presidente nacional do PT, ex-senadora e ex-ministra do governo Lula." },
      { nome: "Dr. Rosinha", partido: "PT", resumo: "Médico e ex-deputado federal." },
      { nome: "Cristina Graeml", partido: "PSD", resumo: "Jornalista, chegou ao 2º turno da prefeitura de Curitiba em 2024." }
    ]
  },
  {
    uf: "RS", nome: "Rio Grande do Sul", regiao: "Sul", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Sanderson", 25], ["Marcel van Hattem", 22], ["Manuela d'Ávila", 20], ["Paulo Pimenta", 18], ["Germano Rigotto", 10], ["Frederico Antunes", 2]] },
      { inst: "Neokemp", campo: "02/10", tipo: "T", res: [["Marcel van Hattem", 34.3], ["Manuela d'Ávila", 25.2], ["Sanderson", 18.8], ["Paulo Pimenta", 11.5], ["Germano Rigotto", 6.1]] },
      { inst: "AtlasIntel", campo: "27/09–02/10", tipo: "V", res: [["Marcel van Hattem", 25.3], ["Sanderson", 24.9], ["Manuela d'Ávila", 21.5], ["Paulo Pimenta", 21.1], ["Germano Rigotto", 3.9]] }
    ],
    candidatos: [
      { nome: "Sanderson", partido: "PL", resumo: "Deputado federal desde 2019 e ex-policial federal. Candidato do bolsonarismo." },
      { nome: "Marcel van Hattem", partido: "Novo", resumo: "Deputado federal desde 2019 e liderança do Novo na Câmara." },
      { nome: "Manuela d'Ávila", partido: "PSOL", resumo: "Ex-deputada federal e candidata a vice-presidente em 2018." },
      { nome: "Paulo Pimenta", partido: "PT", resumo: "Deputado federal e ex-ministro da Secom do governo Lula." },
      { nome: "Germano Rigotto", partido: "MDB", resumo: "Ex-governador do Rio Grande do Sul (2003–2006)." }
    ]
  },
  {
    uf: "SC", nome: "Santa Catarina", regiao: "Sul", vagas: 2,
    pesquisas: [
      { inst: "Quaest", campo: "02–03/10", tipo: "V", res: [["Carol de Toni", 30], ["Carlos Bolsonaro", 24], ["Esperidião Amin", 20], ["Décio Lima", 12], ["Afrânio Boppré", 5], ["Antídio Lunelli", 4]] },
      { inst: "Neokemp", campo: "30/09", tipo: "C", res: [["Carol de Toni", 58], ["Carlos Bolsonaro", 43.8], ["Esperidião Amin", 37.4], ["Décio Lima", 24.8], ["Afrânio Boppré", 17.5], ["Antídio Lunelli", 11]] },
      { inst: "Rumo", campo: "24–26/09", tipo: "T", res: [["Carol de Toni", 20.75], ["Esperidião Amin", 18.1], ["Carlos Bolsonaro", 15.5], ["Antídio Lunelli", 10.45], ["Décio Lima", 10.1], ["Afrânio Boppré", 4.45]] }
    ],
    candidatos: [
      { nome: "Carol de Toni", partido: "PL", resumo: "Deputada federal desde 2019 e ex-presidente da CCJ da Câmara." },
      { nome: "Carlos Bolsonaro", partido: "PL", resumo: "Vereador do Rio de Janeiro por vários mandatos e filho de Jair Bolsonaro. Transferiu o domicílio eleitoral para SC." },
      { nome: "Esperidião Amin", partido: "PP", resumo: "Senador desde 2019 e ex-governador de Santa Catarina por dois mandatos. Busca a reeleição." },
      { nome: "Décio Lima", partido: "PT", resumo: "Ex-deputado federal e ex-presidente do Sebrae." },
      { nome: "Afrânio Boppré", partido: "PSOL", resumo: "Ex-deputado estadual por Santa Catarina." },
      { nome: "Antídio Lunelli", partido: "MDB", resumo: "Ex-prefeito de Jaraguá do Sul." }
    ]
  }
];
