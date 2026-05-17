package com.nyayasarathi.app.ui.advocate_tools

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class AdvocateToolsFragment : Fragment() {

    private lateinit var rvTools: RecyclerView

    private val toolItems = listOf(
        AdvocateToolItem("register_matter", "Register Court Matter", "Register a new court matter"),
        AdvocateToolItem("display_board", "Display Board", "View live court display board"),
        AdvocateToolItem("judges_roster", "Judges Roster", "View current judges roster"),
        AdvocateToolItem("cause_list", "Daily Cause List", "View daily cause list"),
        AdvocateToolItem("e_filing", "e-Filing", "Access court e-Filing portal"),
        AdvocateToolItem("e_gate_pass", "e-Gate Pass", "Access court e-Gate Pass portal")
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_advocate_tools, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        rvTools = view.findViewById(R.id.rv_tools)
        setupRecyclerView()
    }

    private fun setupRecyclerView() {
        val adapter = AdvocateToolAdapter { tool ->
            navigateToTool(tool)
        }
        rvTools.layoutManager = LinearLayoutManager(requireContext())
        rvTools.adapter = adapter
        adapter.submitList(toolItems)
    }

    private fun navigateToTool(tool: AdvocateToolItem) {
        try {
            when (tool.id) {
                "register_matter" -> findNavController().navigate(R.id.registerCourtMatterFragment)
                "display_board" -> findNavController().navigate(R.id.displayBoardFragment)
                "judges_roster" -> findNavController().navigate(R.id.judgesRosterFragment)
                "cause_list" -> findNavController().navigate(R.id.causeListFragment)
                "e_filing" -> findNavController().navigate(R.id.eFilingFragment)
                "e_gate_pass" -> findNavController().navigate(R.id.eGatePassFragment)
            }
        } catch (e: Exception) {
            Toast.makeText(requireContext(), "Navigation not available: ${tool.title}", Toast.LENGTH_SHORT).show()
        }
    }
}

data class AdvocateToolItem(
    val id: String,
    val title: String,
    val description: String
)
