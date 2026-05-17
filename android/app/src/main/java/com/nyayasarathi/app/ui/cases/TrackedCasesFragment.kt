package com.nyayasarathi.app.ui.cases

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.card.MaterialCardView
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.nyayasarathi.app.R
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class TrackedCasesFragment : Fragment() {

    private val viewModel: TrackedCasesViewModel by viewModels()

    private lateinit var progressIndicator: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var layoutEmptyState: LinearLayout
    private lateinit var rvTrackedCases: RecyclerView
    private lateinit var cardStaleBanner: MaterialCardView

    private var trackedCaseAdapter: TrackedCaseAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_tracked_cases, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        progressIndicator = view.findViewById(R.id.progress_indicator)
        tvError = view.findViewById(R.id.tv_error)
        layoutEmptyState = view.findViewById(R.id.layout_empty_state)
        rvTrackedCases = view.findViewById(R.id.rv_tracked_cases)
        cardStaleBanner = view.findViewById(R.id.card_stale_banner)

        setupRecyclerView()
        observeState()

        viewModel.loadTrackedCases()
    }

    private fun setupRecyclerView() {
        trackedCaseAdapter = TrackedCaseAdapter { trackedCase ->
            viewModel.untrackCase(trackedCase.id)
        }
        rvTrackedCases.layoutManager = LinearLayoutManager(requireContext())
        rvTrackedCases.adapter = trackedCaseAdapter
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch {
                    viewModel.trackedCases.collect { state ->
                        when (state) {
                            is UiState.Idle -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                                layoutEmptyState.visibility = View.GONE
                                rvTrackedCases.visibility = View.GONE
                                cardStaleBanner.visibility = View.GONE
                            }
                            is UiState.Loading -> {
                                progressIndicator.visibility = View.VISIBLE
                                tvError.visibility = View.GONE
                                layoutEmptyState.visibility = View.GONE
                                rvTrackedCases.visibility = View.GONE
                                cardStaleBanner.visibility = View.GONE
                            }
                            is UiState.Success -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                                cardStaleBanner.visibility = View.GONE
                                val cases = state.data
                                if (cases.isEmpty()) {
                                    layoutEmptyState.visibility = View.VISIBLE
                                    rvTrackedCases.visibility = View.GONE
                                } else {
                                    layoutEmptyState.visibility = View.GONE
                                    rvTrackedCases.visibility = View.VISIBLE
                                    trackedCaseAdapter?.submitList(cases)
                                }
                            }
                            is UiState.Error -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.VISIBLE
                                tvError.text = state.message
                                layoutEmptyState.visibility = View.GONE
                                rvTrackedCases.visibility = View.GONE
                                cardStaleBanner.visibility = View.GONE
                            }
                        }
                    }
                }

                launch {
                    viewModel.isShowingStaleBanner.collect { isStale ->
                        cardStaleBanner.visibility = if (isStale) View.VISIBLE else View.GONE
                    }
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        trackedCaseAdapter = null
    }
}
