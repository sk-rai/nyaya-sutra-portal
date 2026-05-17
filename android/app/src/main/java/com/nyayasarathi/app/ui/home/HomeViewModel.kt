package com.nyayasarathi.app.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nyayasarathi.app.R
import com.nyayasarathi.app.domain.model.QuickAction
import com.nyayasarathi.app.domain.model.SubscriptionTier
import com.nyayasarathi.app.domain.model.UserInfo
import com.nyayasarathi.app.domain.repository.AuthRepository
import com.nyayasarathi.app.domain.repository.CourtRepository
import com.nyayasarathi.app.util.FeatureGatingUtil
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val courtRepository: CourtRepository
) : ViewModel() {

    private val _userInfo = MutableStateFlow(
        UserInfo(
            name = "",
            email = "",
            phone = "",
            userType = "",
            tier = SubscriptionTier.FREE
        )
    )
    val userInfo: StateFlow<UserInfo> = _userInfo.asStateFlow()

    private val _quickActions = MutableStateFlow<List<QuickAction>>(emptyList())
    val quickActions: StateFlow<List<QuickAction>> = _quickActions.asStateFlow()

    init {
        loadDashboard()
    }

    fun loadDashboard() {
        viewModelScope.launch {
            val name = authRepository.getUserName() ?: "User"
            val tier = authRepository.getUserTier()

            _userInfo.value = UserInfo(
                name = name,
                email = "",
                phone = "",
                userType = "",
                tier = tier
            )

            _quickActions.value = computeQuickActions(tier)
        }
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
            authRepository.clearSession()
        }
    }

    private fun computeQuickActions(userTier: SubscriptionTier): List<QuickAction> {
        val baseActions = listOf(
            QuickAction(
                id = "case_search",
                title = "Case Search",
                icon = R.drawable.ic_search,
                destination = R.id.action_home_to_caseSearch,
                requiredTier = SubscriptionTier.FREE
            ),
            QuickAction(
                id = "tracked_cases",
                title = "My Tracked Cases",
                icon = R.drawable.ic_tracked_cases,
                destination = R.id.action_home_to_trackedCases,
                requiredTier = SubscriptionTier.FREE
            ),
            QuickAction(
                id = "court_directory",
                title = "Court Directory",
                icon = R.drawable.ic_court,
                destination = R.id.action_home_to_courtDirectory,
                requiredTier = SubscriptionTier.FREE
            ),
            QuickAction(
                id = "advocate_directory",
                title = "Advocate Directory",
                icon = R.drawable.ic_advocate,
                destination = R.id.action_home_to_advocateDirectory,
                requiredTier = SubscriptionTier.FREE
            ),
            QuickAction(
                id = "court_calendar",
                title = "Court Calendar",
                icon = R.drawable.ic_calendar,
                destination = R.id.action_home_to_calendar,
                requiredTier = SubscriptionTier.FREE
            ),
            QuickAction(
                id = "subscription",
                title = "Subscription",
                icon = R.drawable.ic_subscription,
                destination = R.id.action_home_to_subscription,
                requiredTier = SubscriptionTier.FREE
            )
        )

        val advocateActions = listOf(
            QuickAction(
                id = "register_court_matter",
                title = "Register Court Matter",
                icon = R.drawable.ic_register_matter,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            ),
            QuickAction(
                id = "e_filing",
                title = "e-Filing",
                icon = R.drawable.ic_e_filing,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            ),
            QuickAction(
                id = "e_gate_pass",
                title = "e-Gate Pass",
                icon = R.drawable.ic_gate_pass,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            ),
            QuickAction(
                id = "display_board",
                title = "Display Board",
                icon = R.drawable.ic_display_board,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            ),
            QuickAction(
                id = "judges_roster",
                title = "Judges Roster",
                icon = R.drawable.ic_judges_roster,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            ),
            QuickAction(
                id = "daily_cause_list",
                title = "Daily Cause List",
                icon = R.drawable.ic_cause_list,
                destination = R.id.action_home_to_advocateTools,
                requiredTier = SubscriptionTier.ADVOCATE_NORMAL
            )
        )

        // Base actions are always shown
        // Advocate actions are shown only for advocate_normal or advocate_premium tiers
        val actions = baseActions.toMutableList()
        if (userTier == SubscriptionTier.ADVOCATE_NORMAL || userTier == SubscriptionTier.ADVOCATE_PREMIUM) {
            actions.addAll(advocateActions)
        }

        return actions
    }
}
