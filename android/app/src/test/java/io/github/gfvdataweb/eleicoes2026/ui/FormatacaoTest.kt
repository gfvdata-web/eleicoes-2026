package io.github.gfvdataweb.eleicoes2026.ui

import io.github.gfvdataweb.eleicoes2026.data.Apuracao
import io.github.gfvdataweb.eleicoes2026.data.Cargo
import io.github.gfvdataweb.eleicoes2026.data.Disputa
import org.junit.Assert.assertEquals
import org.junit.Test
import java.time.Instant
import java.time.ZoneId

class FormatacaoTest {

    private fun apuracao(pct: Double, hora: String = "19:19:13", data: String = "24/10/2026") =
        Apuracao(pct, hora, data, emptyList(), 0, 0, 0, 0)

    @Test
    fun votosComPontoDeMilhar() {
        assertEquals("12.345.678", formatarVotos(12_345_678))
        assertEquals("0", formatarVotos(0))
    }

    @Test
    fun percentualComVirgula() {
        assertEquals("51,20%", formatarPct(51.2))
        assertEquals("0,00%", formatarPct(0.0))
    }

    @Test
    fun rotuloDoTseUsaDiaMesEHora() {
        assertEquals("TSE: 24/10 19:19:13", rotuloTse(apuracao(0.0)))
        assertEquals("TSE: —", rotuloTse(apuracao(0.0, hora = "")))
    }

    @Test
    fun rotuloVerificadoNaHoraLocal() {
        val instante = Instant.parse("2026-10-25T22:20:05Z")

        assertEquals("verificado às 19:20:05", rotuloVerificado(instante, ZoneId.of("America/Sao_Paulo")))
    }

    @Test
    fun ordenaPorNomeComAcentosEPorPctApurado() {
        val pa = Disputa(Cargo.PRESIDENTE, "pa")
        val pb = Disputa(Cargo.PRESIDENTE, "pb")
        val pr = Disputa(Cargo.PRESIDENTE, "pr")
        val dados = mapOf(pa to apuracao(10.0), pb to apuracao(90.0))

        // Pará, Paraíba, Paraná (o "í" não vai depois do "n")
        assertEquals(listOf(pa, pb, pr), ordenar(listOf(pr, pb, pa), dados, porPctApurado = false))
        // mais apurado primeiro; sem dado por último
        assertEquals(listOf(pb, pa, pr), ordenar(listOf(pr, pa, pb), dados, porPctApurado = true))
    }
}
