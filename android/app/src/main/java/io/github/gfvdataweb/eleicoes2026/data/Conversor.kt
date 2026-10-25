package io.github.gfvdataweb.eleicoes2026.data

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.contentOrNull

/** Um candidato no resultado de uma disputa. [pct] = % dos votos válidos; [numero] = número na urna. */
data class Candidato(
    val nome: String,
    val pct: Double,
    val partido: String,
    val votos: Long,
    val numero: Int,
    val eleito: Boolean,
)

/** Resultado de uma disputa (um "-u.json" do TSE) já convertido. */
data class Apuracao(
    val pctApurado: Double,
    /** Hora e data do TSE, como vêm (`HH:mm:ss` e `dd/MM/aaaa`). */
    val hora: String,
    val data: String,
    /** Do mais votado para o menos votado (empate mantém a ordem do TSE). */
    val candidatos: List<Candidato>,
    val validos: Long,
    val brancos: Long,
    val nulos: Long,
    val comparecimento: Long,
) {
    val eleito: Candidato? get() = candidatos.firstOrNull { it.eleito }
}

private fun JsonElement?.objeto(): JsonObject? = this as? JsonObject

private fun JsonElement?.texto(): String? = (this as? JsonPrimitive)?.contentOrNull

/** Decimal do TSE, com vírgula ("87,35"); ausente ou inválido vira 0. */
internal fun decimalTse(s: String?): Double = s?.replace(",", ".")?.toDoubleOrNull() ?: 0.0

private fun inteiroTse(s: String?): Long = s?.toLongOrNull() ?: 0L

/**
 * Converte o JSON "-u.json" do TSE (2026) para [Apuracao]. Porte de `converter()`
 * em `scripts/apuracao.py`, com uma diferença: com 0% apurado devolve os candidatos
 * com 0% (as urnas ainda não fecharam). JSON fora do formato → [IllegalArgumentException].
 */
fun converter(bruto: String): Apuracao {
    val raiz = Json.parseToJsonElement(bruto.removePrefix("﻿")).objeto()
        ?: throw IllegalArgumentException("JSON do TSE sem objeto na raiz")
    val carg = (raiz["carg"] as? JsonArray)?.firstOrNull().objeto()
        ?: throw IllegalArgumentException("JSON do TSE sem carg")
    val candidatos = mutableListOf<Candidato>()
    for (agr in carg["agr"] as? JsonArray ?: JsonArray(emptyList())) {
        for (par in agr.objeto()?.get("par") as? JsonArray ?: JsonArray(emptyList())) {
            val partido = par.objeto()?.get("sg").texto() ?: "—"
            for (elemento in par.objeto()?.get("cand") as? JsonArray ?: JsonArray(emptyList())) {
                val cd = elemento.objeto() ?: continue
                val nome = cd["nmu"].texto()?.ifEmpty { null } ?: cd["nm"].texto() ?: continue
                // o TSE marca e="s" também em quem vai ao 2º turno (st = "2º turno"): isso não é eleito
                val vai2Turno = (cd["st"].texto() ?: "").lowercase().contains("turno")
                val pvap = cd["pvapn"].texto()?.ifEmpty { null } ?: cd["pvap"].texto()
                candidatos += Candidato(
                    nome = nome,
                    pct = decimalTse(pvap),
                    partido = partido,
                    votos = inteiroTse(cd["vap"].texto()),
                    numero = cd["n"].texto()?.toIntOrNull() ?: 0,
                    eleito = cd["e"].texto() == "s" && !vai2Turno,
                )
            }
        }
    }
    val s = raiz["s"].objeto()
    val v = raiz["v"].objeto()
    val ht = raiz["ht"].texto().orEmpty()
    return Apuracao(
        pctApurado = decimalTse(s?.get("pst").texto()),
        hora = ht.ifEmpty { raiz["hg"].texto().orEmpty() },
        // dt acompanha ht; sem ht, a data é a de geração (dg)
        data = (if (ht.isNotEmpty()) raiz["dt"].texto()?.ifEmpty { null } else null) ?: raiz["dg"].texto().orEmpty(),
        candidatos = candidatos.sortedByDescending { it.votos },
        validos = inteiroTse(v?.get("vv").texto()),
        brancos = inteiroTse(v?.get("vb").texto()),
        nulos = inteiroTse((v?.get("tvn") ?: v?.get("vn")).texto()),
        comparecimento = inteiroTse(raiz["e"].objeto()?.get("c").texto()),
    )
}
