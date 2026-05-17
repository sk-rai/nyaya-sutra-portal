package com.nyayasarathi.app.ui.advocate_tools

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class JudgesRosterFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_judges_roster, container, false)
    }
}
