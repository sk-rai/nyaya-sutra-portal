package com.nyayasarathi.app.domain.model

data class Court(
    val id: String,
    val name: String,
    val courtCode: String,
    val type: CourtType,
    val state: String?,
    val district: String?,
    val address: String?,
    val vcLink: String?,
    val email: String?,
    val proceedingsUrl: String?
)

enum class CourtType { SC, HC, DC, AFT, CAT }

data class CourtGroup(
    val type: CourtType,
    val label: String,
    val courts: List<Court>,
    val subGroups: List<StateCourtGroup>?
)

data class StateCourtGroup(
    val state: String,
    val courts: List<Court>
)
