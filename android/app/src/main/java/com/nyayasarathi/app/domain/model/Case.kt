package com.nyayasarathi.app.domain.model

data class TrackedCase(
    val id: String,
    val caseNumber: String,
    val courtCode: String,
    val courtName: String,
    val parties: String,
    val status: CaseStatus,
    val nextHearingDate: String?,
    val filingDate: String?
)

enum class CaseStatus { ACTIVE, PENDING, DISPOSED, ARCHIVED }
