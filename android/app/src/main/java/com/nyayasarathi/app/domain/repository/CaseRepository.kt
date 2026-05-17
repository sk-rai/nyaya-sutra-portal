package com.nyayasarathi.app.domain.repository

import com.nyayasarathi.app.data.remote.dto.CaseSearchData
import com.nyayasarathi.app.data.remote.dto.TrackCaseData
import com.nyayasarathi.app.domain.model.TrackedCase
import com.nyayasarathi.app.util.Result

interface CaseRepository {
    suspend fun searchCase(courtCode: String, caseNumber: String): Result<CaseSearchData>
    suspend fun getTrackedCases(): Result<List<TrackedCase>>
    suspend fun trackCase(caseId: String): Result<TrackCaseData>
    suspend fun untrackCase(caseId: String): Result<Unit>
    suspend fun getCachedTrackedCases(): List<TrackedCase>
}
