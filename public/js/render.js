/**
 * @file render.js - Safe DOM rendering engine (Zero innerHTML with dynamic data).
 */

import { t } from "./i18n.js";

/**
 * Helper to safely create an element with text and class.
 * @param {string} tag
 * @param {string} [className]
 * @param {string} [text]
 * @returns {HTMLElement}
 */
export function createElement(tag, className = "", text = "") {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;
  return el;
}

/**
 * Render AQI metric badge with icon and text (never color alone).
 * @param {object} aqiData
 * @returns {HTMLElement}
 */
export function renderAqiCard(aqiData) {
  const card = createElement("section", "card aqi-card");
  card.setAttribute("aria-label", "Air Quality Status");

  const header = createElement("div", "card-header");
  header.appendChild(createElement("h3", "", `AQI ${aqiData.aqi} - ${aqiData.category}`));
  card.appendChild(header);

  const stats = createElement("div", "aqi-stats-grid");
  stats.appendChild(createElement("div", "stat-badge", `PM2.5: ${aqiData.pm2_5} µg/m³`));
  stats.appendChild(createElement("div", "stat-badge", `PM10: ${aqiData.pm10} µg/m³`));
  stats.appendChild(createElement("div", "stat-source", `Source: ${aqiData.source}`));
  card.appendChild(stats);

  return card;
}

/**
 * Render routine schedule slots.
 * @param {Array<any>} routines
 * @returns {HTMLElement}
 */
export function renderRoutines(routines) {
  const sec = createElement("section", "card routines-card");
  sec.appendChild(createElement("h3", "", "Daily Low-Emission Routine"));

  const list = createElement("div", "routines-list");
  routines.forEach((r) => {
    const item = createElement("div", "routine-item");
    item.appendChild(createElement("h4", "routine-slot", r.slot.toUpperCase()));
    item.appendChild(createElement("p", "routine-action", r.action));
    item.appendChild(createElement("small", "routine-why", `Why: ${r.why}`));
    item.appendChild(createElement("span", "badge-pill", r.exposure_impact));
    list.appendChild(item);
  });
  sec.appendChild(list);
  return sec;
}

/**
 * Render indoor hacks section.
 * @param {Array<any>} hacks
 * @returns {HTMLElement}
 */
export function renderHacks(hacks) {
  const sec = createElement("section", "card hacks-card");
  sec.appendChild(createElement("h3", "", "Indoor Air Quality Hacks"));

  const grid = createElement("div", "hacks-grid");
  hacks.forEach((h) => {
    const card = createElement("article", "hack-card");
    card.appendChild(createElement("h4", "", h.title));
    card.appendChild(createElement("p", "", h.description));
    if (h.fact_check) {
      card.appendChild(createElement("div", "myth-box", h.fact_check));
    }
    grid.appendChild(card);
  });
  sec.appendChild(grid);
  return sec;
}

/**
 * Render deterministic quantified impact summary.
 * @param {object} impact
 * @param {string} lang
 * @returns {HTMLElement}
 */
export function renderImpact(impact, lang) {
  const sec = createElement("section", "card impact-card");
  sec.appendChild(createElement("h3", "", t("impactTitle", lang)));

  const grid = createElement("div", "impact-grid");
  grid.appendChild(createElement("div", "impact-stat", `${impact.daily_co2_saved_grams} g CO2/day Saved`));
  grid.appendChild(createElement("div", "impact-stat", `${impact.exposure_reduction_pct}% Lower PM2.5 Inhaled`));
  sec.appendChild(grid);

  sec.appendChild(createElement("p", "impact-basis", impact.calculation_basis));
  sec.appendChild(createElement("small", "disclaimer", t("disclaimer", lang)));
  return sec;
}
