# SkillTrace India

### National Longitudinal Skilling Outcomes and Impact Measurement Platform
**Production Build v2.0 | Digital Public Infrastructure (DPI) | Government of India Standard**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

---

## Overview

India runs multiple large-scale vocational skilling programmes (PMKVY, DDU-GKY, NAPS/NATS, ITIs under DGT, and State Skill Development Missions). While enrollment and certification are rigorously tracked, post-certification placement, self-employment, retention, and wage progression are frequently lost due to SIM card churn and reliance on self-reported placement claims.

**SkillTrace India** provides a consent-based longitudinal outcomes measurement layer that sits atop existing training registries:
- **Longitudinal Trainee Record:** Unique privacy-preserving identifier (`ST-XX-XXXXXXXX`).
- **Evidence Tiering (A, B, C, D, U):** Separates statutory and employer-confirmed placements from unverified self-reports.
- **Direct 3-Tap Employer Verification:** Zero-login mobile web flow for enterprise HR.
- **DPDP Act 2023 Compliance:** Cryptographic SHA-256 consent receipts, Identity Vault separation, zero raw Aadhaar, and k-anonymity (k >= 10).
- **Risk-Adjusted Provider Delta Scorecards:** Adjusts observed outcomes by District Labour Market Index (LMI) to prevent penalizing training centers in aspirational districts.

---

## Architecture & Technology Stack

- **Backend:** Python 3.12, Django 5, Django REST Framework (DRF), WhiteNoise, Gunicorn
- **Frontend:** CSS Design Tokens (`tokens.css`), Inter, Noto Sans, JetBrains Mono
- **Database:** Relational engine with logical Identity Vault isolation
- **DPI Standards:** LGD (Local Government Directory), NCO-2015, NSQF Levels 1-8

---

## Local Setup & Quickstart

```bash
# Clone the repository
git clone https://github.com/priyanshu-pgb/skilltrace-india.git
cd skilltrace-india

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed synthetic national data
python manage.py migrate
python manage.py seed_data

# Start development server
python manage.py runserver 8000
```

Open `http://127.0.0.1:8000/` in your browser.

---

## Deployment to Render

This repository includes `render.yaml` and `Procfile` configured for automated zero-cost deployment:
- **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --no-input`
- **Start Command:** `gunicorn skilltrace_project.wsgi:application --bind 0.0.0.0:$PORT`
- **Region:** Singapore / Frankfurt / Oregon
