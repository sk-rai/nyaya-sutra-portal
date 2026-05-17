package com.nyayasarathi.app.domain.model

data class SubscriptionPlan(
    val id: String,
    val name: String,
    val tier: SubscriptionTier,
    val pricePerMonth: Int,
    val features: List<String>
)
