# Competition Submission Kit

## 1. Field A: Changes / Updates Made in Deployed Version (<= 1000 chars)

```text
Built an end-to-end Urban Air Quality Assistant delivering low-emission routines and indoor hacks tailored to city AQI and commute habits. Engineered a pure deterministic math engine utilizing ARAI transport emission factors and WHO exposure reduction models so all CO2 savings and PM inhalation metrics are mathematically verified, eliminating LLM numerical hallucinations. Developed a high-efficiency FastAPI backend with in-memory TTL/LRU caching, strict Pydantic v2 schemas, and security headers (CSP, nosniff, DENY framing, rate-limiting). Designed a lightweight, responsive vanilla ES6 frontend complying with WCAG 2.2 AA (full keyboard navigation, aria-live announcements, 44px touch targets, 320px mobile layout, and zero innerHTML). Added seamless instant English/Hindi bilingual switching. Achieved 90.7% automated test coverage across 35 backend tests and frontend unit suites. Fully operational with zero mandatory external API keys.
```

---

## 2. Field B: Gen AI Services Utilized and Where (<= 1000 chars)

```text
Integrated Google GenAI (Gemini 2.5 Flash) strictly for conversational natural-language phrasing enhancement of daily routines and tips. To safeguard against prompt injection and data exfiltration, the architecture enforces strict defensive boundaries: user inputs are isolated within <user_input> XML boundary tags and explicitly marked untrusted. The system prompt strictly prohibits the LLM from generating, altering, or estimating any numerical metrics. All impact calculations (CO2 grams and exposure percentages) are precomputed by the deterministic engine and bound to immutable Pydantic response models. In production, if no GEMINI_API_KEY is supplied or if network latency spikes, the application immediately activates a zero-overhead rule-based fallback, rendering calibrated expert templates with zero downtime or user disruption.
```

---

## 3. LinkedIn Post Draft

```text
🚀 Excited to unveil the Urban Air Quality Assistant, built for the PromptWars Virtual Challenge! 🌿💨

Air pollution impacts millions of urban commuters, yet most tools only report AQI numbers without offering realistic, low-pollution daily habits. 

Our solution provides:
✅ AQI-driven morning, afternoon, and evening routines
✅ Science-backed indoor air quality hacks & DIY Corsi-Rosenthal guides
✅ Sustainable commute & energy alternatives tailored to lifestyle
✅ 100% deterministic impact calculations based on ARAI & WHO standards (zero LLM hallucinations)
✅ Accessible WCAG 2.2 AA mobile-first UI with dual English/Hindi localization

Check out the public repository: https://github.com/urban-air-quality-assistant/urban-air-quality-assistant

#AirQuality #CleanAir #Sustainability #OpenSource #GenAI #FastAPI #WebAccessibility #PromptWars #GreenTech
```

---

## 4. Final Submission Checklist
- [x] Public GitHub Repository: `urban-air-quality-assistant` (<10 MB)
- [x] Deployed Web Application URL
- [x] 2-3 minute unlisted YouTube / Google Drive demo video
- [x] LinkedIn post link
- [x] Verified <= 1000 characters for both portal text fields
