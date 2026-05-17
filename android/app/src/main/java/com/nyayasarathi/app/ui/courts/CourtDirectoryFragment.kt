package com.nyayasarathi.app.ui.courts

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
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.domain.model.CourtGroup
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class CourtDirectoryFragment : Fragment() {

    private val viewModel: CourtDirectoryViewModel by viewModels()

    private lateinit var progressIndicator: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var rvCourtGroups: RecyclerView

    private var courtGroupAdapter: CourtGroupAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_court_directory, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        progressIndicator = view.findViewById(R.id.progress_indicator)
        tvError = view.findViewById(R.id.tv_error)
        rvCourtGroups = view.findViewById(R.id.rv_court_groups)

        setupRecyclerView()
        observeState()
    }

    private fun setupRecyclerView() {
        courtGroupAdapter = CourtGroupAdapter { court ->
            showCourtDetails(court)
        }
        rvCourtGroups.layoutManager = LinearLayoutManager(requireContext())
        rvCourtGroups.adapter = courtGroupAdapter
    }

    private fun showCourtDetails(court: Court) {
        val details = buildString {
            appendLine("Name: ${court.name}")
            appendLine("Code: ${court.courtCode}")
            court.address?.let { appendLine("Address: $it") }
            court.email?.let { appendLine("Email: $it") }
            court.vcLink?.let { appendLine("VC Link: $it") }
            court.proceedingsUrl?.let { appendLine("Proceedings: $it") }
        }

        com.google.android.material.dialog.MaterialAlertDialogBuilder(requireContext())
            .setTitle(court.name)
            .setMessage(details)
            .setPositiveButton(android.R.string.ok, null)
            .show()
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.courtHierarchy.collect { state ->
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
                            courtGroupAdapter?.submitList(state.data)
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

    override fun onDestroyView() {
        super.onDestroyView()
        courtGroupAdapter = null
    }
}
