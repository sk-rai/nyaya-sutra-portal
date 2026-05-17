package com.nyayasarathi.app.util

import retrofit2.HttpException
import java.net.SocketTimeoutException
import java.net.UnknownHostException
import java.io.IOException

object NetworkErrorMapper {
    fun map(throwable: Throwable): Result.Error = when (throwable) {
        is UnknownHostException -> Result.Error(
            message = "No internet connection",
            code = "OFFLINE",
            exception = throwable
        )
        is SocketTimeoutException -> Result.Error(
            message = "Request timed out. Please try again.",
            code = "TIMEOUT",
            exception = throwable
        )
        is IOException -> Result.Error(
            message = "Network error. Please check your connection.",
            code = "NETWORK",
            exception = throwable
        )
        is HttpException -> mapHttpError(throwable)
        else -> Result.Error(
            message = "An unexpected error occurred.",
            code = "UNKNOWN",
            exception = throwable
        )
    }

    private fun mapHttpError(e: HttpException): Result.Error = when (e.code()) {
        401 -> Result.Error("Session expired. Please log in again.", "AUTH_EXPIRED", e)
        403 -> Result.Error("Access denied.", "FORBIDDEN", e)
        404 -> Result.Error("Resource not found.", "NOT_FOUND", e)
        in 500..599 -> Result.Error("Server error. Please try again later.", "SERVER_ERROR", e)
        else -> Result.Error("Request failed (${e.code()}).", "HTTP_${e.code()}", e)
    }
}
