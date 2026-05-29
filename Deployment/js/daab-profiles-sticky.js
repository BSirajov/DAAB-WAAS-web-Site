/**
 * Scientists profiles — sync sticky chrome heights (nav + breadcrumbs).
 */
(function () {
  "use strict";

  if (document.documentElement.getAttribute("data-daab-page-id") !== "scientists-profiles") {
    return;
  }

  function syncNavHeight() {
    if (window.DAAB_NAV && typeof window.DAAB_NAV.syncNavHeight === "function") {
      window.DAAB_NAV.syncNavHeight();
      return;
    }
    var strip = document.querySelector(".nav-strip");
    if (!strip) return;
    var h = Math.ceil(strip.getBoundingClientRect().height);
    if (h > 0) {
      document.documentElement.style.setProperty("--daab-nav-height", h + "px");
    }
  }

  function syncBreadcrumbsHeight() {
    var el = document.getElementById("daab-breadcrumbs");
    if (!el) {
      document.documentElement.style.setProperty("--daab-breadcrumbs-height", "0px");
      return;
    }
    var h = Math.ceil(el.getBoundingClientRect().height);
    document.documentElement.style.setProperty(
      "--daab-breadcrumbs-height",
      (h > 0 ? h : 0) + "px"
    );
  }

  function syncAll() {
    syncNavHeight();
    syncBreadcrumbsHeight();
  }

  function boot() {
    syncAll();
    window.addEventListener("resize", syncAll, { passive: true });
    window.addEventListener("load", syncAll, { passive: true });
  }

  document.addEventListener("daab-primary-nav-ready", syncAll);
  document.addEventListener("DOMContentLoaded", boot);

  if (document.readyState !== "loading") {
    boot();
  }

  var breadcrumbPoll = 0;
  var breadcrumbTimer = window.setInterval(function () {
    syncBreadcrumbsHeight();
    breadcrumbPoll += 1;
    if (document.getElementById("daab-breadcrumbs") || breadcrumbPoll > 80) {
      window.clearInterval(breadcrumbTimer);
    }
  }, 50);
})();
