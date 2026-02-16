// Authentication & Tier Management

// Mock login function (replace with actual auth later)
function login(email, password) {
  // Mock users for demo
  const mockUsers = {
    'guest@example.com': { tier: 'unregistered' },
    'unpaid@example.com': { tier: 'unpaid' },
    'paid@example.com': { tier: 'paid' }
  };

  const user = mockUsers[email];

  if (user) {
    localStorage.setItem('userEmail', email);
    localStorage.setItem('userTier', user.tier);
    localStorage.setItem('isLoggedIn', 'true');

    // Redirect to index page
    window.location.href = 'index.html';
    return true;
  } else {
    return false;
  }
}

// Mock register function
function register(email, password, tier = 'unpaid') {
  localStorage.setItem('userEmail', email);
  localStorage.setItem('userTier', tier);
  localStorage.setItem('isLoggedIn', 'true');

  window.location.href = 'index.html';
}

// Logout function
function logout() {
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userTier');
  localStorage.removeItem('isLoggedIn');
  window.location.href = 'dashboard.html';
}

// Check if user is logged in
function checkAuth() {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  return { isLoggedIn, userTier };
}

// Get current user tier
function getCurrentTier() {
  return localStorage.getItem('userTier') || 'unregistered';
}

// Initialize auth state on page load
document.addEventListener('DOMContentLoaded', () => {
  const { isLoggedIn, userTier } = checkAuth();

  // Update body class based on tier
  document.body.classList.add(`tier-${userTier}`);
});