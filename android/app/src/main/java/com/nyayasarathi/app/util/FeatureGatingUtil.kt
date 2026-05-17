package com.nyayasarathi.app.util

import com.nyayasarathi.app.domain.model.SubscriptionTier

object FeatureGatingUtil {
    fun isFeatureAllowed(requiredTier: SubscriptionTier, userTier: SubscriptionTier): Boolean {
        return userTier.ordinal >= requiredTier.ordinal
    }
}
