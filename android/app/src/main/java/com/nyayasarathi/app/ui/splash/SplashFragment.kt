package com.nyayasarathi.app.ui.splash

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.nyayasarathi.app.R
import com.nyayasarathi.app.data.local.SessionManager
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class SplashFragment : Fragment() {

    @Inject
    lateinit var sessionManager: SessionManager

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_splash, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewLifecycleOwner.lifecycleScope.launch {
            delay(2000L)
            navigateBasedOnAuthState()
        }
    }

    private fun navigateBasedOnAuthState() {
        if (!isAdded) return

        if (sessionManager.isLoggedIn()) {
            findNavController().navigate(R.id.action_splash_to_home)
        } else {
            findNavController().navigate(R.id.action_splash_to_login)
        }
    }
}
