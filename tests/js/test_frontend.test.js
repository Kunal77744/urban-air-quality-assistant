/**
 * @file test_frontend.test.js - Node test runner for frontend logic & safety
 */

import test from "node:test";
import assert from "node:assert/strict";
import { t, translations } from "../../public/js/i18n.js";
import { createElement } from "../../public/js/render.js";

test("i18n provides English and Hindi translations", () => {
  assert.equal(t("appTitle", "en"), "Urban Air Quality Assistant");
  assert.equal(t("appTitle", "hi"), "शहरी वायु गुणवत्ता सहायक");
});

test("i18n falls back safely for missing keys", () => {
  assert.equal(t("nonExistentKey", "en"), "nonExistentKey");
});

test("translations dictionary contains matching keys across languages", () => {
  const enKeys = Object.keys(translations.en);
  const hiKeys = Object.keys(translations.hi);
  assert.deepEqual(enKeys.sort(), hiKeys.sort());
});
