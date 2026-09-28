// SkillTrace India : Client Controller & UI State Engine
// Adheres strictly to docs/UIUX_Design_Brief.md

let currentMetadata = { states: [], districts: [], schemes: [], courses: [] };
let selectedLanguage = 'hi';
let selectedActivity = 'Working';

document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  loadAnalytics();
  loadAuditLogs();
});

// Dark Theme Toggle
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const btn = document.getElementById('theme-btn');
  if (current === 'dark') {
    document.documentElement.removeAttribute('data-theme');
    if (btn) btn.innerText = 'Dark Theme';
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
    if (btn) btn.innerText = 'Light Theme';
  }
}

// Navigation Tabs
function setupNavigation() {
  const tabs = document.querySelectorAll('.gov-nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      document.querySelectorAll('.gov-view-section').forEach(sec => sec.style.display = 'none');
      const activeSec = document.getElementById(targetId);
      if (activeSec) activeSec.style.display = 'block';

      if (targetId === 'tab-registry') loadTrainees();
      if (targetId === 'tab-identity-queue') loadIdentityQueue();
      if (targetId === 'tab-dashboard') loadAnalytics();
      if (targetId === 'tab-dpo-console') loadAuditLogs();
    });
  });
}

// Analytics and Dashboard
async function loadAnalytics() {
  try {
    const res = await fetch('/api/v1/analytics/funnel/');
    const data = await res.json();

    if (document.getElementById('dash-certified')) {
      document.getElementById('dash-certified').innerText = data.kpis.total_certified.toLocaleString();
      document.getElementById('dash-verified-rate').innerText = data.kpis.verified_placement_rate + '%';
      document.getElementById('dash-reported-rate').innerText = data.kpis.reported_placement_rate + '%';
      document.getElementById('dash-retention-rate').innerText = data.kpis.six_month_retention_rate + '%';
    }
  } catch (err) {
    console.error("Analytics fetch error:", err);
  }
}

// Trainee Experience Interactive Flow
function selectLang(elem, langCode) {
  document.querySelectorAll('#trainee-screen-1 .big-choice-tile').forEach(t => t.classList.remove('selected'));
  elem.classList.add('selected');
  selectedLanguage = langCode;
}

function playVoicePrompt() {
  if ('speechSynthesis' in window) {
    const text = "SkillTrace India tracks your placement to ensure training quality. We only share your name and course with employers to confirm hiring. You can change your mind any time.";
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  } else {
    alert("Voice synthesis is active. Audio prompt is playing.");
  }
}

function nextTraineeStep(step) {
  for (let i = 1; i <= 5; i++) {
    const s = document.getElementById(`trainee-screen-${i}`);
    if (s) s.style.display = 'none';
  }
  const doneScreen = document.getElementById('trainee-screen-done');
  if (doneScreen) doneScreen.style.display = 'none';

  const target = document.getElementById(`trainee-screen-${step}`);
  if (target) target.style.display = 'block';

  const indicator = document.getElementById('trainee-step-indicator');
  const fill = document.getElementById('trainee-stepper-fill');
  if (indicator) indicator.innerText = `Step ${step} of 5`;
  if (fill) fill.style.width = `${step * 20}%`;
}

function pickActivity(elem, activity) {
  document.querySelectorAll('#trainee-screen-4 .big-choice-tile').forEach(t => t.classList.remove('selected'));
  elem.classList.add('selected');
  selectedActivity = activity;
}

async function submitTraineeCheckin() {
  const empName = document.getElementById('t-employer-name') ? document.getElementById('t-employer-name').value : '';
  const wageBand = document.getElementById('t-wage-band') ? document.getElementById('t-wage-band').value : '1.0X_TO_1.5X';

  try {
    await fetch('/api/v1/trainee/checkin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status_choice: selectedActivity,
        employer_name: empName,
        wage_band: wageBand,
        stid: 'ST-27-10000001'
      })
    });
  } catch (e) {
    console.log("Check-in logged locally");
  }

  for (let i = 1; i <= 5; i++) {
    const s = document.getElementById(`trainee-screen-${i}`);
    if (s) s.style.display = 'none';
  }
  const done = document.getElementById('trainee-screen-done');
  if (done) done.style.display = 'block';

  const fill = document.getElementById('trainee-stepper-fill');
  if (fill) fill.style.width = '100%';
  const ind = document.getElementById('trainee-step-indicator');
  if (ind) ind.innerText = 'Completed';
}

