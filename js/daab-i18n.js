/**
 * DAAB bilingual environment — language detection, routes, asset roots.
 * Requires i18n/routes.json; optional i18n/ui.json for shell UI.
 */
(function (global) {
  "use strict";

  var ROUTES_URL = null;
  var UI_URL = null;
  var routesCache = null;
  var uiCache = null;
  var navCache = null;
  var searchIndexCache = null;
  var routesInflight = null;
  var uiInflight = null;
  var navInflight = null;
  var searchIndexInflight = null;

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

  function i18nUrl(file) {
    return assetRoot() + "i18n/" + file;
  }

  function detectLang() {
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    var path = location.pathname.replace(/\\/g, "/");
    if (/\/en(\/|$)/.test(path)) return "en";
    if (/\/az(\/|$)/.test(path)) return "az";
    var q = new URLSearchParams(location.search).get("lang");
    if (q === "en" || q === "az") return q;
    return "az";
  }

  function normalizePath(p) {
    return p.replace(/\\/g, "/").replace(/^\//, "").toLowerCase();
  }

  function siteRelativePath(path) {
    path = path.replace(/\\/g, "/");
    var localeIdx = path.search(/\/(az|en)(\/|$)/i);
    if (localeIdx >= 0) {
      return path.slice(localeIdx + 1);
    }
    var base = path.split("/").pop() || "";
    if (/\.html?$/i.test(base)) return base;
    if (!path.endsWith("/")) path += "/";
    return path.replace(/^\//, "") + "index.html";
  }

  function currentPathKey() {
    var path = siteRelativePath(location.pathname);
    var name = path.split("/").pop() || "";
    if (!name || !/\.html?$/i.test(name)) {
      if (!path.endsWith("/")) path += "/";
      path += "index.html";
    }
    return normalizePath(path.replace(/^\//, ""));
  }

  function fetchJson(url) {
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error("Failed to load " + url);
      return res.json();
    });
  }

  function loadCachedJson(url, getCache, setCache, getInflight, setInflight) {
    var cached = getCache();
    if (cached) return Promise.resolve(cached);
    var pending = getInflight();
    if (pending) return pending;
    var promise = fetchJson(url)
      .then(function (data) {
        setCache(data);
        setInflight(null);
        return data;
      })
      .catch(function (err) {
        setInflight(null);
        throw err;
      });
    setInflight(promise);
    return promise;
  }

  function loadRoutes() {
    ROUTES_URL = ROUTES_URL || i18nUrl("routes.json");
    /* Browser cache bust: bump ?v= below when routes.json content changes (JSON "version" field is documentary). */
    return loadCachedJson(
      ROUTES_URL + "?v=7",
      function () { return routesCache; },
      function (data) { routesCache = data; },
      function () { return routesInflight; },
      function (p) { routesInflight = p; }
    );
  }

  function loadUi() {
    UI_URL = UI_URL || i18nUrl("ui.json");
    return loadCachedJson(
      UI_URL + "?v=20",
      function () { return uiCache; },
      function (data) { uiCache = data; },
      function () { return uiInflight; },
      function (p) { uiInflight = p; }
    );
  }

  function loadSearchIndex() {
    return loadCachedJson(
      i18nUrl("search-index.json") + "?v=10",
      function () { return searchIndexCache; },
      function (data) { searchIndexCache = data; },
      function () { return searchIndexInflight; },
      function (p) { searchIndexInflight = p; }
    );
  }

  function loadNav() {
    return loadCachedJson(
      i18nUrl("nav.json") + "?v=11",
      function () { return navCache; },
      function (data) { navCache = data; },
      function () { return navInflight; },
      function (p) { navInflight = p; }
    );
  }

  /** Path relative to current page (e.g. foundation.html, ../mission.html). */
  function pageHref(page, lang) {
    if (!page) return lang === "en" ? "index.html" : "index.html";
    var target = lang === "en" ? page.en : page.az;
    var prefix = lang + "/";
    if (target.toLowerCase().indexOf(prefix) === 0) {
      target = target.slice(prefix.length);
    }
    var pathKey = currentPathKey();
    var hereSuffix = pathKey;
    if (hereSuffix.toLowerCase().indexOf(prefix) === 0) {
      hereSuffix = hereSuffix.slice(prefix.length);
    }
    var hereParts = hereSuffix.split("/").filter(Boolean);
    if (hereParts.length) hereParts.pop();
    var up = hereParts.length;
    return (up ? Array(up + 1).join("../") : "") + target;
  }

  function prominentFigureSuffix(pathKey) {
    var m = pathKey.match(/^(?:az|en)\/prominent_figures\/(.+)$/);
    return m ? m[1] : null;
  }

  function findPage(routes, pathKey) {
    if (prominentFigureSuffix(pathKey)) {
      var pages = routes.pages || [];
      for (var j = 0; j < pages.length; j++) {
        if (pages[j].id === "prominent-figure") return pages[j];
      }
    }
    var pages = routes.pages || [];
    var pageId = document.documentElement.getAttribute("data-daab-page-id");
    if (pageId) {
      for (var k = 0; k < pages.length; k++) {
        var byId = pages[k];
        if (
          byId.id === pageId &&
          (normalizePath(byId.az) === pathKey || normalizePath(byId.en) === pathKey)
        ) {
          return byId;
        }
      }
    }
    for (var i = 0; i < pages.length; i++) {
      var p = pages[i];
      if (normalizePath(p.az) === pathKey || normalizePath(p.en) === pathKey) return p;
    }
    return null;
  }

  function resolveUrl(lang, page, routes) {
    if (!page) return lang === "az" ? assetRoot() + "az/index.html" : assetRoot() + "en/index.html";
    var rel = lang === "en" ? page.en : page.az;
    return assetRoot() + rel;
  }

  function getAlternateUrl(lang, routes) {
    routes = routes || routesCache;
    if (!routes) return null;
    var pathKey = currentPathKey();
    var pf = prominentFigureSuffix(pathKey);
    if (pf) {
      return assetRoot() + lang + "/prominent_figures/" + pf;
    }
    var page = findPage(routes, pathKey);
    return resolveUrl(lang, page, routes);
  }

  function getPageId(routes) {
    routes = routes || routesCache;
    if (!routes) return null;
    var page = findPage(routes, currentPathKey());
    return page ? page.id : null;
  }

  function persistLang(lang) {
    try {
      localStorage.setItem("daab-lang", lang);
    } catch (e) { /* ignore */ }
  }

  function readPersistedLang() {
    try {
      var v = localStorage.getItem("daab-lang");
      return v === "en" || v === "az" ? v : null;
    } catch (e) {
      return null;
    }
  }

  function initGateway() {
    var params = new URLSearchParams(location.search);
    if (params.get("choose") === "1") return;
    var lang = params.get("lang");
    if (lang === "en") {
      persistLang("en");
      location.replace(assetRoot() + "en/index.html");
      return;
    }
    if (lang === "az") {
      persistLang("az");
      location.replace(assetRoot() + "az/index.html");
      return;
    }
    var saved = readPersistedLang();
    if (saved === "en") {
      location.replace(assetRoot() + "en/index.html");
      return;
    }
    if (saved === "az") {
      location.replace(assetRoot() + "az/index.html");
    }
  }

  function absoluteUrl(rel) {
    try {
      return new URL(rel, location.href).href;
    } catch (e) {
      return rel;
    }
  }

  function injectHreflang(page, routes) {
    if (!page) return;
    var head = document.head;
    if (!head) return;
    var azPath = assetRoot() + page.az;
    var enPath = assetRoot() + page.en;
    function setLink(rel, href, hreflang) {
      var sel = 'link[rel="' + rel + '"]' + (hreflang ? '[hreflang="' + hreflang + '"]' : "");
      var el = head.querySelector(sel);
      if (!el) {
        el = document.createElement("link");
        el.rel = rel;
        if (hreflang) el.hreflang = hreflang;
        head.appendChild(el);
      }
      el.href = absoluteUrl(href);
    }
    var lang = detectLang();
    setLink("canonical", lang === "en" ? enPath : azPath);
    setLink("alternate", azPath, "az");
    setLink("alternate", enPath, "en");
    setLink("alternate", azPath, "x-default");
  }

  var DAAB_I18N = {
    assetRoot: assetRoot,
    i18nUrl: i18nUrl,
    detectLang: detectLang,
    loadRoutes: loadRoutes,
    loadUi: loadUi,
    loadNav: loadNav,
    loadSearchIndex: loadSearchIndex,
    pageHref: pageHref,
    getPageId: getPageId,
    getAlternateUrl: getAlternateUrl,
    findPage: function (routes) {
      return findPage(routes, currentPathKey());
    },
    persistLang: persistLang,
    readPersistedLang: readPersistedLang,
    initGateway: initGateway,
    injectHreflang: injectHreflang,
    currentPathKey: currentPathKey
  };

  global.DAAB_I18N = DAAB_I18N;
})(typeof window !== "undefined" ? window : this);
