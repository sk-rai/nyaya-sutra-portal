package com.nyayasarathi.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class RegisterRequest(
    val name: String,
    val email: String,
    val phone: String,
    @SerializedName("user_type") val userType: String
)

data class RegisterData(
    val message: String,
    @SerializedName("user_id") val userId: String?
)

data class OtpRequest(
    val identifier: String,
    val purpose: String
)

data class OtpRequestData(
    val message: String,
    @SerializedName("expires_in") val expiresIn: Int?
)

data class OtpVerifyRequest(
    val identifier: String,
    @SerializedName("otp_code") val otpCode: String
)

data class OtpVerifyData(
    val token: String,
    val user: UserData
)

data class UserData(
    val id: String,
    val name: String,
    val email: String,
    val phone: String,
    @SerializedName("user_type") val userType: String,
    @SerializedName("subscription_tier") val subscriptionTier: String
)
