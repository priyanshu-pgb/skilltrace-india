# SkillBridge

> **Assess. Improve. Connect.**  
> *Difficulties in Tracking Employment Outcomes, Skill Gaps, and the Impact of Skilling Initiatives*

---

## 1. Project Overview

**SkillBridge** is a modern, full-stack college-level career-tech platform designed to address systemic friction in evaluating vocational and technical training. It establishes an evidence-based pipeline that tracks learners from initial skill declarations to practical assessments, mathematical skill-gap analysis, targeted training, post-curriculum re-assessment, and longitudinal employment verification.

### Core Lifecycle

```text
CLAIMED SKILL
      ↓
    ASSESS
      ↓
    VERIFY
      ↓
VERIFIED SKILL
      ↓
COMPARE WITH JOB
      ↓
IDENTIFY SKILL GAP
      ↓
RECOMMEND TRAINING
      ↓
TRACK TRAINING
      ↓
  RE-ASSESS
      ↓
TRACK EMPLOYMENT
      ↓
ANALYZE IMPACT
```

---

## 2. Key Features

1. **Claimed vs. Verified Competencies**:
   - Explicitly decouples self-reported confidence from demonstrated skills.
   - Evaluates skills across three calibrated weights: **MCQ (20%)**, **Practical Coding (50%)**, and **Reviewed Projects (30%)**.
   - Assigns a 5-tier proficiency taxonomy:
     - Level 1: Beginner (0–39%)
     - Level 2: Basic (40–59%)
     - Level 3: Intermediate (60–74%)
     - Level 4: Advanced (75–89%)
     - Level 5: Expert (90–100%)

2. **Assessment & Anti-Cheating Engine**:
   - 10-minute timer with countdown and auto-submission on expiration.
   - Randomized question sampling from curated question banks.
   - Single-attempt evaluation with server-side validation (correct answers are never exposed in the client HTML).
   - Post-submission answer breakdowns with detailed explanations.

3. **Hands-on Practical Coding Workspace**:
   - Sandboxed deterministic code execution for algorithmic challenges.
   - Immediate test-case evaluation ($N/N$ passed) with detailed feedback.

4. **Project Verification Queue**:
   - Trainees submit GitHub repository and live deployment URLs.
   - Administrative review interface allows assigning scores (0–100%) and personalized feedback.

5. **Mathematical Skill-Gap Engine**:
   - Calculates exact numeric level deltas ($\text{Gap} = \text{Required Level} - \text{Verified Level}$).
   - Computes **Job Readiness Match %**:
     $$\text{Job Match} = \frac{\text{Matched Required Skills}}{\text{Total Required Skills}} \times 100$$
   - Displays animated circular progress gauges and requirement alignment tables.

6. **Targeted Training & Re-Assessment Engine**:
   - Maps missing skills directly to specific upskilling courses.
   - Interactive progress slider ($0 \to 100\%$).
   - Post-completion re-assessment comparison cards displaying exact point improvements (e.g., $+40$ pts).

7. **Longitudinal Employment Tracker**:
   - Tracks career outcomes across 6 categories: *Formally Employed*, *Internship*, *Freelancing*, *Self-Employed*, *Higher Studies*, and *Unemployed*.
   - Dynamic form adaptation (omits corporate fields when unemployed).
   - Administrative audit verification badge.

8. **Administrative Impact Analytics**:
   - Macro KPIs: Total Candidates, Assessments Completed, Verified Projects, Employment Rate %, and Average Post-Training Improvement Delta.
   - Real-time interactive charts (Chart.js):
     - Employment Status Distribution (Donut Chart)
     - Longitudinal Before vs After Training Score Progression (Grouped Bar Chart)
     - Market Benchmark vs Trainee Cohort Friction Gaps table.

---

## 3. Technology Stack

- **Backend**: Python 3.14, Django 6.1.1, Django ORM, PyMySQL
- **Database**: MySQL (production-ready via PyMySQL with automatic local development fallback)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System with CSS variables and reduced-motion support), Vanilla JavaScript ES6+, Bootstrap 5.3, Font Awesome 6.5, Chart.js 4.4
- **Testing**: Django Test Framework, Pytest-compatible

---

## 4. Setup & Running Locally

### Prerequisites
- Python 3.10+ installed
- MySQL (Optional: app automatically uses SQLite if MySQL credentials are not active)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/omm-prakash-biswal/SkillPulse-v1.git
   cd SkillPulse-v1
   ```

2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

4. **Run Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed Demonstration Data**:
   ```bash
   python manage.py seed_demo_data
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 5. Demo Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **System Administrator** | `admin` | `adminpassword123` | Access admin analytics, review projects, and inspect macro impact metrics. |
| **Student / Candidate** | `alex_candidate` | `candidatepass123` | Active candidate with claimed/verified skills, assessments, and training. |
| **Employed Candidate** | `priya_analyst` | `candidatepass123` | Demonstrates $+40$ pts re-assessment jump and verified placement outcome. |

---

## 6. Automated Testing

Run the test suite:
```bash
python manage.py test tests
```
The test suite validates authentication, claimed vs. verified calculations, mathematical gap logic, training deltas, employment updates, and role-based access control.

---

## 7. Project Limitations

1. **Self-Reported Baseline**: Initial claimed levels and unverified employment statuses represent user-reported declarations until verified through system evaluations or administrative audits.
2. **Demo Data**: Seeded demonstration users and records are synthetic and designed for educational showcase purposes.
3. **Execution Sandbox**: Practical code evaluation is evaluated in a deterministic sandbox; advanced production deployments should employ isolated Docker/gVisor micro-containers.
