package com.nyayasarathi.app.data.local

import android.content.Context
import com.nyayasarathi.app.domain.model.SubscriptionTier
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SessionManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun saveToken(token: String) {
        prefs.edit().putString(KEY_TOKEN, token).apply()
    }

    fun getToken(): String? {
        return prefs.getString(KEY_TOKEN, null)
    }

    fun clearToken() {
        prefs.edit().remove(KEY_TOKEN).apply()
    }

    fun saveUserInfo(name: String, email: String, phone: String, userType: String, tier: SubscriptionTier) {
        prefs.edit()
            .putString(KEY_USER_NAME, name)
            .putString(KEY_USER_EMAIL, email)
            .putString(KEY_USER_PHONE, phone)
            .putString(KEY_USER_TYPE, userType)
            .putString(KEY_SUBSCRIPTION_TIER, tier.name)
            .apply()
    }

    fun getUserName(): String? {
        return prefs.getString(KEY_USER_NAME, null)
    }

    fun getUserEmail(): String? {
        return prefs.getString(KEY_USER_EMAIL, null)
    }

    fun getUserPhone(): String? {
        return prefs.getString(KEY_USER_PHONE, null)
    }

    fun getUserType(): String? {
        return prefs.getString(KEY_USER_TYPE, null)
    }

    fun getUserTier(): SubscriptionTier {
        val tierString = prefs.getString(KEY_SUBSCRIPTION_TIER, null) ?: return SubscriptionTier.FREE
        return try {
            SubscriptionTier.valueOf(tierString)
        } catch (e: IllegalArgumentException) {
            SubscriptionTier.FREE
        }
    }

    fun updateTier(tier: SubscriptionTier) {
        prefs.edit().putString(KEY_SUBSCRIPTION_TIER, tier.name).apply()
    }

    fun isLoggedIn(): Boolean {
        return getToken() != null
    }

    fun clearSession() {
        prefs.edit().clear().apply()
    }

    companion object {
        private const val PREFS_NAME = "nyaya_session"
        private const val KEY_TOKEN = "jwt_token"
        private const val KEY_USER_NAME = "user_name"
        private const val KEY_USER_EMAIL = "user_email"
        private const val KEY_USER_PHONE = "user_phone"
        private const val KEY_USER_TYPE = "user_type"
        private const val KEY_SUBSCRIPTION_TIER = "subscription_tier"
    }
}
