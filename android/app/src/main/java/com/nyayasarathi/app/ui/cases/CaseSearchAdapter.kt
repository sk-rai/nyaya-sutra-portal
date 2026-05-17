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
import com.nyayasarathi.app.data.remote.dto.CaseDto

class CaseSearchAdapter(
    private val onTrackClick: (CaseDto) -> Unit
) : ListAdapter<CaseDto, CaseSearchAdapter.CaseViewHolder>(CaseDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CaseViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_case_result, parent, false)
        return CaseViewHolder(view)
    }

    override fun onBindViewHolder(holder: CaseViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class CaseViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvCaseNumber: TextView = itemView.findViewById(R.id.tv_case_number)
        private val tvParties: TextView = itemView.findViewById(R.id.tv_parties)
        private val tvCourtName: TextView = itemView.findViewById(R.id.tv_court_name)
        private val tvNextHearing: TextView = itemView.findViewById(R.id.tv_next_hearing)
        private val chipStatus: Chip = itemView.findViewById(R.id.chip_status)
        private val btnTrack: MaterialButton = itemView.findViewById(R.id.btn_track)

        fun bind(caseDto: CaseDto) {
            tvCaseNumber.text = caseDto.caseNumber
            tvParties.text = caseDto.parties
            tvCourtName.text = caseDto.courtName
            chipStatus.text = caseDto.status

            if (caseDto.nextHearingDate != null) {
                tvNextHearing.visibility = View.VISIBLE
                tvNextHearing.text = itemView.context.getString(
                    R.string.next_hearing_format, caseDto.nextHearingDate
                )
            } else {
                tvNextHearing.visibility = View.GONE
            }

            btnTrack.setOnClickListener {
                onTrackClick(caseDto)
            }
        }
    }

    private class CaseDiffCallback : DiffUtil.ItemCallback<CaseDto>() {
        override fun areItemsTheSame(oldItem: CaseDto, newItem: CaseDto): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: CaseDto, newItem: CaseDto): Boolean {
            return oldItem == newItem
        }
    }
}
