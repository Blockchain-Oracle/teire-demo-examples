plugins {
    alias(libs.plugins.kotlin.jvm)
}

repositories {
    mavenCentral()
}

// Every resolved version is recorded in gradle.lockfile.
dependencyLocking {
    lockAllConfigurations()
}

dependencies {
    implementation(libs.okhttp)
    testImplementation(libs.junit.jupiter)
    testRuntimeOnly(libs.junit.platform.launcher)
}

kotlin {
    jvmToolchain(21)
}

tasks.test {
    useJUnitPlatform()
}

dependencies {
    constraints {
        implementation("com.squareup.okio:okio:1.17.6") {
            because("Teire: fixes GHSA-w33c-445m-f8w7")
        }
    }
}
