package com.nyayasarathi.app.util

import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.domain.model.CourtGroup
import com.nyayasarathi.app.domain.model.CourtType
import com.nyayasarathi.app.domain.model.StateCourtGroup

object CourtGroupingUtil {

    private val typeLabels = mapOf(
        CourtType.SC to "Supreme Court",
        CourtType.HC to "High Courts",
        CourtType.DC to "District Courts",
        CourtType.AFT to "Armed Forces Tribunal",
        CourtType.CAT to "Central Administrative Tribunal"
    )

    fun groupCourts(courts: List<Court>): List<CourtGroup> {
        val grouped = courts.groupBy { it.type }

        return CourtType.values().mapNotNull { type ->
            val courtsOfType = grouped[type] ?: return@mapNotNull null

            val subGroups = if (type == CourtType.HC || type == CourtType.DC) {
                courtsOfType
                    .groupBy { it.state ?: "Unknown" }
                    .map { (state, stateCourts) ->
                        StateCourtGroup(state = state, courts = stateCourts.sortedBy { it.name })
                    }
                    .sortedBy { it.state }
            } else {
                null
            }

            CourtGroup(
                type = type,
                label = typeLabels[type] ?: type.name,
                courts = courtsOfType.sortedBy { it.name },
                subGroups = subGroups
            )
        }
    }
}
