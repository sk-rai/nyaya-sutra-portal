package com.nyayasarathi.app.data.repository

import com.nyayasarathi.app.data.local.SessionManager
import com.nyayasarathi.app.data.remote.api.AuthApiService
import com.nyayasarathi.app.data.remote.dto.*
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.domain.repository.AuthRepository
import com.nyayasarathi.app.util.NetworkErrorMapper
import com.nyayasarathi.app.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val authApiService: AuthApiService,
    private val sessionManager: SessionManager
) : AuthRepository {

    override suspend fun register(name: String, email: String, phone: String, userType: String): Result<RegisterData> {
        return try {
            val response = authApiService.register(RegisterRequest(name, email, phone, userType))
            if (response.success && response.data != null) {
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Registration failed",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun requestOtp(identifier: String, purpose: String): Result<OtpRequestData> {
        return try {
            val response = authApiService.requestOtp(OtpRequest(identifier, purpose))
            if (response.success && response.data != null) {
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Failed to send OTP",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun verifyOtp(identifier: String, otpCode: String): Result<OtpVerifyData> {
        return try {
            val response = authApiService.verifyOtp(OtpVerifyRequest(identifier, otpCode))
            if (response.success && response.data != null) {
                // Save session on successful verification
                val user = response.data.user
                val tier = SubscriptionTier.fromString(user.subscriptionTier)
                sessionManager.saveToken(response.data.token)
                sessionManager.saveUserInfo(user.name, user.email, user.phone, user.userType, tier)
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "OTP verification failed",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun logout(): Result<Unit> {
        return try {
            authApiService.logout()
            sessionManager.clearSession()
            Result.Success(Unit)
        } catch (e: Exception) {
            // Clear session even if API call fails
            sessionManager.clearSession()
            Result.Success(Unit)
        }
    }

    override fun isLoggedIn(): Boolean = sessionManager.isLoggedIn()

    override fun getToken(): String? = sessionManager.getToken()

    override fun getUserName(): String? = sessionManager.getUserName()

    override fun getUserTier(): SubscriptionTier = sessionManager.getUserTier()

    override fun clearSession() = sessionManager.clearSession()

    override fun saveSession(token: String, name: String, email: String, phone: String, userType: String, tier: SubscriptionTier) {
        sessionManager.saveToken(token)
        sessionManager.saveUserInfo(name, email, phone, userType, tier)
    }
}
