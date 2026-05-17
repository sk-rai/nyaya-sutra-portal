package com.nyayasarathi.app.util

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(
        val message: String,
        val code: String? = null,
        val exception: Throwable? = null
    ) : Result<Nothing>()
}
