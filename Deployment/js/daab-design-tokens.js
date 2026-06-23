/**
 * DAAB design tokens for JavaScript (breakpoints, layout, z-index).
 * CSS custom properties remain authoritative for styling; this module
 * exposes matchMedia helpers built from the DEFAULTS below. Values mirror
 * i18n/design-system.json, which stays as the human-readable reference.
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
