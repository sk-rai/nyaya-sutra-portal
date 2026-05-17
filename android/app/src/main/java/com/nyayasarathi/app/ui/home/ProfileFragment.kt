package com.nyayasarathi.app.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import com.google.android.material.button.MaterialButton
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.SubscriptionTier
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class ProfileFragment : Fragment() {

    private val homeViewModel: HomeViewModel by viewModels()

    private lateinit var tvUserName: TextView
    private lateinit var tvUserEmail: TextView
    private lateinit var tvUserTier: TextView
    private lateinit var btnLogout: MaterialButton

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_profile, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tvUserName = view.findViewById(R.id.tv_user_name)
        tvUserEmail = view.findViewById(R.id.tv_user_email)
        tvUserTier = view.findViewById(R.id.tv_user_tier)
        btnLogout = view.findViewById(R.id.btn_logout)

        setupClickListeners()
        observeState()
    }

    private fun setupClickListeners() {
        btnLogout.setOnClickListener {
            homeViewModel.logout()
            findNavController().navigate(R.id.action_splash_to_login)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                homeViewModel.userInfo.collect { userInfo ->
                    tvUserName.text = userInfo.name
                    tvUserEmail.text = userInfo.email
                    tvUserTier.text = formatTierName(userInfo.tier)
                }
            }
        }
    }

    private fun formatTierName(tier: SubscriptionTier): String {
        return when (tier) {
            SubscriptionTier.FREE -> "Free Tier"
            SubscriptionTier.INDIVIDUAL -> "Individual Tier"
            SubscriptionTier.ADVOCATE_NORMAL -> "Advocate Normal"
            SubscriptionTier.ADVOCATE_PREMIUM -> "Advocate Premium"
        }
    }
}
