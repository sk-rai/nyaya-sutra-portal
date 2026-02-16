// Print & Copy Control - Enforces tier-based restrictions

// Disable right-click context menu (basic protection)
document.addEventListener('contextmenu', (e) => {
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  if (userTier !== 'paid') {
    e.preventDefault();
    showUpgradePrompt();
  }
});

// Disable text selection for unpaid users
document.addEventListener('DOMContentLoaded', () => {
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  if (userTier !== 'paid') {
    document.body.style.userSelect = 'none';
    document.body.style.webkitUserSelect = 'none';
    document.body.style.MozUserSelect = 'none';
    document.body.style.msUserSelect = 'none';
  }
});

// Disable browser print for unpaid users
window.addEventListener('beforeprint', (e) => {
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  if (userTier !== 'paid') {
    e.preventDefault();
    showUpgradePrompt();
    return false;
  }
});

// Show upgrade prompt
function showUpgradePrompt() {
  alert('🔒 Printing and copying are available only for paid subscribers. Please upgrade your plan to unlock these features.');
}

// Custom print function (for paid users only)
function safePrint(contentId) {
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  if (userTier === 'paid') {
    window.print();
  } else {
    showUpgradePrompt();
  }
}

// Custom copy function (for paid users only)
async function safeCopy(text) {
  const userTier = localStorage.getItem('userTier') || 'unregistered';

  if (userTier === 'paid') {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.error('Failed to copy:', err);
      return false;
    }
  } else {
    showUpgradePrompt();
    return false;
  }
}