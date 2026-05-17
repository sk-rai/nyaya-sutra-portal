package com.nyayasarathi.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class CaseSearchData(
    val cases: List<CaseDto>
)

data class CaseDto(
    val id: String,
    @SerializedName("case_number") val caseNumber: String,
    @SerializedName("court_code") val courtCode: String,
    @SerializedName("court_name") val courtName: String,
    val parties: String,
    val status: String,
    @SerializedName("next_hearing_date") val nextHearingDate: String?,
    @SerializedName("filing_date") val filingDate: String?
)

data class TrackCaseRequest(
    @SerializedName("case_id") val caseId: String
)

data class TrackCaseData(
    val message: String,
    @SerializedName("tracked_case") val trackedCase: CaseDto?
)

data class TrackedCasesData(
    val cases: List<CaseDto>
)
