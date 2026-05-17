package com.nyayasarathi.app.domain.repository

import com.nyayasarathi.app.data.remote.dto.OtpRequestData
import com.nyayasarathi.app.data.remote.dto.OtpVerifyData
import com.nyayasarathi.app.data.remote.dto.RegisterData
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.util.Result

interface AuthRepository {
    suspend fun register(name: String, email: String, phone: String, userType: String): Result<RegisterData>
    suspend fun requestOtp(identifier: String, purpose: String): Result<OtpRequestData>
    suspend fun verifyOtp(identifier: String, otpCode: String): Result<OtpVerifyData>
    suspend fun logout(): Result<Unit>
    fun isLoggedIn(): Boolean
    fun getToken(): String?
    fun getUserName(): String?
    fun getUserTier(): SubscriptionTier
    fun clearSession()
    fun saveSession(token: String, name: String, email: String, phone: String, userType: String, tier: SubscriptionTier)
}
