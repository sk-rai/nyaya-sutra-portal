/**
 * Nyaya Sutra API Service Layer
 * 
 * Handles all communication with the backend API.
 * - Base URL configuration (Render deployment)
 * - Token storage (localStorage)
 * - Auth header injection
 * - Standard error handling
 */

const NyayaAPI = (() => {
  // ─── Configuration ───────────────────────────────────────────────
  const BASE_URL = 'https://nyaya-sutra-api.onrender.com';
  const TOKEN_KEY = 'nyaya_token';
  const USER_KEY = 'nyaya_user';
  const SESSION_KEY = 'nyaya_session_id';

  // ─── Token Management ────────────────────────────────────────────

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  }

  function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  }

  function getUser() {
    const data = localStorage.getItem(USER_KEY);
    return data ? JSON.parse(data) : null;
  }

  function setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function clearUser() {
    localStorage.removeItem(USER_KEY);
  }

  function setSessionId(id) {
    localStorage.setItem(SESSION_KEY, id);
  }

  function getSessionId() {
    return localStorage.getItem(SESSION_KEY);
  }

  function isLoggedIn() {
    return !!getToken();
  }

  function getUserTier() {
    const user = getUser();
    return user ? user.tier : 'free';
  }

  // ─── HTTP Helper ─────────────────────────────────────────────────

  async function request(method, path, body = null, requiresAuth = true) {
    const url = `${BASE_URL}${path}`;
    const headers = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth) {
      const token = getToken();
      if (!token) {
        throw new APIError('UNAUTHORIZED', 'Please login to continue.', 401);
      }
      headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
      method,
      headers,
      mode: 'cors',
    };

    if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json();

      if (!data.success) {
        const err = data.error || {};
        throw new APIError(
          err.code || 'UNKNOWN_ERROR',
          err.message || 'Something went wrong.',
          response.status
        );
      }

      return data.data;
    } catch (error) {
      if (error instanceof APIError) {
        // If token expired, clear auth state
        if (error.status === 401) {
          clearToken();
          clearUser();
        }
        throw error;
      }
      // Network error
      throw new APIError(
        'NETWORK_ERROR',
        'Unable to connect to server. Please check your internet connection.',
        0
      );
    }
  }

  // ─── Custom Error Class ──────────────────────────────────────────

  class APIError extends Error {
    constructor(code, message, status) {
      super(message);
      this.code = code;
      this.status = status;
      this.name = 'APIError';
    }
  }

  // ─── Auth Endpoints ──────────────────────────────────────────────

  async function register(data) {
    const result = await request('POST', '/api/auth/register', data, false);
    return result;
  }

  async function requestOTP(identifier, purpose = 'login') {
    const result = await request('POST', '/api/auth/otp/request', {
      identifier,
      purpose,
    }, false);
    return result;
  }

  async function verifyOTP(identifier, otpCode) {
    const result = await request('POST', '/api/auth/otp/verify', {
      identifier,
      otp_code: otpCode,
    }, false);

    // Store token and user data
    if (result.token) {
      setToken(result.token);
    }
    if (result.user) {
      setUser(result.user);
    }

    return result;
  }

  async function logout() {
    const sessionId = getSessionId();
    try {
      if (sessionId) {
        await request('POST', '/api/auth/logout', { session_id: sessionId });
      }
    } catch (e) {
      // Logout should always succeed locally even if server call fails
    }
    clearToken();
    clearUser();
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userTier');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
  }

  // ─── Courts Endpoints ────────────────────────────────────────────

  async function getCourts(courtType = '') {
    let path = '/api/courts';
    if (courtType) {
      path += `?court_type=${encodeURIComponent(courtType)}`;
    }
    return await request('GET', path, null, false);
  }

  // ─── Cases Endpoints ─────────────────────────────────────────────

  async function searchCase(courtCode, caseNumber) {
    const path = `/api/cases/search?court_code=${encodeURIComponent(courtCode)}&case_number=${encodeURIComponent(caseNumber)}`;
    return await request('GET', path);
  }

  // ─── Tracking Endpoints ──────────────────────────────────────────

  async function getTrackedCases() {
    return await request('GET', '/api/tracking');
  }

  async function trackCase(caseId, alertOnHearing = true, alertOnStatusChange = true) {
    return await request('POST', '/api/tracking', {
      case_id: caseId,
      alert_on_hearing: alertOnHearing,
      alert_on_status_change: alertOnStatusChange,
    });
  }

  async function untrackCase(caseId) {
    return await request('DELETE', `/api/tracking/${caseId}`);
  }

  // ─── Relationships Endpoints ─────────────────────────────────────

  async function getCaseRelationships(caseId) {
    return await request('GET', `/api/cases/${caseId}/relationships`);
  }

  async function createCaseRelationship(caseId, relatedCaseId, relationshipType) {
    return await request('POST', '/api/cases/relationships', {
      case_id: caseId,
      related_case_id: relatedCaseId,
      relationship_type: relationshipType,
    });
  }

  // ─── Subscription Endpoints ──────────────────────────────────────

  async function createSubscriptionOrder(tier) {
    return await request('POST', '/api/subscriptions/create-order', { tier });
  }

  // ─── Health Check ────────────────────────────────────────────────

  async function healthCheck() {
    return await request('GET', '/api/health', null, false);
  }

  // ─── Public API ──────────────────────────────────────────────────

  return {
    // Config
    BASE_URL,
    APIError,

    // Auth state
    isLoggedIn,
    getToken,
    getUser,
    getUserTier,
    setSessionId,

    // Auth actions
    register,
    requestOTP,
    verifyOTP,
    logout,

    // Courts
    getCourts,

    // Cases
    searchCase,

    // Tracking
    getTrackedCases,
    trackCase,
    untrackCase,

    // Relationships
    getCaseRelationships,
    createCaseRelationship,

    // Subscriptions
    createSubscriptionOrder,

    // Utility
    healthCheck,
  };
})();
