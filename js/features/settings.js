/* ── Settings ── */
function loadSettingsData() {
  loadCompanyProfile().catch(e => console.error('company', e));
  loadPlanInfo().catch(e => console.error('plan', e));
  loadTeamMembers().catch(e => console.error('team', e));
  loadNotificationSettings().catch(e => console.error('notifications', e));
}

async function loadCompanyProfile() {
  const c = await apiFetch('/api/settings/company');
  document.getElementById('company-name').value     = c.name;
  document.getElementById('company-industry').value = c.industry;
  document.getElementById('company-email').value    = c.primary_email;
  document.getElementById('company-timezone').value = c.timezone;
  document.getElementById('company-website').value  = c.website;
  document.getElementById('company-language').value = c.language;
}

async function saveCompanyProfile() {
  const btn = document.getElementById('save-company-btn');
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Saving…';
  try {
    await apiFetch('/api/settings/company', {
      method: 'PUT',
      body: JSON.stringify({
        name:          document.getElementById('company-name').value,
        industry:      document.getElementById('company-industry').value,
        primary_email: document.getElementById('company-email').value,
        timezone:      document.getElementById('company-timezone').value,
        website:       document.getElementById('company-website').value,
        language:      document.getElementById('company-language').value
      })
    });
    btn.textContent = 'Saved ✓';
  } catch (e) {
    alert(e.message);
    btn.textContent = original;
  } finally {
    setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 1500);
  }
}

async function loadPlanInfo() {
  const p = await apiFetch('/api/settings/plan');
  document.getElementById('plan-name-tag').textContent = `✦ ${p.plan_name}`;
  document.getElementById('plan-price').innerHTML = `$${p.plan_price.toFixed(0)} <span>/ month</span>`;
  document.getElementById('plan-responses-label').textContent = `${p.responses_used.toLocaleString()} / ${p.responses_limit.toLocaleString()}`;
  document.getElementById('plan-responses-bar').style.width = `${Math.min(100, Math.round((p.responses_used / p.responses_limit) * 100))}%`;
  document.getElementById('plan-seats-label').textContent = `${p.seats_used} / ${p.seats_limit}`;
  document.getElementById('plan-seats-bar').style.width = `${Math.min(100, Math.round((p.seats_used / p.seats_limit) * 100))}%`;
}

const AVATAR_STYLES = [
  'background:var(--accent-soft);color:var(--accent);',
  'background:var(--good-bg);color:var(--good);',
  'background:var(--warn-bg);color:var(--warn);'
];

function getInitials(name) {
  return name.split(' ').filter(Boolean).slice(0, 2).map(p => p[0].toUpperCase()).join('');
}

async function loadTeamMembers() {
  const members = await apiFetch('/api/settings/team');
  document.getElementById('team-list').innerHTML = members.map((m, i) => `
    <div class="team-member">
      <div class="avatar" style="${AVATAR_STYLES[i % AVATAR_STYLES.length]}">${escapeHtml(getInitials(m.name))}</div>
      <div>
        <div class="member-name">${escapeHtml(m.name)}</div>
        <div class="member-role">${escapeHtml(m.email)}</div>
      </div>
      <span class="role-badge ${m.role}">${m.role.charAt(0).toUpperCase() + m.role.slice(1)}</span>
    </div>`).join('');
}

async function inviteTeamMember() {
  const name = window.prompt('Team member name:');
  if (!name) return;
  const email = window.prompt('Team member email:');
  if (!email) return;
  const role = (window.prompt('Role (admin / editor / viewer):', 'viewer') || 'viewer').toLowerCase();
  try {
    const result = await apiFetch('/api/settings/team', {
      method: 'POST',
      body: JSON.stringify({ name, email, role })
    });
    await loadTeamMembers();
    alert(`Invited ${result.name}. Temporary password: ${result.temporary_password}`);
  } catch (e) {
    alert(e.message);
  }
}

let notificationSettingsCache = [];

async function loadNotificationSettings() {
  notificationSettingsCache = await apiFetch('/api/settings/notifications');
  renderNotificationsList();
}

function renderNotificationsList() {
  document.getElementById('notifications-list').innerHTML = notificationSettingsCache.map(n => `
    <div style="display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="font-size:14px;font-weight:500;color:var(--ink);">${escapeHtml(n.label)}</div>
        <div style="font-size:12px;color:var(--ink-3);margin-top:2px;">${escapeHtml(n.description)}</div>
      </div>
      <div class="toggle-switch ${n.enabled ? 'on' : 'off'}" onclick="toggleNotification('${n.key}')">
        <div class="knob"></div>
      </div>
    </div>`).join('');
}

async function toggleNotification(key) {
  const item = notificationSettingsCache.find(n => n.key === key);
  if (!item) return;
  try {
    const updated = await apiFetch(`/api/settings/notifications/${key}`, {
      method: 'PUT',
      body: JSON.stringify({ enabled: !item.enabled })
    });
    item.enabled = updated.enabled;
    renderNotificationsList();
  } catch (e) {
    alert(e.message);
  }
}
