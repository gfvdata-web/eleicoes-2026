package io.github.gfvdataweb.eleicoes2026.data

import kotlinx.coroutines.runBlocking
import mockwebserver3.Dispatcher
import mockwebserver3.MockResponse
import mockwebserver3.MockWebServer
import mockwebserver3.RecordedRequest
import okhttp3.Headers.Companion.headersOf
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.concurrent.CopyOnWriteArrayList
import java.util.concurrent.atomic.AtomicInteger

/** [Tse] contra um TSE local (MockWebServer), em `/oficial/ele2026/`. Nada acessa a internet. */
class TseTest {

    private val corpo = jsonDoTse(
        "87,35",
        candidatoJson("LUIZ INACIO LULA DA SILVA", 13, "PT", 61, "51,20", nmu = "LULA"),
        candidatoJson("FLAVIO NANTES BOLSONARO", 22, "PL", 58, "48,80", nmu = "FLAVIO BOLSONARO"),
    )

    /** Resposta do servidor de teste; os testes trocam [codigo] no meio do caminho. */
    @Volatile private var codigo = 200
    private val etagsRecebidos = CopyOnWriteArrayList<String?>()
    private val pedidos = AtomicInteger()
    private val caminhos = CopyOnWriteArrayList<String>()

    private val servidor = MockWebServer().apply {
        dispatcher = object : Dispatcher() {
            override fun dispatch(request: RecordedRequest): MockResponse {
                pedidos.incrementAndGet()
                caminhos += request.url.encodedPath
                val etag = request.headers["If-None-Match"]
                etagsRecebidos += etag
                return when {
                    codigo != 200 -> MockResponse(code = codigo)
                    etag == "\"v1\"" -> MockResponse(code = 304, headers = headersOf("ETag", "\"v1\""))
                    else -> MockResponse(code = 200, headers = headersOf("ETag", "\"v1\""), body = corpo)
                }
            }
        }
        start()
    }

    private val tse = Tse(OkHttpClient(), servidor.url("/oficial/ele2026/"))
    private val brasil = Disputa(Cargo.PRESIDENTE, "br")

    @After
    fun fecha() = servidor.close()

    @Test
    fun caminhoSegueOPadraoDoTse() {
        assertEquals("6258/dados/br/br-c0001-e006258-u.json", brasil.caminho)
        assertEquals("6260/dados/es/es-c0003-e006260-u.json", Disputa(Cargo.GOVERNADOR, "es").caminho)
        assertEquals(29, DISPUTAS_PRESIDENTE.size) // br + 27 UFs + zz
        assertEquals(6, DISPUTAS_GOVERNADOR.size)
    }

    @Test
    fun primeiraBuscaBaixaEConverte() = runBlocking {
        val rodada = tse.buscar(listOf(brasil))

        assertEquals(87.35, rodada.dados.getValue(brasil).pctApurado, 0.0001)
        assertFalse(rodada.semConexao)
        assertFalse(rodada.limitado)
        assertEquals(listOf("/oficial/ele2026/6258/dados/br/br-c0001-e006258-u.json"), caminhos.toList())
        assertEquals(60, tse.intervaloSeg)
    }

    @Test
    fun etagVoltaNoPedidoSeguinteE304ReaproveitaOUltimoResultado() = runBlocking {
        tse.buscar(listOf(brasil))
        val rodada = tse.buscar(listOf(brasil))

        assertEquals(listOf(null, "\"v1\""), etagsRecebidos.toList())
        assertEquals(87.35, rodada.dados.getValue(brasil).pctApurado, 0.0001)
        assertEquals("LULA", rodada.dados.getValue(brasil).candidatos[0].nome)
        assertFalse(rodada.semConexao)
        assertFalse(rodada.limitado)
    }

    @Test
    fun resposta429DobraOIntervaloAteOMaximoEVoltaAoNormalNoSucesso() = runBlocking {
        codigo = 429
        val esperado = listOf(120, 240, 300, 300)
        for (intervalo in esperado) {
            val rodada = tse.buscar(listOf(brasil))
            assertTrue(rodada.limitado)
            assertTrue(rodada.dados.isEmpty())
            assertEquals(intervalo, tse.intervaloSeg)
        }

        codigo = 200
        val rodada = tse.buscar(listOf(brasil))
        assertFalse(rodada.limitado)
        assertEquals(60, tse.intervaloSeg)
        assertEquals(1, rodada.dados.size)
    }

    @Test
    fun resposta503TambemDobraEMantemOUltimoResultado() = runBlocking {
        tse.buscar(listOf(brasil))
        codigo = 503

        val rodada = tse.buscar(listOf(brasil))

        assertTrue(rodada.limitado)
        assertEquals(120, tse.intervaloSeg)
        assertEquals(87.35, rodada.dados.getValue(brasil).pctApurado, 0.0001)
    }

    @Test
    fun erroDoServidorMantemOUltimoResultadoEMarcaSemConexao() = runBlocking {
        tse.buscar(listOf(brasil))
        codigo = 500

        val rodada = tse.buscar(listOf(brasil))

        assertTrue(rodada.semConexao)
        assertFalse(rodada.limitado)
        assertEquals(60, tse.intervaloSeg)
        assertEquals(1, rodada.dados.size)
    }

    @Test
    fun semServidorMarcaSemConexao() = runBlocking {
        val semServidor = Tse(OkHttpClient(), "http://localhost:1/oficial/ele2026/".toHttpUrl())

        val rodada = semServidor.buscar(listOf(brasil))

        assertTrue(rodada.semConexao)
        assertTrue(rodada.dados.isEmpty())
    }

    @Test
    fun buscaTodasAsDisputasPedidas() = runBlocking {
        val rodada = tse.buscar(DISPUTAS_PRESIDENTE + DISPUTAS_GOVERNADOR)

        assertEquals(35, rodada.dados.size)
        assertEquals(35, pedidos.get())
    }
}
