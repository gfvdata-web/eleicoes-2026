// Senadores eleitos em 2022, com mandato até 31/01/2031. Não estão em disputa em 2026.
// Partido = filiação atual conhecida (pode diferir do partido pelo qual foram eleitos).
// `nota` = observação mostrada na tabela (ex.: concorre a governador; se vencer, assume o suplente).
// `governador` = nome do senador em dados.js (concorre a governador em 2026).
// `suplente` = 1º suplente, que assume a vaga se o titular for eleito governador.
//   Nomes: Wikipédia, "Lista de senadores do Brasil da 57.ª legislatura" (consulta em 04/10/2026).
//   Partidos conferidos em 04/10/2026 com Gazeta do Povo (29/07/2026), ND Mais (10/08/2026) e imprensa local.
//   Mauro Carvalho Júnior: saiu do PRD em 2026 (RDNews, 20/07/2026); sem nova filiação encontrada.
// As outras 54 cadeiras (2 por UF) vêm das pesquisas em senado.js.
window.SENADO_ATUAL = [
  { uf: "AC", nome: "Alan Rick", partido: "Republicanos", nota: "Concorre a governador do Acre. Se eleito, a vaga passa ao suplente.",
    governador: "Alan Rick", suplente: { nome: "Gemil Júnior", partido: "PSD" } },
  { uf: "AL", nome: "Renan Filho", partido: "MDB", nota: "Concorre a governador de Alagoas. Se eleito, a vaga passa ao suplente.",
    governador: "Renan Filho", suplente: { nome: "Fernando Farias", partido: "MDB" } },
  { uf: "AP", nome: "Davi Alcolumbre", partido: "União Brasil", nota: "Presidente do Senado (2025–2027)." },
  { uf: "AM", nome: "Omar Aziz", partido: "PSD", nota: "Concorre a governador do Amazonas. Se eleito, a vaga passa ao suplente.",
    governador: "Omar Aziz", suplente: { nome: "Cheila Moreira", partido: "PT" } },
  { uf: "BA", nome: "Otto Alencar", partido: "PSD", nota: "" },
  { uf: "CE", nome: "Camilo Santana", partido: "PT", nota: "" },
  { uf: "DF", nome: "Damares Alves", partido: "Republicanos", nota: "" },
  { uf: "ES", nome: "Magno Malta", partido: "PL", nota: "" },
  { uf: "GO", nome: "Wilder Morais", partido: "PL", nota: "Concorre a governador de Goiás. Se eleito, a vaga passa ao suplente.",
    governador: "Wilder Morais", suplente: { nome: "Izaura Cardoso", partido: "PSD" } },
  { uf: "MA", nome: "Ana Paula Lobato", partido: "PSB", nota: "Suplente de Flávio Dino; assumiu em 2024, quando ele foi para o STF." },
  { uf: "MT", nome: "Wellington Fagundes", partido: "PL", nota: "Concorre a governador de Mato Grosso. Se eleito, a vaga passa ao suplente.",
    governador: "Wellington Fagundes", suplente: { nome: "Mauro Carvalho Júnior", partido: "Sem partido" } },
  { uf: "MS", nome: "Tereza Cristina", partido: "PP", nota: "" },
  { uf: "MG", nome: "Cleitinho", partido: "Republicanos", nota: "Concorre a governador de Minas Gerais. Se eleito, a vaga passa ao suplente.",
    governador: "Cleitinho", suplente: { nome: "Alexandre Diniz", partido: "PL" } },
  { uf: "PA", nome: "Beto Faro", partido: "PT", nota: "" },
  { uf: "PB", nome: "Efraim Filho", partido: "PL", nota: "Concorre a governador da Paraíba. Se eleito, a vaga passa ao suplente.",
    governador: "Efraim Filho", suplente: { nome: "André Amaral", partido: "União Brasil" } },
  { uf: "PR", nome: "Sergio Moro", partido: "PL", nota: "Concorre a governador do Paraná. Se eleito, a vaga passa ao suplente.",
    governador: "Sergio Moro", suplente: { nome: "Luís Felipe Cunha", partido: "União Brasil" } },
  { uf: "PE", nome: "Teresa Leitão", partido: "PT", nota: "" },
  { uf: "PI", nome: "Wellington Dias", partido: "PT", nota: "" },
  { uf: "RJ", nome: "Romário", partido: "PL", nota: "" },
  { uf: "RN", nome: "Rogério Marinho", partido: "PL", nota: "" },
  { uf: "RS", nome: "Hamilton Mourão", partido: "Republicanos", nota: "" },
  { uf: "RO", nome: "Jaime Bagattoli", partido: "PL", nota: "" },
  { uf: "RR", nome: "Dr. Hiran", partido: "PP", nota: "" },
  { uf: "SC", nome: "Jorge Seif", partido: "PL", nota: "" },
  { uf: "SP", nome: "Marcos Pontes", partido: "PL", nota: "" },
  { uf: "SE", nome: "Laércio Oliveira", partido: "PP", nota: "" },
  { uf: "TO", nome: "Professora Dorinha", partido: "União Brasil", nota: "Concorre a governadora do Tocantins. Se eleita, a vaga passa ao suplente.",
    governador: "Professora Dorinha", suplente: { nome: "Professora Lu", partido: "União Brasil" } }
];

// Cores de identidade dos partidos (usadas no hemiciclo). Partido ausente daqui usa cinza.
window.CORES_PARTIDOS = {
  "PT": "#c8102e", "PSOL": "#7a1f4b", "PCdoB": "#9e2a2b", "Rede": "#14a79d", "PSB": "#e3b505",
  "PDT": "#a0522d", "PV": "#4c9a2a", "MDB": "#2e7d4f", "PSD": "#ef8a17", "União Brasil": "#2f8fce",
  "PP": "#6b3fa0", "Republicanos": "#0b5d6b", "PSDB": "#8db6e0", "Podemos": "#8bc34a",
  "PL": "#1b2f6e", "Novo": "#f4692b", "Solidariedade": "#d88aa6", "Avante": "#b58ad6",
  "PRD": "#8a8a7f", "Sem partido": "#cfcdc6", "—": "#b9b7af"
};
