package com.nyayasarathi.app.ui.legal

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class BareActsFragment : Fragment() {

    private lateinit var etSearch: TextInputEditText
    private lateinit var rvBareActs: RecyclerView
    private lateinit var tvEmptyState: TextView

    private var bareActAdapter: BareActAdapter? = null
    private val allBareActs = listOf(
        BareAct("1", "Indian Penal Code, 1860", "IPC", "Criminal law provisions"),
        BareAct("2", "Code of Criminal Procedure, 1973", "CrPC", "Criminal procedure"),
        BareAct("3", "Code of Civil Procedure, 1908", "CPC", "Civil procedure"),
        BareAct("4", "Indian Evidence Act, 1872", "IEA", "Rules of evidence"),
        BareAct("5", "Constitution of India", "COI", "Fundamental law of the land"),
        BareAct("6", "Indian Contract Act, 1872", "ICA", "Contract law"),
        BareAct("7", "Transfer of Property Act, 1882", "TPA", "Property transfer rules"),
        BareAct("8", "Limitation Act, 1963", "LA", "Time limits for legal proceedings"),
        BareAct("9", "Specific Relief Act, 1963", "SRA", "Specific relief provisions"),
        BareAct("10", "Negotiable Instruments Act, 1881", "NIA", "Cheque and promissory notes"),
        BareAct("11", "Bharatiya Nyaya Sanhita, 2023", "BNS", "New criminal code replacing IPC"),
        BareAct("12", "Bharatiya Nagarik Suraksha Sanhita, 2023", "BNSS", "New criminal procedure code")
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_bare_acts, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        etSearch = view.findViewById(R.id.et_search)
        rvBareActs = view.findViewById(R.id.rv_bare_acts)
        tvEmptyState = view.findViewById(R.id.tv_empty_state)

        setupRecyclerView()
        setupSearch()
    }

    private fun setupRecyclerView() {
        bareActAdapter = BareActAdapter { bareAct ->
            showBareActDetails(bareAct)
        }
        rvBareActs.layoutManager = LinearLayoutManager(requireContext())
        rvBareActs.adapter = bareActAdapter
        bareActAdapter?.submitList(allBareActs)
    }

    private fun setupSearch() {
        etSearch.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                val query = s?.toString()?.lowercase() ?: ""
                val filtered = if (query.isBlank()) {
                    allBareActs
                } else {
                    allBareActs.filter {
                        it.name.lowercase().contains(query) ||
                        it.shortName.lowercase().contains(query)
                    }
                }
                bareActAdapter?.submitList(filtered)
                tvEmptyState.visibility = if (filtered.isEmpty()) View.VISIBLE else View.GONE
                rvBareActs.visibility = if (filtered.isEmpty()) View.GONE else View.VISIBLE
            }
        })
    }

    private fun showBareActDetails(bareAct: BareAct) {
        com.google.android.material.dialog.MaterialAlertDialogBuilder(requireContext())
            .setTitle(bareAct.name)
            .setMessage("${bareAct.shortName}\n\n${bareAct.description}\n\n(Full text would be displayed here)")
            .setPositiveButton(android.R.string.ok, null)
            .show()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        bareActAdapter = null
    }
}

data class BareAct(
    val id: String,
    val name: String,
    val shortName: String,
    val description: String
)
