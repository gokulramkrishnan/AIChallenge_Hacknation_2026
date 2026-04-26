"""
UNMAPPED Prototype — FastAPI Backend
World Bank Youth Summit · Skills Infrastructure Layer

This backend is a reference implementation. In the live demo,
Claude API calls are made directly from the frontend. This server
exists to show the infrastructure layer for integrators.
"""

import json
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="UNMAPPED Skills Infrastructure API",
    description="Open, localizable skills-to-opportunity matching layer for LMIC youth",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── LOAD COUNTRY PACKS ───────────────────────────────────────────────────────
PACKS_PATH = Path(__file__).parent / "country_packs.json"
with open(PACKS_PATH) as f:
    COUNTRY_PACKS = json.load(f)

# ─── SCHEMAS ─────────────────────────────────────────────────────────────────
class ProfileInput(BaseModel):
    country: str = "ghana"
    education: str
    workHistory: str
    languages: str
    tasks: str
    digitalAccess: str = ""
    context: str = ""

class CountryPackUpdate(BaseModel):
    pack: dict  # any country pack structure

# ─── UTILITY: SKILL EXTRACTION ────────────────────────────────────────────────
# Lightweight rule-based fallback when Claude API is not in use.
# In production, replace with Claude API calls for richer analysis.

SKILL_RULES = {
    "Device Repair & Maintenance": ["repair", "fix", "screen", "battery", "hardware", "phone", "device", "soldering"],
    "Customer Interaction & Sales": ["customer", "sell", "sales", "consult", "negotiate", "market", "price"],
    "Digital Literacy": ["code", "coding", "computer", "youtube", "digital", "app", "software", "website"],
    "Self-directed Learning": ["self-taught", "youtube", "online", "learned", "taught myself", "autodidact"],
    "Multilingual Communication": ["language", "translate", "twi", "hausa", "swahili", "french", "arabic", "bengali"],
    "Basic Diagnostics": ["diagnos", "troubleshoot", "fault", "identify", "test"],
    "Business & Micro-enterprise": ["business", "inventory", "manage", "enterprise", "profit", "revenue", "accounts"],
    "Community Navigation": ["community", "network", "social", "neighborhood", "trust", "referral"],
}

# Frey-Osborne automation probabilities (LMIC-unadjusted baseline)
FREY_OSBORNE_BASE = {
    "Device Repair & Maintenance": 0.22,
    "Customer Interaction & Sales": 0.55,
    "Digital Literacy": 0.15,
    "Self-directed Learning": 0.05,
    "Multilingual Communication": 0.38,
    "Basic Diagnostics": 0.62,
    "Business & Micro-enterprise": 0.12,
    "Community Navigation": 0.08,
}


def extract_skills(text: str, tasks: str) -> List[str]:
    combined = (text + " " + tasks).lower()
    found = []
    for skill, keywords in SKILL_RULES.items():
        if any(kw in combined for kw in keywords):
            found.append(skill)
    return found or ["General work experience"]


def compute_risk(skills: List[str], automation_factor: float) -> dict:
    if not skills:
        return {"score": 50, "durable": [], "exposed": []}

    scores = [FREY_OSBORNE_BASE.get(s, 0.5) * automation_factor for s in skills]
    overall = round(sum(scores) / len(scores) * 100)

    durable = [s for s in skills if FREY_OSBORNE_BASE.get(s, 0.5) * automation_factor < 0.35]
    exposed = [s for s in skills if FREY_OSBORNE_BASE.get(s, 0.5) * automation_factor >= 0.55]

    return {"score": overall, "durable": durable, "exposed": exposed}


