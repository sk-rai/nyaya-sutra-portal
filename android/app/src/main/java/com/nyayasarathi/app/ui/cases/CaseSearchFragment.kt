package com.nyayasarathi.app.ui.cases

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.util.UiState
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class CaseSearchFragment : Fragment() {

    private val viewModel: CaseSearchViewModel by viewModels()

    private lateinit var tilCourtSelector: TextInputLayout
    private lateinit var actvCourt: MaterialAutoCompleteTextView
    private lateinit var tilCaseNumber: TextInputLayout
    private lateinit var etCaseNumber: TextInputEditText
    private lateinit var btnSearch: MaterialButton
    private lateinit var progressIndicator: LinearProgressIndicator
    private lateinit var tvError: TextView
    private lateinit var tvEmptyState: TextView
    private lateinit var rvSearchResults: RecyclerView

    private var caseSearchAdapter: CaseSearchAdapter? = null
    private var courts: List<Court> = emptyList()
    private var selectedCourt: Court? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_case_search, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tilCourtSelector = view.findViewById(R.id.til_court_selector)
        actvCourt = view.findViewById(R.id.actv_court)
        tilCaseNumber = view.findViewById(R.id.til_case_number)
        etCaseNumber = view.findViewById(R.id.et_case_number)
        btnSearch = view.findViewById(R.id.btn_search)
        progressIndicator = view.findViewById(R.id.progress_indicator)
        tvError = view.findViewById(R.id.tv_error)
        tvEmptyState = view.findViewById(R.id.tv_empty_state)
        rvSearchResults = view.findViewById(R.id.rv_search_results)

        setupRecyclerView()
        setupCourtSelector()
        setupSearchButton()
        observeState()
    }

    private fun setupRecyclerView() {
        caseSearchAdapter = CaseSearchAdapter { caseDto ->
            viewModel.trackCase(caseDto.id)
            Toast.makeText(requireContext(), R.string.case_tracked_success, Toast.LENGTH_SHORT).show()
        }
        rvSearchResults.layoutManager = LinearLayoutManager(requireContext())
        rvSearchResults.adapter = caseSearchAdapter
    }

    private fun setupCourtSelector() {
        actvCourt.setOnItemClickListener { _, _, position, _ ->
            selectedCourt = courts.getOrNull(position)
        }
    }

    private fun setupSearchButton() {
        btnSearch.setOnClickListener {
            val courtCode = selectedCourt?.courtCode
            val caseNumber = etCaseNumber.text?.toString()?.trim()

            if (courtCode.isNullOrEmpty()) {
                tilCourtSelector.error = getString(R.string.error_select_court)
                return@setOnClickListener
            }
            tilCourtSelector.error = null

            if (caseNumber.isNullOrEmpty()) {
                tilCaseNumber.error = getString(R.string.error_enter_case_number)
                return@setOnClickListener
            }
            tilCaseNumber.error = null

            viewModel.searchCase(courtCode, caseNumber)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch {
                    viewModel.courts.collect { courtList ->
                        courts = courtList
                        val courtNames = courtList.map { "${it.name} (${it.courtCode})" }
                        val adapter = ArrayAdapter(
                            requireContext(),
                            android.R.layout.simple_dropdown_item_1line,
                            courtNames
                        )
                        actvCourt.setAdapter(adapter)
                    }
                }

                launch {
                    viewModel.searchState.collect { state ->
                        when (state) {
                            is UiState.Idle -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                                tvEmptyState.visibility = View.GONE
                                rvSearchResults.visibility = View.GONE
                            }
                            is UiState.Loading -> {
                                progressIndicator.visibility = View.VISIBLE
                                tvError.visibility = View.GONE
                                tvEmptyState.visibility = View.GONE
                                rvSearchResults.visibility = View.GONE
                            }
                            is UiState.Success -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.GONE
                                val cases = state.data.cases
                                if (cases.isEmpty()) {
                                    tvEmptyState.visibility = View.VISIBLE
                                    rvSearchResults.visibility = View.GONE
                                } else {
                                    tvEmptyState.visibility = View.GONE
                                    rvSearchResults.visibility = View.VISIBLE
                                    caseSearchAdapter?.submitList(cases)
                                }
                            }
                            is UiState.Error -> {
                                progressIndicator.visibility = View.GONE
                                tvError.visibility = View.VISIBLE
                                tvError.text = state.message
                                tvEmptyState.visibility = View.GONE
                                rvSearchResults.visibility = View.GONE
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        caseSearchAdapter = null
    }
}
