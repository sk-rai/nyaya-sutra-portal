package com.nyayasarathi.app.domain.repository

import com.nyayasarathi.app.data.remote.dto.RazorpayOrderData
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.util.Result

interface SubscriptionRepository {
    suspend fun createOrder(planId: String): Result<RazorpayOrderData>
    fun getCurrentTier(): SubscriptionTier
    fun updateTier(tier: SubscriptionTier)
}