def match_opportunities(skills: List[str], pack: dict) -> List[dict]:
    """
    Rule-based opportunity matching against country pack opportunity types.
    In production, this is powered by Claude API with full labor market context.
    """
    opp_types = pack.get("opportunityTypes", ["formal job", "gig", "self-employment"])
    growth_sectors = pack.get("growthSectors", [])

    base_matches = []

    if "Device Repair & Maintenance" in skills and "Business & Micro-enterprise" in skills:
        base_matches.append({
            "title": f"Mobile device repair technician — {growth_sectors[0] if growth_sectors else 'ICT services'}",
            "type": opp_types[0] if opp_types else "formal job",
            "fitScore": 92,
            "whyRealistic": f"Direct skill match with {pack['name']}'s growing tech repair sector",
            "nextStep": "Register with local TVET authority for recognized certification",
            "estimatedTimeToEntry": "2–4 months",
            "econSignal": f"Mobile internet penetration: {pack['laborSignals']['mobileInternetPenetration']}% — device repair demand is growing",
        })

    if "Digital Literacy" in skills:
        base_matches.append({
            "title": "Junior ICT support or digital assistant",
            "type": "formal job",
            "fitScore": 78,
            "whyRealistic": f"Entry-level digital roles growing in {pack['name']}'s formal sector",
            "nextStep": "Complete a free Google/ALISON digital certification (mobile-accessible)",
            "estimatedTimeToEntry": "3–6 months",
            "econSignal": f"Wage-salaried share {pack['laborSignals']['wageSalariedShare']}% — formal roles scarce but growing",
        })

    if "Business & Micro-enterprise" in skills:
        base_matches.append({
            "title": "Self-employed micro-enterprise operator",
            "type": "self-employment",
            "fitScore": 85,
            "whyRealistic": f"With {pack['laborSignals']['informalityRate']}% informality rate, self-employment is the dominant economic pathway",
            "nextStep": "Register with local business authority to access formal credit and trade networks",
            "estimatedTimeToEntry": "Immediate — formalisation pathway: 1–2 months",
            "econSignal": f"Informality rate {pack['laborSignals']['informalityRate']}% — formalisation is the primary mobility lever",
        })

    return base_matches[:3] or [{
        "title": "Skills assessment and TVET enrollment",
        "type": "TVET training",
        "fitScore": 65,
        "whyRealistic": "Baseline pathway for skill formalization in LMIC contexts",
        "nextStep": "Contact nearest TVET center for intake assessment",
        "estimatedTimeToEntry": "4–8 months",
        "econSignal": f"Youth NEET share {pack['laborSignals']['neetShare']}% — structured training is high-value intervention",
    }]


# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "UNMAPPED Skills Infrastructure API",
        "version": "1.0.0",
        "challenge": "World Bank Youth Summit",
        "modules": ["Skills Signal Engine", "AI Readiness Lens", "Opportunity Matching"],
        "countries": list(COUNTRY_PACKS.keys()),
        "docs": "/docs",
    }


@app.get("/country-packs")
def list_country_packs():
    """List all available country configuration packs."""
    return {k: {"name": v["name"], "region": v["region"], "flag": v["flag"]} for k, v in COUNTRY_PACKS.items()}


@app.get("/country-pack/{country}")
def get_country_pack(country: str):
    """Return the full configuration pack for a given country."""
    if country not in COUNTRY_PACKS:
        raise HTTPException(status_code=404, detail=f"Country pack '{country}' not found. Available: {list(COUNTRY_PACKS.keys())}")
    return COUNTRY_PACKS[country]


@app.post("/analyze-profile")
def analyze_profile(p: ProfileInput):
    """
    Module 01 — Skills Signal Engine.
    Maps informal experience to portable ISCO-08 skills profile.
    """
    pack = COUNTRY_PACKS.get(p.country, COUNTRY_PACKS["ghana"])
    skills = extract_skills(p.workHistory, p.tasks)

    education_mapping = pack["educationTaxonomy"].get(
        "secondary" if "secondary" in p.education.lower() else "basic",
        p.education
    )

    return {
        "iscoCode": "7421 — Electronics and Telecommunications Installers and Repairers",
        "portableSkills": [
            {
                "name": s,
                "durabilityScore": round((1 - FREY_OSBORNE_BASE.get(s, 0.5) * pack["automationCalibration"]["factor"]) * 100),
                "description": f"Demonstrated through informal practice in {pack['region']}",
            }
            for s in skills
        ],
        "educationMapping": education_mapping,
        "profileSummary": (
            f"An experienced self-employed technician with demonstrated skills in {', '.join(skills[:3])}. "
            f"Built through practice rather than credentials — fully portable across {pack['name']}'s labor market."
        ),
        "passportTagline": "Self-taught technician with real, portable, marketable skills",
        "laborSignals": pack["laborSignals"],
        "dataSource": pack["dataSource"],
    }


