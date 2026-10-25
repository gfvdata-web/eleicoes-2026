package io.github.gfvdataweb.eleicoes2026.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.PrimaryTabRow
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Tab
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.repeatOnLifecycle
import io.github.gfvdataweb.eleicoes2026.data.Apuracao
import io.github.gfvdataweb.eleicoes2026.data.Candidato
import io.github.gfvdataweb.eleicoes2026.data.Cargo
import io.github.gfvdataweb.eleicoes2026.data.DISPUTAS_GOVERNADOR
import io.github.gfvdataweb.eleicoes2026.data.DISPUTAS_PRESIDENTE
import io.github.gfvdataweb.eleicoes2026.data.Disputa
import io.github.gfvdataweb.eleicoes2026.ui.theme.LocalCoresDaApuracao

private val CORES_DOS_CANDIDATOS = listOf(Color(0xFF2563EB), Color(0xFFEA580C), Color(0xFF7C3AED), Color(0xFF0D9488))

/** Cor estável do candidato: pela posição na ordem do número da urna (não muda quando a ordem por votos muda). */
private fun corDoCandidato(candidato: Candidato, todos: List<Candidato>): Color {
    val indice = todos.sortedBy { it.numero }.indexOf(candidato)
    return CORES_DOS_CANDIDATOS[indice.coerceAtLeast(0) % CORES_DOS_CANDIDATOS.size]
}

/** Raiz da interface: barra superior, abas Presidente | Governador e a lista da aba. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ApuracaoTela(modelo: ApuracaoViewModel) {
    val estado by modelo.estado.collectAsStateWithLifecycle()
    // A consulta roda só com o app na tela (STARTED); em segundo plano, para.
    val ciclo = LocalLifecycleOwner.current.lifecycle
    LaunchedEffect(ciclo, modelo) {
        ciclo.repeatOnLifecycle(Lifecycle.State.STARTED) { modelo.acompanhar() }
    }
    var aba by rememberSaveable { mutableIntStateOf(0) }
    var porPctApurado by rememberSaveable { mutableIntStateOf(0) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Apuração 2026") },
                actions = {
                    IconButton(onClick = modelo::atualizarAgora) {
                        Icon(Icons.Default.Refresh, contentDescription = "Atualizar agora")
                    }
                },
            )
        },
    ) { margem ->
        Column(Modifier.fillMaxSize().padding(margem)) {
            PrimaryTabRow(selectedTabIndex = aba) {
                Tab(selected = aba == 0, onClick = { aba = 0 }, text = { Text("Presidente") })
                Tab(selected = aba == 1, onClick = { aba = 1 }, text = { Text("Governador") })
            }
            if (estado.semConexao || estado.limitado) {
                val cores = LocalCoresDaApuracao.current
                Text(
                    text = if (estado.semConexao) "sem conexão — mostrando o último resultado" else "TSE pediu mais calma — atualizando mais devagar",
                    color = cores.aviso,
                    style = MaterialTheme.typography.labelLarge,
                    modifier = Modifier.fillMaxWidth().background(cores.avisoFundo).padding(horizontal = 16.dp, vertical = 8.dp),
                )
            }
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                val verificado = estado.verificadoEm?.let { rotuloVerificado(it) }
                if (aba == 0) {
                    item {
                        CartaoDisputa("Brasil", estado.dados[Disputa(Cargo.PRESIDENTE, "br")], detalhado = true, verificado = verificado)
                    }
                    item { Ordem(porPctApurado == 1) { porPctApurado = if (it) 1 else 0 } }
                    val ufs = DISPUTAS_PRESIDENTE.filter { it.uf != "br" }
                    items(ordenar(ufs, estado.dados, porPctApurado == 1), key = { it.caminho }) { disputa ->
                        CartaoDisputa(nomeDaDisputa(disputa), estado.dados[disputa], detalhado = false)
                    }
                } else {
                    item { Ordem(porPctApurado == 1) { porPctApurado = if (it) 1 else 0 } }
                    items(ordenar(DISPUTAS_GOVERNADOR, estado.dados, porPctApurado == 1), key = { it.caminho }) { disputa ->
                        CartaoDisputa(nomeDaDisputa(disputa), estado.dados[disputa], detalhado = true)
                    }
                    if (verificado != null) item { Rodape(verificado) }
                }
            }
        }
    }
}

@Composable
private fun Rodape(texto: String) {
    Text(texto, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

/** Alternador de ordem da lista: Nome | % apurado. */
@Composable
private fun Ordem(porPctApurado: Boolean, aoMudar: (Boolean) -> Unit) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Ordenar por", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
        FilterChip(selected = !porPctApurado, onClick = { aoMudar(false) }, label = { Text("Nome") })
        FilterChip(selected = porPctApurado, onClick = { aoMudar(true) }, label = { Text("% apurado") })
    }
}

