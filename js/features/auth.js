/* ── Auth overlay ── */
function showAuthOverlay(show) {
  document.getElementById('auth-overlay').classList.toggle('hidden', !show);
}

function setAuthTab(tab) {
  document.querySelectorAll('.auth-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.getElementById('login-form').style.display = tab === 'login' ? 'block' : 'none';
  document.getElementById('register-form').style.display = tab === 'register' ? 'block' : 'none';
}

async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const errEl = document.getElementById('login-error');
  errEl.textContent = '';
  try {
    const body = new URLSearchParams({ username: email, password });
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || 'Invalid email or password.');
    }
    const data = await res.json();
    authToken = data.access_token;
    localStorage.setItem('if_token', authToken);
    await afterAuth();
  } catch (e) {
    errEl.textContent = e.message;
  }
}

async function handleRegister(event) {
  event.preventDefault();
  const name = document.getElementById('register-name').value;
  const company_name = document.getElementById('register-company').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;
  const errEl = document.getElementById('register-error');
  errEl.textContent = '';
  try {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, company_name, email, password }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || 'Registration failed.');
    }
    document.getElementById('login-email').value = email;
    document.getElementById('login-password').value = password;
    setAuthTab('login');
    await handleLogin({ preventDefault: () => {} });
  } catch (e) {
    errEl.textContent = e.message;
  }
}

async function afterAuth() {
  try {
    currentUser = await apiFetch('/api/auth/me');
  } catch (e) {
    return;
  }
  showAuthOverlay(false);
  document.getElementById('current-user-name').textContent = currentUser.name;
  document.getElementById('current-user-email').textContent = currentUser.email;
  const target = pendingPage || { id: 'analytics', btn: document.querySelectorAll('.nav-link')[1] };
  pendingPage = null;
  navigateTo(target.id, target.btn);
}

function logoutAndGoHome() {
  clearAuth();
  navigateTo('landing', document.querySelectorAll('.nav-link')[0]);
}
