package io.github.gfvdataweb.eleicoes2026.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertThrows
import org.junit.Assert.assertTrue
import org.junit.Test

class ConversorTest {

    @Test
    fun fixtureRealDoBrasilComZeroApuradoDevolveOsCandidatosComZero() {
        val a = converter(fixtureTse("br-c0001-e006258-u.json"))

        assertEquals(listOf("FLAVIO BOLSONARO", "LULA"), a.candidatos.map { it.nome })
        assertEquals(0.0, a.pctApurado, 0.0)
        assertTrue(a.candidatos.all { it.pct == 0.0 && it.votos == 0L && !it.eleito })
        assertEquals("19:19:13", a.hora) // ht vazio: vale hg
        assertEquals("24/10/2026", a.data)
        assertEquals(listOf("PL", "PT"), a.candidatos.map { it.partido })
        assertNull(a.eleito)
    }

    @Test
    fun fixtureRealDoEspiritoSantoComZeroApurado() {
        val a = converter(fixtureTse("es-c0003-e006260-u.json"))

        assertEquals(listOf("LORENZO PAZOLINI", "RICARDO FERRAÇO"), a.candidatos.map { it.nome })
        assertEquals(0.0, a.pctApurado, 0.0)
        assertTrue(a.candidatos.all { it.pct == 0.0 })
        assertEquals("17:45:07", a.hora)
        assertEquals("REPUBLICANOS", a.candidatos[0].partido)
        assertEquals("MDB", a.candidatos[1].partido)
    }

    @Test
    fun apuracaoEmAndamentoLeVirgulaDecimalHoraDoTseETotais() {
        val bruto = jsonDoTse(
            "87,35",
            candidatoJson("LUIZ INACIO LULA DA SILVA", 13, "PT", 61_000_000, "51,20", nmu = "LULA"),
            candidatoJson("FLAVIO NANTES BOLSONARO", 22, "PL", 58_000_000, "48,80"),
            ht = "21:30:00",
            dt = "25/10/2026",
        )

        val a = converter(bruto)

        assertEquals(87.35, a.pctApurado, 0.0001)
        assertEquals("21:30:00", a.hora)
        assertEquals("25/10/2026", a.data)
        // nome: nmu quando existe, senão nm; ordem: mais votado primeiro
        assertEquals(listOf("LULA", "FLAVIO NANTES BOLSONARO"), a.candidatos.map { it.nome })
        assertEquals(51.20, a.candidatos[0].pct, 0.0001) // pvapn vazio: vale pvap
        assertEquals(61_000_000L, a.candidatos[0].votos)
        assertEquals(13, a.candidatos[0].numero)
        assertEquals("PT", a.candidatos[0].partido)
        assertEquals(900L, a.validos)
        assertEquals(50L, a.brancos)
        assertEquals(60L, a.nulos) // tvn antes de vn
        assertEquals(1000L, a.comparecimento)
        assertNull(a.eleito)
    }

    @Test
    fun candidatoMarcadoEleitoVira() {
        val bruto = jsonDoTse(
            "100,00",
            candidatoJson("A", 13, "PT", 70, "70,00", e = "s", st = "Eleito"),
            candidatoJson("B", 22, "PL", 30, "30,00"),
        )

        val a = converter(bruto)

        assertTrue(a.candidatos[0].eleito)
        assertFalse(a.candidatos[1].eleito)
        assertEquals("A", a.eleito?.nome)
    }

    @Test
    fun quemVaiAoSegundoTurnoNaoEEleito() {
        val bruto = jsonDoTse(
            "99,00",
            candidatoJson("A", 13, "PT", 48, "48,00", e = "s", st = "2º turno"),
            candidatoJson("B", 22, "PL", 40, "40,00", e = "s", st = "2º Turno"),
        )

        val a = converter(bruto)

        assertTrue(a.candidatos.none { it.eleito })
        assertNull(a.eleito)
    }

    @Test
    fun semTvnOsNulosVemDeVn() {
        val bruto = jsonDoTse("10,00", candidatoJson("A", 1, "X", 1, "1,00")).replace("\"tvn\": \"60\", ", "")

        assertEquals(10L, converter(bruto).nulos)
    }

    @Test
    fun jsonForaDoFormatoLancaIllegalArgument() {
        assertThrows(IllegalArgumentException::class.java) { converter("{ \"s\": {} }") }
        assertThrows(IllegalArgumentException::class.java) { converter("isto não é json") }
    }
}