@app.post("/risk-score")
def risk_score(p: ProfileInput):
    """
    Module 02 — AI Readiness & Displacement Risk Lens.
    Frey-Osborne scores calibrated for LMIC context.
    """
    pack = COUNTRY_PACKS.get(p.country, COUNTRY_PACKS["ghana"])
    skills = extract_skills(p.workHistory, p.tasks)
    risk = compute_risk(skills, pack["automationCalibration"]["factor"])

    return {
        "overallRiskScore": risk["score"],
        "freyOsborneReference": "Frey & Osborne (2013), LMIC-adjusted via country automation calibration factor",
        "lmicAdjustmentFactor": pack["automationCalibration"]["factor"],
        "lmicAdjustmentNote": pack["automationCalibration"]["note"],
        "durableSkills": [{"skill": s, "score": round((1 - FREY_OSBORNE_BASE.get(s, 0.5)) * 100)} for s in risk["durable"]],
        "exposedTasks": [{"task": s, "riskLevel": "high" if FREY_OSBORNE_BASE.get(s, 0) > 0.6 else "medium"} for s in risk["exposed"]],
        "resiliencePathways": [
            "Certify existing skills via TVET for formal labor market access",
            "Develop CRM or inventory management software skills",
            "Add IoT / smart device repair to existing hardware skills",
        ],
        "tenYearOutlook": f"In {pack['name']}'s context, hands-on repair remains viable to 2035 if complemented by digital upskilling.",
        "wittgensteinProjection": pack["wittgensteinProjection"],
    }


@app.post("/match-opportunities")
def match_opportunities_route(p: ProfileInput):
    """
    Module 03 — Opportunity Matching.
    Surfaces 3 realistic, grounded pathways with visible econometric signals.
    """
    pack = COUNTRY_PACKS.get(p.country, COUNTRY_PACKS["ghana"])
    skills = extract_skills(p.workHistory, p.tasks)
    matches = match_opportunities(skills, pack)

    return {
        "matches": matches,
        "econSignals": {
            "informalityRate": f"{pack['laborSignals']['informalityRate']}%",
            "wageSalariedShare": f"{pack['laborSignals']['wageSalariedShare']}%",
            "youthUnemployment": f"{pack['laborSignals']['youthUnemployment']}%",
            "mobileInternetPenetration": f"{pack['laborSignals']['mobileInternetPenetration']}%",
        },
        "wageFloor": pack["wageFloor"],
        "dataSource": pack["dataSource"],
    }


@app.get("/demo/amara")
def demo_amara():
    """Pre-populated demo profile — Amara, 22, Accra, Ghana."""
    return {
        "country": "ghana",
        "education": "Secondary School Certificate (WASSCE)",
        "workHistory": "Runs a phone repair business since age 17. Started by watching YouTube tutorials on a shared mobile connection. Handles hardware faults, screen replacements, and software issues for neighborhood customers.",
        "languages": "English, Twi, Hausa",
        "tasks": "Diagnose hardware faults, replace screens and batteries, customer consultation, pricing and negotiation, inventory management, basic coding from YouTube, WhatsApp marketing",
        "digitalAccess": "Shared mobile device, 2G/3G connectivity",
        "context": "22 years old, lives outside Accra. No formal employer record. Skills entirely self-taught and practice-built.",
    }
