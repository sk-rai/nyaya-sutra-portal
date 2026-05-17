package com.nyayasarathi.app.ui.auth

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.nyayasarathi.app.R
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class RegisterFragment : Fragment() {

    private val authViewModel: AuthViewModel by activityViewModels()

    private lateinit var tilName: TextInputLayout
    private lateinit var etName: TextInputEditText
    private lateinit var tilEmail: TextInputLayout
    private lateinit var etEmail: TextInputEditText
    private lateinit var tilPhone: TextInputLayout
    private lateinit var etPhone: TextInputEditText
    private lateinit var tilUserType: TextInputLayout
    private lateinit var dropdownUserType: MaterialAutoCompleteTextView
    private lateinit var btnRegister: MaterialButton
    private lateinit var progressBar: LinearProgressIndicator
    private lateinit var tvError: TextView

    private val userTypes = arrayOf("individual", "advocate")

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_register, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tilName = view.findViewById(R.id.til_name)
        etName = view.findViewById(R.id.et_name)
        tilEmail = view.findViewById(R.id.til_email)
        etEmail = view.findViewById(R.id.et_email)
        tilPhone = view.findViewById(R.id.til_phone)
        etPhone = view.findViewById(R.id.et_phone)
        tilUserType = view.findViewById(R.id.til_user_type)
        dropdownUserType = view.findViewById(R.id.dropdown_user_type)
        btnRegister = view.findViewById(R.id.btn_register)
        progressBar = view.findViewById(R.id.progress_bar)
        tvError = view.findViewById(R.id.tv_error)

        setupDropdown()
        setupClickListeners()
        observeState()
    }

    private fun setupDropdown() {
        val adapter = ArrayAdapter(
            requireContext(),
            android.R.layout.simple_dropdown_item_1line,
            userTypes.map { it.replaceFirstChar { c -> c.uppercase() } }
        )
        dropdownUserType.setAdapter(adapter)
    }

    private fun setupClickListeners() {
        btnRegister.setOnClickListener {
            clearErrors()

            val name = etName.text?.toString() ?: ""
            val email = etEmail.text?.toString() ?: ""
            val phone = etPhone.text?.toString() ?: ""
            val userType = when (dropdownUserType.text?.toString()?.lowercase()) {
                "individual" -> "individual"
                "advocate" -> "advocate"
                else -> ""
            }

            val validation = authViewModel.validateRegistrationInput(name, email, phone)

            if (!validation.isValid) {
                validation.errors["name"]?.let { tilName.error = it }
                validation.errors["email"]?.let { tilEmail.error = it }
                validation.errors["phone"]?.let { tilPhone.error = it }
                return@setOnClickListener
            }

            if (userType.isEmpty()) {
                tilUserType.error = "Please select a user type"
                return@setOnClickListener
            }

            authViewModel.register(name.trim(), email.trim(), phone.trim(), userType)
        }
    }

    private fun clearErrors() {
        tilName.error = null
        tilEmail.error = null
        tilPhone.error = null
        tilUserType.error = null
        tvError.visibility = View.GONE
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                authViewModel.registrationState.collect { state ->
                    when (state) {
                        is UiState.Idle -> {
                            progressBar.visibility = View.GONE
                            btnRegister.isEnabled = true
                        }
                        is UiState.Loading -> {
                            progressBar.visibility = View.VISIBLE
                            tvError.visibility = View.GONE
                            btnRegister.isEnabled = false
                        }
                        is UiState.Success -> {
                            progressBar.visibility = View.GONE
                            btnRegister.isEnabled = true
                            val email = etEmail.text?.toString()?.trim() ?: ""
                            authViewModel.resetRegistrationState()
                            val action = RegisterFragmentDirections.actionRegisterToOtp(email)
                            findNavController().navigate(action)
                        }
                        is UiState.Error -> {
                            progressBar.visibility = View.GONE
                            btnRegister.isEnabled = true
                            tvError.text = state.message
                            tvError.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }
    }
}
