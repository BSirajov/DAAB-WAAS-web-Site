/**
 * Preserve scroll position / logical section when switching AZ ↔ EN.
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "daab-lang-position";
  var HASH_SYNC_PAGES = { activities: 1, charter: 1, foundation: 1 };

  var SKIP_IDS = {
    content: 1,
    "search-overlay": 1,
    "search-input": 1,
    "search-results": 1,
    eventsTimelineMenu: 1,
    charterArticlesMenu: 1,
    charterArticlesWidget: 1,
    primaryNavMenu: 1,
    pagination: 1,
    tableBody: 1,
    searchInput: 1,
    filterCountry: 1,
    filterDegree: 1,
    filterIxtilas: 1,
    perPageSel: 1,
    resultCount: 1,
    noResults: 1,
    "no-results": 1,
    "scientists-catalog": 1,
    cardsGrid: 1,
    cardSearch: 1,
    cardSearchEmpty: 1
  };

  var ANCHOR_SELECTOR = [
    "main article.news-card[id]",
    "main section.charter-card[id]",
    "main section.section-block[id]",
    "main article[id]",
    "main section[id]",
    "main [data-daab-section-id]"
  ].join(", ");

  function pageId() {
    return (
      document.documentElement.getAttribute("data-daab-page-id") ||
      (global.DAAB_I18N &&
        global.DAAB_I18N.getPageId &&
        global.DAAB_I18N.getPageId()) ||
      ""
    );
  }

  function hashId() {
    if (!location.hash) return "";
    try {
      return decodeURIComponent(location.hash.slice(1));
    } catch (e) {
      return location.hash.slice(1);
    }
  }

  function scrollRatio() {
    var max = Math.max(
      1,
      document.documentElement.scrollHeight - window.innerHeight
    );
    return window.scrollY / max;
  }

  function anchorWeight(el) {
    if (el.classList.contains("news-card")) return 120;
    if (el.classList.contains("charter-card")) return 120;
    if (el.hasAttribute("data-daab-section-id")) return 100;
    if (el.classList.contains("section-block")) return 90;
    if (el.tagName === "ARTICLE") return 70;
    if (el.tagName === "SECTION") return 50;
    return 0;
  }

  function getLogicalAnchor() {
    if (isNearPageTop()) {
      return null;
    }

    var id = hashId();
    if (id && !SKIP_IDS[id] && document.getElementById(id)) {
      return id;
    }

    var candidates = document.querySelectorAll(ANCHOR_SELECTOR);
    var best = null;
    var bestScore = -Infinity;
    var viewBottom = window.innerHeight;
    var focusLine = window.innerHeight * 0.32;

    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      var anchorId = el.id || el.getAttribute("data-daab-section-id");
      if (!anchorId || SKIP_IDS[anchorId]) continue;
      var rect = el.getBoundingClientRect();
      if (rect.bottom <= 0 || rect.top >= viewBottom) continue;
      var visible =
        Math.min(rect.bottom, viewBottom) - Math.max(rect.top, 0);
      var mid = rect.top + rect.height / 2;
      var dist = Math.abs(mid - focusLine);
      var score = visible * 2 - dist + anchorWeight(el);
      if (score > bestScore) {
        bestScore = score;
        best = anchorId;
      }
    }
    return best;
  }

  function navOffset() {
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
        if (crumbs) {
          h += crumbs.getBoundingClientRect().height;
        }
      }
    }
    return Math.ceil(h) + 20;
  }

  /** True when nav + hero/header should remain in view (not mid-article). */
  function isNearPageTop() {
    var y = window.scrollY || document.documentElement.scrollTop || 0;
    return y <= navOffset() + 32;
  }

  function clearUrlHash() {
    if (!location.hash) return;
    if (global.history && global.history.replaceState) {
      global.history.replaceState(
        null,
        "",
        location.pathname + location.search
      );
    }
  }

  function isProfileCardAnchor(id) {
    if (!id) return false;
    var el = document.getElementById(id);
    return !!(el && el.classList && el.classList.contains("card"));
  }

  function shouldDeferProfileRestore() {
    return pageId() === "scientists-profiles" && isProfileCardAnchor(hashId());
  }

  function scrollToAnchor(id, smooth) {
    if (!id) return false;
    var el =
      document.getElementById(id) ||
      document.querySelector('[data-daab-section-id="' + id + '"]');
    if (!el) return false;
    var top =
      el.getBoundingClientRect().top + window.pageYOffset - navOffset();
    var root = document.documentElement;
    var prevInline = root.style.scrollBehavior;
    if (!smooth) {
      root.style.scrollBehavior = "auto";
    }
    window.scrollTo({
      top: Math.max(0, top),
      behavior: smooth ? "smooth" : "auto"
    });
    if (!smooth) {
      global.requestAnimationFrame(function () {
        root.style.scrollBehavior = prevInline;
      });
    }
    return true;
  }

  function splitUrl(url) {
    var hash = "";
    var search = "";
    var base = url || "";
    var hashIdx = base.indexOf("#");
    if (hashIdx >= 0) {
      hash = base.slice(hashIdx);
      base = base.slice(0, hashIdx);
    }
    var qIdx = base.indexOf("?");
    if (qIdx >= 0) {
      search = base.slice(qIdx);
      base = base.slice(0, qIdx);
    }
    return { base: base, search: search, hash: hash };
  }

  function appendHash(url, anchor) {
    if (!url || !anchor) return url;
    var parts = splitUrl(url);
    return parts.base + parts.search + "#" + encodeURIComponent(anchor);
  }

  function saveIntent(targetLang, anchor) {
    var atTop = isNearPageTop();
    var payload = {
      pageId: pageId(),
      anchor: atTop ? null : anchor || null,
      ratio: atTop ? 0 : scrollRatio(),
      targetLang: targetLang,
      ts: Date.now()
    };
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) { /* ignore */ }
    return payload;
  }

  function readIntent() {
    try {
      var raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function clearIntent() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) { /* ignore */ }
  }

  function decorateAlternateUrl(url, targetLang) {
    var anchor = getLogicalAnchor();
    saveIntent(targetLang, anchor);
    return appendHash(url, anchor);
  }

  function restoreTop() {
    var root = document.documentElement;
    var prevInline = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
    global.requestAnimationFrame(function () {
      root.style.scrollBehavior = prevInline;
    });
    return true;
  }

  function restoreFromIntent() {
    var intent = readIntent();

    if (
      intent &&
      !intent.anchor &&
      typeof intent.ratio === "number" &&
      intent.ratio <= 0.04
    ) {
      clearUrlHash();
      restoreTop();
      clearIntent();
      return true;
    }

    var id = hashId();
    if (id && scrollToAnchor(id, false)) {
      clearIntent();
      return true;
    }

    if (!intent) return false;

    var currentPage = pageId();
    if (intent.pageId && currentPage && intent.pageId !== currentPage) {
      clearIntent();
      return false;
    }

    if (intent.anchor && scrollToAnchor(intent.anchor, false)) {
      if (global.history && global.history.replaceState) {
        global.history.replaceState(
          null,
          "",
          "#" + encodeURIComponent(intent.anchor)
        );
      }
      clearIntent();
      return true;
    }

    if (typeof intent.ratio === "number") {
      if (!intent.anchor && intent.ratio <= 0.04) {
        restoreTop();
        clearIntent();
        return true;
      }
      var max = Math.max(
        1,
        document.documentElement.scrollHeight - window.innerHeight
      );
      window.scrollTo(0, Math.round(intent.ratio * max));
      clearIntent();
      return true;
    }

    clearIntent();
    return false;
  }

  var restorePending = false;

  function tryRestore(attempt) {
    if (restoreFromIntent()) {
      restorePending = false;
      return;
    }
    if (attempt < 24) {
      global.requestAnimationFrame(function () {
        tryRestore(attempt + 1);
      });
    } else {
      restorePending = false;
    }
  }

  function initRestore() {
    if (document.body && document.body.classList.contains("daab-gateway")) {
      return;
    }
    if (pageId() === "scientists-profiles") {
      if (!hashId()) {
        clearIntent();
        return;
      }
      if (shouldDeferProfileRestore()) {
        return;
      }
    }
    if (restorePending) return;
    restorePending = true;
    tryRestore(0);
  }

  var hashSyncTimer = null;
  function syncHashFromScroll() {
    if (!HASH_SYNC_PAGES[pageId()]) return;
    if (hashSyncTimer) return;
    hashSyncTimer = global.setTimeout(function () {
      hashSyncTimer = null;
      if (isNearPageTop()) {
        clearUrlHash();
        return;
      }
      var anchor = getLogicalAnchor();
      if (!anchor || anchor === hashId()) return;
      if (global.history && global.history.replaceState) {
        global.history.replaceState(
          null,
          "",
          location.pathname + location.search + "#" + encodeURIComponent(anchor)
        );
      }
    }, 150);
  }

  if (global.history && "scrollRestoration" in global.history) {
    if (location.hash || readIntent()) {
      global.history.scrollRestoration = "manual";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRestore);
  } else {
    initRestore();
  }

  global.addEventListener("pageshow", function (ev) {
    if (ev.persisted || location.hash) {
      initRestore();
    }
  });

  global.addEventListener("load", function () {
    initRestore();
  }, { once: true });

  global.addEventListener("hashchange", function () {
    var id = hashId();
    if (pageId() === "scientists-profiles" && isProfileCardAnchor(id)) {
      return;
    }
    if (id) scrollToAnchor(id, false);
  });

  global.addEventListener("scroll", syncHashFromScroll, { passive: true });

  global.DAAB_LANG_POSITION = {
    getLogicalAnchor: getLogicalAnchor,
    isNearPageTop: isNearPageTop,
    decorateAlternateUrl: decorateAlternateUrl,
    appendHash: appendHash,
    scrollToAnchor: scrollToAnchor,
    navOffset: navOffset,
    saveIntent: saveIntent,
    restoreFromIntent: restoreFromIntent
  };
})(typeof window !== "undefined" ? window : this);
