/**
 * Injects a short page subtitle beneath the hero h1 from i18n/page-subtitles.json.
 */
(function (global) {
  "use strict";

  var CACHE = null;
  var VERSION = "4";

  function assetRoot() {
    var I18N = global.DAAB_I18N;
    if (I18N && typeof I18N.assetRoot === "function") return I18N.assetRoot();
    var explicit = document.documentElement.getAttribute("data-daab-asset-root");
    if (explicit) return explicit;
    return "../";
  }

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && typeof I18N.detectLang === "function") return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(location.pathname.replace(/\\/g, "/")) ? "en" : "az";
  }

  function pageId() {
    var attr = document.documentElement.getAttribute("data-daab-page-id");
    if (attr) return attr;
    var I18N = global.DAAB_I18N;
    if (I18N && typeof I18N.getPageId === "function") {
      return I18N.getPageId() || "";
    }
    return "";
  }

  function heroHeading() {
    return document.querySelector(
      "header.hero h1, header.page-hero h1, header .activities-hero-wrap h1, header .hero-inner h1"
    );
  }

  function loadSubtitles() {
    if (CACHE) return Promise.resolve(CACHE);
    var url = assetRoot() + "i18n/page-subtitles.json?v=" + VERSION;
    return fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error("page-subtitles.json " + res.status);
        return res.json();
      })
      .then(function (data) {
        CACHE = data && data.pages ? data.pages : {};
        return CACHE;
      })
      .catch(function () {
        CACHE = {};
        return CACHE;
      });
  }

  function inject(text) {
    if (document.getElementById("page-hero-subtitle")) return;
    var h1 = heroHeading();
    if (!h1 || h1.closest("nav")) return;
    if (h1.nextElementSibling && h1.nextElementSibling.classList.contains("page-hero-subtitle")) return;

    var el = document.createElement("p");
    el.className = "page-hero-subtitle";
    el.setAttribute("role", "doc-subtitle");
    el.textContent = text;

    var subtitleId = "page-hero-subtitle";
    el.id = subtitleId;
    if (!h1.getAttribute("aria-describedby")) {
      h1.setAttribute("aria-describedby", subtitleId);
    }

    h1.insertAdjacentElement("afterend", el);
  }

  function init() {
    var id = pageId();
    if (!id) return;
    var lang = detectLang();
    loadSubtitles().then(function (pages) {
      var entry = pages[id];
      if (!entry) return;
      var text = entry[lang] || entry.en || entry.az;
      if (!text) return;
      inject(text);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  global.DAAB_PAGE_SUBTITLE = { init: init };
})(typeof window !== "undefined" ? window : this);
