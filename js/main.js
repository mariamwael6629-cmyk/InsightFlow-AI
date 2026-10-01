/* ── Silent session check on load ── */
window.addEventListener('load', async () => {
  if (!authToken) return;
  try {
    currentUser = await apiFetch('/api/auth/me');
    document.getElementById('current-user-name').textContent = currentUser.name;
    document.getElementById('current-user-email').textContent = currentUser.email;
  } catch (e) {
    clearAuth();
  }
});