/**
 * Cartão de uma disputa: % apurado, barra dividida entre os candidatos (pelos votos)
 * e, em [detalhado], uma linha por candidato com % válidos e votos, mais os totais.
 * Sem [apuracao] (ainda não carregou), só o título.
 */
@Composable
private fun CartaoDisputa(titulo: String, apuracao: Apuracao?, detalhado: Boolean, verificado: String? = null) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
    ) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(titulo, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                if (apuracao != null) {
                    Text("${formatarPct(apuracao.pctApurado)} apurado", style = MaterialTheme.typography.titleSmall)
                }
            }
            if (apuracao == null) {
                Text("Aguardando dados do TSE", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                return@Column
            }
            Barra(apuracao.candidatos)
            if (detalhado) {
                apuracao.candidatos.forEach { LinhaDoCandidato(it, apuracao.candidatos) }
                Text(
                    "Válidos ${formatarVotos(apuracao.validos)} · Brancos ${formatarVotos(apuracao.brancos)} · " +
                        "Nulos ${formatarVotos(apuracao.nulos)} · Comparecimento ${formatarVotos(apuracao.comparecimento)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            } else {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    apuracao.candidatos.sortedBy { it.numero }.forEach { c ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Bolinha(corDoCandidato(c, apuracao.candidatos))
                            Spacer(Modifier.width(6.dp))
                            Text("${c.nome.substringBefore(' ')} ${formatarPct(c.pct)}", style = MaterialTheme.typography.bodySmall)
                            if (c.eleito) Selo("Eleito")
                        }
                    }
                }
            }
            Rodape(rotuloTse(apuracao))
            if (verificado != null) Rodape(verificado)
        }
    }
}

@Composable
private fun LinhaDoCandidato(candidato: Candidato, todos: List<Candidato>) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Bolinha(corDoCandidato(candidato, todos))
        Spacer(Modifier.width(8.dp))
        Column(Modifier.weight(1f)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(candidato.nome, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
                if (candidato.eleito) Selo("Eleito")
            }
            Text(candidato.partido, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Column(horizontalAlignment = Alignment.End) {
            Text(formatarPct(candidato.pct), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
            Text("${formatarVotos(candidato.votos)} votos", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun Bolinha(cor: Color) {
    Box(Modifier.size(10.dp).clip(CircleShape).background(cor))
}

/** Selo verde "Eleito". */
@Composable
private fun Selo(texto: String) {
    val cores = LocalCoresDaApuracao.current
    Text(
        texto,
        color = cores.ok,
        style = MaterialTheme.typography.labelSmall,
        fontWeight = FontWeight.SemiBold,
        modifier = Modifier.padding(start = 8.dp).clip(RoundedCornerShape(50)).background(cores.okFundo).padding(horizontal = 8.dp, vertical = 2.dp),
    )
}

/** Barra horizontal dividida pelos votos (na ordem do número da urna); sem votos ainda, uma faixa neutra. */
@Composable
private fun Barra(candidatos: List<Candidato>) {
    val comVotos = candidatos.sortedBy { it.numero }.filter { it.votos > 0 }
    val moldura = Modifier.fillMaxWidth().height(10.dp).clip(RoundedCornerShape(5.dp))
    if (comVotos.isEmpty()) {
        Box(moldura.background(MaterialTheme.colorScheme.outlineVariant))
    } else {
        Row(moldura) {
            comVotos.forEach { c ->
                Box(Modifier.weight(c.votos.toFloat()).fillMaxSize().background(corDoCandidato(c, candidatos)))
            }
        }
    }
}
