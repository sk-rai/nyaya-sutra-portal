package com.nyayasarathi.app.domain.model

data class UserInfo(
    val name: String,
    val email: String,
    val phone: String,
    val userType: String,
    val tier: SubscriptionTier
)

enum class SubscriptionTier {
    FREE, INDIVIDUAL, ADVOCATE_NORMAL, ADVOCATE_PREMIUM;

    companion object {
        fun fromString(value: String): SubscriptionTier {
            return when (value.lowercase()) {
                "free" -> FREE
                "individual" -> INDIVIDUAL
                "advocate_normal" -> ADVOCATE_NORMAL
                "advocate_premium" -> ADVOCATE_PREMIUM
                else -> FREE
            }
        }
    }
}
