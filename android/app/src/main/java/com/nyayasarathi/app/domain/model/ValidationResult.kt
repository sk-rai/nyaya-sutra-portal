package com.nyayasarathi.app.domain.model

data class ValidationResult(
    val isValid: Boolean,
    val errors: Map<String, String> = emptyMap()
)
