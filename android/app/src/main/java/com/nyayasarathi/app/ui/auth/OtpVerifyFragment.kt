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
import androidx.navigation.fragment.navArgs
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.nyayasarathi.app.R
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class OtpVerifyFragment : Fragment() {

    private val authViewModel: AuthViewModel by activityViewModels()
    private val args: OtpVerifyFragmentArgs by navArgs()

    private lateinit var tvIdentifier: TextView
    private lateinit var tilOtp: TextInputLayout
    private lateinit var etOtp: TextInputEditText
    private lateinit var btnVerify: MaterialButton
    private lateinit var progressBar: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var tvResendOtp: TextView

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_otp_verify, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tvIdentifier = view.findViewById(R.id.tv_identifier)
        tilOtp = view.findViewById(R.id.til_otp)
        etOtp = view.findViewById(R.id.et_otp)
        btnVerify = view.findViewById(R.id.btn_verify)
        progressBar = view.findViewById(R.id.progress_bar)
        tvError = view.findViewById(R.id.tv_error)
        tvResendOtp = view.findViewById(R.id.tv_resend_otp)

        tvIdentifier.text = args.identifier

        setupClickListeners()
        observeState()
    }

    private fun setupClickListeners() {
        btnVerify.setOnClickListener {
            val otpCode = etOtp.text?.toString()?.trim() ?: ""
            if (otpCode.length != 6) {
                tilOtp.error = "Please enter a valid 6-digit OTP"
                return@setOnClickListener
            }
            tilOtp.error = null
            tvError.visibility = View.GONE
            authViewModel.verifyOtp(args.identifier, otpCode)
        }

        tvResendOtp.setOnClickListener {
            tvError.visibility = View.GONE
            authViewModel.requestOtp(args.identifier)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                authViewModel.otpVerifyState.collect { state ->
                    when (state) {
                        is UiState.Idle -> {
                            progressBar.visibility = View.GONE
                            btnVerify.isEnabled = true
                        }
                        is UiState.Loading -> {
                            progressBar.visibility = View.VISIBLE
                            tvError.visibility = View.GONE
                            btnVerify.isEnabled = false
                            tvResendOtp.isEnabled = false
                        }
                        is UiState.Success -> {
                            progressBar.visibility = View.GONE
                            btnVerify.isEnabled = true
                            tvResendOtp.isEnabled = true
                            authViewModel.resetOtpVerifyState()
                            findNavController().navigate(R.id.action_otp_to_home)
                        }
                        is UiState.Error -> {
                            progressBar.visibility = View.GONE
                            btnVerify.isEnabled = true
                            tvResendOtp.isEnabled = true
                            tvError.text = state.message
                            tvError.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }
    }
}
