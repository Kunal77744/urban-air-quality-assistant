/**
 * @file main.js - Application bootstrap and event handling.
 */

import { announce, setDocumentLang } from "./a11y.js";
import { generatePlanApi, searchCitiesApi } from "./api.js";
import { t } from "./i18n.js";
import {
  createElement,
  renderAqiCard,
  renderHacks,
  renderImpact,
  renderRoutines,
} from "./render.js";
import { getState, setState, subscribe } from "./state.js";

async function handleGeneratePlan() {
  const current = getState();
  setState({ loading: true, error: null });
  announce(t("loadingText", current.lang));

  try {
    const payload = {
      city: current.city,
      latitude: current.lat,
      longitude: current.lon,
      profile: current.profile,
      language: current.lang,
    };
    const plan = await generatePlanApi(payload);
    setState({ plan, loading: false });
    announce("Personalized clean air plan loaded successfully.");
  } catch (err) {
    setState({ loading: false, error: err.message || "Failed to load plan" });
    announce("Error loading plan. Please try again.", "assertive");
  }
}

function handleLanguageToggle() {
  const current = getState();
  const nextLang = current.lang === "en" ? "hi" : "en";
  setDocumentLang(nextLang);
  setState({ lang: nextLang });
  handleGeneratePlan();
}

function renderApp(state) {
  const container = document.getElementById("results-container");
  if (!container) return;
  container.replaceChildren();

  if (state.loading) {
    container.appendChild(createElement("div", "loading-spinner", t("loadingText", state.lang)));
    return;
  }
  if (state.error) {
    container.appendChild(createElement("div", "error-banner", state.error));
    return;
  }
  if (state.plan) {
    container.appendChild(renderAqiCard(state.plan.air_quality));
    container.appendChild(renderImpact(state.plan.impact, state.lang));
    container.appendChild(renderRoutines(state.plan.routines));
    container.appendChild(renderHacks(state.plan.indoor_hacks));
  }
}

function setupEventListeners() {
  const langBtn = document.getElementById("lang-toggle-btn");
  if (langBtn) langBtn.addEventListener("click", handleLanguageToggle);

  const genBtn = document.getElementById("generate-plan-btn");
  if (genBtn) genBtn.addEventListener("click", handleGeneratePlan);

  const cityInput = document.getElementById("city-input");
  if (cityInput) {
    cityInput.addEventListener("change", (e) => {
      setState({ city: e.target.value });
    });
  }

  const modeSelect = document.getElementById("commute-mode-select");
  if (modeSelect) {
    modeSelect.addEventListener("change", (e) => {
      const p = getState().profile;
      setState({ profile: { ...p, commute_mode: e.target.value } });
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  subscribe(renderApp);
  handleGeneratePlan(); // 1-click instant initial plan
});
