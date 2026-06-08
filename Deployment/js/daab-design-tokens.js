/**
 * DAAB design tokens for JavaScript (breakpoints, layout, z-index).
 * CSS custom properties remain authoritative for styling; this module
 * keeps matchMedia and layout logic in sync with i18n/design-system.json.
 */
(function (global) {
  "use strict";

  var DEFAULTS = {
    breakpoints: { navCompact: 1180, sidebarStack: 1060 },
    layout: { contentMax: 1220, contentMaxNarrow: 1060, shellPaddingX: 24 },
    sticky: { navHeightDesktop: 86, navHeightCompact: 72, breadcrumbsMinHeight: 40 },
    zIndex: { nav: 9999, searchOverlay: 999999 },
  };

  var tokens = Object.assign({}, DEFAULTS);
  var loadPromise = null;

  function assetRoot() {
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root != null && root !== "") {
      return root.endsWith("/") ? root : root + "/";
    }
    var path = location.pathname.replace(/\\/g, "/");
    if (/\/(az|en)\//.test(path)) {
      var parts = path.split("/").filter(Boolean);
      var langIdx = parts.findIndex(function (p) {
        return p === "az" || p === "en";
      });
      if (langIdx >= 0) {
        var depth = parts.length - langIdx - 2;
        if (depth < 0) depth = 0;
        return depth ? Array(depth + 1).join("../") : "./";
      }
    }
    return "";
  }

  function deepMerge(base, patch) {
    if (!patch || typeof patch !== "object") return base;
    Object.keys(patch).forEach(function (key) {
      if (
        patch[key] &&
        typeof patch[key] === "object" &&
        !Array.isArray(patch[key]) &&
        base[key] &&
        typeof base[key] === "object"
      ) {
        deepMerge(base[key], patch[key]);
      } else {
        base[key] = patch[key];
      }
    });
    return base;
  }

  function load() {
    if (loadPromise) return loadPromise;
    var url = assetRoot() + "i18n/design-system.json?v=1";
    loadPromise = fetch(url)
      .then(function (res) {
        if (!res.ok) return tokens;
        return res.json();
      })
      .then(function (json) {
        if (json) deepMerge(tokens, json);
        return tokens;
      })
      .catch(function () {
        return tokens;
      });
    return loadPromise;
  }

  function maxWidthQuery(px) {
    return "(max-width: " + px + "px)";
  }

  function navCompactMq() {
    return global.matchMedia(maxWidthQuery(tokens.breakpoints.navCompact));
  }

  function sidebarStackMq() {
    return global.matchMedia(maxWidthQuery(tokens.breakpoints.sidebarStack));
  }

  var api = {
    get: function () {
      return tokens;
    },
    load: load,
    navCompactMq: navCompactMq,
    sidebarStackMq: sidebarStackMq,
    isNavCompact: function () {
      return navCompactMq().matches;
    },
    isSidebarStack: function () {
      return sidebarStackMq().matches;
    },
  };

  global.DAAB_DESIGN = api;
})(typeof window !== "undefined" ? window : this);
