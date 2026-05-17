package com.nyayasarathi.app.ui.advocates

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R

class AdvocateAdapter : ListAdapter<Advocate, AdvocateAdapter.AdvocateViewHolder>(AdvocateDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AdvocateViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_advocate, parent, false)
        return AdvocateViewHolder(view)
    }

    override fun onBindViewHolder(holder: AdvocateViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class AdvocateViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvName: TextView = itemView.findViewById(R.id.tv_advocate_name)
        private val tvCourt: TextView = itemView.findViewById(R.id.tv_advocate_court)
        private val tvContact: TextView = itemView.findViewById(R.id.tv_advocate_contact)

        fun bind(advocate: Advocate) {
            tvName.text = advocate.name
            tvCourt.text = advocate.courtName
            tvContact.text = advocate.phone ?: advocate.email ?: ""
        }
    }

    class AdvocateDiffCallback : DiffUtil.ItemCallback<Advocate>() {
        override fun areItemsTheSame(oldItem: Advocate, newItem: Advocate): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Advocate, newItem: Advocate): Boolean {
            return oldItem == newItem
        }
    }
}
