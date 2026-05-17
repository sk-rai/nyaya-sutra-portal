package com.nyayasarathi.app.data.remote.api

import com.nyayasarathi.app.data.remote.ApiResponse
import com.nyayasarathi.app.data.remote.dto.*
import retrofit2.http.Body
import retrofit2.http.POST

interface SubscriptionApiService {
    @POST("api/subscriptions/create-order")
    suspend fun createOrder(@Body request: CreateOrderRequest): ApiResponse<RazorpayOrderData>
}
