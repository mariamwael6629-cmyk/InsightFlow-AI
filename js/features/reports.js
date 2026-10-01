/* ── Reports ── */
function loadReportsData() {
  loadReportsList().catch(e => console.error('reports', e));
  loadComparison().catch(e => console.error('comparison', e));
}

async function loadReportsList() {
  const reports = await apiFetch('/api/reports');
  document.getElementById('reports-grid').innerHTML = reports.map(r => `
    <div class="report-card">
      <div class="report-icon" style="background:${r.icon_bg};">${r.icon}</div>
      <div class="report-title">${escapeHtml(r.title)}</div>
      <div class="report-desc">${escapeHtml(r.description)}</div>
      <div class="report-meta"><span class="report-date">${formatDate(r.report_date)}</span><button class="dl-btn">↓ PDF</button></div>
    </div>`).join('');
}

async function loadComparison() {
  const rows = await apiFetch('/api/reports/comparison');
  if (!rows.length) return;
  document.getElementById('comparison-header').innerHTML = `
    <span>Metric</span><span>${escapeHtml(rows[0].previous_label)}</span><span>${escapeHtml(rows[0].current_label)}</span>`;
  const maxVal = Math.max(...rows.map(r => Math.max(r.previous_value, r.current_value)), 1);
  document.getElementById('comparison-rows').innerHTML = rows.map(r => {
    const prevPct = Math.round((r.previous_value / maxVal) * 100);
    const curPct  = Math.round((r.current_value  / maxVal) * 100);
    const curColor     = r.trend === 'up' ? 'var(--accent)' : 'var(--good)';
    const curTextColor = r.trend === 'up' ? 'var(--accent)' : 'var(--good)';
    return `
    <div class="comp-row">
      <span style="color:var(--ink-2);">${escapeHtml(r.metric_name)}</span>
      <div class="comp-bar-wrap">
        <div class="comp-bar-bg"><div class="comp-bar-fill" style="width:${prevPct}%;background:var(--accent-lite);"></div></div>
        <span style="font-size:12px;color:var(--ink-2);min-width:32px;">${escapeHtml(r.previous_display)}</span>
      </div>
      <div class="comp-bar-wrap">
        <div class="comp-bar-bg"><div class="comp-bar-fill" style="width:${curPct}%;background:${curColor};"></div></div>
        <span style="font-size:12px;color:${curTextColor};min-width:32px;">${escapeHtml(r.current_display)}</span>
      </div>
    </div>`;
  }).join('');
}
