package io.github.gfvdataweb.eleicoes2026

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import io.github.gfvdataweb.eleicoes2026.ui.ApuracaoTela
import io.github.gfvdataweb.eleicoes2026.ui.ApuracaoViewModel
import io.github.gfvdataweb.eleicoes2026.ui.theme.Apuracao2026Theme

/** Única Activity do app; a tela é Compose. */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent {
            Apuracao2026Theme {
                ApuracaoTela(viewModel(factory = ApuracaoViewModel.fabrica()))
            }
        }
    }
}
