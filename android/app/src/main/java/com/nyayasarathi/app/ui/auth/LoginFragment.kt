package com.nyayasarathi.app.ui.auth

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.nyayasarathi.app.R
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class LoginFragment : Fragment() {

    private val authViewModel: AuthViewModel by activityViewModels()

    private lateinit var tilIdentifier: TextInputLayout
    private lateinit var etIdentifier: TextInputEditText
    private lateinit var btnRequestOtp: MaterialButton
    private lateinit var progressBar: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var tvRegisterLink: TextView

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_login, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tilIdentifier = view.findViewById(R.id.til_identifier)
        etIdentifier = view.findViewById(R.id.et_identifier)
        btnRequestOtp = view.findViewById(R.id.btn_request_otp)
        progressBar = view.findViewById(R.id.progress_bar)
        tvError = view.findViewById(R.id.tv_error)
        tvRegisterLink = view.findViewById(R.id.tv_register_link)

        setupClickListeners()
        observeState()
    }

    private fun setupClickListeners() {
        btnRequestOtp.setOnClickListener {
            val identifier = etIdentifier.text?.toString()?.trim() ?: ""
            if (identifier.isEmpty()) {
                tilIdentifier.error = "Please enter your email or phone number"
                return@setOnClickListener
            }
            tilIdentifier.error = null
            authViewModel.requestOtp(identifier)
        }

        tvRegisterLink.setOnClickListener {
            findNavController().navigate(R.id.action_login_to_register)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                authViewModel.otpRequestState.collect { state ->
                    when (state) {
                        is UiState.Idle -> {
                            progressBar.visibility = View.GONE
                            tvError.visibility = View.GONE
                            btnRequestOtp.isEnabled = true
                        }
                        is UiState.Loading -> {
                            progressBar.visibility = View.VISIBLE
                            tvError.visibility = View.GONE
                            btnRequestOtp.isEnabled = false
                        }
                        is UiState.Success -> {
                            progressBar.visibility = View.GONE
                            btnRequestOtp.isEnabled = true
                            val identifier = etIdentifier.text?.toString()?.trim() ?: ""
                            authViewModel.resetOtpRequestState()
                            val action = LoginFragmentDirections.actionLoginToOtp(identifier)
                            findNavController().navigate(action)
                        }
                        is UiState.Error -> {
                            progressBar.visibility = View.GONE
                            btnRequestOtp.isEnabled = true
                            tvError.text = state.message
                            tvError.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }
    }
}
