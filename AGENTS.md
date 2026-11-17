# MISSION: Urban Air Quality Assistant (PromptWars Virtual, Challenge 6)
Re-read this file at the start of every phase and before every merge.

## 1. HISTORY (REMEMBER THROUGHOUT)
On our previous challenge you did good work: Security 98-99, Efficiency 100,
Testing 99-100, Accessibility 99-100, Alignment 95-100. But we did NOT reach
Rank 1 because CODE QUALITY stayed stuck at 88-89 in every attempt, and once
Alignment dropped to 95. A 97.04 score gave only rank #934 of ~53,000, and ~9
people tied at Rank 1. Only our LAST of 3 attempts counts. The early rank (#14)
is meaningless because most participants have not submitted yet.
This time ALL SIX parameters must be 100 (minimum 98, no exceptions).
Code Quality is the top priority, but NEVER at the cost of another parameter.
Treat every lost point as hundreds of lost ranks.

## 2. PRODUCT
Brief (verbatim): "Create a GenAI-powered assistant that suggests low-emission
daily routines, indoor air quality hacks, and sustainable alternatives tailored
to a user's location and lifestyle, while clearly explaining the direct impact
of their choices." Responsive UI that makes adopting low-pollution habits
frictionless.
Judged by an AI on: Code Quality, Security, Efficiency, Testing, Accessibility,
Problem Statement Alignment. The judge reads the public GitHub repo, deployed
app and README. Deadline: 29 Nov 2026 11:59 PM IST.
Submission needs: public GitHub repo named `urban-air-quality-assistant`
(<10 MB), deployed link, demo video (YouTube unlisted or Drive with access;
NOT Instagram), LinkedIn post link, and two text fields of max 1024 chars each.

## 3. WHY CODE QUALITY STAYED LOW (fix all of these)
- Large files, long functions, monolithic app.js / main module
- Mixed responsibilities (routing + logic + formatting together)
- Duplication, inconsistent naming and error handling
- Magic numbers/strings, broad `except Exception`, missing hints/docstrings
- Over-engineering: needless layers. Prefer SIMPLE, FLAT, CONSISTENT, READABLE.
  Every file must justify its existence.
- Weak test code (long, repetitive, no fixtures/parametrize)
- Messy repo: junk files, unclear commits, no lint config
- Frontend: global state, giant functions, innerHTML, no JSDoc, no module split

## 4. ORDER OF WORK
1. Spawn ALL 16 agents below. Nobody idle. Each has tasks, deliverables, veto.
2. Orchestrator writes docs/PLAN.md (file tree, module boundaries, API
   contract, impact formulas, test matrix, task split, dependency order).
3. Architect + Code Quality Auditor approve the plan. Then start Phase 1.

## 5. TEAM (ALL ACTIVE)
1 ORCHESTRATOR: PLAN.md, assignments, merges, runs the full gate suite after
  every merge, owns docs/DECISIONS.md.
2 ARCHITECT: minimal layering (routes -> services -> models; core/ for config,
  logging, errors, cache). Enforces SRP and size limits. Removes needless
  abstraction.
3 BACKEND: FastAPI. Open-Meteo geocoding + air quality (no key), planner,
  deterministic impact engine, LLM service. App works fully with NO API key.
4 FRONTEND: vanilla JS ES modules (api.js, state.js, render.js, i18n.js,
  a11y.js, main.js), semantic HTML, one CSS file with design tokens, EN/HI
  toggle, mobile-first, loading/empty/error states, JSDoc types.
5 CODE QUALITY AUDITOR (independent, adversarial, #1 priority): reviews EVERY
  change like a hostile AI judge and can block any merge. Checks: function <=25
  lines, module <=200 lines, low complexity, no duplication, no magic numbers,
  naming, docstrings, type hints, mypy --strict, ruff, black, ESLint, Prettier,
  no dead code/TODO/print/commented code, test-code quality, commit hygiene.
  Writes docs/CODE_QUALITY_REPORT.md.
6 SECURITY: strict CSP, nosniff, X-Frame-Options DENY, Referrer-Policy,
  Permissions-Policy, Pydantic limits on all inputs, textContent only (no
  innerHTML with user/LLM data), prompt-injection defense (<user_input> tags,
  declared untrusted, schema-validated LLM output), rate limiting, restricted
  CORS, env-only secrets, pinned deps, no stack traces to client.
7 PERFORMANCE: TTL+LRU caches (geocoding, AQI, LLM), async httpx with
  connection reuse, timeouts, bounded retries, debounced search, gzip, small
  payloads, no redundant calls. Proves cache hits in tests.
8 QA/TEST: pytest + pytest-cov >=90% (aim 95%), >=1 test per requirement R1-R7,
  security tests (XSS, injection, oversized input), error paths, cache, LLM
  fallback, impact math. Use fixtures + parametrize, mock ALL external HTTP, JS
  unit tests for i18n/render logic.
9 ACCESSIBILITY: WCAG 2.2 AA, landmarks, skip link, labels, aria-live,
  keyboard-only flow, visible focus, contrast >=4.5:1, AQI never by colour
  alone (icon + text), reduced motion, 44px touch targets, lang attribute
  switching, works at 320px width and 200% zoom. Reports Lighthouse a11y score.
10 ALIGNMENT & DOCS: README with requirement-to-file table (R1-R7 -> UI element,
  module, test), mermaid architecture diagram, formulas with sources and
  assumptions, setup/run/test/deploy, limitations, health disclaimer, CI badge,
  demo script that shows every requirement visibly.
11 DEVOPS: pyproject.toml (ruff, black, mypy, pytest), .editorconfig,
  .env.example, .gitignore, pre-commit, GitHub Actions CI (lint, mypy, tests,
  coverage), Vercel config (api/index.py + public/), repo <10 MB, tags.
12 FINAL JUDGE (independent, never wrote code): scores 0-100 on each of the 6
  parameters with file/line evidence, as strict as a real competition judge.
  Anything <98 returns to its owner. Repeat until all >=98.
13 REFACTORING: after each phase hunts long functions, duplication, unclear
  names, inconsistent patterns, over-engineering; reports to the Auditor.
14 LLM/PROMPT ENGINEER: Gemini prompts via google-genai in JSON mode (model name
  from env var), JSON schema, injection defenses, rule-based fallback. The LLM
  only writes friendly wording; it NEVER outputs numbers.
15 CONTENT & i18n REVIEWER: Hindi/English quality, tone, health-advice safety,
  "estimate" labels, disclaimer; every claim has a formula or a source.
16 REPO HYGIENE & RELEASE: no junk/secrets, <10 MB, conventional commits,
  pinned deps, fresh-clone install test, README links work, demo script matches
  the real UI.

## 6. REQUIREMENTS (each must be visible in UI, code, tests AND README)
R1 Location-tailored: city search + live AQI/PM2.5/PM10, graceful fallback.
R2 Lifestyle-tailored: commute mode/distance, kids/elderly/asthma, work type,
   home type, cooking fuel, exercise habit.
R3 Low-emission daily routines: morning/afternoon/evening plan driven by AQI.
R4 Indoor air hacks: ventilation timing, purifier/DIY, cooking ventilation,
   plant myths vs facts, dust-safe cleaning.
R5 Sustainable alternatives: metro/bus/cycle/carpool, induction/LPG vs
   biomass, no-burning alternatives.
R6 Direct impact explained: each suggestion has a "Why" line + estimated impact
   (exposure %, g CO2 / PM saved) from a DETERMINISTIC engine with documented
   formulas, labeled "estimate". LLM never produces numbers.
R7 Frictionless responsive UI: plan in <=3 interactions, EN/HI toggle,
   loading/empty/error states.

## 7. PHASES AND GATES (next phase starts only after previous gate passes)
P0 PLAN: docs/PLAN.md reviewed by all agents.
P1 BACKEND + TESTS. Gate: ruff, black, mypy --strict, pytest >=90% all green.
P2 FRONTEND + A11Y. Gate: ESLint/Prettier clean, keyboard-only OK, no console
   errors, Lighthouse a11y 100 and best-practices 100.
P3 SECURITY + PERFORMANCE. Gate: headers verified, injection tests pass, cache
   hit proven.
P4 DOCS + CI + DEPLOY CONFIG. Gate: fresh clone -> install -> lint -> test OK.
P5 CODE QUALITY SWEEP: Auditor full-repo pass, Refactoring agent fixes, then
   re-run ALL gates.
P6 FINAL JUDGE AUDIT: 6-parameter score table with evidence. Loop fixes until
   every parameter >=98. After ANY change re-run the full gate suite.
P7 GITHUB + DEPLOY: push to the public GitHub repo (use `gh` if authenticated,
   else print the exact commands). Deploy to Vercel (use `vercel` CLI if logged
   in, else print exact steps). GEMINI_API_KEY only as a Vercel env var, never
   in the repo. Verify the deployed URL: /api/health, a full plan flow,
   security headers, UI at 320px and desktop. Fix anything that breaks in
   production. Confirm repo is public, <10 MB, README renders.
P8 DEMO PACKAGE: docs/DEMO_SCRIPT.md, a 2-3 minute shot-by-shot script with
   narration that visibly shows R1-R7 in order (city search, profile, plan,
   indoor hacks, sustainable alternatives, "Why" impact lines, EN/HI toggle,
   keyboard-only use, mobile view, no-API-key fallback). If you can record the
   screen, do it; otherwise give the script plus a one-take recording checklist.
P9 SUBMISSION KIT in docs/SUBMISSION.md: (a) "Describe the changes/updates made
   in the deployed version" (<=1000 chars), (b) "Gen AI services utilized and
   where" (<=1000 chars), (c) LinkedIn post draft in English with hashtags,
   (d) final checklist of form fields (repo, deployed, video, LinkedIn links).
   Character counts must be VERIFIED by a command, not guessed. Content must
   match the real code.
P10 FINAL VERIFICATION: fresh clone -> install -> lint -> mypy -> tests -> run
   locally -> compare with deployed behaviour. Re-run the Final Judge on the
   deployed build. Tag v1.

## 8. HARD RULES
- Never trade one parameter for another; every fix is re-verified on all 6.
- Simplicity beats cleverness. No gold-plating.
- No hallucinated facts; every number computed or cited, labeled estimate.
- No secrets in repo; app works without any API key (GEMINI_API_KEY optional).
- Work only inside this folder. Keep the repo small and clean.

## 9. AUTONOMY
Work end-to-end without waiting for me. Do not stop after the plan; continue
through P10. Commit after each phase with a conventional commit message. Ask me
only if truly blocked; otherwise decide and log it in docs/DECISIONS.md.
At the very end give ONE final report: repo URL, deployed URL, file tree,
6-parameter score table with evidence, remaining risks, and a short list of
what the human must still do (record/upload video, post on LinkedIn, set the
Gemini key in Vercel if not done, fill the portal form).
