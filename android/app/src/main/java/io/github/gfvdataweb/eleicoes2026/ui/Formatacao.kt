package io.github.gfvdataweb.eleicoes2026.ui

import io.github.gfvdataweb.eleicoes2026.data.Apuracao
import io.github.gfvdataweb.eleicoes2026.data.Disputa
import io.github.gfvdataweb.eleicoes2026.data.NOMES_UF
import java.text.Collator
import java.text.NumberFormat
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Locale

// Formatação e ordenação puras (sem Compose), testáveis com JUnit.

private val PT_BR: Locale = Locale.forLanguageTag("pt-BR")

private val HORA = DateTimeFormatter.ofPattern("HH:mm:ss")

/** Votos com ponto de milhar: 12345678 -> "12.345.678". */
fun formatarVotos(votos: Long): String = NumberFormat.getIntegerInstance(PT_BR).format(votos)

/** Percentual com vírgula e duas casas: 51.2 -> "51,20%". */
fun formatarPct(pct: Double): String = String.format(PT_BR, "%.2f%%", pct)

/** "TSE: 24/10 19:19:13" (a data do TSE vem como dd/MM/aaaa). */
fun rotuloTse(apuracao: Apuracao): String {
    if (apuracao.hora.isEmpty()) return "TSE: —"
    val dia = apuracao.data.take(5)
    return if (dia.isEmpty()) "TSE: ${apuracao.hora}" else "TSE: $dia ${apuracao.hora}"
}

/** "verificado às 19:20:05", na hora local. */
fun rotuloVerificado(em: Instant, fuso: ZoneId = ZoneId.systemDefault()): String =
    "verificado às ${HORA.format(em.atZone(fuso))}"

/** Nome da disputa na lista: o da UF ("Espírito Santo", "Exterior"; "Brasil" para `br`). */
fun nomeDaDisputa(disputa: Disputa): String =
    if (disputa.uf == "br") "Brasil" else NOMES_UF[disputa.uf] ?: disputa.uf.uppercase()

/** Ordena as [disputas] por nome (alfabética, com acentos) ou, com [porPctApurado], do mais para o menos apurado. */
fun ordenar(disputas: List<Disputa>, dados: Map<Disputa, Apuracao>, porPctApurado: Boolean): List<Disputa> {
    val colador = Collator.getInstance(PT_BR)
    val porNome = Comparator<Disputa> { a, b -> colador.compare(nomeDaDisputa(a), nomeDaDisputa(b)) }
    if (!porPctApurado) return disputas.sortedWith(porNome)
    // sem dado ainda = -1, vai para o fim
    val porPct = compareByDescending<Disputa> { dados[it]?.pctApurado ?: -1.0 }
    return disputas.sortedWith(porPct.then(porNome))
}
