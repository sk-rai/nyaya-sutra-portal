package com.nyayasarathi.app.ui.courts

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.domain.model.CourtGroup
import com.nyayasarathi.app.domain.repository.CourtRepository
import com.nyayasarathi.app.util.CourtGroupingUtil
import com.nyayasarathi.app.util.Result
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class CourtDirectoryViewModel @Inject constructor(
    private val courtRepository: CourtRepository
) : ViewModel() {

    private val _courtHierarchy = MutableStateFlow<UiState<List<CourtGroup>>>(UiState.Idle)
    val courtHierarchy: StateFlow<UiState<List<CourtGroup>>> = _courtHierarchy.asStateFlow()

    init {
        loadCourts()
    }

    fun loadCourts() {
        viewModelScope.launch {
            _courtHierarchy.value = UiState.Loading
            when (val result = courtRepository.getCourts()) {
                is Result.Success -> {
                    val groups = CourtGroupingUtil.groupCourts(result.data)
                    _courtHierarchy.value = UiState.Success(groups)
                }
                is Result.Error -> {
                    // Fallback to cached courts
                    val cached = courtRepository.getCachedCourts()
                    if (cached.isNotEmpty()) {
                        val groups = CourtGroupingUtil.groupCourts(cached)
                        _courtHierarchy.value = UiState.Success(groups)
                    } else {
                        _courtHierarchy.value = UiState.Error(result.message, result.code)
                    }
                }
            }
        }
    }
}
