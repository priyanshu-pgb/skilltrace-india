# Architecture — SOPAN Platform

> Auto-generated and verified for GSD Mission Control on 2026-09-30

## Overview

SOPAN (सोपान • Career Ladder) is an enterprise-grade longitudinal skilling outcome registry and impact measurement platform built with Python/Django, modern vanilla tokenized styling (Apple SF Pro & Blinkit hybrid aesthetic), and cloud-native containerized hosting on Render.

```
┌────────────────────────────────────────────────────────────────────────┐
│             USER TIERS (Candidate, Trainer/Admin, Employer)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│           PRESENTATION & INTERACTION LAYER                             │
│   • Apple Design Token CSS & Micro-Animations                          │
│   • Conversational Mentor AI Proctor (Mentor Maya & Trainer Vikram)    │
│   • Live Ticker Marquee & 2D Flat Vector SVG Illustrations            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│           DJANGO CORE SERVICES & DOMAIN APPS                           │
│   • accounts/    : Custom User, Profiles, DPDP Consent Ledger          │
│   • skills/      : Claimed vs. Verified Portfolio & Score Calculation  │
│   • assessments/ : 80+ MCQs & Sandboxed Practical Coding Engine        │
│   • employment/  : Multi-year Milestones & 1-Click Employer Audits     │
│   • analytics/   : Retention Curves, Attrition Diagnostics, KPIs       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│           DATA PERSISTENCE & CLOUD DEPLOYMENT                          │
│   • PostgreSQL / SQLite Fallback with Transaction Safety               │
│   • Whitenoise Static Asset Pipeline with Compression                  │
│   • Live Render Web Service: https://sopan-career.onrender.com/       │
└────────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. accounts (`SkillPulse-v1/accounts/`)
- **Purpose:** Custom User authentication model (`role='user'|'admin'`), user profiles, contact consent flags, and demographic district classification.
- **Key Files:** `models.py`, `views.py`, `forms.py`.

### 2. skills (`SkillPulse-v1/skills/`)
- **Purpose:** Skills taxonomy, claimed ability benchmarks, automated normalized scoring algorithm (MCQ 20% + Practical 50% + Project 30%), and tamper-proof verification badges.
- **Key Files:** `models.py`, `views.py`.

### 3. assessments (`SkillPulse-v1/assessments/`)
- **Purpose:** 10-domain question banks, anti-cheating proctoring timers, non-blocking question navigators, and multi-language code evaluation sandboxes.
- **Key Files:** `models.py`, `views.py`, `templates/assessments/take_assessment.html`.

### 4. employment (`SkillPulse-v1/employment/`)
- **Purpose:** Longitudinal employment records, 3/6/12/24-month livelihood milestone tracking, wage progression logs, 1-click employer validation links, and 30s WhatsApp check-in simulation.
- **Key Files:** `models.py`, `views.py`, `urls.py`.

### 5. analytics (`SkillPulse-v1/analytics/`)
- **Purpose:** National command center data feeds, retention survival curves (0-24m), wage escalation dual-axis metrics, and systemic attrition root-cause diagnostics.
- **Key Files:** `views.py`, `static/js/charts.js`.

## Data Flow

1. **Candidate Registration & Consent:** Candidate registers, consents to longitudinal follow-ups under DPDP Act 2023, and logs self-claimed skills.
2. **Objective Verification:** Candidate completes randomized 10-question MCQ test or practical coding task in the Assessment Center. Server calculates score and updates verified index.
3. **Employer Outcome Validation:** When employed or receiving wage increments, a tokenized verification URL is generated for HR/employers to confirm in 1 click without credentials.
4. **Longitudinal Persistence:** Automated WhatsApp triggers prompt 30s wage updates at 3, 6, and 12-month intervals, populating national retention analytics.

## Technical Debt & Ongoing Hardening

- [x] Zero-barrier assessment questions seeded for all 10 skill domains
- [x] Clean removal of blocking required attributes in assessment forms
- [x] Dual launcher support for conversational chatbot
- [ ] Connect production WhatsApp Cloud API webhook receiver (currently high-fidelity simulator)
- [ ] Transition from local SQLite to cloud-managed PostgreSQL instance for multi-region clustering

---

*Last updated: 2026-09-30*
