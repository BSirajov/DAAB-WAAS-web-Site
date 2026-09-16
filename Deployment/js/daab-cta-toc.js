/**
 * Compatibility shim — the shared drawer lives in daab-toc-drawer.js.
 */
(function () {
  "use strict";
  if (window.DAAB_TOC_DRAWER && typeof window.DAAB_TOC_DRAWER.init === "function") {
    window.DAAB_TOC_DRAWER.init();
  }
})();
