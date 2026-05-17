package com.nyayasarathi.app.ui.cases

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.google.android.material.chip.Chip
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.TrackedCase

class TrackedCaseAdapter(
    private val onUntrackClick: (TrackedCase) -> Unit
) : ListAdapter<TrackedCase, TrackedCaseAdapter.TrackedCaseViewHolder>(TrackedCaseDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TrackedCaseViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_tracked_case, parent, false)
        return TrackedCaseViewHolder(view)
    }

    override fun onBindViewHolder(holder: TrackedCaseViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class TrackedCaseViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvCaseNumber: TextView = itemView.findViewById(R.id.tv_case_number)
        private val tvParties: TextView = itemView.findViewById(R.id.tv_parties)
        private val tvCourtName: TextView = itemView.findViewById(R.id.tv_court_name)
        private val tvNextHearing: TextView = itemView.findViewById(R.id.tv_next_hearing)
        private val chipStatus: Chip = itemView.findViewById(R.id.chip_status)
        private val btnUntrack: MaterialButton = itemView.findViewById(R.id.btn_untrack)

        fun bind(trackedCase: TrackedCase) {
            tvCaseNumber.text = trackedCase.caseNumber
            tvParties.text = trackedCase.parties
            tvCourtName.text = trackedCase.courtName
            chipStatus.text = trackedCase.status.name

            if (trackedCase.nextHearingDate != null) {
                tvNextHearing.visibility = View.VISIBLE
                tvNextHearing.text = itemView.context.getString(
                    R.string.next_hearing_format, trackedCase.nextHearingDate
                )
            } else {
                tvNextHearing.visibility = View.GONE
            }

            btnUntrack.setOnClickListener {
                onUntrackClick(trackedCase)
            }
        }
    }

    private class TrackedCaseDiffCallback : DiffUtil.ItemCallback<TrackedCase>() {
        override fun areItemsTheSame(oldItem: TrackedCase, newItem: TrackedCase): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: TrackedCase, newItem: TrackedCase): Boolean {
            return oldItem == newItem
        }
    }
}
