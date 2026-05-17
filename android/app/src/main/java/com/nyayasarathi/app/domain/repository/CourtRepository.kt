package com.nyayasarathi.app.domain.repository

import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.util.Result

interface CourtRepository {
    suspend fun getCourts(): Result<List<Court>>
    suspend fun getCachedCourts(): List<Court>
}
