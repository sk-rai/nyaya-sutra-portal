package com.nyayasarathi.app.ui.advocates

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.google.android.material.textfield.TextInputEditText
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class AdvocateDirectoryFragment : Fragment() {

    private val viewModel: AdvocateDirectoryViewModel by viewModels()

    private lateinit var etSearch: TextInputEditText
    private lateinit var actvCourtFilter: MaterialAutoCompleteTextView
    private lateinit var rvAdvocates: RecyclerView
    private lateinit var tvEmptyState: TextView

    private var advocateAdapter: AdvocateAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_advocate_directory, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        etSearch = view.findViewById(R.id.et_search)
        actvCourtFilter = view.findViewById(R.id.actv_court_filter)
        rvAdvocates = view.findViewById(R.id.rv_advocates)
        tvEmptyState = view.findViewById(R.id.tv_empty_state)

        setupRecyclerView()
        setupSearch()
        setupCourtFilter()
        observeState()
    }

    private fun setupRecyclerView() {
        advocateAdapter = AdvocateAdapter()
        rvAdvocates.layoutManager = LinearLayoutManager(requireContext())
        rvAdvocates.adapter = advocateAdapter
    }

    private fun setupSearch() {
        etSearch.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                viewModel.filterByName(s?.toString() ?: "")
            }
        })
    }

    private fun setupCourtFilter() {
        val courtOptions = listOf("All Courts", "Delhi High Court", "Bombay High Court", "Supreme Court", "Madras High Court", "Calcutta High Court", "Karnataka High Court")
        val courtCodes = listOf(null, "DLHC", "BOMHC", "SC", "MDHC", "CALHC", "KARHC")

        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, courtOptions)
        actvCourtFilter.setAdapter(adapter)
        actvCourtFilter.setOnItemClickListener { _, _, position, _ ->
            viewModel.filterByCourt(courtCodes.getOrNull(position))
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.filteredAdvocates.collect { advocates ->
                    if (advocates.isEmpty()) {
                        tvEmptyState.visibility = View.VISIBLE
                        rvAdvocates.visibility = View.GONE
                    } else {
                        tvEmptyState.visibility = View.GONE
                        rvAdvocates.visibility = View.VISIBLE
                        advocateAdapter?.submitList(advocates)
                    }
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        advocateAdapter = null
    }
}
