package com.nyayasarathi.app.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.data.remote.dto.OtpRequestData
import com.nyayasarathi.app.data.remote.dto.OtpVerifyData
import com.nyayasarathi.app.data.remote.dto.RegisterData
import com.nyayasarathi.app.domain.model.ValidationResult
import com.nyayasarathi.app.domain.repository.AuthRepository
import com.nyayasarathi.app.util.Result
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _registrationState = MutableStateFlow<UiState<RegisterData>>(UiState.Idle)
    val registrationState: StateFlow<UiState<RegisterData>> = _registrationState.asStateFlow()

    private val _otpRequestState = MutableStateFlow<UiState<OtpRequestData>>(UiState.Idle)
    val otpRequestState: StateFlow<UiState<OtpRequestData>> = _otpRequestState.asStateFlow()

    private val _otpVerifyState = MutableStateFlow<UiState<OtpVerifyData>>(UiState.Idle)
    val otpVerifyState: StateFlow<UiState<OtpVerifyData>> = _otpVerifyState.asStateFlow()

    fun register(name: String, email: String, phone: String, userType: String) {
        viewModelScope.launch {
            _registrationState.value = UiState.Loading
            when (val result = authRepository.register(name, email, phone, userType)) {
                is Result.Success -> {
                    _registrationState.value = UiState.Success(result.data)
                }
                is Result.Error -> {
                    _registrationState.value = UiState.Error(result.message, result.code)
                }
            }
        }
    }

    fun requestOtp(identifier: String) {
        viewModelScope.launch {
            _otpRequestState.value = UiState.Loading
            when (val result = authRepository.requestOtp(identifier, "login")) {
                is Result.Success -> {
                    _otpRequestState.value = UiState.Success(result.data)
                }
                is Result.Error -> {
                    _otpRequestState.value = UiState.Error(result.message, result.code)
                }
            }
        }
    }

    fun verifyOtp(identifier: String, otpCode: String) {
        viewModelScope.launch {
            _otpVerifyState.value = UiState.Loading
            when (val result = authRepository.verifyOtp(identifier, otpCode)) {
                is Result.Success -> {
                    _otpVerifyState.value = UiState.Success(result.data)
                }
                is Result.Error -> {
                    _otpVerifyState.value = UiState.Error(result.message, result.code)
                }
            }
        }
    }

    fun validateRegistrationInput(name: String, email: String, phone: String): ValidationResult {
        val errors = mutableMapOf<String, String>()

        if (name.trim().isEmpty()) {
            errors["name"] = "Name is required"
        }

        val emailRegex = Regex("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$")
        if (!emailRegex.matches(email.trim())) {
            errors["email"] = "Please enter a valid email address"
        }

        val phoneRegex = Regex("^[6-9]\\d{9}$")
        if (!phoneRegex.matches(phone.trim())) {
            errors["phone"] = "Please enter a valid 10-digit mobile number"
        }

        return ValidationResult(
            isValid = errors.isEmpty(),
            errors = errors
        )
    }

    fun resetOtpRequestState() {
        _otpRequestState.value = UiState.Idle
    }

    fun resetRegistrationState() {
        _registrationState.value = UiState.Idle
    }

    fun resetOtpVerifyState() {
        _otpVerifyState.value = UiState.Idle
    }
}
