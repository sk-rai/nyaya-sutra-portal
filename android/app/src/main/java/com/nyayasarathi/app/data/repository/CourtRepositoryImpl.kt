package com.nyayasarathi.app.data.repository

import com.nyayasarathi.app.data.local.db.CourtDao
import com.nyayasarathi.app.data.local.db.CourtEntity
import com.nyayasarathi.app.data.remote.api.CourtApiService
import com.nyayasarathi.app.data.remote.dto.CourtDto
import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.domain.model.CourtType
import com.nyayasarathi.app.domain.repository.CourtRepository
import com.nyayasarathi.app.util.NetworkErrorMapper
import com.nyayasarathi.app.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CourtRepositoryImpl @Inject constructor(
    private val courtApiService: CourtApiService,
    private val courtDao: CourtDao
) : CourtRepository {

    override suspend fun getCourts(): Result<List<Court>> {
        return try {
            val response = courtApiService.getCourts()
            if (response.success && response.data != null) {
                val courts = response.data.courts.map { it.toDomain() }
                // Cache to Room
                val entities = response.data.courts.map { it.toEntity() }
                courtDao.deleteAll()
                courtDao.insertAll(entities)
                Result.Success(courts)
            } else {
                // Try cache fallback
                val cached = getCachedCourts()
                if (cached.isNotEmpty()) {
                    Result.Success(cached)
                } else {
                    Result.Error(
                        message = response.error?.message ?: "Failed to load courts",
                        code = response.error?.code
                    )
                }
            }
        } catch (e: Exception) {
            // Try cache fallback on network error
            val cached = getCachedCourts()
            if (cached.isNotEmpty()) {
                Result.Success(cached)
            } else {
                NetworkErrorMapper.map(e)
            }
        }
    }

    override suspend fun getCachedCourts(): List<Court> {
        return courtDao.getAllCourts().map { it.toDomain() }
    }

    private fun CourtDto.toDomain(): Court {
        return Court(
            id = id,
            name = name,
            courtCode = courtCode,
            type = parseCourtType(type),
            state = state,
            district = district,
            address = address,
            vcLink = vcLink,
            email = email,
            proceedingsUrl = proceedingsUrl
        )
    }

    private fun CourtDto.toEntity(): CourtEntity {
        return CourtEntity(
            id = id,
            name = name,
            courtCode = courtCode,
            type = type,
            state = state,
            district = district,
            address = address,
            vcLink = vcLink,
            email = email,
            proceedingsUrl = proceedingsUrl,
            lastUpdated = System.currentTimeMillis()
        )
    }

    private fun CourtEntity.toDomain(): Court {
        return Court(
            id = id,
            name = name,
            courtCode = courtCode,
            type = parseCourtType(type),
            state = state,
            district = district,
            address = address,
            vcLink = vcLink,
            email = email,
            proceedingsUrl = proceedingsUrl
        )
    }

    private fun parseCourtType(type: String): CourtType {
        return when (type.uppercase()) {
            "SC" -> CourtType.SC
            "HC" -> CourtType.HC
            "DC" -> CourtType.DC
            "AFT" -> CourtType.AFT
            "CAT" -> CourtType.CAT
            else -> CourtType.DC
        }
    }
}
