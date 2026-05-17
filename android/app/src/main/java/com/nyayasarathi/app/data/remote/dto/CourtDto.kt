package com.nyayasarathi.app.data.remote.dto

import com.google.gson.annotations.SerializedName

data class CourtsData(
    val courts: List<CourtDto>
)

data class CourtDto(
    val id: String,
    val name: String,
    @SerializedName("court_code") val courtCode: String,
    val type: String,
    val state: String?,
    val district: String?,
    val address: String?,
    @SerializedName("vc_link") val vcLink: String?,
    val email: String?,
    @SerializedName("vc_match_id") val vcMatchId: String?,
    @SerializedName("proceedings_url") val proceedingsUrl: String?
)
