/**
 * @file state.js - Reactive state container with subscription listeners.
 */

/**
 * @typedef {object} AppState
 * @property {string} lang
 * @property {string} city
 * @property {number|null} lat
 * @property {number|null} lon
 * @property {object} profile
 * @property {object|null} plan
 * @property {boolean} loading
 * @property {string|null} error
 */

/** @type {AppState} */
const initialState = {
  lang: "en",
  city: "New Delhi",
  lat: 28.6139,
  lon: 77.2090,
  profile: {
    commute_mode: "motorcycle",
    commute_distance_km: 10.0,
    has_vulnerable_members: false,
    has_asthma_or_respiratory: false,
    work_from_home: false,
    cooking_fuel: "lpg",
    exercise_habit: "morning_outdoor",
  },
  plan: null,
  loading: false,
  error: null,
};

let state = { ...initialState };
const listeners = new Set();

/**
 * Get snapshot of current application state.
 * @returns {AppState}
 */
export function getState() {
  return state;
}

/**
 * Update state and notify subscribers.
 * @param {Partial<AppState>} updates
 */
export function setState(updates) {
  state = { ...state, ...updates };
  listeners.forEach((listener) => listener(state));
}

/**
 * Subscribe to state transitions.
 * @param {(state: AppState) => void} listener
 * @returns {() => void} Unsubscribe function
 */
export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}
