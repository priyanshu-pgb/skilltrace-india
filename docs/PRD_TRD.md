# SkillTrace India: Product and Technical Requirements (PRD + TRD v2.0)

## Executive Summary
SkillTrace India is a national longitudinal skilling outcomes and impact measurement platform designed for zero-cost operation and seamless migration to Government of India MeghRaj cloud infrastructure.

## Stack
- Framework: Python 3.12, Django 5, Django REST Framework
- Database: PostgreSQL / SQLite with Identity Vault logical separation
- Frontend: Vanilla JS + CSS Tokens (Inter, Noto Sans, JetBrains Mono)
- Security: DPDP Act 2023 Compliant, zero raw Aadhaar, HMAC-SHA256 salted phone hashing, k-anonymity (k >= 10)
- Deployment: Render / Docker / Gunicorn / WhiteNoise
