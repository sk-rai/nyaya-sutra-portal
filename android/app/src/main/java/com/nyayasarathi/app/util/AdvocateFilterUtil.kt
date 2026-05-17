package com.nyayasarathi.app.util

import com.nyayasarathi.app.ui.advocates.Advocate

object AdvocateFilterUtil {

    fun filterByName(advocates: List<Advocate>, query: String): List<Advocate> {
        if (query.isBlank()) return advocates
        val lowerQuery = query.lowercase()
        return advocates.filter { it.name.lowercase().contains(lowerQuery) }
    }

    fun filterByCourt(advocates: List<Advocate>, courtCode: String?): List<Advocate> {
        if (courtCode.isNullOrBlank()) return advocates
        return advocates.filter { it.courtCode == courtCode }
    }

    fun applyFilters(advocates: List<Advocate>, nameQuery: String, courtCode: String?): List<Advocate> {
        return filterByCourt(filterByName(advocates, nameQuery), courtCode)
    }
}
