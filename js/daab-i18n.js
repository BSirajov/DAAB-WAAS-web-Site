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
      ROUTES_URL + "?v=22",
      function () { return routesCache; },
      function (data) { routesCache = data; },
      function () { return routesInflight; },
      function (p) { routesInflight = p; }
    );
  }

  function loadUi() {
    UI_URL = UI_URL || i18nUrl("ui.json");
    return loadCachedJson(
      UI_URL + "?v=58",
      function () { return uiCache; },
      function (data) { uiCache = data; },
      function () { return uiInflight; },
      function (p) { uiInflight = p; }
    );
  }

  function loadSearchIndex() {
    return loadCachedJson(
      i18nUrl("search-index.json") + "?v=32",
      function () { return searchIndexCache; },
      function (data) { searchIndexCache = data; },
      function () { return searchIndexInflight; },
      function (p) { searchIndexInflight = p; }
    );
  }

  function loadNav() {
    return loadCachedJson(
      i18nUrl("nav.json") + "?v=26",
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

  function findPage(routes, pathKey) {
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
    var page = findPage(routes, pathKey);
    return resolveUrl(lang, page, routes);
  }

  function getPageId(routes) {
    routes = routes || routesCache;
    if (!routes) return null;
    var page = findPage(routes, currentPathKey());
    return page ? page.id : null;
  }

  var PREFS_KEY = "daab-prefs";
  var PREFS_VERSION = 1;
  var LANG_KEY = "daab-lang";
  var LIST_SORT = ["ad_soyad", "yasadigi_olke", "ixtilas", "elmi_derece", "cinsi"];
  var LIST_GROUP = ["", "yasadigi_olke", "ixtilas", "elmi_derece", "cinsi"];
  var LIST_VIEW = ["cards", "table"];
  var LIST_PER = ["20", "50", "100", "999999"];
  var PROFILE_SORT = ["name", "country", "ixtilas"];
  var PROFILE_GROUP = ["", "country", "ixtilas", "degree"];
  var SESSION_PREF_KEYS = [
    "daab-scientists-list-sort",
    "daab-scientists-list-group",
    "daab-scientists-list-view",
    "daab-profiles-sort",
    "daab-profiles-group"
  ];

  function emptyPrefs() {
    return { v: PREFS_VERSION };
  }

  function readPrefs() {
    try {
      var raw = localStorage.getItem(PREFS_KEY);
      if (!raw) return emptyPrefs();
      var data = JSON.parse(raw);
      if (!data || typeof data !== "object" || data.v !== PREFS_VERSION) return emptyPrefs();
      return data;
    } catch (e) {
      return emptyPrefs();
    }
  }

  function writePrefs(data) {
    try {
      data.v = PREFS_VERSION;
      localStorage.setItem(PREFS_KEY, JSON.stringify(data));
    } catch (e) { /* private mode or blocked storage */ }
  }

  function sanitizeDir(dir) {
    if (dir === 1 || dir === -1) return dir;
    if (dir === "asc" || dir === "1") return 1;
    if (dir === "desc" || dir === "-1") return -1;
    return null;
  }

  function allow(value, allowed) {
    return allowed.indexOf(value) >= 0 ? value : null;
  }

  function readLang() {
    try {
      var data = readPrefs();
      if (data.lang === "en" || data.lang === "az") return data.lang;
      var legacy = localStorage.getItem(LANG_KEY);
      return legacy === "en" || legacy === "az" ? legacy : null;
    } catch (e) {
      return null;
    }
  }

  function writeLang(lang) {
    if (lang !== "en" && lang !== "az") return;
    try {
      var data = readPrefs();
      data.lang = lang;
      writePrefs(data);
      localStorage.setItem(LANG_KEY, lang);
    } catch (e) { /* ignore */ }
  }

  function sectionFrom(src, sortAllowed, groupAllowed) {
    if (!src || typeof src !== "object") return null;
    var out = {};
    var sort = allow(src.sort, sortAllowed);
    var group = allow(src.group, groupAllowed);
    var dir = sanitizeDir(src.dir);
    if (sort) out.sort = sort;
    if (group != null && groupAllowed.indexOf(src.group) >= 0) out.group = src.group;
    if (dir) out.dir = dir;
    return out;
  }

  function readList() {
    try {
      var src = readPrefs().list;
      var out = sectionFrom(src, LIST_SORT, LIST_GROUP) || {};
      if (src && typeof src === "object") {
        var view = allow(src.view, LIST_VIEW);
        var per = allow(src.per == null ? "" : String(src.per), LIST_PER);
        if (view) out.view = view;
        if (per) out.per = per;
      }
      if (!out.sort && !out.view && !out.group && !out.per) {
        out = migrateListSession(out);
      }
      return out;
    } catch (e) {
      return {};
    }
  }

  function migrateListSession(out) {
    try {
      var raw = sessionStorage.getItem("daab-scientists-list-sort");
      if (raw) {
        var parsed = JSON.parse(raw);
        var sort = parsed && allow(parsed.sortCol, LIST_SORT);
        var dir = parsed && sanitizeDir(parsed.sortDir);
        if (sort) out.sort = sort;
        if (dir) out.dir = dir;
      }
      var group = sessionStorage.getItem("daab-scientists-list-group") || "";
      if (LIST_GROUP.indexOf(group) >= 0 && group) out.group = group;
      var view = sessionStorage.getItem("daab-scientists-list-view");
      if (allow(view, LIST_VIEW)) out.view = view;
      if (out.sort || out.view || out.group) writeList(out);
    } catch (e) { /* ignore */ }
    return out;
  }

  function writeList(snapshot) {
    try {
      var data = readPrefs();
      var prev = data.list && typeof data.list === "object" ? data.list : {};
      var next = {
        view: prev.view,
        group: prev.group,
        sort: prev.sort,
        dir: prev.dir,
        per: prev.per
      };
      snapshot = snapshot || {};
      if (allow(snapshot.view, LIST_VIEW)) next.view = snapshot.view;
      if (LIST_GROUP.indexOf(snapshot.group) >= 0) next.group = snapshot.group;
      if (allow(snapshot.sort, LIST_SORT)) next.sort = snapshot.sort;
      if (sanitizeDir(snapshot.dir)) next.dir = sanitizeDir(snapshot.dir);
      if (allow(snapshot.per == null ? "" : String(snapshot.per), LIST_PER)) {
        next.per = String(snapshot.per);
      }
      if (!allow(next.view, LIST_VIEW)) delete next.view;
      if (LIST_GROUP.indexOf(next.group) < 0) delete next.group;
      if (!allow(next.sort, LIST_SORT)) delete next.sort;
      if (!sanitizeDir(next.dir)) delete next.dir;
      else next.dir = sanitizeDir(next.dir);
      if (!allow(next.per == null ? "" : String(next.per), LIST_PER)) delete next.per;
      data.list = next;
      writePrefs(data);
    } catch (e) { /* ignore */ }
  }

  function readProfiles() {
    try {
      var out = sectionFrom(readPrefs().profiles, PROFILE_SORT, PROFILE_GROUP) || {};
      if (!out.sort && !out.group) out = migrateProfileSession(out);
      return out;
    } catch (e) {
      return {};
    }
  }

  function migrateProfileSession(out) {
    try {
      var raw = sessionStorage.getItem("daab-profiles-sort");
      if (raw) {
        var parsed = JSON.parse(raw);
        var sort = parsed && allow(parsed.sortCol, PROFILE_SORT);
        var dir = parsed && sanitizeDir(parsed.sortDir);
        if (sort) out.sort = sort;
        if (dir) out.dir = dir;
      }
      var group = sessionStorage.getItem("daab-profiles-group") || "";
      if (PROFILE_GROUP.indexOf(group) >= 0 && group) out.group = group;
      if (out.sort || out.group) writeProfiles(out);
    } catch (e) { /* ignore */ }
    return out;
  }

  function writeProfiles(snapshot) {
    try {
      var data = readPrefs();
      var prev = data.profiles && typeof data.profiles === "object" ? data.profiles : {};
      var next = { group: prev.group, sort: prev.sort, dir: prev.dir };
      snapshot = snapshot || {};
      if (PROFILE_GROUP.indexOf(snapshot.group) >= 0) next.group = snapshot.group;
      if (allow(snapshot.sort, PROFILE_SORT)) next.sort = snapshot.sort;
      if (sanitizeDir(snapshot.dir)) next.dir = sanitizeDir(snapshot.dir);
      if (PROFILE_GROUP.indexOf(next.group) < 0) delete next.group;
      if (!allow(next.sort, PROFILE_SORT)) delete next.sort;
      if (!sanitizeDir(next.dir)) delete next.dir;
      else next.dir = sanitizeDir(next.dir);
      data.profiles = next;
      writePrefs(data);
    } catch (e) { /* ignore */ }
  }

  function resetPrefs() {
    try {
      localStorage.removeItem(PREFS_KEY);
    } catch (e) { /* ignore */ }
    try {
      localStorage.removeItem(LANG_KEY);
    } catch (e2) { /* ignore */ }
    try {
      var drop = [];
      var i;
      for (i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key && key.indexOf("daab-table-col-width:") === 0) drop.push(key);
      }
      for (i = 0; i < drop.length; i++) localStorage.removeItem(drop[i]);
    } catch (e3) { /* ignore */ }
    try {
      SESSION_PREF_KEYS.forEach(function (key) {
        sessionStorage.removeItem(key);
      });
    } catch (e4) { /* ignore */ }
  }

  function persistLang(lang) {
    writeLang(lang);
  }

  function readPersistedLang() {
    return readLang();
  }

  function initGateway() {
    var params;
    try {
      params = new URLSearchParams(location.search);
    } catch (e) {
      params = new URLSearchParams();
    }
    if (params.get("choose") === "1" || params.get("legacy") === "1") return;
    var requested = params.get("lang");
    if (requested !== "en" && requested !== "az") requested = "";
    if (requested) writeLang(requested);
    var lang = requested || readPersistedLang() || "az";
    try {
      sessionStorage.removeItem("daab-lang-position");
      sessionStorage.removeItem("daab-force-page-top");
      sessionStorage.setItem("daab-home-entry", "1");
    } catch (e2) { /* ignore */ }
    location.replace(assetRoot() + lang + "/index.html" + (location.search || ""));
  }

  global.DAAB_PREFS = {
    VERSION: PREFS_VERSION,
    KEY: PREFS_KEY,
    readLang: readLang,
    writeLang: writeLang,
    readList: readList,
    writeList: writeList,
    readProfiles: readProfiles,
    writeProfiles: writeProfiles,
    reset: resetPrefs
  };

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
