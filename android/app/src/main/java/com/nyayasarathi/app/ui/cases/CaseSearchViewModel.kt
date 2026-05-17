package com.nyayasarathi.app.ui.cases

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.data.remote.dto.CaseSearchData
import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.domain.repository.CaseRepository
import com.nyayasarathi.app.domain.repository.CourtRepository
import com.nyayasarathi.app.util.Result
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class CaseSearchViewModel @Inject constructor(
    private val caseRepository: CaseRepository,
    private val courtRepository: CourtRepository
) : ViewModel() {

    private val _searchState = MutableStateFlow<UiState<CaseSearchData>>(UiState.Idle)
    val searchState: StateFlow<UiState<CaseSearchData>> = _searchState.asStateFlow()

    private val _courts = MutableStateFlow<List<Court>>(emptyList())
    val courts: StateFlow<List<Court>> = _courts.asStateFlow()

    init {
        loadCourts()
    }

    private fun loadCourts() {
        viewModelScope.launch {
            when (val result = courtRepository.getCourts()) {
                is Result.Success -> _courts.value = result.data
                is Result.Error -> {
                    // Fallback to cached courts
                    val cached = courtRepository.getCachedCourts()
                    _courts.value = cached
                }
            }
        }
    }

    fun searchCase(courtCode: String, caseNumber: String) {
        viewModelScope.launch {
            _searchState.value = UiState.Loading
            when (val result = caseRepository.searchCase(courtCode, caseNumber)) {
                is Result.Success -> {
                    _searchState.value = UiState.Success(result.data)
                }
                is Result.Error -> {
                    _searchState.value = UiState.Error(result.message, result.code)
                }
            }
        }
    }

    fun trackCase(caseId: String) {
        viewModelScope.launch {
            when (val result = caseRepository.trackCase(caseId)) {
                is Result.Success -> {
                    // Case tracked successfully - no state change needed for search results
                }
                is Result.Error -> {
                    // Could emit a one-shot event here for error display
                }
            }
        }
    }
}
