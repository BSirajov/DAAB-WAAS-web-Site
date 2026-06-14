/**
 * Membership application backend config (public — safe to deploy).
 *
 * Setup:
 * 1. Create a form at https://formspree.io (free tier works for testing).
 * 2. Set notification email to info@daab-waas.com (or bilik.birlik@gmail.com).
 * 3. Paste your form URL below, e.g. "https://formspree.io/f/abcxyz".
 *
 * Optional override on a single page: <html data-daab-form-endpoint="https://formspree.io/f/...">
 */
(function (global) {
  "use strict";

  global.DAAB_APPLICATION_CONFIG = {
    formspreeEndpoint: "",
  };
})(typeof window !== "undefined" ? window : global);
