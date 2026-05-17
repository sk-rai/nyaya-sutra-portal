package com.nyayasarathi.app.ui.courts

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.Court
import com.nyayasarathi.app.domain.model.CourtGroup

class CourtGroupAdapter(
    private val onCourtClick: (Court) -> Unit
) : ListAdapter<CourtGroup, CourtGroupAdapter.CourtGroupViewHolder>(CourtGroupDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CourtGroupViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_court_group, parent, false)
        return CourtGroupViewHolder(view)
    }

    override fun onBindViewHolder(holder: CourtGroupViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class CourtGroupViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvGroupLabel: TextView = itemView.findViewById(R.id.tv_group_label)
        private val tvCourtCount: TextView = itemView.findViewById(R.id.tv_court_count)
        private val ivExpandIcon: ImageView = itemView.findViewById(R.id.iv_expand_icon)
        private val layoutCourts: LinearLayout = itemView.findViewById(R.id.layout_courts)

        private var isExpanded = false

        fun bind(group: CourtGroup) {
            tvGroupLabel.text = group.label
            tvCourtCount.text = "(${group.courts.size})"
            layoutCourts.visibility = View.GONE
            isExpanded = false
            ivExpandIcon.rotation = 0f

            itemView.setOnClickListener {
                isExpanded = !isExpanded
                layoutCourts.visibility = if (isExpanded) View.VISIBLE else View.GONE
                ivExpandIcon.animate().rotation(if (isExpanded) 180f else 0f).setDuration(200).start()
            }

            layoutCourts.removeAllViews()
            for (court in group.courts) {
                val courtView = LayoutInflater.from(itemView.context)
                    .inflate(R.layout.item_court, layoutCourts, false)
                courtView.findViewById<TextView>(R.id.tv_court_name).text = court.name
                courtView.findViewById<TextView>(R.id.tv_court_code).text = court.courtCode
                courtView.setOnClickListener { onCourtClick(court) }
                layoutCourts.addView(courtView)
            }
        }
    }

    class CourtGroupDiffCallback : DiffUtil.ItemCallback<CourtGroup>() {
        override fun areItemsTheSame(oldItem: CourtGroup, newItem: CourtGroup): Boolean {
            return oldItem.type == newItem.type
        }

        override fun areContentsTheSame(oldItem: CourtGroup, newItem: CourtGroup): Boolean {
            return oldItem == newItem
        }
    }
}
