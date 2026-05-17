package com.nyayasarathi.app.ui.advocate_tools

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.google.android.material.textfield.TextInputEditText
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class RegisterCourtMatterFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_register_court_matter, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val actvState = view.findViewById<MaterialAutoCompleteTextView>(R.id.actv_state)
        val actvCourtType = view.findViewById<MaterialAutoCompleteTextView>(R.id.actv_court_type)
        val etMatterDetails = view.findViewById<TextInputEditText>(R.id.et_matter_details)
        val btnRegister = view.findViewById<MaterialButton>(R.id.btn_register)

        val states = listOf("Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh")
        actvState.setAdapter(ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, states))

        val courtTypes = listOf("High Court", "District Court", "Sessions Court", "Magistrate Court")
        actvCourtType.setAdapter(ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, courtTypes))

        btnRegister.setOnClickListener {
            Toast.makeText(requireContext(), "Court matter registration - placeholder", Toast.LENGTH_SHORT).show()
        }
    }
}
