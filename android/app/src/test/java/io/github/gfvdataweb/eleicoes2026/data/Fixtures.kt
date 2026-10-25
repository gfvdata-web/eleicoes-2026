package io.github.gfvdataweb.eleicoes2026.data

// JSONs do TSE para os testes: os reais salvos em src/test/resources/tse/ e um sintético.

/** Lê um JSON real do TSE de `src/test/resources/tse/`. */
internal fun fixtureTse(nome: String): String =
    checkNotNull(object {}.javaClass.getResource("/tse/$nome")) { "Fixture ausente: $nome" }.readText()

/** Um candidato (dentro do seu próprio agrupamento/partido) no formato do "-u.json". */
internal fun candidatoJson(
    nome: String,
    numero: Int,
    partido: String,
    votos: Long,
    pvap: String,
    e: String = "n",
    st: String = "",
    nmu: String = "",
): String =
    """{ "par": [ { "sg": "$partido", "cand": [ { "n": "$numero", "nm": "$nome", "nmu": "$nmu", "e": "$e", "st": "$st", "vap": "$votos", "pvap": "$pvap", "pvapn": "" } ] } ] }"""

/** Um "-u.json" sintético de 1 cargo, com os totais de `s`, `e` e `v` preenchidos. */
internal fun jsonDoTse(
    pst: String,
    vararg agrupamentos: String,
    hg: String = "20:00:00",
    ht: String = "",
    dt: String = "",
): String =
    """{ "dg": "25/10/2026", "hg": "$hg", "ht": "$ht", "dt": "$dt",
         "carg": [ { "agr": [ ${agrupamentos.joinToString(",")} ] } ],
         "s": { "pst": "$pst" }, "e": { "c": "1000" },
         "v": { "vv": "900", "vb": "50", "tvn": "60", "vn": "10" } }"""
