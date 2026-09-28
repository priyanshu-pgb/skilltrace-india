/**
 * SkillBridge - Chart Initialization Helpers (Chart.js)
 */

window.SkillBridgeCharts = {
  /**
   * Render Claimed vs Verified Comparison Bar Chart
   */
  renderUserSkillsChart(canvasId, labels, claimedData, verifiedData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Claimed Level Equivalent',
            data: claimedData,
            backgroundColor: 'rgba(203, 213, 225, 0.7)',
            borderColor: '#94a3b8',
            borderWidth: 1,
            borderRadius: 4,
          },
          {
            label: 'Verified Score (%)',
            data: verifiedData,
            backgroundColor: 'rgba(79, 70, 229, 0.85)',
            borderColor: '#4f46e5',
            borderWidth: 1,
            borderRadius: 4,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { family: 'Inter', weight: 600 } }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.raw}%`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: function(value) { return value + '%'; }
            }
          }
        }
      }
    });
  },

  /**
   * Render Employment Status Distribution Donut Chart
   */
  renderEmploymentDonut(canvasId, labels, counts) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: counts,
          backgroundColor: [
            '#10b981', // Employed
            '#0ea5e9', // Internship
            '#8b5cf6', // Freelance
            '#f59e0b', // Self-employed
            '#6366f1', // Higher studies
            '#ef4444', // Unemployed
          ],
          borderWidth: 2,
          borderColor: '#ffffff',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: { boxWidth: 12, font: { family: 'Inter' } }
          }
        },
        cutout: '70%'
      }
    });
  },

  /**
   * Render Before vs After Impact Comparison Bar Chart
   */
  renderImpactChart(canvasId, labels, beforeScores, afterScores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Score Before Training',
            data: beforeScores,
            backgroundColor: '#cbd5e1',
            borderRadius: 4,
          },
          {
            label: 'Score After Training (Re-Assessed)',
            data: afterScores,
            backgroundColor: '#10b981',
            borderRadius: 4,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { font: { family: 'Inter', weight: 600 } } }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: { callback: function(val) { return val + '%'; } }
          }
        }
      }
    });
  }
};
