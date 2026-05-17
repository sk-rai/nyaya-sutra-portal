package com.nyayasarathi.app.ui.police

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R

class PoliceAuthorityAdapter : ListAdapter<PoliceAuthority, PoliceAuthorityAdapter.AuthorityViewHolder>(AuthorityDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AuthorityViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_police_authority, parent, false)
        return AuthorityViewHolder(view)
    }

    override fun onBindViewHolder(holder: AuthorityViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class AuthorityViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvDesignation: TextView = itemView.findViewById(R.id.tv_designation)
        private val tvName: TextView = itemView.findViewById(R.id.tv_name)
        private val tvPhone: TextView = itemView.findViewById(R.id.tv_phone)
        private val tvEmail: TextView = itemView.findViewById(R.id.tv_email)

        fun bind(authority: PoliceAuthority) {
            tvDesignation.text = authority.designation
            tvName.text = authority.name
            tvPhone.text = authority.phone
            tvEmail.text = authority.email
        }
    }

    class AuthorityDiffCallback : DiffUtil.ItemCallback<PoliceAuthority>() {
        override fun areItemsTheSame(oldItem: PoliceAuthority, newItem: PoliceAuthority): Boolean {
            return oldItem.designation == newItem.designation && oldItem.name == newItem.name
        }

        override fun areContentsTheSame(oldItem: PoliceAuthority, newItem: PoliceAuthority): Boolean {
            return oldItem == newItem
        }
    }
}
