package com.nyayasarathi.app.data.repository

import com.nyayasarathi.app.data.local.db.TrackedCaseDao
import com.nyayasarathi.app.data.local.db.TrackedCaseEntity
import com.nyayasarathi.app.data.remote.api.CaseApiService
import com.nyayasarathi.app.data.remote.dto.CaseDto
import com.nyayasarathi.app.data.remote.dto.CaseSearchData
import com.nyayasarathi.app.data.remote.dto.TrackCaseData
import com.nyayasarathi.app.data.remote.dto.TrackCaseRequest
import com.nyayasarathi.app.domain.model.CaseStatus
import com.nyayasarathi.app.domain.model.TrackedCase
import com.nyayasarathi.app.domain.repository.CaseRepository
import com.nyayasarathi.app.util.NetworkErrorMapper
import com.nyayasarathi.app.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CaseRepositoryImpl @Inject constructor(
    private val caseApiService: CaseApiService,
    private val trackedCaseDao: TrackedCaseDao
) : CaseRepository {

    override suspend fun searchCase(courtCode: String, caseNumber: String): Result<CaseSearchData> {
        return try {
            val response = caseApiService.searchCase(courtCode, caseNumber)
            if (response.success && response.data != null) {
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Search failed",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun getTrackedCases(): Result<List<TrackedCase>> {
        return try {
            val response = caseApiService.getTrackedCases()
            if (response.success && response.data != null) {
                val cases = response.data.cases.map { it.toDomain() }
                // Cache to Room
                val entities = response.data.cases.map { it.toEntity() }
                trackedCaseDao.deleteAll()
                trackedCaseDao.insertAll(entities)
                Result.Success(cases)
            } else {
                // Try cache fallback
                val cached = getCachedTrackedCases()
                if (cached.isNotEmpty()) {
                    Result.Success(cached)
                } else {
                    Result.Error(
                        message = response.error?.message ?: "Failed to load tracked cases",
                        code = response.error?.code
                    )
                }
            }
        } catch (e: Exception) {
            // Try cache fallback on network error
            val cached = getCachedTrackedCases()
            if (cached.isNotEmpty()) {
                Result.Success(cached)
            } else {
                NetworkErrorMapper.map(e)
            }
        }
    }

    override suspend fun trackCase(caseId: String): Result<TrackCaseData> {
        return try {
            val response = caseApiService.trackCase(TrackCaseRequest(caseId))
            if (response.success && response.data != null) {
                Result.Success(response.data)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Failed to track case",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun untrackCase(caseId: String): Result<Unit> {
        return try {
            val response = caseApiService.untrackCase(caseId)
            if (response.success) {
                // Remove from local cache
                trackedCaseDao.deleteById(caseId)
                Result.Success(Unit)
            } else {
                Result.Error(
                    message = response.error?.message ?: "Failed to untrack case",
                    code = response.error?.code
                )
            }
        } catch (e: Exception) {
            NetworkErrorMapper.map(e)
        }
    }

    override suspend fun getCachedTrackedCases(): List<TrackedCase> {
        return trackedCaseDao.getAllTrackedCases().map { it.toDomain() }
    }

    private fun CaseDto.toDomain(): TrackedCase {
        return TrackedCase(
            id = id,
            caseNumber = caseNumber,
            courtCode = courtCode,
            courtName = courtName,
            parties = parties,
            status = parseCaseStatus(status),
            nextHearingDate = nextHearingDate,
            filingDate = filingDate
        )
    }

    private fun CaseDto.toEntity(): TrackedCaseEntity {
        return TrackedCaseEntity(
            id = id,
            caseNumber = caseNumber,
            courtCode = courtCode,
            courtName = courtName,
            parties = parties,
            status = status,
            nextHearingDate = nextHearingDate,
            filingDate = filingDate,
            lastUpdated = System.currentTimeMillis()
        )
    }

    private fun TrackedCaseEntity.toDomain(): TrackedCase {
        return TrackedCase(
            id = id,
            caseNumber = caseNumber,
            courtCode = courtCode,
            courtName = courtName,
            parties = parties,
            status = parseCaseStatus(status),
            nextHearingDate = nextHearingDate,
            filingDate = filingDate
        )
    }

    private fun parseCaseStatus(status: String): CaseStatus {
        return when (status.uppercase()) {
            "ACTIVE" -> CaseStatus.ACTIVE
            "PENDING" -> CaseStatus.PENDING
            "DISPOSED" -> CaseStatus.DISPOSED
            "ARCHIVED" -> CaseStatus.ARCHIVED
            else -> CaseStatus.ACTIVE
        }
    }
}
