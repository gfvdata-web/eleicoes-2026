package io.github.gfvdataweb.eleicoes2026.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import io.github.gfvdataweb.eleicoes2026.data.Apuracao
import io.github.gfvdataweb.eleicoes2026.data.DISPUTAS_GOVERNADOR
import io.github.gfvdataweb.eleicoes2026.data.DISPUTAS_PRESIDENTE
import io.github.gfvdataweb.eleicoes2026.data.Disputa
import io.github.gfvdataweb.eleicoes2026.data.Tse
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.withTimeoutOrNull
import java.time.Instant

/** O que a tela mostra. Os [dados] ficam na memória: erro de rede mantém o último resultado. */
data class EstadoDaApuracao(
    val dados: Map<Disputa, Apuracao> = emptyMap(),
    val verificadoEm: Instant? = null,
    val semConexao: Boolean = false,
    val limitado: Boolean = false,
    val atualizando: Boolean = false,
)

/** Consulta o TSE enquanto a tela está visível (ver [acompanhar]); o intervalo é o do [Tse]. */
class ApuracaoViewModel(
    private val tse: Tse,
    private val agora: () -> Instant = Instant::now,
) : ViewModel() {
    private val _estado = MutableStateFlow(EstadoDaApuracao())
    val estado: StateFlow<EstadoDaApuracao> = _estado.asStateFlow()

    private val pedidos = Channel<Unit>(Channel.CONFLATED)

    /** Botão "Atualizar agora": encurta a espera da rodada atual. */
    fun atualizarAgora() {
        pedidos.trySend(Unit)
    }

    /**
     * Consulta, espera o intervalo (ou um pedido de "atualizar agora") e repete.
     * Quem chama usa `repeatOnLifecycle(STARTED)`: com o app fora da tela, para.
     */
    suspend fun acompanhar() {
        pedidos.tryReceive() // pedido antigo, de antes de a tela voltar
        while (true) {
            atualizar()
            withTimeoutOrNull(tse.intervaloSeg * 1000L) { pedidos.receive() }
        }
    }

    internal suspend fun atualizar() {
        _estado.update { it.copy(atualizando = true) }
        val rodada = tse.buscar(DISPUTAS_PRESIDENTE + DISPUTAS_GOVERNADOR)
        _estado.update {
            it.copy(
                // a rodada traz só o que já existe; o que veio antes e não veio agora fica
                dados = it.dados + rodada.dados,
                verificadoEm = agora(),
                semConexao = rodada.semConexao,
                limitado = rodada.limitado,
                atualizando = false,
            )
        }
    }

    companion object {
        fun fabrica() = viewModelFactory { initializer { ApuracaoViewModel(Tse()) } }
    }
}
