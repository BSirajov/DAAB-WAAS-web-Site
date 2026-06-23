/**
 * Scientists profiles — re-sync chrome after late breadcrumb injection.
 */
(function (global) {
  "use strict";

  if (document.documentElement.getAttribute("data-daab-page-id") !== "scientists-profiles") {
    return;
  }

  function syncAll() {
    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
      return;
    }
    if (window.DAAB_NAV && typeof window.DAAB_NAV.syncNavHeight === "function") {
      window.DAAB_NAV.syncNavHeight();
    }
    if (window.DAAB_BREADCRUMBS && typeof window.DAAB_BREADCRUMBS.syncHeight === "function") {
      window.DAAB_BREADCRUMBS.syncHeight();
    }
  }

  var booted = false;
  function boot() {
    if (booted) return;
    booted = true;
    syncAll();
    window.addEventListener("resize", syncAll, { passive: true });
    window.addEventListener("load", syncAll, { passive: true });
  }

  document.addEventListener("daab-primary-nav-ready", syncAll);
  document.addEventListener("daab-breadcrumbs-ready", syncAll);
  document.addEventListener("DOMContentLoaded", boot);

  if (document.readyState !== "loading") {
    boot();
  }

  global.setTimeout(syncAll, 120);
  global.setTimeout(syncAll, 600);
})(window);