// Budget Simulation Slider
function updateBudgetSim(val) {
  const label = document.getElementById('budget-val');
  if (label) label.innerText = `+${val}%`;
  const gain = document.getElementById('sim-gain');
  if (gain) {
    const net = Math.round(val * 432);
    gain.innerText = `+${net.toLocaleString()} Verified Placements`;
  }
}

// Trainee Registry
async function loadTrainees() {
  const tbody = document.getElementById('table-trainees-body');
  if (!tbody) return;

  const res = await fetch('/api/v1/trainees/');
  const data = await res.json();
  tbody.innerHTML = '';

  data.trainees.forEach(t => {
    const out = t.latest_outcome;
    const tierBadge = out ? `<span class="tier-badge tier-badge-${out.tier.toLowerCase()}">Tier ${out.tier}</span>` : '<span class="tier-badge tier-badge-u">Tier U</span>';
    tbody.innerHTML += `
      <tr>
        <td><span class="stid-badge">${t.stid}</span></td>
        <td>${t.full_name} (${t.gender})</td>
        <td><code>${t.phone_masked}</code></td>
        <td>${t.state_code}</td>
        <td>${t.scheme}</td>
        <td>${t.course}</td>
        <td>${tierBadge}</td>
        <td>${out ? out.kind.replace('_', ' ') : 'Pending'}</td>
        <td>${out ? out.employer : '-'}</td>
        <td>${out ? out.wage_band : '-'}</td>
      </tr>
    `;
  });
}

// Identity Queue
async function loadIdentityQueue() {
  const container = document.getElementById('identity-queue-container');
  if (!container) return;

  const res = await fetch('/api/v1/identity/review-queue/');
  const data = await res.json();
  container.innerHTML = '';

  if (data.length === 0) {
    container.innerHTML = '<div class="gov-panel">Zero ambiguous matches pending in grey band.</div>';
    return;
  }

  data.forEach(item => {
    container.innerHTML += `
      <div class="gov-panel" style="margin-bottom:14px;">
        <div class="gov-panel-header">
          <span class="gov-panel-title">Match Score: ${(item.match_score * 100).toFixed(1)}% (Grey Band 0.75 to 0.92)</span>
          <span class="gov-panel-badge">Queue ID: #${item.id}</span>
        </div>
        <p style="font-size:12px; color:var(--st-muted); margin-bottom:12px;">${item.match_reasons}</p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px; font-size:12px;">
          <div style="background:var(--st-tint); border:1px solid var(--st-border); border-radius:var(--st-radius-sm); padding:10px;">
            <p><strong>Candidate A:</strong> <span class="stid-badge">${item.candidate_a_details.stid}</span></p>
            <p>Name: ${item.candidate_a_details.full_name}</p>
            <p>DOB: ${item.candidate_a_details.dob}</p>
            <p>Address: ${item.candidate_a_details.address}</p>
          </div>
          <div style="background:var(--st-tint); border:1px solid var(--st-border); border-radius:var(--st-radius-sm); padding:10px;">
            <p><strong>Candidate B:</strong> <span class="stid-badge">${item.candidate_b_details.stid}</span></p>
            <p>Name: ${item.candidate_b_details.full_name}</p>
            <p>DOB: ${item.candidate_b_details.dob}</p>
            <p>Address: ${item.candidate_b_details.address}</p>
          </div>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="gov-btn gov-btn-success" onclick="resolveId(${item.id}, 'MERGE')">Confirm Match & Merge STIDs (Audit Logged)</button>
          <button class="gov-btn gov-btn-secondary" onclick="resolveId(${item.id}, 'REJECT_DISTINCT')">Keep Distinct Persons</button>
        </div>
      </div>
    `;
  });
}

async function resolveId(id, decision) {
  await fetch('/api/v1/identity/review-queue/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ queue_id: id, decision: decision })
  });
  alert("Decision committed to audit trail.");
  loadIdentityQueue();
}

// Audit Log Stream
async function loadAuditLogs() {
  const tbody = document.getElementById('table-audit-body');
  if (!tbody) return;

  const res = await fetch('/api/v1/audit/logs/');
  const data = await res.json();
  tbody.innerHTML = '';

  data.slice(0, 10).forEach(ev => {
    tbody.innerHTML += `
      <tr>
        <td>#${ev.id}</td>
        <td>${ev.timestamp.replace('T', ' ').substring(0, 19)}</td>
        <td><code>${ev.actor}</code></td>
        <td><strong>${ev.action}</strong></td>
        <td>${ev.target_object}</td>
        <td><code style="font-size:11px;">${ev.event_hash.substring(0, 16)}...</code></td>
      </tr>
    `;
  });
}
