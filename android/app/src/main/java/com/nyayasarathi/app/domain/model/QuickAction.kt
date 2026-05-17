package com.nyayasarathi.app.domain.model

data class QuickAction(
    val id: String,
    val title: String,
    val icon: Int,  // drawable resource id
    val destination: Int,  // navigation action id
    val requiredTier: SubscriptionTier
)
