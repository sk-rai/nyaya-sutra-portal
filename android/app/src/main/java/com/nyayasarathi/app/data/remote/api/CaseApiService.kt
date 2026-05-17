package com.nyayasarathi.app.data.remote.api

import com.nyayasarathi.app.data.remote.ApiResponse
import com.nyayasarathi.app.data.remote.dto.*
import retrofit2.http.*

interface CaseApiService {
    @GET("api/cases/search")
    suspend fun searchCase(
        @Query("court_code") courtCode: String,
        @Query("case_number") caseNumber: String
    ): ApiResponse<CaseSearchData>

    @GET("api/tracking")
    suspend fun getTrackedCases(): ApiResponse<TrackedCasesData>

    @POST("api/tracking")
    suspend fun trackCase(@Body request: TrackCaseRequest): ApiResponse<TrackCaseData>

    @DELETE("api/tracking/{case_id}")
    suspend fun untrackCase(@Path("case_id") caseId: String): ApiResponse<Unit>
}
