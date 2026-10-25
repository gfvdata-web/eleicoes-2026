package io.github.gfvdataweb.eleicoes2026.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.withContext
import okhttp3.HttpUrl
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.IOException
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.TimeUnit

/** Cargo disputado no 2º turno: [eleicao] e [codigo] são os do caminho dos arquivos do TSE. */
enum class Cargo(val eleicao: String, val codigo: String) {
    PRESIDENTE("6258", "0001"),
    GOVERNADOR("6260", "0003"),
}

/** Uma disputa: um cargo em uma abrangência [uf] ("br", sigla minúscula ou "zz" = Exterior). */
data class Disputa(val cargo: Cargo, val uf: String) {
    val caminho: String get() = "${cargo.eleicao}/dados/$uf/$uf-c${cargo.codigo}-e00${cargo.eleicao}-u.json"
}

/** O que uma rodada de consultas trouxe. [dados] só tem as disputas que já têm algum resultado (novo ou o anterior, em 304). */
data class Rodada(
    val dados: Map<Disputa, Apuracao>,
    /** Alguma consulta falhou por rede (IOException) ou por JSON inválido. */
    val semConexao: Boolean,
    /** O TSE respondeu 429 ou 503 a alguma consulta. */
    val limitado: Boolean,
)

/**
 * Lê a apuração direto do TSE. Até [PARALELAS] consultas ao mesmo tempo; guarda o
 * ETag de cada URL (pedido condicional, 304 reaproveita o último resultado) e o
 * intervalo de atualização: [INTERVALO_BASE_SEG], dobrado a cada rodada limitada
 * (429/503) até [INTERVALO_MAXIMO_SEG], de volta ao normal numa rodada sem limite.
 */
class Tse(
    private val cliente: OkHttpClient = clientePadrao(),
    private val base: HttpUrl = BASE,
) {
    private class Guardado(val etag: String?, val apuracao: Apuracao)

    private val guardados = ConcurrentHashMap<Disputa, Guardado>()

    /** Intervalo (segundos) até a próxima rodada; muda a cada [buscar]. */
    @Volatile
    var intervaloSeg: Int = INTERVALO_BASE_SEG
        private set

    private sealed interface Resultado {
        object Sucesso : Resultado
        object Limitado : Resultado
        object Falha : Resultado
    }

    /** Consulta todas as [disputas] (até 8 em paralelo) e atualiza o [intervaloSeg]. */
    suspend fun buscar(disputas: List<Disputa>): Rodada {
        val porta = Semaphore(PARALELAS)
        val resultados = coroutineScope {
            disputas.map { disputa -> async { porta.withPermit { consultar(disputa) } } }.map { it.await() }
        }
        val limitado = resultados.any { it == Resultado.Limitado }
        intervaloSeg = if (limitado) minOf(intervaloSeg * 2, INTERVALO_MAXIMO_SEG) else INTERVALO_BASE_SEG
        return Rodada(
            dados = disputas.mapNotNull { d -> guardados[d]?.let { d to it.apuracao } }.toMap(),
            semConexao = resultados.any { it == Resultado.Falha },
            limitado = limitado,
        )
    }

    private suspend fun consultar(disputa: Disputa): Resultado = withContext(Dispatchers.IO) {
        val url = base.resolve(disputa.caminho) ?: return@withContext Resultado.Falha
        val anterior = guardados[disputa]
        val pedido = Request.Builder().url(url).apply {
            anterior?.etag?.let { header("If-None-Match", it) }
        }.build()
        try {
            cliente.newCall(pedido).execute().use { resposta ->
                when {
                    resposta.code == 304 && anterior != null -> Resultado.Sucesso
                    resposta.code == 429 || resposta.code == 503 -> Resultado.Limitado
                    !resposta.isSuccessful -> Resultado.Falha
                    else -> {
                        val apuracao = converter(resposta.body.string())
                        guardados[disputa] = Guardado(resposta.header("ETag"), apuracao)
                        Resultado.Sucesso
                    }
                }
            }
        } catch (erro: IOException) {
            Resultado.Falha
        } catch (erro: IllegalArgumentException) {
            // JSON fora do formato (SerializationException é IllegalArgumentException)
            Resultado.Falha
        }
    }

    companion object {
        const val INTERVALO_BASE_SEG = 60
        const val INTERVALO_MAXIMO_SEG = 300
        const val PARALELAS = 8

        val BASE: HttpUrl = "https://resultados.tse.jus.br/oficial/ele2026/".toHttpUrl()

        fun clientePadrao(): OkHttpClient = OkHttpClient.Builder()
            .callTimeout(30, TimeUnit.SECONDS)
            .build()
    }
}

/** Nomes das 27 UFs (chave = sigla minúscula, ordem alfabética da sigla) e de `zz` = Exterior. */
val NOMES_UF: Map<String, String> = linkedMapOf(
    "ac" to "Acre", "al" to "Alagoas", "am" to "Amazonas", "ap" to "Amapá", "ba" to "Bahia",
    "ce" to "Ceará", "df" to "Distrito Federal", "es" to "Espírito Santo", "go" to "Goiás",
    "ma" to "Maranhão", "mg" to "Minas Gerais", "ms" to "Mato Grosso do Sul", "mt" to "Mato Grosso",
    "pa" to "Pará", "pb" to "Paraíba", "pe" to "Pernambuco", "pi" to "Piauí", "pr" to "Paraná",
    "rj" to "Rio de Janeiro", "rn" to "Rio Grande do Norte", "ro" to "Rondônia", "rr" to "Roraima",
    "rs" to "Rio Grande do Sul", "sc" to "Santa Catarina", "se" to "Sergipe", "sp" to "São Paulo",
    "to" to "Tocantins", "zz" to "Exterior",
)

/** Estados com 2º turno para governador. */
val UFS_GOVERNADOR: List<String> = listOf("ac", "am", "df", "es", "rn", "to")

val DISPUTAS_PRESIDENTE: List<Disputa> = listOf(Disputa(Cargo.PRESIDENTE, "br")) +
    NOMES_UF.keys.map { Disputa(Cargo.PRESIDENTE, it) }

val DISPUTAS_GOVERNADOR: List<Disputa> = UFS_GOVERNADOR.map { Disputa(Cargo.GOVERNADOR, it) }
