/**
 * Legal pages: on entry with #page-title (or no section hash), jump instantly
 * so the page title sits just below the sticky nav — not mid-document.
 * Section navigation uses the shared News/Charter sidebar timeline scripts.
 */
(function (global) {
  "use strict";

  var LEGAL_IDS = {
    "legal-notice": true,
    privacy: true,
    cookies: true,
    terms: true
  };

  var pageId = document.documentElement.getAttribute("data-daab-page-id") || "";
  if (!LEGAL_IDS[pageId]) return;

  if ("scrollRestoration" in history) {
    try {
      history.scrollRestoration = "manual";
    } catch (e) {
      /* ignore */
    }
  }

  function stickyOffset() {
    if (
      global.DAAB_LANG_POSITION &&
      typeof global.DAAB_LANG_POSITION.navOffset === "function"
    ) {
      return global.DAAB_LANG_POSITION.navOffset();
    }
    var root = document.documentElement;
    var style = global.getComputedStyle(root);
    var h = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
    if (!isFinite(h) || h <= 0) {
      h = parseFloat(style.getPropertyValue("--daab-nav-height"));
      if (!isFinite(h) || h <= 0) {
        var nav = document.querySelector(".nav-strip");
        h = nav ? nav.getBoundingClientRect().height : 86;
      }
      var crumbsH = parseFloat(style.getPropertyValue("--daab-breadcrumbs-height"));
      if (isFinite(crumbsH) && crumbsH > 0) {
        h += crumbsH;
      } else {
        var crumbs = document.getElementById("daab-breadcrumbs");
        if (crumbs) h += crumbs.getBoundingClientRect().height;
      }
    }
    return Math.ceil(h) + 12;
  }

  function pageTitleEl() {
    return (
      document.getElementById("page-title") ||
      document.querySelector(".hero h1") ||
      document.querySelector("h1")
    );
  }

  function shouldJumpToTitle() {
    var hash = String(location.hash || "").toLowerCase();
    return (
      !hash ||
      hash === "#" ||
      hash === "#top" ||
      hash === "#page-title" ||
      hash === "#content"
    );
  }

  function jumpToPageTitle() {
    if (!shouldJumpToTitle()) return;

    var html = document.documentElement;
    var body = document.body;
    html.style.setProperty("scroll-behavior", "auto", "important");
    if (body) body.style.setProperty("scroll-behavior", "auto", "important");

    if (location.hash && global.history && global.history.replaceState) {
      var hash = String(location.hash).toLowerCase();
      if (hash === "#top" || hash === "#") {
        global.history.replaceState(null, "", location.pathname + location.search);
      }
    }

    var title = pageTitleEl();
    if (!title) {
      html.scrollTop = 0;
      if (body) body.scrollTop = 0;
      global.scrollTo(0, 0);
      return;
    }

    if (typeof title.scrollIntoView === "function") {
      try {
        title.scrollIntoView({ block: "start", behavior: "instant" });
      } catch (e1) {
        try {
          title.scrollIntoView({ block: "start", behavior: "auto" });
        } catch (e2) {
          title.scrollIntoView(true);
        }
      }
    }

    var y =
      title.getBoundingClientRect().top +
      (global.pageYOffset || html.scrollTop || 0) -
      stickyOffset();
    y = Math.max(0, Math.round(y));
    html.scrollTop = y;
    if (body) body.scrollTop = y;
    global.scrollTo(0, y);
  }

  try {
    sessionStorage.removeItem("daab-force-page-top");
    sessionStorage.removeItem("daab-lang-position");
  } catch (e2) {
    /* ignore */
  }

  function boot() {
    if (!shouldJumpToTitle()) return;
    jumpToPageTitle();
    global.requestAnimationFrame(jumpToPageTitle);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  global.addEventListener("pageshow", function () {
    if (shouldJumpToTitle()) jumpToPageTitle();
  });
  global.addEventListener(
    "load",
    function () {
      if (shouldJumpToTitle()) jumpToPageTitle();
    },
    { once: true, passive: true }
  );
  document.addEventListener("daab-breadcrumbs-ready", function () {
    if (shouldJumpToTitle()) jumpToPageTitle();
  });
  document.addEventListener("daab-primary-nav-ready", function () {
    if (shouldJumpToTitle()) jumpToPageTitle();
  });

  if (shouldJumpToTitle()) {
    global.setTimeout(jumpToPageTitle, 0);
    global.setTimeout(jumpToPageTitle, 100);
    global.setTimeout(jumpToPageTitle, 250);
    global.setTimeout(jumpToPageTitle, 500);
  }
})(typeof window !== "undefined" ? window : globalThis);
