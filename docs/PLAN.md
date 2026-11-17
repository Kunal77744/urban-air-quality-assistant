# Master Implementation Plan: Urban Air Quality Assistant (PromptWars 6)

## 1. Project Goal & Score Target
Achieve 100 on all six parameters evaluated by competition judges:
- **Code Quality**: 100/100 (Clean architecture, <=25 lines/function, <=200 lines/file, strict typing, 0 dead code, no magic values).
- **Security**: 100/100 (Strict CSP, nosniff, DENY framing, no innerHTML, prompt injection guards, Pydantic input bounds).
- **Efficiency**: 100/100 (TTL+LRU caches, async httpx with client connection reuse, <50ms local response, payload optimization).
- **Testing**: 100/100 (pytest + coverage >= 95%, full test suite for R1-R7, fixtures, parametrize, mock external HTTP, JS unit tests).
- **Accessibility**: 100/100 (WCAG 2.2 AA compliant, semantic landmarks, skip links, aria-live, high contrast, keyboard navigable, 44px touch targets).
- **Alignment**: 100/100 (Complete implementation of R1 through R7 with clear visibility in UI, Code, Tests, and Documentation).

---

## 2. Architecture & File Tree Budget (<=200 lines/module)

```text
urban-air-quality-assistant/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI pipeline: lint, type-check, tests, coverage
├── api/
│   └── index.py                   # Vercel serverless entrypoint
├── core/
│   ├── __init__.py
│   ├── config.py                  # Pydantic BaseSettings, environment configuration
│   ├── constants.py               # Centralized emission factors, AQI categories, thresholds
│   ├── cache.py                   # Memory TTL & LRU cache with hit/miss tracking
│   ├── errors.py                  # Custom domain exceptions & global exception handlers
│   └── logging.py                 # Structured JSON/console logging without secrets
├── models/
│   ├── __init__.py
│   ├── user_profile.py            # Commute, household, work, exercise, cooking schemas
│   ├── air_quality.py             # AQI, PM2.5, PM10, pollutant models
│   └── routine_plan.py            # Plan response, routines, hacks, impact metrics
├── services/
│   ├── __init__.py
│   ├── geocoding_service.py       # Open-Meteo Geocoding client with fallback
│   ├── aqi_service.py             # Open-Meteo Air Quality client with fallback
│   ├── impact_engine.py           # Deterministic emission & exposure math
│   ├── routine_planner.py         # AQI-driven morning/afternoon/evening routine engine
│   └── llm_service.py             # Optional Gemini phrasing with schema-locked fallback
├── routes/
│   ├── __init__.py
│   ├── health.py                  # Health check & uptime
│   ├── geo.py                     # Geocoding search endpoint
│   ├── aqi.py                     # Live air quality endpoint
│   └── plan.py                    # Combined plan generation endpoint
├── public/
│   ├── index.html                 # Semantic, accessible HTML5 structure
│   ├── styles.css                 # Clean CSS with design tokens & high contrast
│   ├── js/
│   │   ├── api.js                 # Fetch wrapper with timeouts & error normalization
│   │   ├── state.js               # Reactive pub-sub local state container
│   │   ├── i18n.js                # Dual English/Hindi translation dictionaries
│   │   ├── render.js              # Safe DOM rendering (textContent only, no innerHTML)
│   │   ├── a11y.js                # Keyboard trapping, aria-live announcements, focus
│   │   └── main.js                # App bootstrapping & event delegation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Reusable pytest fixtures & mock clients
│   ├── test_impact_engine.py      # Math tests for all emission formulas (R6)
│   ├── test_aqi_service.py        # Geocoding & AQI fetching and caching (R1)
│   ├── test_routine_planner.py    # Routine generation logic (R2, R3, R4, R5)
│   ├── test_security.py           # Injection defense, XSS, payload limit tests
│   ├── test_api_routes.py         # FastAPI route integration tests (R1-R7)
│   ├── test_llm_service.py        # Gemini client & deterministic fallback tests
│   └── js/
│       └── test_frontend.test.js  # Node test runner for i18n & rendering safety
├── docs/
│   ├── PLAN.md                    # This architecture and execution plan
│   ├── DECISIONS.md               # Architecture decision records
│   ├── CODE_QUALITY_REPORT.md     # Independent adversarial auditor report
│   ├── DEMO_SCRIPT.md             # 2-3 minute shot-by-shot demo script
│   └── SUBMISSION.md              # Portal submission kit with exact char counts
├── pyproject.toml                 # Tool configs: ruff, black, mypy, pytest, coverage
├── vercel.json                    # Vercel deployment routes and serverless config
├── .env.example                   # Environment variable template
├── .gitignore                     # Clean ignore rules (no secrets, no caches)
├── AGENTS.md                      # Competition mission brief
└── README.md                      # Primary competition documentation
```

---

## 3. Module Boundaries & Single Responsibility Principle (SRP)
- **`core/`**: Shared non-business logic (settings, cache, constants, exceptions). Zero dependency on routes or services.
- **`models/`**: Strict Pydantic schemas validating all inbound and outbound payloads.
- **`services/impact_engine.py`**: **Pure deterministic math**. Zero network calls, zero LLM reliance. Computes emissions and exposure reduction.
- **`services/routine_planner.py`**: Evaluates lifestyle parameters and AQI band to generate tailored routines, indoor hacks, and sustainable travel alternatives.
- **`services/llm_service.py`**: Accepts strictly deterministic plans and uses Gemini purely to polish natural language tone. If disabled or unconfigured, returns deterministic template text directly.
- **`routes/`**: Handles request parsing, HTTP status codes, and passes data to services. Controllers remain under 50 lines.

---

## 4. API Specification

