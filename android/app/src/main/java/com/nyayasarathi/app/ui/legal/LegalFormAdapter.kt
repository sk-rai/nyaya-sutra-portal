package com.nyayasarathi.app.ui.legal

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.nyayasarathi.app.R

class LegalFormAdapter(
    private val onDownloadClick: (LegalForm) -> Unit
) : ListAdapter<LegalForm, LegalFormAdapter.LegalFormViewHolder>(LegalFormDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): LegalFormViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_legal_form, parent, false)
        return LegalFormViewHolder(view)
    }

    override fun onBindViewHolder(holder: LegalFormViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class LegalFormViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvName: TextView = itemView.findViewById(R.id.tv_form_name)
        private val tvDescription: TextView = itemView.findViewById(R.id.tv_form_description)
        private val tvFormat: TextView = itemView.findViewById(R.id.tv_form_format)
        private val btnDownload: MaterialButton = itemView.findViewById(R.id.btn_download)

        fun bind(form: LegalForm) {
            tvName.text = form.name
            tvDescription.text = form.description
            tvFormat.text = form.format
            btnDownload.setOnClickListener { onDownloadClick(form) }
        }
    }

    class LegalFormDiffCallback : DiffUtil.ItemCallback<LegalForm>() {
        override fun areItemsTheSame(oldItem: LegalForm, newItem: LegalForm): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: LegalForm, newItem: LegalForm): Boolean {
            return oldItem == newItem
        }
    }
}
