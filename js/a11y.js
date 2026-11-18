/**
 * @file a11y.js - Accessibility announcements and focus helpers (WCAG 2.2 AA).
 */

/**
 * Announce dynamic text to screen readers via aria-live container.
 * @param {string} message
 * @param {"polite"|"assertive"} [mode]
 */
export function announce(message, mode = "polite") {
  const container = document.getElementById("a11y-announcer");
  if (!container) return;
  container.setAttribute("aria-live", mode);
  container.textContent = message;
}

/**
 * Update document language attribute for screen reader pronunciation.
 * @param {string} lang
 */
export function setDocumentLang(lang) {
  document.documentElement.lang = lang === "hi" ? "hi" : "en";
}

/**
 * Move keyboard focus smoothly to target element.
 * @param {HTMLElement|string} target
 */
export function moveFocus(target) {
  const el = typeof target === "string" ? document.querySelector(target) : target;
  if (!el) return;
  el.setAttribute("tabindex", "-1");
  el.focus();
}
