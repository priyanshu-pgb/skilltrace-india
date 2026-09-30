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
  },

  /**
   * Render Longitudinal Retention & Wage Progression Dual-Axis Chart
   */
  renderLongitudinalChart(canvasId, labels, retentionRates, avgWages) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Retention Rate (%)',
            data: retentionRates,
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            fill: true,
            tension: 0.3,
            yAxisID: 'y',
            pointRadius: 6,
            pointHoverRadius: 8,
          },
          {
            label: 'Avg Monthly Wage (₹)',
            data: avgWages,
            borderColor: '#10b981',
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.3,
            yAxisID: 'y1',
            pointRadius: 6,
            pointHoverRadius: 8,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', labels: { font: { family: 'Inter', weight: 600 } } },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                if (ctx.datasetIndex === 0) return `Retention: ${ctx.raw}%`;
                return `Monthly Wage: ₹${ctx.raw.toLocaleString('en-IN')}`;
              }
            }
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            min: 0,
            max: 100,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: 'Cohort Retention Rate' }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { callback: v => '₹' + (v/1000) + 'k' },
            title: { display: true, text: 'Monthly Take-Home Wage' }
          }
        }
      }
    });
  },

  /**
   * Render Systemic Root-Causes for Non-Placement / Attrition
   */
  renderAttritionDonut(canvasId, labels, counts) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: counts,
          backgroundColor: [
            '#ef4444', // Relocation refusal
            '#f59e0b', // Wage dissatisfaction
            '#ec4899', // Family/marriage
            '#8b5cf6', // Skill mismatch
            '#6366f1', // Local opportunity lack
            '#64748b', // Health/personal
            '#0ea5e9', // Joined informal
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
            labels: { boxWidth: 12, font: { family: 'Inter', size: 11 } }
          }
        },
        cutout: '65%'
      }
    });
  },

  /**
   * Render Demographic Equity Chart
   */
  renderDemographicBar(canvasId, labels, rates) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Placement / Livelihood Rate (%)',
          data: rates,
          backgroundColor: ['#ec4899', '#3b82f6', '#8b5cf6'],
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: { callback: v => v + '%' }
          }
        }
      }
    });
  }
};

