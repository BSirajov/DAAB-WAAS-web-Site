/**
 * DAAB performance helpers — connection-aware preloads, lazy images, rAF throttle.
 */
(function (global) {
  "use strict";

  function connectionInfo() {
    return (
      global.navigator &&
      (global.navigator.connection ||
        global.navigator.mozConnection ||
        global.navigator.webkitConnection)
    );
  }

  function heavyPreloadOk() {
    var conn = connectionInfo();
    if (!conn) return true;
    if (conn.saveData) return false;
    var type = String(conn.effectiveType || "").toLowerCase();
    if (type === "slow-2g" || type === "2g") return false;
    return true;
  }

  function prefersReducedMotion() {
    try {
      return global.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch (e) {
      return false;
    }
  }

  function shouldEnhanceLazyImages() {
    return !prefersReducedMotion();
  }

  function isCriticalImage(img) {
    if (!img || img.nodeType !== 1) return true;
    if (img.getAttribute("loading") === "eager") return true;
    if (img.getAttribute("fetchpriority") === "high") return true;
    if (img.classList && img.classList.contains("nav-brand-logo")) return true;
    if (img.closest && img.closest(".hero, .page-logo, .nav-strip")) {
      var inNav = img.closest(".nav-strip");
      if (!inNav || img.classList.contains("nav-brand-logo")) return true;
    }
    if (img.hasAttribute("data-thumb-src")) return true;
    return false;
  }

  function enhanceLazyImages(root) {
    if (!shouldEnhanceLazyImages()) return;
    var scope = root && root.querySelectorAll ? root : document;
    var images = scope.querySelectorAll ? scope.querySelectorAll("img") : [];
    var i;
    for (i = 0; i < images.length; i++) {
      var img = images[i];
      if (isCriticalImage(img)) continue;
      if (!img.getAttribute("loading")) img.setAttribute("loading", "lazy");
      if (!img.getAttribute("decoding")) img.setAttribute("decoding", "async");
      if (!img.getAttribute("fetchpriority")) img.setAttribute("fetchpriority", "low");
    }
  }

  function rafThrottle(fn) {
    var scheduled = false;
    var lastArgs = null;
    return function throttled() {
      lastArgs = arguments;
      if (scheduled) return;
      scheduled = true;
      global.requestAnimationFrame(function () {
        scheduled = false;
        fn.apply(null, lastArgs);
      });
    };
  }

  function bootLazyImages() {
    enhanceLazyImages(document);
    if (typeof MutationObserver === "undefined") return;
    var pending = false;
    var observer = new MutationObserver(function () {
      if (pending) return;
      pending = true;
      global.requestAnimationFrame(function () {
        pending = false;
        enhanceLazyImages(document);
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  global.DAAB_PERF = {
    heavyPreloadOk: heavyPreloadOk,
    enhanceLazyImages: enhanceLazyImages,
    rafThrottle: rafThrottle,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootLazyImages, { once: true });
  } else {
    bootLazyImages();
  }
})(typeof window !== "undefined" ? window : this);
