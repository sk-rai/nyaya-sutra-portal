package com.nyayasarathi.app.ui.cases

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.domain.model.TrackedCase
import com.nyayasarathi.app.domain.repository.CaseRepository
import com.nyayasarathi.app.util.Result
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class TrackedCasesViewModel @Inject constructor(
    private val caseRepository: CaseRepository
) : ViewModel() {

    private val _trackedCases = MutableStateFlow<UiState<List<TrackedCase>>>(UiState.Idle)
    val trackedCases: StateFlow<UiState<List<TrackedCase>>> = _trackedCases.asStateFlow()

    private val _isShowingStaleBanner = MutableStateFlow(false)
    val isShowingStaleBanner: StateFlow<Boolean> = _isShowingStaleBanner.asStateFlow()

    fun loadTrackedCases() {
        viewModelScope.launch {
            _trackedCases.value = UiState.Loading
            _isShowingStaleBanner.value = false

            when (val result = caseRepository.getTrackedCases()) {
                is Result.Success -> {
                    _trackedCases.value = UiState.Success(result.data)
                    _isShowingStaleBanner.value = false
                }
                is Result.Error -> {
                    // Attempt offline fallback
                    val cachedCases = caseRepository.getCachedTrackedCases()
                    if (cachedCases.isNotEmpty()) {
                        _trackedCases.value = UiState.Success(cachedCases)
                        _isShowingStaleBanner.value = true
                    } else {
                        _trackedCases.value = UiState.Error(result.message, result.code)
                        _isShowingStaleBanner.value = false
                    }
                }
            }
        }
    }

    fun untrackCase(caseId: String) {
        viewModelScope.launch {
            when (caseRepository.untrackCase(caseId)) {
                is Result.Success -> {
                    // Remove the case from the current list
                    val currentState = _trackedCases.value
                    if (currentState is UiState.Success) {
                        val updatedList = currentState.data.filter { it.id != caseId }
                        _trackedCases.value = UiState.Success(updatedList)
                    }
                }
                is Result.Error -> {
                    // Could emit a one-shot event for error display
                }
            }
        }
    }
}
