/**
 * @file api.js - Safe client-side API requests with timeout & error handling.
 */

const DEFAULT_TIMEOUT_MS = 6000;

/**
 * Fetch with configurable timeout and error normalization.
 * @param {string} url
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export async function safeFetch(url, options = {}) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });
    clearTimeout(id);
    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    clearTimeout(id);
    throw err;
  }
}

/**
 * Search matching cities.
 * @param {string} query
 * @returns {Promise<Array<any>>}
 */
export async function searchCitiesApi(query) {
  if (!query || query.trim().length < 2) return [];
  return await safeFetch(`/api/geo/search?q=${encodeURIComponent(query.trim())}`);
}

/**
 * Generate complete routine plan.
 * @param {object} payload
 * @returns {Promise<any>}
 */
export async function generatePlanApi(payload) {
  return await safeFetch("/api/plan/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
