package com.nyayasarathi.app.ui.legal

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R

class BareActAdapter(
    private val onItemClick: (BareAct) -> Unit
) : ListAdapter<BareAct, BareActAdapter.BareActViewHolder>(BareActDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): BareActViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_bare_act, parent, false)
        return BareActViewHolder(view)
    }

    override fun onBindViewHolder(holder: BareActViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class BareActViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvName: TextView = itemView.findViewById(R.id.tv_act_name)
        private val tvShortName: TextView = itemView.findViewById(R.id.tv_act_short_name)
        private val tvDescription: TextView = itemView.findViewById(R.id.tv_act_description)

        fun bind(bareAct: BareAct) {
            tvName.text = bareAct.name
            tvShortName.text = bareAct.shortName
            tvDescription.text = bareAct.description
            itemView.setOnClickListener { onItemClick(bareAct) }
        }
    }

    class BareActDiffCallback : DiffUtil.ItemCallback<BareAct>() {
        override fun areItemsTheSame(oldItem: BareAct, newItem: BareAct): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: BareAct, newItem: BareAct): Boolean {
            return oldItem == newItem
        }
    }
}
