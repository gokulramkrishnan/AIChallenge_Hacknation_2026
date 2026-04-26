# UNMAPPED — World Bank Youth Summit · Hackathon Submission

> Config-driven skills infrastructure layer that turns invisible youth capability into portable economic signals and realistic opportunity paths using local data.

---

## What this is

UNMAPPED is a working prototype of an open, localizable infrastructure layer that closes the distance between a young person's real skills and real economic opportunity. It is infrastructure — not just an app. Any government, NGO, training provider, or employer can configure it with local data without rebuilding from scratch.

**Built for:** World Bank Youth Summit Hackathon  
**Challenge:** UNMAPPED — Skills-to-Opportunity Matching for LMIC Youth  
**Modules implemented:** All 3 (Skills Signal Engine · AI Readiness Lens · Opportunity Matching)

---

## Quick start — demo mode (no backend needed)

The React frontend calls the Claude API directly. For a live hackathon demo, you only need the frontend:

```bash
npm install
npm run dev
```

Open `http://localhost:5173` — Amara's profile is pre-loaded. Click **Analyze profile** to see all three modules.

---

## Full stack (with backend)

```bash
# Backend
pip install fastapi uvicorn pydantic
uvicorn backend:app --reload --port 8000

# Frontend
npm install
npm run dev
```

---

## Project structure

```
unmapped/
├── src/
│   └── App.jsx          ← Complete React frontend (all 3 modules + skills passport)
├── backend.py           ← FastAPI backend (reference implementation)
├── country_packs.json   ← 4 country configurations (Ghana, Kenya, Bangladesh, Nigeria)
├── pitch_deck.html      ← Standalone pitch deck (open in browser, print to PDF)
├── index.html
├── package.json
└── vite.config.js
```

---

## Modules

### Module 01 — Skills Signal Engine
- Input: education level, informal work history, languages, tasks
- Output: ISCO-08 mapped portable skills profile
- Human-readable, ESCO-categorized, explainable to non-experts
- **Portable across borders and sectors**

### Module 02 — AI Readiness & Displacement Risk Lens
- Output: Frey-Osborne automation risk score, LMIC-adjusted per country
- Shows durable vs. exposed skills with explanations
- Calibrated using country automation factor (0.85×–1.10×)
- **Incorporates Frey-Osborne (2013) real dataset**

### Module 03 — Opportunity Matching
- Output: 3 realistic, grounded pathways (not aspirational)
- Each pathway shows a visible econometric signal
- **Surfaces ILO informality rate, wage-salaried share, youth NEET share**

---

## Country packs

| Country | Region | Informality | Wage-salaried | Auto factor |
|---------|--------|-------------|---------------|-------------|
| Ghana 🇬🇭 | Sub-Saharan Africa · Urban | 78% | 32% | 0.85× |
| Kenya 🇰🇪 | East Africa · Mixed | 73% | 29% | 1.00× |
| Bangladesh 🇧🇩 | South Asia · Rural/peri-urban | 85% | 45% | 1.10× |
| Nigeria 🇳🇬 | West Africa · Urban | 80% | 22% | 0.90× |

**Configurable without changing code:**
- Labor market data source and structure
- Education taxonomy and credential mapping
- Automation exposure calibration
- Opportunity types surfaced
- UI language (language field in pack)

---

## Data sources

| Source | Used for |
|--------|----------|
| ILO ILOSTAT 2023 | Informality rate, wage-salaried share, youth unemployment |
| World Bank WDI 2024 | GDP per capita, employment indicators |
| Frey & Osborne (2013) | Automation probability by occupation task |
| Wittgenstein Centre | Education attainment projections 2025–2035 |
| ILO ISCO-08 | Occupational classification backbone |
| ESCO Taxonomy | Portable multilingual skills categories |
| ITU Digital Development | Mobile internet penetration by country |

---

## Demo flow (4 questions, 4 answers)

1. **What skills does this person really have?** → Skills Signal Engine
2. **What is at risk from automation?** → AI Readiness Lens
3. **What opportunities are realistic now?** → Opportunity Matching
4. **How does this change by country?** → Live country switch (Ghana → Bangladesh → Nigeria)

---

## Pitch line

> "UNMAPPED is a config-driven skills infrastructure layer that turns invisible youth capability into portable signals and realistic opportunity paths using local data."

---

## Sprint 2 (not in scope for 24h)

- Full country data ingestion pipeline
- Employer-side marketplace interface  
- Live labor-market API scraping
- Government policymaker admin dashboard
- Multilingual UI (language field ready in country packs)
