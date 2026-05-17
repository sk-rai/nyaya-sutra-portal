package com.nyayasarathi.app.ui.subscription

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
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.SubscriptionPlan
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class SubscriptionFragment : Fragment() {

    private val viewModel: SubscriptionViewModel by viewModels()

    private lateinit var progressIndicator: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var rvPlans: RecyclerView

    private var planAdapter: SubscriptionPlanAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_subscription, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        progressIndicator = view.findViewById(R.id.progress_indicator)
        tvError = view.findViewById(R.id.tv_error)
        rvPlans = view.findViewById(R.id.rv_plans)

        observeState()
    }

    private fun setupRecyclerView(currentTier: com.nyayasarathi.app.domain.model.SubscriptionTier) {
        planAdapter = SubscriptionPlanAdapter(currentTier) { plan ->
            onSubscribeClicked(plan)
        }
        rvPlans.layoutManager = LinearLayoutManager(requireContext())
        rvPlans.adapter = planAdapter
    }

    private fun onSubscribeClicked(plan: SubscriptionPlan) {
        viewModel.createOrder(plan.id)
    }

    private fun launchRazorpayCheckout(orderId: String, amount: Int, razorpayKey: String) {
        // Placeholder for Razorpay SDK integration
        // In production, this would launch the Razorpay checkout activity
        Toast.makeText(
            requireContext(),
            "Razorpay checkout placeholder - Order: $orderId, Amount: ₹${amount / 100}",
            Toast.LENGTH_LONG
        ).show()
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch {
                    viewModel.currentTier.collect { tier ->
                        setupRecyclerView(tier)
                        // Re-submit plans when tier changes
                        planAdapter?.submitList(viewModel.plans.value)
                    }
                }

                launch {
                    viewModel.plans.collect { plans ->
                        planAdapter?.submitList(plans)
                    }
                }

                launch {
                    viewModel.orderState.collect { state ->
                        when (state) {
                            is UiState.Idle -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                            }
                            is UiState.Loading -> {
                                progressIndicator.visibility = View.VISIBLE
                                tvError.visibility = View.GONE
                            }
                            is UiState.Success -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                                val orderData = state.data
                                launchRazorpayCheckout(
                                    orderData.orderId,
                                    orderData.amount,
                                    orderData.razorpayKey
                                )
                            }
                            is UiState.Error -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.VISIBLE
                                tvError.text = state.message
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        planAdapter = null
    }
}
