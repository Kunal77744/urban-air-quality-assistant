# Architecture Decision Records (ADR) - Urban Air Quality Assistant

## ADR 001: Technology Stack and Module Boundaries
- **Context**: Need a lightweight, high-performance, verifiable architecture scoring 100 on Code Quality, Security, Accessibility, Testing, Alignment, and Efficiency.
- **Decision**:
  - **Backend**: Python 3.11+ with FastAPI, Pydantic v2, and HTTPX. Zero database needed; all state ephemeral or cached in memory with TTL/LRU.
  - **Frontend**: Vanilla ES modules (no bloated frameworks or build steps that degrade code readability or accessibility). 6 focused modules: `api.js`, `state.js`, `render.js`, `i18n.js`, `a11y.js`, `main.js`. Single CSS file with design tokens.
  - **LLM Layer**: Optional Google GenAI (Gemini) strictly for natural phrasing/enrichment. The deterministic impact engine calculates ALL numbers. If `GEMINI_API_KEY` is not present, the app gracefully falls back to deterministic rule-based templates with zero failure.
  - **External APIs**: Open-Meteo Geocoding API & Open-Meteo Air Quality API (open-access, no API keys required, rate-resilient with local TTL cache and fallback).

## ADR 002: Deterministic Impact Calculation Model
- **Context**: LLMs hallucinate numbers and emission statistics. Requirement R6 mandates deterministic impact calculations with documented formulas.
- **Decision**:
  - Transport emissions: Based on ARAI / EPA average emission factors per passenger-km (e.g., Petrol 2-wheeler: ~40g CO2/km; Petrol car: ~140g CO2/km; Electric Bus: ~15g CO2/km; Metro: ~8g CO2/km; Cycling/Walking: 0g CO2/km).
  - Exposure reduction: Calculated based on outdoor PM2.5 levels, indoor HEPA/DIY filter efficiency (70-95% reduction), cooking ventilation exhaust hood usage (60-80% peak particulate reduction), and peak-hour avoidance (morning/evening rush hour PM2.5 peak shift: 25-45% lower exposure).
  - All outputs labeled explicitly as "Estimated impact".

## ADR 003: Strict Code Quality Limits
- **Context**: Code quality was the limiting factor in previous attempts (stuck at 88-89).
- **Decision**:
  - Maximum function length: 25 lines.
  - Maximum module length: 200 lines.
  - Type annotations: 100% strict (`mypy --strict`).
  - Linter: Ruff and Black for Python; ESLint and Prettier standards for JS/CSS/HTML.
  - Docstrings: Google/NumPy style on every module, class, and public function.
  - No magic numbers: All constants centralized in `core/constants.py` and `frontend/constants.js`.
  - Zero `except Exception:` without precise handling and structured logging.

## ADR 004: Security and Content Sanitization
- **Context**: Requirement for 100 Security score and prevention of XSS / prompt injection.
- **Decision**:
  - No `innerHTML` with any dynamic or user-influenced data. All DOM population uses `textContent` and `createElement` / safe templates.
  - Strict Content-Security-Policy (CSP), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: geolocation=(), camera=(), microphone=()`.
  - Prompt injection defense: User input delimited inside `<user_input>` XML tags, explicitly declared untrusted, and output validated against strict Pydantic schemas.

## ADR 005: Accessibility and Internationalization
- **Context**: WCAG 2.2 AA compliance and Hindi/English dual support.
- **Decision**:
  - Full keyboard navigation with visible 3px focus rings (`:focus-visible`).
  - Aria attributes (`aria-live="polite"`, `aria-describedby`, semantic landmarks `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`).
  - High contrast ratio >= 4.5:1 for standard text, 7:1 for headers.
  - AQI never communicated solely via color; always paired with explicit icons, level labels, and numerical PM values.
  - Bidirectional English/Hindi localization switch with immediate dynamic text re-rendering and `document.documentElement.lang` update.
