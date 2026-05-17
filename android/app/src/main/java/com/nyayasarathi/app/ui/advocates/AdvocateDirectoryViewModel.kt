package com.nyayasarathi.app.ui.advocates

import androidx.lifecycle.ViewModel
import com.nyayasarathi.app.util.AdvocateFilterUtil
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

@HiltViewModel
class AdvocateDirectoryViewModel @Inject constructor() : ViewModel() {

    private val _advocates = MutableStateFlow<List<Advocate>>(emptyList())
    val advocates: StateFlow<List<Advocate>> = _advocates.asStateFlow()

    private val _filteredAdvocates = MutableStateFlow<List<Advocate>>(emptyList())
    val filteredAdvocates: StateFlow<List<Advocate>> = _filteredAdvocates.asStateFlow()

    private var nameQuery: String = ""
    private var selectedCourtCode: String? = null

    init {
        loadPlaceholderData()
    }

    private fun loadPlaceholderData() {
        val placeholderAdvocates = listOf(
            Advocate("1", "Adv. Rajesh Kumar", "DLHC", "Delhi High Court", "9876543210", "rajesh@example.com"),
            Advocate("2", "Adv. Priya Sharma", "BOMHC", "Bombay High Court", "9876543211", "priya@example.com"),
            Advocate("3", "Adv. Suresh Patel", "DLHC", "Delhi High Court", "9876543212", "suresh@example.com"),
            Advocate("4", "Adv. Meena Gupta", "MDHC", "Madras High Court", "9876543213", "meena@example.com"),
            Advocate("5", "Adv. Anil Verma", "SC", "Supreme Court", "9876543214", "anil@example.com"),
            Advocate("6", "Adv. Kavita Singh", "CALHC", "Calcutta High Court", "9876543215", "kavita@example.com"),
            Advocate("7", "Adv. Deepak Joshi", "BOMHC", "Bombay High Court", "9876543216", "deepak@example.com"),
            Advocate("8", "Adv. Sunita Rao", "KARHC", "Karnataka High Court", "9876543217", "sunita@example.com")
        )
        _advocates.value = placeholderAdvocates
        _filteredAdvocates.value = placeholderAdvocates
    }

    fun filterByName(query: String) {
        nameQuery = query
        applyFilters()
    }

    fun filterByCourt(courtCode: String?) {
        selectedCourtCode = courtCode
        applyFilters()
    }

    private fun applyFilters() {
        _filteredAdvocates.value = AdvocateFilterUtil.applyFilters(
            _advocates.value, nameQuery, selectedCourtCode
        )
    }
}
