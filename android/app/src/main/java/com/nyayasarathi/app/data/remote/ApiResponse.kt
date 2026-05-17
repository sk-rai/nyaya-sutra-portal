package com.nyayasarathi.app.data.remote

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: ApiError?
)

data class ApiError(
    val code: String,
    val message: String
)
