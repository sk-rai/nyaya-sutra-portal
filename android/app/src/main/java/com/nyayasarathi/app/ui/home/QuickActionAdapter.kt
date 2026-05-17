package com.nyayasarathi.app.ui.home

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.card.MaterialCardView
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.QuickAction
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.util.FeatureGatingUtil

class QuickActionAdapter(
    private val userTier: SubscriptionTier,
    private val onClick: (QuickAction) -> Unit
) : ListAdapter<QuickAction, QuickActionAdapter.QuickActionViewHolder>(QuickActionDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): QuickActionViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_quick_action, parent, false)
        return QuickActionViewHolder(view)
    }

    override fun onBindViewHolder(holder: QuickActionViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class QuickActionViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val cardView: MaterialCardView = itemView.findViewById(R.id.card_quick_action)
        private val ivIcon: ImageView = itemView.findViewById(R.id.iv_action_icon)
        private val tvTitle: TextView = itemView.findViewById(R.id.tv_action_title)
        private val tvLockIndicator: TextView = itemView.findViewById(R.id.tv_lock_indicator)

        fun bind(action: QuickAction) {
            ivIcon.setImageResource(action.icon)
            tvTitle.text = action.title

            val isAllowed = FeatureGatingUtil.isFeatureAllowed(action.requiredTier, userTier)

            if (!isAllowed) {
                tvLockIndicator.text = action.requiredTier.name.replace("_", " ")
                tvLockIndicator.visibility = View.VISIBLE
                cardView.alpha = 0.6f
            } else {
                tvLockIndicator.visibility = View.GONE
                cardView.alpha = 1.0f
            }

            cardView.setOnClickListener {
                onClick(action)
            }
        }
    }

    class QuickActionDiffCallback : DiffUtil.ItemCallback<QuickAction>() {
        override fun areItemsTheSame(oldItem: QuickAction, newItem: QuickAction): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: QuickAction, newItem: QuickAction): Boolean {
            return oldItem == newItem
        }
    }
}
