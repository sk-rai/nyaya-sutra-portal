package com.nyayasarathi.app.data.remote.api

import com.nyayasarathi.app.data.remote.ApiResponse
import com.nyayasarathi.app.data.remote.dto.CourtsData
import retrofit2.http.GET

interface CourtApiService {
    @GET("api/courts")
    suspend fun getCourts(): ApiResponse<CourtsData>
}
