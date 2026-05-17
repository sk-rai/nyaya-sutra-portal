package com.nyayasarathi.app.ui.police

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class PoliceAuthoritiesFragment : Fragment() {

    private lateinit var actvState: MaterialAutoCompleteTextView
    private lateinit var actvDistrict: MaterialAutoCompleteTextView
    private lateinit var rvAuthorities: RecyclerView
    private lateinit var tvEmptyState: TextView

    private var authorityAdapter: PoliceAuthorityAdapter? = null

    private val stateDistrictMap = mapOf(
        "Delhi" to listOf("Central", "North", "South", "East", "West", "New Delhi"),
        "Maharashtra" to listOf("Mumbai", "Pune", "Nagpur", "Thane", "Nashik"),
        "Karnataka" to listOf("Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Mangaluru"),
        "Tamil Nadu" to listOf("Chennai", "Coimbatore", "Madurai", "Salem"),
        "Uttar Pradesh" to listOf("Lucknow", "Noida", "Agra", "Varanasi", "Kanpur")
    )

    private val placeholderAuthorities = mapOf(
        "Delhi-Central" to listOf(
            PoliceAuthority("DCP Central", "Shri R.K. Sharma", "011-23456789", "dcp.central@delhipolice.gov.in"),
            PoliceAuthority("ACP Connaught Place", "Shri A.K. Singh", "011-23456790", "acp.cp@delhipolice.gov.in")
        ),
        "Maharashtra-Mumbai" to listOf(
            PoliceAuthority("Commissioner of Police", "Shri V.K. Patel", "022-22621855", "cp@mumbaipolice.gov.in"),
            PoliceAuthority("DCP Zone 1", "Shri M.S. Deshmukh", "022-22621856", "dcp.zone1@mumbaipolice.gov.in")
        )
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_police_authorities, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        actvState = view.findViewById(R.id.actv_state)
        actvDistrict = view.findViewById(R.id.actv_district)
        rvAuthorities = view.findViewById(R.id.rv_authorities)
        tvEmptyState = view.findViewById(R.id.tv_empty_state)

        setupRecyclerView()
        setupStateSelector()
    }

    private fun setupRecyclerView() {
        authorityAdapter = PoliceAuthorityAdapter()
        rvAuthorities.layoutManager = LinearLayoutManager(requireContext())
        rvAuthorities.adapter = authorityAdapter
    }

    private fun setupStateSelector() {
        val states = stateDistrictMap.keys.toList()
        val stateAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, states)
        actvState.setAdapter(stateAdapter)

        actvState.setOnItemClickListener { _, _, position, _ ->
            val selectedState = states[position]
            val districts = stateDistrictMap[selectedState] ?: emptyList()
            val districtAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, districts)
            actvDistrict.setAdapter(districtAdapter)
            actvDistrict.setText("", false)
            authorityAdapter?.submitList(emptyList())
            tvEmptyState.visibility = View.VISIBLE
            rvAuthorities.visibility = View.GONE
        }

        actvDistrict.setOnItemClickListener { _, _, position, _ ->
            val selectedState = actvState.text.toString()
            val districts = stateDistrictMap[selectedState] ?: emptyList()
            val selectedDistrict = districts.getOrNull(position) ?: return@setOnItemClickListener
            val key = "$selectedState-$selectedDistrict"
            val authorities = placeholderAuthorities[key] ?: listOf(
                PoliceAuthority("SP $selectedDistrict", "Officer Name", "N/A", "N/A")
            )
            authorityAdapter?.submitList(authorities)
            tvEmptyState.visibility = View.GONE
            rvAuthorities.visibility = View.VISIBLE
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        authorityAdapter = null
    }
}

data class PoliceAuthority(
    val designation: String,
    val name: String,
    val phone: String,
    val email: String
)
