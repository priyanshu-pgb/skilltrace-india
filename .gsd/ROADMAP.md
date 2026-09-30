---
milestone: Milestone 1 - Production SOPAN Platform & Mission Control
version: 1.7.1
updated: 2026-09-30T20:30:00Z
---

# Roadmap

> **Current Phase:** 3 - Production Deployment & Verification
> **Status:** verifying

## Must-Haves (from SPEC)

- [x] DPDP-compliant longitudinal outcome tracking and milestone progression
- [x] Comprehensive 10-skill assessment center with randomized MCQs and coding tasks
- [x] 1-click tokenized employer verification flow without HR login barriers
- [x] 2D flat vector editorial cartoon styling (Mentor Maya & Trainer Vikram)
- [x] Dedicated Render deployment under `sopan-career.onrender.com`

---

## Phases

### Phase 1: Core Architecture & Longitudinal Ledger
**Status:** Complete
**Objective:** Establish core Django apps, custom accounts, longitudinal employment records, and milestone timeline tracking.
**Requirements:** REQ-01, REQ-02

**Plans:**
- [x] Plan 1.1: Core database migrations, custom User model, and seed data generator
- [x] Plan 1.2: Longitudinal livelihood tracker, milestone timeline, and wage progression

---

### Phase 2: Assessment Engine & 2D Humanized Illustrations
**Status:** Complete
**Objective:** Deliver 10-skill assessment catalog, zero-failure dynamic question fallback, and handcrafted 2D vector illustrations.
**Depends on:** Phase 1

**Plans:**
- [x] Plan 2.1: Design and render handcrafted 2D SVGs (Mentor Maya, Trainer Vikram, SOPAN logo)
- [x] Plan 2.2: Author 80 calibrated MCQs across 8 missing skills + 8 multi-language practical tasks
- [x] Plan 2.3: Build non-blocking assessment interface with sticky question navigator bar

---

### Phase 3: Production Deployment & Verification
**Status:** Complete
**Objective:** Deploy containerized application to Render Cloud, configure environment variables, and verify live endpoints.
**Depends on:** Phase 2

**Plans:**
- [x] Plan 3.1: Configure Whitenoise, Gunicorn, Procfile, and Render build pipeline
- [x] Plan 3.2: Provision dedicated `sopan-career.onrender.com` service on Render and verify HTTP 200
- [x] Plan 3.3: Execute comprehensive end-to-end test suite (`python manage.py test tests`)

---

### Phase 4: Multilingual Voice IVR & Field Integration
**Status:** In Progress
**Objective:** Integrate automated WhatsApp Business API webhooks, Rozgar Sahayak telephony logs, and state dashboard exports.
**Depends on:** Phase 3

**Plans:**
- [ ] Plan 4.1: Integrate live WhatsApp webhook handlers for 30s quick check-ins
- [ ] Plan 4.2: Automated CSV/Excel reporting export for NITI Aayog aspirational district partners

---

## Progress Summary

| Phase | Status | Plans | Complete |
|-------|--------|-------|----------|
| 1: Core Architecture | Complete | 2/2 | 100% |
| 2: Assessment Engine | Complete | 3/3 | 100% |
| 3: Production Deployment | Complete | 3/3 | 100% |
| 4: Field Integrations | In Progress | 0/2 | 0% |

---

*Last updated: 2026-09-30*
