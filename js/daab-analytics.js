/**
 * DAAB / WAAS — Google Analytics 4 (production only).
 * Config: i18n/analytics.json — set measurementId (G-XXXXXXXXXX) to enable.
 */
(function (global) {
  "use strict";

  var loaded = false;

  function assetRoot() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.assetRoot) return I18N.assetRoot();
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root != null && root !== "") {
      return root.endsWith("/") ? root : root + "/";
    }
    return "";
  }

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function pageId() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.getPageId) {
      var id = I18N.getPageId();
      if (id) return id;
    }
    return document.documentElement.getAttribute("data-daab-page-id") || "";
  }

  function shouldSkip(config) {
    var host = String(location.hostname || "").toLowerCase();
    var hosts = config.productionHosts || ["daab-waas.com", "www.daab-waas.com"];
    if (hosts.indexOf(host) === -1) return true;

    var flags = config.skipQueryFlags || [];
    if (!flags.length) return false;
    var params = new URLSearchParams(location.search || "");
    for (var i = 0; i < flags.length; i += 1) {
      if (params.has(flags[i])) return true;
    }
    return false;
  }

  function fetchConfig() {
    var url = assetRoot() + "i18n/analytics.json";
    return fetch(url, { credentials: "same-origin", cache: "no-cache" }).then(function (res) {
      if (!res.ok) throw new Error("analytics config " + res.status);
      return res.json();
    });
  }

  function injectGtag(measurementId) {
    if (loaded || document.getElementById("daab-ga4-script")) return;
    loaded = true;

    global.dataLayer = global.dataLayer || [];
    function gtag() {
      global.dataLayer.push(arguments);
    }
    global.gtag = gtag;
    gtag("js", new Date());

    var script = document.createElement("script");
    script.id = "daab-ga4-script";
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
    document.head.appendChild(script);

    var lang = detectLang();
    var pid = pageId();
    var pagePath = location.pathname + location.search;

    var config = {
      send_page_view: true,
      page_path: pagePath,
      page_location: location.href,
      language: lang
    };
    if (pid) {
      config.daab_page_id = pid;
      config.daab_lang = lang;
    }

    gtag("config", measurementId, config);
  }

  function hasAnalyticsConsent() {
    var api = global.DAAB_COOKIE;
    if (api && typeof api.hasAnalyticsConsent === "function") {
      return api.hasAnalyticsConsent();
    }
    try {
      var raw = global.localStorage.getItem("daab-cookie-consent");
      if (!raw) return false;
      var data = JSON.parse(raw);
      return !!(data && data.analytics);
    } catch (e) {
      return false;
    }
  }

  function ensureCookieConsentScript() {
    if (document.getElementById("daab-cookie-consent-script")) return;
    if (global.DAAB_COOKIE) return;
    var script = document.createElement("script");
    script.id = "daab-cookie-consent-script";
    script.src = assetRoot() + "js/daab-cookie-consent.js?v=6";
    script.defer = true;
    document.head.appendChild(script);
  }

  function tryLoadGa(config) {
    if (!config || config.provider !== "ga4") return;
    if (shouldSkip(config)) return;
    if (!hasAnalyticsConsent()) return;
    var measurementId = String(config.measurementId || "").trim();
    if (!/^G-[A-Z0-9]+$/i.test(measurementId)) return;
    injectGtag(measurementId);
  }

  function init() {
    ensureCookieConsentScript();
    fetchConfig()
      .then(function (config) {
        tryLoadGa(config);
        global.addEventListener("daab-cookie-consent", function () {
          tryLoadGa(config);
        });
      })
      .catch(function () {
        /* analytics optional — never break the page */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);
