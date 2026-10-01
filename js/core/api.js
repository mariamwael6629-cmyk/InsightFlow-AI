/* ── API client ── */
const API_BASE = window.API_BASE_URL || 'http://127.0.0.1:8000';
const PROTECTED_PAGES = ['analytics', 'reports', 'settings'];
let authToken = localStorage.getItem('if_token');
let currentUser = null;
let pendingPage = null;

function clearAuth() {
  authToken = null;
  currentUser = null;
  localStorage.removeItem('if_token');
}

async function apiFetch(path, options = {}) {
  const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  const res = await fetch(`${API_BASE}${path}`, Object.assign({}, options, { headers }));
  if (res.status === 401) {
    clearAuth();
    throw new Error('Your session expired. Please sign in again.');
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  if (res.status === 204) return null;
  return res.json();
}
