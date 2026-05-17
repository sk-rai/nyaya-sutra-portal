package com.nyayasarathi.app.ui.advocate_tools

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.google.android.material.button.MaterialButton
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class EFilingFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_e_filing, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<MaterialButton>(R.id.btn_open_portal).setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://efiling.ecourts.gov.in"))
            startActivity(intent)
        }
    }
}
