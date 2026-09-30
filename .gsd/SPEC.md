# Project: SOPAN - National Longitudinal Skilling Outcomes & Impact Platform

> **Status:** `FINALIZED`
>
> 🔒 **Planning Lock**: This specification is marked `FINALIZED` and serves as the architectural contract for the SOPAN (सोपान) platform.

## Vision
A consent-based, longitudinal skilling-outcomes and impact-measurement system that bridges India's post-training outcome data gap. SOPAN tracks multi-year employment retention, wage progression, skill relevancy, and training partner accountability through automated 30s WhatsApp check-ins, assisted tele-calling workflows, and tamper-proof 1-click employer audit links.

## Goals
1. **Longitudinal Outcome Tracking** — Track 3, 6, 12, and 24-month livelihood milestones beyond initial training and certification.
2. **Standardized Competency Verification** — Provide randomized 10-question MCQ evaluations and practical coding challenges across 10 core technical and soft skill domains.
3. **Low-Burden Verification for Employers** — 1-click tokenized employer validation links with zero HR login friction.
4. **Training Provider Accountability** — Dynamic performance benchmarking comparing NSDC/State Mission training providers by audited retention rate and wage increase deltas.
5. **Humanized & Inclusive UX** — 2D flat vector editorial cartoon guides (Mentor Maya & Trainer Vikram), bilingual English/Hindi interface tokens, and conversational AI guidance.

## Non-Goals (Out of Scope)
- Building a private proprietary video streaming LMS (SOPAN aggregates and verifies competencies from accredited institutions).
- Replacing official Aadhaar/DigiLocker infrastructure (SOPAN references unified IDs without storing sensitive biometric credentials).
- Manual paper auditing or high-friction desktop-only spreadsheets.

## Constraints
- **DPDP Act 2023 Compliance**: Explicit consent logging, privacy-by-design data isolation, and purpose-limited contact fields.
- **Python / Django Framework**: Django 5.x with SQLite fallback for rapid testing and PostgreSQL for cloud scale.
- **Production Cloud**: Containerized deployment on Render with Gunicorn, Whitenoise, and automated collectstatic.
- **2D Cartoon Visual Style**: Editorial clean vector illustration aesthetic (explicitly prohibiting glossy 3D AI renders).

## Success Criteria
- [x] Zero-barrier assessment catalog: all 10 skills equipped with randomized MCQs and sandboxed practicals.
- [x] Dedicated production deployment at `https://sopan-career.onrender.com/` returning HTTP 200 OK.
- [x] Working conversational chatbot proctor with dual launcher triggers (navbar + bottom-right).
- [x] Comprehensive test suite with 100% passing tests (`python manage.py test tests`).
- [x] GSD Mission Control extension integration with real-time health score 100/100.

## Core Architectural Deliverables

| Component | Status | Location | Notes |
| :--- | :--- | :--- | :--- |
| **Longitudinal Tracker** | Complete | `employment/` | Multi-month milestone ledger & wage escalation |
| **Assessment Engine** | Complete | `assessments/` | 80 curated MCQs + 8 practical sandbox tasks |
| **AI Guide & Chatbot** | Complete | `core/` & `templates/` | Dual-trigger Mentor Maya / Trainer Vikram proctor |
| **Employer Audit** | Complete | `employment/` | Tokenized 1-click verification URLs |
| **Mission Control** | Complete | `.gsd/` | Spec-driven GSD state, roadmap, and doctor |

---

*Last updated: 2026-09-30*
