/* ── Hero Chart ── */
window.addEventListener('load', () => {
  const ctx = document.getElementById('heroChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
      datasets: [
        {
          label: 'Positive',
          data: [55,58,61,60,64,67,65,69,71,70,72,75],
          borderColor: '#845433',
          backgroundColor: 'rgba(132,84,51,0.07)',
          fill: true, tension: 0.45, pointRadius: 0, borderWidth: 2.5
        },
        {
          label: 'Negative',
          data: [22,20,18,19,15,14,16,12,11,13,10,9],
          borderColor: '#c53030',
          backgroundColor: 'rgba(197,48,48,0.04)',
          fill: true, tension: 0.45, pointRadius: 0, borderWidth: 1.5, borderDash: [5,5]
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: {
        x: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#999491', font: { size: 11 } } },
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#999491', font: { size: 11 } }, min: 0, max: 100 }
      },
      animation: { duration: 1800, easing: 'easeInOutQuart' }
    }
  });
});
