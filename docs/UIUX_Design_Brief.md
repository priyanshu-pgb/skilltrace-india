# SkillTrace India: UI/UX Design Brief and App Flow

## 1. Design Vision

**One line:** Calm, trustworthy, and simple enough for a trainee on a 2G phone, yet rigorous enough for a Secretary reading a national dashboard.

**Feel:** clean and official, but warm. Not a cold government portal, not a flashy startup. Think "a helpful district office that finally works well."

**Design pillars**

| Pillar | What it means on screen |
| --- | --- |
| Trust | Every number shows its coverage and evidence mix. Consent and privacy are visible, never hidden in fine print |
| Low burden | One question per screen, big tap targets, pre filled answers, three taps to finish |
| Inclusive | Language first, voice first, icons with words, works offline and on low end phones |
| Clarity over decoration | White space, plain words, one accent colour per screen |
| Honest data | Never show a bare percentage. Always show "based on X of Y people, Z% verified" |

## 2. Users and Their Surfaces

| User | Main device | Surface | Design priority |
| --- | --- | --- | --- |
| Trainee | Budget Android, sometimes feature phone | WhatsApp/Telegram bot, mobile web page, IVR | Extreme simplicity, local language, voice |
| Employer | Phone or desktop | 3 tap verification page, bulk upload page | Zero learning curve, under 30 seconds |
| Field agent / trainer | Phone, often offline | Workbench PWA | Speed, offline safety, big buttons |
| District / state officer | Laptop | Dashboard, alerts, action cases | Scannable, drill down, exports |
| Policy maker | Laptop, tablet | National overview, ROI, gaps | Story first, few numbers, clear takeaways |
| Auditor | Laptop | Evidence trail viewer | Traceability, read only |
| DPO / admin | Laptop | Consent ledger, audit log, grievances | Precision, filters, safety confirmations |

## 3. Colour Palette

| Role | Name | Hex | Use |
| --- | --- | --- | --- |
| Primary | Deep Indigo | `#1F3A93` | Header, primary buttons, links |
| Primary dark | Midnight | `#142766` | Hover, pressed, headings on tint |
| Accent | Saffron | `#F28C1B` | Key call to action, highlights, progress |
| Success / verified | Peacock Green | `#1E8E5A` | Verified outcomes, success states |
| Info | Sky | `#2B7BE4` | Info banners, neutral chart series |
| Warning | Marigold | `#E0A400` | Needs attention, medium risk |
| Danger | Brick Red | `#C8382F` | Errors, fraud flags, destructive actions |
| Background | Warm White | `#FAF8F5` | App background |
| Surface | White | `#FFFFFF` | Cards, tables |
| Surface tint | Indigo Mist | `#EEF1FA` | Sections, selected rows |
| Border | Stone | `#E3DED6` | Dividers, inputs |
| Text primary | Ink | `#1B1F2A` | Body and headings |
| Text secondary | Slate | `#5B6270` | Helper text |

## 4. Evidence Tier Colours
- Tier A: `#1E8E5A` green - Registry or document verified
- Tier B: `#3E9B6B` light green - Employer or provider confirmed
- Tier C: `#E0A400` marigold - Self report with corroboration
- Tier D: `#E07B2A` orange - Unverified self report
- Tier U: `#8A90A0` grey - Unknown, unreachable

## 5. Typography
- Latin UI and numbers: Inter
- Indic scripts: Noto Sans family (Devanagari, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Gurmukhi, Odia)
- Code, IDs (STID): JetBrains Mono
