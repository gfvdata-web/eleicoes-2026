import org.gradle.api.tasks.testing.logging.TestExceptionFormat

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
}

// Versão do app. O CI injeta os dois valores (ORG_GRADLE_PROJECT_eleicoesVersionCode
// = número da run, que só cresce; eleicoesVersionName = rótulo legível). Sem eles,
// o build local fica com 1 / "dev".
val appVersionCode = providers.gradleProperty("eleicoesVersionCode").map(String::toInt).getOrElse(1)
val appVersionName = providers.gradleProperty("eleicoesVersionName").getOrElse("dev")

android {
    namespace = "io.github.gfvdataweb.eleicoes2026"
    compileSdk = libs.versions.compileSdk.get().toInt()

    defaultConfig {
        // Identidade do app no Android: depois de publicado NÃO muda.
        applicationId = "io.github.gfvdataweb.eleicoes2026"
        minSdk = libs.versions.minSdk.get().toInt()
        targetSdk = libs.versions.targetSdk.get().toInt()
        versionCode = appVersionCode
        versionName = appVersionName
    }

    buildTypes {
        debug {
            // O debug instala ao lado do app oficial (outro id, nome "(debug)").
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
        release {
            // Sem R8: o APK de release roda o mesmo código que os testes exercitam.
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    lint {
        // Lint barra o build em qualquer aviso. Ficam de fora só as checagens
        // que dependem da data (versão nova publicada etc.).
        abortOnError = true
        warningsAsErrors = true
        disable += setOf(
            "GradleDependency",
            "NewerVersionAvailable",
            "AndroidGradlePluginVersion",
            "OldTargetApi",
        )
    }
}

kotlin {
    compilerOptions {
        // Aviso do compilador também quebra o build.
        allWarningsAsErrors = true
    }
}

tasks.withType<Test>().configureEach {
    testLogging {
        events("failed")
        exceptionFormat = TestExceptionFormat.FULL
    }
}

dependencies {
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.material.icons.core)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.okhttp)

    testImplementation(libs.junit)
    testImplementation(libs.okhttp.mockwebserver)
}
