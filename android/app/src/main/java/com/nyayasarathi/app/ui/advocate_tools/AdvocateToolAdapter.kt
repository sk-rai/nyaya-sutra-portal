package com.nyayasarathi.app.ui.advocate_tools

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.nyayasarathi.app.R

class AdvocateToolAdapter(
    private val onItemClick: (AdvocateToolItem) -> Unit
) : ListAdapter<AdvocateToolItem, AdvocateToolAdapter.ToolViewHolder>(ToolDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ToolViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_advocate_tool, parent, false)
        return ToolViewHolder(view)
    }

    override fun onBindViewHolder(holder: ToolViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ToolViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvTitle: TextView = itemView.findViewById(R.id.tv_tool_title)
        private val tvDescription: TextView = itemView.findViewById(R.id.tv_tool_description)

        fun bind(tool: AdvocateToolItem) {
            tvTitle.text = tool.title
            tvDescription.text = tool.description
            itemView.setOnClickListener { onItemClick(tool) }
        }
    }

    class ToolDiffCallback : DiffUtil.ItemCallback<AdvocateToolItem>() {
        override fun areItemsTheSame(oldItem: AdvocateToolItem, newItem: AdvocateToolItem): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: AdvocateToolItem, newItem: AdvocateToolItem): Boolean {
            return oldItem == newItem
        }
    }
}
