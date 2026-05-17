package com.nyayasarathi.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class CreateOrderRequest(
    @SerializedName("plan_id") val planId: String
)

data class RazorpayOrderData(
    @SerializedName("order_id") val orderId: String,
    val amount: Int,
    val currency: String,
    @SerializedName("razorpay_key") val razorpayKey: String
)
