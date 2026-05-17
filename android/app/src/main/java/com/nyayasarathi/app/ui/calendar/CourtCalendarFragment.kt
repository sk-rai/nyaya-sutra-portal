package com.nyayasarathi.app.ui.calendar

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.GridLayout
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.nyayasarathi.app.R
import dagger.hilt.android.AndroidEntryPoint
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

@AndroidEntryPoint
class CourtCalendarFragment : Fragment() {

    private lateinit var actvCourtType: MaterialAutoCompleteTextView
    private lateinit var tvMonthYear: TextView
    private lateinit var gridCalendar: GridLayout

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_court_calendar, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        actvCourtType = view.findViewById(R.id.actv_court_type)
        tvMonthYear = view.findViewById(R.id.tv_month_year)
        gridCalendar = view.findViewById(R.id.grid_calendar)

        setupCourtSelector()
        displayCurrentMonth()
    }

    private fun setupCourtSelector() {
        val courtTypes = listOf(
            "Supreme Court",
            "High Courts",
            "District Courts",
            "Armed Forces Tribunal",
            "Central Administrative Tribunal"
        )
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, courtTypes)
        actvCourtType.setAdapter(adapter)
    }

    private fun displayCurrentMonth() {
        val calendar = Calendar.getInstance()
        val dateFormat = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
        tvMonthYear.text = dateFormat.format(calendar.time)

        gridCalendar.removeAllViews()

        // Day headers
        val dayHeaders = listOf("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        for (header in dayHeaders) {
            val tv = TextView(requireContext()).apply {
                text = header
                textSize = 12f
                gravity = android.view.Gravity.CENTER
                setPadding(8, 8, 8, 8)
                layoutParams = GridLayout.LayoutParams().apply {
                    width = 0
                    height = ViewGroup.LayoutParams.WRAP_CONTENT
                    columnSpec = GridLayout.spec(GridLayout.UNDEFINED, 1f)
                }
            }
            gridCalendar.addView(tv)
        }

        // Calendar days
        calendar.set(Calendar.DAY_OF_MONTH, 1)
        val firstDayOfWeek = calendar.get(Calendar.DAY_OF_WEEK) - 1
        val daysInMonth = calendar.getActualMaximum(Calendar.DAY_OF_MONTH)

        // Empty cells before first day
        for (i in 0 until firstDayOfWeek) {
            val tv = TextView(requireContext()).apply {
                text = ""
                layoutParams = GridLayout.LayoutParams().apply {
                    width = 0
                    height = ViewGroup.LayoutParams.WRAP_CONTENT
                    columnSpec = GridLayout.spec(GridLayout.UNDEFINED, 1f)
                }
            }
            gridCalendar.addView(tv)
        }

        // Day cells
        for (day in 1..daysInMonth) {
            val dayOfWeek = (firstDayOfWeek + day - 1) % 7
            val tv = TextView(requireContext()).apply {
                text = day.toString()
                textSize = 14f
                gravity = android.view.Gravity.CENTER
                setPadding(8, 12, 8, 12)
                layoutParams = GridLayout.LayoutParams().apply {
                    width = 0
                    height = ViewGroup.LayoutParams.WRAP_CONTENT
                    columnSpec = GridLayout.spec(GridLayout.UNDEFINED, 1f)
                }
                // Color code: Sunday = holiday (red), Saturday = half-day, others = working
                when (dayOfWeek) {
                    0 -> setTextColor(resources.getColor(android.R.color.holo_red_dark, null))
                    6 -> setTextColor(resources.getColor(android.R.color.holo_orange_dark, null))
                    else -> setTextColor(resources.getColor(android.R.color.holo_green_dark, null))
                }
            }
            gridCalendar.addView(tv)
        }
    }
}
