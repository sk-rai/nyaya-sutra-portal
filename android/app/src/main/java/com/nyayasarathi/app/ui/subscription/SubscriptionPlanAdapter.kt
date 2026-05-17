package com.nyayasarathi.app.ui.subscription

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.SubscriptionPlan
import com.nyayasarathi.app.domain.model.SubscriptionTier

class SubscriptionPlanAdapter(
    private val currentTier: SubscriptionTier,
    private val onSubscribeClick: (SubscriptionPlan) -> Unit
) : ListAdapter<SubscriptionPlan, SubscriptionPlanAdapter.PlanViewHolder>(PlanDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PlanViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_subscription_plan, parent, false)
        return PlanViewHolder(view)
    }

    override fun onBindViewHolder(holder: PlanViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class PlanViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvPlanName: TextView = itemView.findViewById(R.id.tv_plan_name)
        private val tvCurrentBadge: TextView = itemView.findViewById(R.id.tv_current_badge)
        private val tvPlanPrice: TextView = itemView.findViewById(R.id.tv_plan_price)
        private val tvPlanFeatures: TextView = itemView.findViewById(R.id.tv_plan_features)
        private val btnSubscribe: MaterialButton = itemView.findViewById(R.id.btn_subscribe)

        fun bind(plan: SubscriptionPlan) {
            tvPlanName.text = plan.name
            tvPlanPrice.text = if (plan.pricePerMonth == 0) {
                "Free"
            } else {
                "₹${plan.pricePerMonth}/month"
            }
            tvPlanFeatures.text = plan.features.joinToString("\n") { "• $it" }

            val isCurrent = plan.tier == currentTier
            tvCurrentBadge.visibility = if (isCurrent) View.VISIBLE else View.GONE

            if (isCurrent || plan.tier == SubscriptionTier.FREE) {
                btnSubscribe.visibility = View.GONE
            } else {
                btnSubscribe.visibility = View.VISIBLE
                btnSubscribe.setOnClickListener { onSubscribeClick(plan) }
            }
        }
    }

    class PlanDiffCallback : DiffUtil.ItemCallback<SubscriptionPlan>() {
        override fun areItemsTheSame(oldItem: SubscriptionPlan, newItem: SubscriptionPlan): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: SubscriptionPlan, newItem: SubscriptionPlan): Boolean {
            return oldItem == newItem
        }
    }
}
