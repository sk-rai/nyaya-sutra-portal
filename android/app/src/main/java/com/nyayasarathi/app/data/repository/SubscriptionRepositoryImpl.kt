package com.nyayasarathi.app.data.repository

import com.nyayasarathi.app.data.local.SessionManager
import com.nyayasarathi.app.data.remote.api.SubscriptionApiService
import com.nyayasarathi.app.data.remote.dto.CreateOrderRequest
import com.nyayasarathi.app.data.remote.dto.RazorpayOrderData
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.domain.repository.SubscriptionRepository
import com.nyayasarathi.app.util.NetworkErrorMapper
import com.nyayasarathi.app.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SubscriptionRepositoryImpl @Inject constructor(
    private val subscriptionApiService: SubscriptionApiService,
    private val sessionManager: SessionManager
) : SubscriptionRepository {

    override suspend fun createOrder(planId: String): Result<RazorpayOrderData> {
        return try {
            val response = subscriptionApiService.createOrder(CreateOrderRequest(planId))
            if (response.success && response.data != null) {
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Failed to create order",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override fun getCurrentTier(): SubscriptionTier {
        return sessionManager.getUserTier()
    }

    override fun updateTier(tier: SubscriptionTier) {
        sessionManager.updateTier(tier)
    }
}