### `GET /api/health`
- **Output**: `{"status": "healthy", "version": "1.0.0", "cache_stats": {...}}`

### `GET /api/geo/search?q={city}`
- **Params**: `q` (string, 2 to 64 chars, sanitized).
- **Output**: Array of `{"name": str, "latitude": float, "longitude": float, "country": str, "admin1": str}`.

### `GET /api/aqi/live?lat={lat}&lon={lon}`
- **Params**: `lat` (-90 to 90), `lon` (-180 to 180).
- **Output**: `{"aqi": int, "category": str, "pm2_5": float, "pm10": float, "source": str, "timestamp": str}`.

### `POST /api/plan/generate`
- **Input**:
  - `location`: `{"city": str, "latitude": float, "longitude": float}`
  - `profile`: `{"commute_mode": str, "commute_km": float, "vulnerable_members": bool, "has_asthma": bool, "work_type": str, "cooking_fuel": str, "exercise_habit": str}`
  - `language`: `"en"` | `"hi"`
- **Output**:
  - `aqi_summary`: AQI level, PM2.5, status banner.
  - `routines`: Morning, afternoon, and evening recommended routines.
  - `indoor_hacks`: Tailored indoor ventilation, filtration, cooking, and dust-mitigation actions.
  - `sustainable_alternatives`: Low-emission commute and energy alternatives.
  - `impact_summary`:
    - `co2_saved_grams`: float
    - `pm_exposure_reduction_pct`: float
    - `explanation`: string (with formula breakdown).

---

## 5. Deterministic Impact Formulas (R6)
1. **Commute CO2 Emission Savings ($g\text{ CO}_2$)**:
   $$\Delta \text{CO}_2 = (\text{EF}_{\text{current}} - \text{EF}_{\text{alternative}}) \times D_{\text{roundtrip}}$$
   - Factors (g CO2 / passenger-km):
     - Petrol Car: 140 g/km
     - Petrol 2-Wheeler: 42 g/km
     - Electric Bus: 18 g/km
     - Metro Rail: 8 g/km
     - Cycle / Walk: 0 g/km
   - *Reference*: ARAI (Automotive Research Association of India) & CPCB urban emission baselines.

2. **Indoor Exposure Reduction ($\%$ Reduction)**:
   $$\text{Exposure Reduction} = 1 - (1 - E_{\text{vent}}) \times (1 - E_{\text{filter}}) \times (1 - E_{\text{cook}})$$
   - Timing ventilation to lowest AQI window: $20\%-35\%$ reduction.
   - Using HEPA or DIY Corsi-Rosenthal filter: $65\%-80\%$ PM2.5 reduction.
   - Using range hood / cross-draft during cooking: $50\%-70\%$ cooking peak PM reduction.
   - *Reference*: EPA Indoor Air Quality Clean Air Guidelines & WHO Air Quality Guidelines 2021.

---

## 6. Test Matrix (Requirement Coverage)

| Req ID | Description | Covered In Test File | Verifications |
|:---|:---|:---|:---|
| **R1** | City search & live AQI/PM | `test_aqi_service.py`, `test_api_routes.py` | Geocoding validation, cache hit, Open-Meteo parsing, fallback data |
| **R2** | Lifestyle-tailored profile | `test_routine_planner.py` | Vulnerable groups (asthma/kids/elderly), commute distance, fuels |
| **R3** | Daily routines (AQI-driven) | `test_routine_planner.py` | Morning/afternoon/evening schedule adapted for Hazardous vs Moderate AQI |
| **R4** | Indoor air hacks | `test_routine_planner.py` | Vent timing, DIY filtration, plant myth explanation, dust control |
| **R5** | Sustainable alternatives | `test_impact_engine.py` | Metro, EV bus, cycle comparisons against car/motorcycle |
| **R6** | Direct impact explained | `test_impact_engine.py`, `test_api_routes.py` | Deterministic math verification, "Why" strings, zero LLM numbers |
| **R7** | Frictionless responsive UI | `test_frontend.test.js`, browser/manual | <=3 clicks to plan, EN/HI toggle, zero innerHTML, keyboard focus |

---

## 7. Execution Phases & Gates
- **Phase 0 (Plan)**: Architecture & Plan sign-off.
- **Phase 1 (Backend + Tests)**: FastAPI, Core, Models, Services, Routes, Tests. Gate: ruff, black, mypy --strict, pytest >=95%.
- **Phase 2 (Frontend + A11y)**: Vanilla ES modules, Semantic HTML, CSS, EN/HI i18n, A11y. Gate: ESLint/Prettier clean, keyboard OK, Lighthouse 100.
- **Phase 3 (Security + Performance)**: Security headers, CSP, prompt injection defense, cache verification.
- **Phase 4 (Docs + CI + Deploy)**: README, CI workflow, Vercel config, pyproject.toml.
- **Phase 5 (Code Quality Sweep)**: Full repo audit against function <=25 lines, module <=200 lines, 0 dead code.
- **Phase 6 (Final Judge Audit)**: 6-parameter scoring table (target all 100).
- **Phase 7 (GitHub + Deploy)**: Deploy to Vercel, public repo push.
- **Phase 8 (Demo Package)**: docs/DEMO_SCRIPT.md.
- **Phase 9 (Submission Kit)**: docs/SUBMISSION.md with automated character length validation.
- **Phase 10 (Final Verification)**: Fresh clone test, tagging v1.

---

## 8. Architect & Auditor Sign-off
- **Architect Approval**: **APPROVED** (Minimal layering, strict SRP, 0 unnecessary abstractions).
- **Code Quality Auditor Approval**: **APPROVED** (Hard limits enforced: <=25 lines/function, <=200 lines/file, mypy strict, no magic strings).
