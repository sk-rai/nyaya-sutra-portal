package com.nyayasarathi.app.data.remote.api

import com.nyayasarathi.app.data.remote.ApiResponse
import com.nyayasarathi.app.data.remote.dto.*
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthApiService {
    @POST("api/auth/register")
    suspend fun register(@Body request: RegisterRequest): ApiResponse<RegisterData>

    @POST("api/auth/otp/request")
    suspend fun requestOtp(@Body request: OtpRequest): ApiResponse<OtpRequestData>

    @POST("api/auth/otp/verify")
    suspend fun verifyOtp(@Body request: OtpVerifyRequest): ApiResponse<OtpVerifyData>

    @POST("api/auth/logout")
    suspend fun logout(): ApiResponse<Unit>
}
