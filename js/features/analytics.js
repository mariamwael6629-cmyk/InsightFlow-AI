/* ── Analytics ── */
let trendChartInstance = null;
let donutChartInstance = null;

function loadAnalyticsData() {
  loadMetrics().catch(e => console.error('metrics', e));
  loadTrendChart().catch(e => console.error('trend', e));
  loadDonutChart().catch(e => console.error('categories', e));
  loadHeatmap().catch(e => console.error('heatmap', e));
  loadIssues().catch(e => console.error('issues', e));
  loadRecommendations().catch(e => console.error('recommendations', e));
}

async function loadMetrics() {
  const m = await apiFetch('/api/analytics/metrics');
  const fieldMap = { total_responses: 'total', avg_sentiment: 'sentiment', issues_flagged: 'issues', ai_suggestions: 'ai' };
  Object.entries(fieldMap).forEach(([key, prefix]) => {
    const card = m[key];
    document.getElementById(`m-${prefix}-value`).textContent = card.value;
    const deltaEl = document.getElementById(`m-${prefix}-delta`);
    deltaEl.textContent = card.delta;
    deltaEl.className = `m-delta ${card.trend}`;
  });
}

async function loadTrendChart() {
  const points = await apiFetch('/api/analytics/trend');
  const data = {
    labels: points.map(p => new Date(p.stat_date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'short' })),
    datasets: [
      { label: 'Positive', data: points.map(p => p.positive_pct), borderColor: '#3a5496', backgroundColor: 'rgba(58,84,150,0.06)', fill: true, tension: 0.4, pointRadius: 4, pointBackgroundColor: '#3a5496', borderWidth: 2 },
      { label: 'Neutral',  data: points.map(p => p.neutral_pct),  borderColor: '#8b939f', backgroundColor: 'transparent', tension: 0.4, pointRadius: 4, pointBackgroundColor: '#8b939f', borderWidth: 2, borderDash: [5,4] },
      { label: 'Negative', data: points.map(p => p.negative_pct), borderColor: '#c53030', backgroundColor: 'transparent', tension: 0.4, pointRadius: 4, pointBackgroundColor: '#c53030', borderWidth: 2, borderDash: [3,3] }
    ]
  };
  if (trendChartInstance) {
    trendChartInstance.data = data;
    trendChartInstance.update();
    return;
  }
  trendChartInstance = new Chart(document.getElementById('trendChart').getContext('2d'), {
    type: 'line',
    data,
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#8b939f', font: { size: 11 } } },
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#8b939f', font: { size: 11 }, stepSize: 20 }, min: 0, max: 100 }
      }
    }
  });
}

async function loadDonutChart() {
  const categories = await apiFetch('/api/analytics/categories');

  document.getElementById('category-legend').innerHTML = categories.map(c => `
    <span class="tag" style="background:${hexToRgba(c.color, 0.12)};color:${c.color};font-size:11px;">● ${escapeHtml(c.category)} ${Math.round(c.percentage)}%</span>`).join('');

  const data = {
    labels: categories.map(c => c.category),
    datasets: [{ data: categories.map(c => c.percentage), backgroundColor: categories.map(c => c.color), borderWidth: 0, hoverOffset: 7 }]
  };
  if (donutChartInstance) {
    donutChartInstance.data = data;
    donutChartInstance.update();
  } else {
    donutChartInstance = new Chart(document.getElementById('donutChart').getContext('2d'), {
      type: 'doughnut',
      data,
      options: { responsive: true, maintainAspectRatio: false, cutout: '72%', plugins: { legend: { display: false } } }
    });
  }
}

async function loadHeatmap() {
  const cells = await apiFetch('/api/analytics/heatmap');
  const hm = document.getElementById('heatmap');
  hm.innerHTML = '';
  cells.forEach(c => {
    const cell = document.createElement('div');
    cell.className = 'hm-cell';
    const i = c.score / 9;
    if (i < 0.3)       cell.style.background = `rgba(38,122,78,${0.2 + i * 0.5})`;
    else if (i < 0.65) cell.style.background = `rgba(160,82,10,${0.2 + i * 0.4})`;
    else               cell.style.background = `rgba(197,48,48,${0.25 + i * 0.5})`;
    cell.title = `Mood score: ${c.score}/9`;
    hm.appendChild(cell);
  });
}

async function loadIssues() {
  const issues = await apiFetch('/api/analytics/issues');
  const maxCount = Math.max(...issues.map(i => i.count), 1);
  document.getElementById('issues-list').innerHTML = issues.map(iss => `
    <div class="issue-item">
      <span class="issue-rank">${iss.rank}</span>
      <span class="issue-label">${escapeHtml(iss.label)}</span>
      <div class="issue-bar-bg">
        <div class="issue-bar" style="width:${Math.round((iss.count / maxCount) * 100)}%;background:${iss.color};"></div>
      </div>
      <span class="issue-count">${iss.count}</span>
    </div>`).join('');
}

const PRIORITY_META = {
  high: { label: '🔴 High Priority', cls: 'high' },
  med:  { label: '🟡 Medium Priority', cls: 'med' },
  low:  { label: '🟢 Low Priority', cls: 'low' }
};

async function loadRecommendations() {
  const recs = await apiFetch('/api/analytics/recommendations');
  document.getElementById('rec-grid').innerHTML = recs.map(r => {
    const meta = PRIORITY_META[r.priority] || { label: r.priority, cls: r.priority };
    return `
    <div class="rec-item">
      <div class="rec-priority ${meta.cls}">${meta.label}</div>
      <div class="rec-text"><strong>${escapeHtml(r.title)}</strong> ${escapeHtml(r.detail)}</div>
    </div>`;
  }).join('');
}
