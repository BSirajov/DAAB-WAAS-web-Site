/**
 * Membership application backend config (public — safe to deploy).
 *
 * Default: POST to mail.php in the same folder as application.html (az/ or en/).
 * Upload mail.php + repo-root mail-application-send.php to the server.
 *
 * Optional Formspree override: set formspreeEndpoint below, or on the page:
 *   <html data-daab-form-endpoint="https://formspree.io/f/...">
 */
(function (global) {
  "use strict";

  global.DAAB_APPLICATION_CONFIG = {
    submitEndpoint: "mail.php",
    formspreeEndpoint: "",
  };
})(typeof window !== "undefined" ? window : global);
