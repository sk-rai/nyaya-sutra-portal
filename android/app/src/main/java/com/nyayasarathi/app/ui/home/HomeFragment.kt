package com.nyayasarathi.app.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.QuickAction
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.util.FeatureGatingUtil
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class HomeFragment : Fragment() {

    private val homeViewModel: HomeViewModel by viewModels()

    private lateinit var tvGreeting: TextView
    private lateinit var tvTier: TextView
    private lateinit var rvQuickActions: RecyclerView

    private var quickActionAdapter: QuickActionAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tvGreeting = view.findViewById(R.id.tv_greeting)
        tvTier = view.findViewById(R.id.tv_tier)
        rvQuickActions = view.findViewById(R.id.rv_quick_actions)

        setupRecyclerView()
        observeState()
    }

    private fun setupRecyclerView() {
        rvQuickActions.layoutManager = GridLayoutManager(requireContext(), 2)
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch {
                    homeViewModel.userInfo.collect { userInfo ->
                        tvGreeting.text = getString(R.string.greeting_format, userInfo.name)
                        tvTier.text = formatTierName(userInfo.tier)

                        // Recreate adapter with updated tier
                        quickActionAdapter = QuickActionAdapter(userInfo.tier) { action ->
                            onQuickActionClicked(action, userInfo.tier)
                        }
                        rvQuickActions.adapter = quickActionAdapter
                    }
                }

                launch {
                    homeViewModel.quickActions.collect { actions ->
                        quickActionAdapter?.submitList(actions)
                    }
                }
            }
        }
    }

    private fun onQuickActionClicked(action: QuickAction, userTier: SubscriptionTier) {
        if (!FeatureGatingUtil.isFeatureAllowed(action.requiredTier, userTier)) {
            Toast.makeText(
                requireContext(),
                getString(R.string.feature_locked_message, formatTierName(action.requiredTier)),
                Toast.LENGTH_SHORT
            ).show()
            return
        }
        findNavController().navigate(action.destination)
    }

    private fun formatTierName(tier: SubscriptionTier): String {
        return when (tier) {
            SubscriptionTier.FREE -> "Free Tier"
            SubscriptionTier.INDIVIDUAL -> "Individual Tier"
            SubscriptionTier.ADVOCATE_NORMAL -> "Advocate Normal"
            SubscriptionTier.ADVOCATE_PREMIUM -> "Advocate Premium"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        quickActionAdapter = null
    }
}
