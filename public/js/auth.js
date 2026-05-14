/**
 * Authentication & Session Management
 * Works with NyayaAPI service layer for real backend calls.
 */

// Check if user is logged in
function checkAuth() {
  const isLoggedIn = NyayaAPI.isLoggedIn();
  const user = NyayaAPI.getUser();
  const userTier = user ? user.tier : 'free';

  return { isLoggedIn, userTier, user };
}

// Get current user tier
function getCurrentTier() {
  return NyayaAPI.getUserTier();
}

// Logout function
async function logout() {
  await NyayaAPI.logout();
  window.location.href = 'dashboard.html';
}

// Redirect to login if not authenticated
function requireAuth() {
  if (!NyayaAPI.isLoggedIn()) {
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

// Initialize auth state on page load
document.addEventListener('DOMContentLoaded', () => {
  const { isLoggedIn, userTier } = checkAuth();

  // Update body class based on tier
  document.body.classList.add(`tier-${userTier}`);

  // Update nav login/logout buttons if they exist
  const loginBtn = document.querySelector('.btn-login-nav');
  const logoutBtn = document.querySelector('.btn-logout-nav');
  const userNameEl = document.querySelector('.user-name-display');

  if (isLoggedIn) {
    if (loginBtn) loginBtn.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'inline-block';
    if (userNameEl) {
      const user = NyayaAPI.getUser();
      userNameEl.textContent = user ? user.name : '';
    }
  } else {
    if (loginBtn) loginBtn.style.display = 'inline-block';
    if (logoutBtn) logoutBtn.style.display = 'none';
  }
});
