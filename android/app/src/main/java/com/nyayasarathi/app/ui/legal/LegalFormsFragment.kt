package com.nyayasarathi.app.ui.legal

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class LegalFormsFragment : Fragment() {

    private lateinit var rvLegalForms: RecyclerView

    private val legalForms = listOf(
        LegalForm("1", "Vakalatnama", "Power of Attorney for Advocate", "PDF"),
        LegalForm("2", "Bail Application", "Application for bail under CrPC", "PDF"),
        LegalForm("3", "Written Statement", "Defence statement in civil suit", "DOCX"),
        LegalForm("4", "Plaint", "Statement of claim in civil suit", "DOCX"),
        LegalForm("5", "Affidavit", "Sworn statement format", "PDF"),
        LegalForm("6", "Caveat Petition", "Notice to be heard before order", "PDF"),
        LegalForm("7", "Interlocutory Application", "Application during pending suit", "PDF"),
        LegalForm("8", "Writ Petition", "Constitutional remedy petition", "DOCX"),
        LegalForm("9", "Appeal Memo", "Memorandum of appeal format", "PDF"),
        LegalForm("10", "Revision Petition", "Petition for revision of order", "PDF")
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_legal_forms, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        rvLegalForms = view.findViewById(R.id.rv_legal_forms)
        setupRecyclerView()
    }

    private fun setupRecyclerView() {
        val adapter = LegalFormAdapter { form ->
            Toast.makeText(
                requireContext(),
                "Download ${form.name} (${form.format}) - placeholder",
                Toast.LENGTH_SHORT
            ).show()
        }
        rvLegalForms.layoutManager = LinearLayoutManager(requireContext())
        rvLegalForms.adapter = adapter
        adapter.submitList(legalForms)
    }
}

data class LegalForm(
    val id: String,
    val name: String,
    val description: String,
    val format: String
)
