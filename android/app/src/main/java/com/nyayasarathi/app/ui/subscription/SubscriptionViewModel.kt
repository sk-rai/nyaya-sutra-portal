package com.nyayasarathi.app.ui.subscription

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.data.remote.dto.RazorpayOrderData
import com.nyayasarathi.app.domain.model.SubscriptionPlan
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.domain.repository.SubscriptionRepository
import com.nyayasarathi.app.util.Result
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class SubscriptionViewModel @Inject constructor(
    private val subscriptionRepository: SubscriptionRepository
) : ViewModel() {

    private val _plans = MutableStateFlow<List<SubscriptionPlan>>(emptyList())
    val plans: StateFlow<List<SubscriptionPlan>> = _plans.asStateFlow()

    private val _orderState = MutableStateFlow<UiState<RazorpayOrderData>>(UiState.Idle)
    val orderState: StateFlow<UiState<RazorpayOrderData>> = _orderState.asStateFlow()

    private val _currentTier = MutableStateFlow(subscriptionRepository.getCurrentTier())
    val currentTier: StateFlow<SubscriptionTier> = _currentTier.asStateFlow()

    init {
        loadPlans()
    }

    private fun loadPlans() {
        _plans.value = listOf(
            SubscriptionPlan(
                id = "free",
                name = "Free",
                tier = SubscriptionTier.FREE,
                pricePerMonth = 0,
                features = listOf("Court Directory", "Court Calendar", "Legal Resources")
            ),
            SubscriptionPlan(
                id = "individual",
                name = "Individual",
                tier = SubscriptionTier.INDIVIDUAL,
                pricePerMonth = 50,
                features = listOf("All Free features", "Case Tracking (up to 5)", "Advocate Directory")
            ),
            SubscriptionPlan(
                id = "advocate_normal",
                name = "Advocate Normal",
                tier = SubscriptionTier.ADVOCATE_NORMAL,
                pricePerMonth = 199,
                features = listOf("All Individual features", "Unlimited Case Tracking", "Register Court Matter", "Display Board", "Cause List")
            ),
            SubscriptionPlan(
                id = "advocate_premium",
                name = "Advocate Premium",
                tier = SubscriptionTier.ADVOCATE_PREMIUM,
                pricePerMonth = 599,
                features = listOf("All Advocate Normal features", "e-Filing Access", "e-Gate Pass", "Priority Support")
            )
        )
    }

    fun createOrder(planId: String) {
        viewModelScope.launch {
            _orderState.value = UiState.Loading
            when (val result = subscriptionRepository.createOrder(planId)) {
                is Result.Success -> {
                    _orderState.value = UiState.Success(result.data)
                }
                is Result.Error -> {
                    _orderState.value = UiState.Error(result.message, result.code)
                }
            }
        }
    }

    fun onPaymentSuccess(paymentId: String, orderId: String, signature: String) {
        // Update local tier after successful payment
        // In a real app, verify with backend first
        val plan = _plans.value.find { orderState.value is UiState.Success }
        // For now, just reset order state
        _orderState.value = UiState.Idle
    }

    fun onPaymentFailure(errorCode: Int, errorMessage: String) {
        _orderState.value = UiState.Error("Payment failed: $errorMessage")
    }
}
