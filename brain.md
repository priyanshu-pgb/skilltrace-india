# brain.md: SkillTrace India

> Single source of truth for anyone (human or AI assistant) working on this repo. Read this first. Keep it short and current.

## 1. What we are building
**SkillTrace India** is a consent based platform that tracks what happens to trainees **after** certification across all Indian skilling schemes (PMKVY, NAPS/NATS, ITI, DDU-GKY, state missions). It links training to outcomes (placement, self employment, apprenticeship, retention, wage band), grades every outcome by **evidence tier**, and turns the data into fair analytics, alerts and action cases.

It sits **on top of** existing systems. It does not replace them and it is not a job portal.

Team: students, **zero budget**, using free tiers and open source. Built with synthetic data until written permission for real data exists.

Full docs: `docs/PRD_TRD.md` (product and technical), `docs/UIUX_Design_Brief.md` (design and flows).

## 2. Tech stack (decided)
- Python 3.12, **Django 5**, Django REST Framework, drf-spectacular
- PostgreSQL 16 (app DB) + **separate Postgres DB for identity vault**
- Redis, Celery, Celery Beat
- Splink + RapidFuzz (identity matching), scikit-learn, statsmodels, HuggingFace (IndicBERT), Bhashini
- Frontend: React/Next.js + Tailwind (dashboards, workbench PWA); Django templates + HTMX (trainee and employer pages)
- Docker Compose, Caddy, GitHub Actions, Sentry, Prometheus/Grafana, Metabase
- Hosting: Oracle Always Free VM (fallback: Render/Koyeb), Cloudflare free

## 3. Repo layout
```
config/            settings (base, dev, prod), urls, celery.py
apps/core          state config, LGD masters, base models, audit
apps/identity      Person(STID), ContactPoint, crosswalk, matching, review queue
apps/consent       ConsentArtefact, notices, withdrawal, DPDP requests
apps/ingestion     scheme adapters, uploads, data quality, rejects
apps/programs      Scheme, Course, Provider, Batch, Enrolment, Assessment, Certificate
apps/outcomes      OutcomeEpisode, EvidenceItem, rules engine, retention, wage bands
apps/followup      Survey, FollowUpTask, orchestrator, channel gateways, workbench API
apps/employers     Employer, VerificationRequest, trust, fraud rules
apps/analytics     materialized views, scorecards, weights, exports
apps/insights      reason classification, skill gap, demand vs supply
apps/alerts        alert rules, ActionCase workflow
apps/accounts      users, roles, scopes
apps/publicapi     de-identified read API + k anonymity guard
integrations/      sms, whatsapp, telegram, ivr, digilocker, epfo, ncs (mock + real)
ml/                matching, propensity, fraud, nlp
deploy/  docs/  tests/
```

## 4. Non negotiable rules
**Privacy and legal**
1. **Never store or log raw Aadhaar.** Do not collect it in the student build. Use mobile OTP, APAAR, DigiLocker (mock now).
2. PII lives **only** in the identity vault DB. Analytics and public API see the pseudonymous **STID** only.
3. No message is sent without a **consent purpose check**. No registry linkage without lawful basis.
4. Every PII read writes an **AuditEvent** (who, what, purpose). Audit log is append only and hash chained.
5. Public aggregates must pass **k anonymity (k >= 10)**. Suppress small cells.
6. Never use real trainee data in dev. Use the synthetic generator only.
7. Never commit secrets. Use `.env` (git ignored) and SOPS/age for shared secrets.

**Data and logic**
8. Every outcome has an **evidence tier** (A, B, C, D, U). Never publish a bare percentage: show *verified rate, reported rate, coverage, n*.
9. **Unreachable is a status**, never dropped. It feeds non response weights.
10. Rules are **versioned** (`rules_vN.yaml`). Never hardcode thresholds in views.
11. Wage is stored as a **band**, relative to state minimum wage, not exact salary.
12. Provider comparison must be **risk adjusted** with confidence intervals. No punitive automation without human review.
13. Every record carries `state_code` and `district_code` (LGD).

**Code**
14. Every external service (SMS, WhatsApp, registry, identity) sits behind an **interface** with a mock and a real implementation. Core code never imports a vendor SDK directly.
15. All queryset access goes through **scoped managers** (state, district, provider). No raw unscoped queries in views.
16. Long work runs in **Celery tasks**, idempotent, retry safe.
17. Bulk loads use `COPY` or `bulk_create`, never row by row in a loop.
18. All user facing strings use gettext. No hardcoded text.

## 5. Glossary
| Term | Meaning |
|---|---|
| STID | SkillTrace ID, random non derivable person ID |
| Wave | Follow up point: T+30, 90, 180, 365, 730 days after certification |
| Tier A to D, U | Evidence confidence levels (A strongest, U unknown) |
| Episode | One job, business, apprenticeship or study period in a trainee timeline |
| Vault | Separate encrypted DB holding PII |
| Adapter | Class mapping one scheme's data export to our schema |
| State config pack | JSON with local min wage, languages, schedule, rule overrides |
| LGD | Local Government Directory codes (state, district, block, village) |
| NCO, NSQF, NIC | Occupation, qualification level, industry classification codes |
| Sub sample | 5 to 10% of a cohort chased intensively to correct non response bias |

## 6. Design tokens (short)
Primary `#1F3A93`, accent (next action) `#F28C1B`, success `#1E8E5A`, warning `#E0A400`, danger `#C8382F`, background `#FAF8F5`, text `#1B1F2A`. Fonts: Inter + Noto Sans (Indic). Body text 16px minimum. Tap targets 48px. Tier badges always show the letter, not just colour. Full spec: `docs/UIUX_Design_Brief.md`.

## 7. App flow (one paragraph)
Trainee enrolled, gets notice, picks language, agrees with OTP consent, STID created. On certification the case opens. At each wave the orchestrator asks one tap "what are you doing now" through the cheapest channel and escalates if no reply. If employed, the employer gets a 3 tap link to confirm. The rules engine assigns an evidence tier, fraud rules check anomalies, analytics refresh, alerts open action cases for officers, and closed cases are re checked next wave.

## 8. Common commands
```bash
docker compose up -d                 # start db, vault, redis, web, worker, beat
python manage.py migrate
python manage.py seed_data           # LGD, NCO, NSQF, NIC + synthetic cohorts
python manage.py createsuperuser
pytest -q --cov=skilltrace           # tests
```
