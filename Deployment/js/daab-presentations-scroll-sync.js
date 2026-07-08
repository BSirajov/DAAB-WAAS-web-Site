/**
 * Forum sidebar pages — proportional scroll sync between sidebar TOC and main feed.
 * Desktop only: both panels share the same scroll progress.
 */
(function (window, document) {
  "use strict";

  var PAGE_IDS = {
    "activities-news": true,
    "forum-2024-presentations": true,
    "forum-rector-speeches": true,
    "forum-anas-leadership-speeches": true,
  };
  var DESKTOP_MQ = "(min-width: 1061px)";

  if (!PAGE_IDS[document.documentElement.getAttribute("data-daab-page-id") || ""]) return;

  var sidebarBody = document.querySelector(".sidebar-widget .widget-body");
  var newsFeed = document.querySelector(".news-feed");
  if (!sidebarBody || !newsFeed) return;

  var desktopMq = window.matchMedia(DESKTOP_MQ);
  var syncing = false;
  var pausedUntil = 0;

  function stickyTopOffset() {
    var style = window.getComputedStyle(document.documentElement);
    var stack = style.getPropertyValue("--daab-sticky-top-stack").trim();
    var nav = style.getPropertyValue("--daab-nav-height").trim();
    var base = stack ? parseFloat(stack) : parseFloat(nav);
    if (!isFinite(base)) base = 86;
    return base + 12;
  }

  function mainScrollMetrics() {
    var rect = newsFeed.getBoundingClientRect();
    var feedTop = window.scrollY + rect.top;
    var feedHeight = newsFeed.offsetHeight;
    var viewH = window.innerHeight;
    var start = feedTop - stickyTopOffset();
    var end = feedTop + feedHeight - viewH;
    var range = Math.max(0, end - start);
    return { start: start, range: range };
  }

  function mainProgress() {
    var metrics = mainScrollMetrics();
    if (metrics.range <= 0) return 0;
    return Math.min(1, Math.max(0, (window.scrollY - metrics.start) / metrics.range));
  }

  function sidebarMaxScroll() {
    return Math.max(0, sidebarBody.scrollHeight - sidebarBody.clientHeight);
  }

  function sidebarProgress() {
    var max = sidebarMaxScroll();
    if (max <= 0) return 0;
    return sidebarBody.scrollTop / max;
  }

  function isActive() {
    return desktopMq.matches && sidebarMaxScroll() > 0;
  }

  function pauseSync(ms) {
    pausedUntil = Date.now() + (ms || 900);
  }

  function syncSidebarFromMain() {
    if (!isActive() || syncing || Date.now() < pausedUntil) return;
    var max = sidebarMaxScroll();
    if (max <= 0) return;
    syncing = true;
    sidebarBody.scrollTop = mainProgress() * max;
    syncing = false;
  }

  function syncMainFromSidebar() {
    if (!isActive() || syncing || Date.now() < pausedUntil) return;
    var metrics = mainScrollMetrics();
    if (metrics.range <= 0) return;
    syncing = true;
    window.scrollTo(0, metrics.start + sidebarProgress() * metrics.range);
    syncing = false;
  }

  var mainScheduled = false;
  function onMainScroll() {
    if (mainScheduled) return;
    mainScheduled = true;
    window.requestAnimationFrame(function () {
      mainScheduled = false;
      syncSidebarFromMain();
    });
  }

  var sidebarScheduled = false;
  function onSidebarScroll() {
    if (sidebarScheduled) return;
    sidebarScheduled = true;
    window.requestAnimationFrame(function () {
      sidebarScheduled = false;
      syncMainFromSidebar();
    });
  }

  window.addEventListener("scroll", onMainScroll, { passive: true });
  sidebarBody.addEventListener("scroll", onSidebarScroll, { passive: true });

  document.querySelectorAll(".timeline-list a[href^='#']").forEach(function (link) {
    link.addEventListener("click", function () {
      pauseSync(1200);
    });
  });

  window.addEventListener("resize", onMainScroll, { passive: true });
  if (typeof desktopMq.addEventListener === "function") {
    desktopMq.addEventListener("change", onMainScroll);
  } else if (typeof desktopMq.addListener === "function") {
    desktopMq.addListener(onMainScroll);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", syncSidebarFromMain);
  } else {
    syncSidebarFromMain();
  }
})(window, document);
