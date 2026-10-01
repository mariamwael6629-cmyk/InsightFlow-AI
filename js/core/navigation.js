/* ── Page Navigation ── */
function navigateTo(id, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (id === 'analytics') loadAnalyticsData();
  if (id === 'reports') loadReportsData();
  if (id === 'settings') loadSettingsData();
}

function showPage(id, btn) {
  if (PROTECTED_PAGES.includes(id) && !authToken) {
    pendingPage = { id, btn };
    showAuthOverlay(true);
    return;
  }
  navigateTo(id, btn);
}

function setFilter(btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function setSettingsTab(el) {
  document.querySelectorAll('.settings-nav-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
}

function toggleFaq(el) {
  const isOpen = el.classList.contains('open');
  document.querySelectorAll('.faq-q.open').forEach(q => {
    q.classList.remove('open');
    q.nextElementSibling.classList.remove('open');
  });
  if (!isOpen) {
    el.classList.add('open');
    el.nextElementSibling.classList.add('open');
  }
}
