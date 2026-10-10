/**
 * Injects language switcher and optional hreflang tags on DAAB pages.
 */
(function () {
  "use strict";

  function urlParams() {
    return new URLSearchParams(location.search || "");
  }

  function readParam(key) {
    return urlParams().get(key) || "";
  }

  function readListParam(key) {
    var raw = readParam(key);
    if (!raw) return [];
    return raw
      .split(",")
      .map(function (part) {
        return part.trim();
      })
      .filter(Boolean);
  }

  function writeParams(map) {
    var params = urlParams();
    Object.keys(map || {}).forEach(function (key) {
      var val = map[key];
      if (val == null || val === "" || (Array.isArray(val) && !val.length)) {
        params.delete(key);
      } else if (Array.isArray(val)) {
        params.set(key, val.join(","));
      } else {
        params.set(key, String(val));
      }
    });
    var qs = params.toString();
    var next = location.pathname + (qs ? "?" + qs : "") + (location.hash || "");
    var current = location.pathname + location.search + location.hash;
    if (next !== current && window.history && window.history.replaceState) {
      window.history.replaceState(null, "", next);
    }
    if (typeof refreshLangHrefs === "function") refreshLangHrefs();
  }

  window.DAAB_URL_STATE = {
    get: readParam,
    list: readListParam,
    write: writeParams
  };

  function navCompactMediaQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.navCompactMq === "function") {
      return window.DAAB_DESIGN.navCompactMq();
    }
    return window.matchMedia("(max-width: 1180px)");
  }

  var compactNavMq = navCompactMediaQuery();
  var switcherNode = null;
  var loadedRoutes = null;
  var langNavBound = false;

  function getI18n() {
    return window.DAAB_I18N || null;
  }

  function detectLang() {
    var I18N = getI18n();
    if (I18N) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(location.pathname.replace(/\\/g, "/")) ? "en" : "az";
  }

  function fallbackLabels(lang) {
    if (lang === "en") {
      return {
        label: "Language",
        az: "AZ",
        en: "EN",
        azFull: "Azerbaijani",
        enFull: "English",
        switchTo: "Switch to {lang}",
        current: "Current language"
      };
    }
    return {
      label: "Dil seçimi",
      az: "AZ",
      en: "EN",
      azFull: "Azərbaycan dili",
      enFull: "İngilis dili",
      switchTo: "{lang} dilinə keç",
      current: "Hazırkı dil"
    };
  }

  function fallbackAlternateUrl(lang) {
    var path = location.pathname.replace(/\\/g, "/");
    var search = location.search || "";
    var hash = location.hash || "";
    if (lang === "en") {
      if (/\/az\//.test(path)) return path.replace("/az/", "/en/") + search + hash;
      if (/\/az\/[^/]+\.html$/i.test(path)) return path.replace(/\/az\//i, "/en/") + search + hash;
      return "../en/index.html";
    }
    if (/\/en\//.test(path)) return path.replace("/en/", "/az/") + search + hash;
    if (/\/en\/[^/]+\.html$/i.test(path)) return path.replace(/\/en\//i, "/az/") + search + hash;
    return "../az/index.html";
  }

  function flagSvg(code) {
    if (code === "az") {
      return (
        '<svg class="daab-lang-flag" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">' +
        '<rect width="60" height="30" fill="#00b9e4"/>' +
        '<rect y="10" width="60" height="10" fill="#ef3340"/>' +
        '<rect y="20" width="60" height="10" fill="#509e2f"/>' +
        '<circle cx="27" cy="15" r="4" fill="#fff"/>' +
        '<circle cx="28.4" cy="15" r="3.4" fill="#ef3340"/>' +
        '<path d="M33.4 11.5l1 2.2 2.4.1-1.9 1.5.7 2.3-2.2-1.3-2.2 1.3.7-2.3-1.9-1.5 2.4-.1z" fill="#fff"/>' +
        "</svg>"
      );
    }
    return (
      '<svg class="daab-lang-flag" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">' +
      '<defs><clipPath id="daab-uk-clip"><rect width="60" height="30"/></clipPath></defs>' +
      '<g clip-path="url(#daab-uk-clip)">' +
      '<rect width="60" height="30" fill="#012169"/>' +
      '<path d="M0 0L60 30M60 0L0 30" stroke="#fff" stroke-width="6"/>' +
      '<path d="M0 0L60 30M60 0L0 30" stroke="#c8102e" stroke-width="3.6"/>' +
      '<path d="M30 0 V30 M0 15 H60" stroke="#fff" stroke-width="10"/>' +
      '<path d="M30 0 V30 M0 15 H60" stroke="#c8102e" stroke-width="6"/>' +
      "</g></svg>"
    );
  }

  function buildLangLink(code, url, isActive, labels) {
    var a = document.createElement("a");
    a.href = url || "#";
    a.hreflang = code;
    a.lang = code;
    a.className = "daab-lang-link daab-lang-link-" + code;
    a.setAttribute("data-lang", code);

    var fullName = labels[code + "Full"] || labels[code];
    var ariaLabel;
    if (isActive) {
      ariaLabel = (labels.current || "Current language") + ": " + fullName;
      a.setAttribute("aria-current", "true");
    } else {
      var tmpl = labels.switchTo || "Switch to {lang}";
      ariaLabel = tmpl.replace("{lang}", fullName);
    }
    a.setAttribute("aria-label", ariaLabel);
    a.setAttribute("title", fullName);

    a.innerHTML =
      flagSvg(code) +
      '<span class="daab-lang-code" aria-hidden="true">' + labels[code] + "</span>";
    return a;
  }

  function resolveLabels(ui, lang) {
    if (ui && ui.langSwitch) {
      return ui.langSwitch[lang] || ui.langSwitch.az || fallbackLabels(lang);
    }
    return fallbackLabels(lang);
  }

  function resolveUrls(routes, lang) {
    var I18N = getI18n();
    var search = location.search || "";
    var azUrl = fallbackAlternateUrl("az");
    var enUrl = fallbackAlternateUrl("en");
    if (I18N && routes) {
      azUrl = I18N.getAlternateUrl("az", routes) || azUrl;
      enUrl = I18N.getAlternateUrl("en", routes) || enUrl;
    }
    if (search && azUrl.indexOf("?") < 0) azUrl += search;
    if (search && enUrl.indexOf("?") < 0) enUrl += search;
    /* Scroll/hash for the alternate page is applied on click via decorateAlternateUrl. */
    return { az: azUrl, en: enUrl };
  }

  function stripHash(url) {
    var hashIdx = (url || "").indexOf("#");
    return hashIdx >= 0 ? url.slice(0, hashIdx) : url || "";
  }

  function withParam(url, key, value) {
    var hash = "";
    var base = url || "";
    var hashIdx = base.indexOf("#");
    if (hashIdx >= 0) {
      hash = base.slice(hashIdx);
      base = base.slice(0, hashIdx);
    }
    var qIdx = base.indexOf("?");
    var path = qIdx >= 0 ? base.slice(0, qIdx) : base;
    var params = new URLSearchParams(qIdx >= 0 ? base.slice(qIdx + 1) : "");
    params.set(key, value);
    var qs = params.toString();
    return path + (qs ? "?" + qs : "") + hash;
  }

  /**
   * Equivalent page in `lang`, plus whether routes.json knows the pair.
   * Query string is copied; the section hash is added at navigation time.
   */
  function applyLiveQuery(url) {
    var hash = "";
    var base = url || "";
    var hashIdx = base.indexOf("#");
    if (hashIdx >= 0) {
      hash = base.slice(hashIdx);
      base = base.slice(0, hashIdx);
    }
    var qIdx = base.indexOf("?");
    if (qIdx >= 0) base = base.slice(0, qIdx);
    return base + (location.search || "") + hash;
  }

  function alternateBase(lang) {
    var I18N = getI18n();
    var url = stripHash(fallbackAlternateUrl(lang));
    var known = false;
    if (I18N && loadedRoutes) {
      var page = I18N.findPage(loadedRoutes);
      if (page) {
        var routed = I18N.getAlternateUrl(lang, loadedRoutes);
        if (routed) {
          url = routed;
          known = true;
        }
      }
    }
    return { url: applyLiveQuery(stripHash(url)), known: known };
  }

  function liveLangUrl(lang) {
    var alt = alternateBase(lang);
    var Pos = window.DAAB_LANG_POSITION;
    var anchor = "";
    if (Pos && typeof Pos.currentSwitchAnchor === "function") {
      anchor = Pos.currentSwitchAnchor() || "";
    }
    if (anchor && Pos && typeof Pos.appendHash === "function") {
      return { url: Pos.appendHash(alt.url, anchor), anchor: anchor, known: alt.known };
    }
    return { url: alt.url, anchor: anchor, known: alt.known };
  }

  function refreshLangHrefs() {
    var links = document.querySelectorAll("a.daab-lang-link[data-lang]");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      if (
        link.classList.contains("daab-lang-link--disabled") ||
        link.getAttribute("aria-disabled") === "true"
      ) {
        continue;
      }
      var code = link.getAttribute("data-lang");
      if (code !== "az" && code !== "en") continue;
      link.href = liveLangUrl(code).url;
    }
  }

  function parentCandidates(lang) {
    var path = location.pathname.replace(/\\/g, "/");
    var swapped = path.replace(/\/(az|en)(?=\/|$)/i, "/" + lang);
    var parts = swapped.split("/").filter(Boolean);
    if (parts.length && /\.html?$/i.test(parts[parts.length - 1])) parts.pop();
    if (parts.length && parts[parts.length - 1].toLowerCase() === "index.html") parts.pop();
    var urls = [];
    while (parts.length > 1) {
      parts.pop();
      urls.push("/" + parts.join("/") + "/index.html");
    }
    urls.push("/" + lang + "/index.html");
    return urls;
  }

  function urlExists(url) {
    return fetch(url, { method: "HEAD", cache: "no-store" })
      .then(function (res) {
        return !!(res && res.ok);
      })
      .catch(function () {
        return true;
      });
  }

  function goReplace(url, anchor) {
    var Pos = window.DAAB_LANG_POSITION;
    if (window.history && "scrollRestoration" in window.history) {
      window.history.scrollRestoration = "manual";
    }
    if (Pos && typeof Pos.saveIntent === "function") {
      Pos.saveIntent(null, anchor || null);
    }
    location.replace(url);
  }

  /**
   * Shared language switch for the nav strip, footer, and mobile menu.
   * Replaces the current history entry so toggling AZ ⇄ EN does not stack.
   */
  function navigateLangSwitch(lang) {
    if (lang !== "az" && lang !== "en") return;
    var I18N = getI18n();
    if (I18N) I18N.persistLang(lang);
    document.dispatchEvent(
      new CustomEvent("daab-before-lang-switch", { detail: { lang: lang } })
    );
    var alt = liveLangUrl(lang);
    if (alt.known) {
      goReplace(alt.url, alt.anchor);
      return;
    }
    urlExists(alt.url).then(function (ok) {
      if (ok) {
        goReplace(alt.url, alt.anchor);
        return;
      }
      var parents = parentCandidates(lang);
      var i = 0;
      function next() {
        if (i >= parents.length) {
          goReplace(withParam(parents[parents.length - 1], "notice", "missing"));
          return;
        }
        var candidate = parents[i];
        i += 1;
        urlExists(candidate).then(function (exists) {
          if (exists) goReplace(withParam(candidate, "notice", "missing"));
          else next();
        });
      }
      next();
    });
  }

  function bindLangLinkClicks() {
    if (langNavBound) return;
    langNavBound = true;
    document.addEventListener(
      "pointerdown",
      function (ev) {
        var link = ev.target && ev.target.closest && ev.target.closest("a.daab-lang-link[data-lang]");
        if (!link) return;
        refreshLangHrefs();
      },
      true
    );
    document.addEventListener(
      "click",
      function (ev) {
        var link = ev.target && ev.target.closest && ev.target.closest("a.daab-lang-link[data-lang]");
        if (!link) return;
        if (
          link.classList.contains("daab-lang-link--disabled") ||
          link.getAttribute("aria-disabled") === "true"
        ) {
          ev.preventDefault();
          return;
        }
        var lang = link.getAttribute("data-lang");
        if (lang !== "az" && lang !== "en") return;
        var built = liveLangUrl(lang);
        link.href = built.url;
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button !== 0) {
          var I18N = getI18n();
          if (I18N) I18N.persistLang(lang);
          return;
        }
        ev.preventDefault();
        navigateLangSwitch(lang);
      },
      true
    );
  }

  function mirrorLangSwitch(node) {
    if (!node) return;
    var footer = document.querySelector(".footer-bottom");
    if (footer && !footer.querySelector(".daab-lang-switch")) {
      var footerClone = node.cloneNode(true);
      footerClone.classList.add("daab-lang-switch--footer");
      footer.insertBefore(footerClone, footer.firstChild);
    }
    var menu = document.getElementById("primaryNavMenu");
    if (menu && !menu.querySelector(".daab-lang-switch")) {
      var menuClone = node.cloneNode(true);
      menuClone.classList.add("daab-lang-switch--menu");
      var divider = menu.querySelector(".nav-divider");
      if (divider && divider.nextSibling) menu.insertBefore(menuClone, divider.nextSibling);
      else if (divider) menu.appendChild(menuClone);
      else menu.insertBefore(menuClone, menu.firstChild);
    }
    if (menu && menu.getAttribute("data-daab-lang-mirror") !== "1") {
      menu.setAttribute("data-daab-lang-mirror", "1");
      var obs = new MutationObserver(function () {
        if (!switcherNode || menu.querySelector(".daab-lang-switch")) return;
        var again = switcherNode.cloneNode(true);
        again.classList.add("daab-lang-switch--menu");
        var div = menu.querySelector(".nav-divider");
        if (div && div.nextSibling) menu.insertBefore(again, div.nextSibling);
        else menu.appendChild(again);
      });
      obs.observe(menu, { childList: true });
    }
  }

  function showMissingLangNotice() {
    if (readParam("notice") !== "missing") return;
    if (document.querySelector(".daab-lang-notice")) return;
    var lang = detectLang();
    var bar = document.createElement("div");
    bar.className = "daab-lang-notice";
    bar.setAttribute("role", "status");
    bar.textContent =
      lang === "en"
        ? "This page has no English version. Showing the closest related page."
        : "Bu səhifənin azərbaycanca versiyası yoxdur. Ən yaxın səhifə göstərilir.";
    var main = document.querySelector("main") || document.body;
    if (main.firstChild) main.insertBefore(bar, main.firstChild);
    else main.appendChild(bar);
    writeParams({ notice: "" });
  }

  function buildSwitcher(ui, routes, lang) {
    var labels = resolveLabels(ui, lang);
    var urls = resolveUrls(routes, lang);
    var pairMode = (document.documentElement.getAttribute("data-daab-lang-pair") || "").trim();

    var wrap = document.createElement("div");
    wrap.className = "daab-lang-switch";
    wrap.setAttribute("role", "navigation");
    wrap.setAttribute("aria-label", labels.label);

    var linkAz = buildLangLink("az", urls.az, lang === "az", labels);
    var linkEn = buildLangLink("en", urls.en, lang === "en", labels);

    if (pairMode === "az-only") {
      linkEn.setAttribute("aria-disabled", "true");
      linkEn.classList.add("daab-lang-link--disabled");
      linkEn.removeAttribute("href");
      linkEn.title = lang === "az" ? "İngilis versiyası hazırlanır" : "English version coming soon";
      linkEn.setAttribute(
        "aria-label",
        lang === "az" ? "İngilis versiyası hazırlanır" : "English version coming soon"
      );
    } else if (pairMode === "en-pending" && lang === "en") {
      linkEn.setAttribute("aria-disabled", "true");
      linkEn.classList.add("daab-lang-link--disabled");
      linkEn.removeAttribute("href");
      linkEn.title = "English version coming soon";
    }

    wrap.appendChild(linkAz);
    wrap.appendChild(linkEn);
    return wrap;
  }

  function ensureNavActions(inner) {
    if (!inner) return null;
    var actions = inner.querySelector(".nav-actions");
    if (!actions) {
      actions = document.createElement("div");
      actions.className = "nav-actions";
      actions.setAttribute("role", "group");
      inner.appendChild(actions);
    }
    return actions;
  }

  function migrateNavTools(inner) {
    var actions = ensureNavActions(inner);
    if (!actions) return;
    var search = document.getElementById("nav-search-btn");
    if (search && search.parentNode !== actions) {
      actions.insertBefore(search, actions.firstChild);
    }
    inner.querySelectorAll(":scope > .daab-lang-switch").forEach(function (lang) {
      if (lang.parentNode !== actions) {
        actions.appendChild(lang);
      }
    });
  }

  function placeSwitcher(node) {
    if (!node) return;
    var inner = document.querySelector(".nav-inner");
    if (!inner) return;
    switcherNode = node;
    var existing = inner.querySelector(".daab-lang-switch");
    if (existing && existing !== node) existing.remove();
    var actions = ensureNavActions(inner);
    if (actions) {
      actions.appendChild(node);
      migrateNavTools(inner);
    } else {
      inner.appendChild(node);
    }
  }

  function mountSwitcher(ui, routes, lang) {
    bindLangLinkClicks();
    var node;
    try {
      node = buildSwitcher(ui, routes, lang);
    } catch (err) {
      console.warn("[daab-shell] Switcher build failed:", err);
      node = buildSwitcher(null, null, lang);
    }
    placeSwitcher(node);
    mirrorLangSwitch(node);
  }

  function repositionSwitcher() {
    if (switcherNode) placeSwitcher(switcherNode);
  }

  function assetRootPrefix() {
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root == null || root === "") return "";
    return root.endsWith("/") ? root : root + "/";
  }

  function isLegalDocHref(href) {
    return /(?:^|\/)(legal-notice|privacy|cookies|terms)\.html(?:$|[?#])/i.test(
      href || ""
    );
  }

  /** Turn /az/... and /en/... into asset-root-relative hrefs (file:// + nested hosts). */
  function rewriteSiteRootHrefs(scope) {
    var prefix = assetRootPrefix();
    var root = scope || document;
    var nodes = root.querySelectorAll(
      'a[href*="legal-notice.html"], a[href*="privacy.html"], a[href*="cookies.html"], a[href*="terms.html"]'
    );
    for (var i = 0; i < nodes.length; i++) {
      var a = nodes[i];
      var href = a.getAttribute("href") || "";
      if (!href || href.charAt(0) === "#" || href.indexOf("//") === 0) continue;
      if (!isLegalDocHref(href)) continue;

      /* Always land on the hero page title */
      if (href.indexOf("#page-title") === -1) {
        href = href.split("#")[0] + "#page-title";
      }

      if (href.charAt(0) === "/" && prefix) {
        href = prefix + href.slice(1);
      }
      a.setAttribute("href", href);
    }
  }

  function stickyOffsetForTitle() {
    if (window.DAAB_LANG_POSITION && typeof window.DAAB_LANG_POSITION.navOffset === "function") {
      return window.DAAB_LANG_POSITION.navOffset();
    }
    var root = document.documentElement;
    var style = window.getComputedStyle(root);
    var h = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
    if (!isFinite(h) || h <= 0) {
      h = parseFloat(style.getPropertyValue("--daab-nav-height"));
      if (!isFinite(h) || h <= 0) {
        var nav = document.querySelector(".nav-strip");
        h = nav ? nav.getBoundingClientRect().height : 86;
      }
      var crumbs = document.getElementById("daab-breadcrumbs");
      if (crumbs) h += crumbs.getBoundingClientRect().height;
    }
    return Math.ceil(h) + 12;
  }

  /** Instant jump so the page title sits just under sticky chrome */
  function jumpPageTopInstant() {
    var html = document.documentElement;
    var body = document.body;
    html.style.setProperty("scroll-behavior", "auto", "important");
    if (body) body.style.setProperty("scroll-behavior", "auto", "important");
    var title =
      document.getElementById("page-title") ||
      document.querySelector(".hero h1") ||
      document.querySelector("h1");
    if (!title) {
      html.scrollTop = 0;
      if (body) body.scrollTop = 0;
      window.scrollTo(0, 0);
      return;
    }
    var y =
      title.getBoundingClientRect().top +
      (window.pageYOffset || html.scrollTop || 0) -
      stickyOffsetForTitle();
    y = Math.max(0, Math.round(y));
    html.scrollTop = y;
    if (body) body.scrollTop = y;
    window.scrollTo(0, y);
  }

  function prepareLegalNavigation() {
    try {
      sessionStorage.removeItem("daab-lang-position");
      sessionStorage.setItem("daab-force-page-top", String(Date.now()));
    } catch (err) {
      /* private mode */
    }
    document.documentElement.style.setProperty("scroll-behavior", "auto", "important");
  }

  function bindFooterLegalTopJump() {
    if (document.documentElement.getAttribute("data-daab-footer-legal-top") === "1") {
      return;
    }
    document.documentElement.setAttribute("data-daab-footer-legal-top", "1");
    rewriteSiteRootHrefs(document);
    document.addEventListener(
      "click",
      function (ev) {
        var a =
          ev.target &&
          ev.target.closest &&
          ev.target.closest(
            ".footer-legal-links a[href], .daab-cookie-banner a[href]"
          );
        if (!a) return;
        if (ev.defaultPrevented) return;
        if (ev.button != null && ev.button !== 0) return;
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;

        var hrefAttr = a.getAttribute("href") || "";
        if (!hrefAttr || hrefAttr.charAt(0) === "#") return;

        /* Resolved absolute URL from the browser — reliable across depths */
        var abs = a.href || "";
        if (!/legal-notice|privacy|cookies|terms/i.test(abs)) return;

        prepareLegalNavigation();
        ev.preventDefault();

        var url;
        try {
          url = new URL(abs);
        } catch (errUrl) {
          location.assign(hrefAttr);
          return;
        }

        var here = location.pathname.replace(/\/+$/, "") || "/";
        var dest = url.pathname.replace(/\/+$/, "") || "/";
        var titleHash = "#page-title";
        if (here === dest && url.search === location.search) {
          if (window.history && window.history.replaceState) {
            window.history.replaceState(
              null,
              "",
              location.pathname + location.search + titleHash
            );
          } else {
            location.hash = "page-title";
          }
          jumpPageTopInstant();
          return;
        }

        /* Open legal page at the hero page title */
        location.assign(url.origin + url.pathname + url.search + titleHash);
      },
      true
    );
  }

  function init() {
    var I18N = getI18n();
    if (!I18N) return;

    var lang = detectLang();
    document.documentElement.lang = lang;

    if (document.body && document.body.classList.contains("daab-gateway")) {
      return;
    }

    bindFooterLegalTopJump();

    showMissingLangNotice();

    Promise.all([I18N.loadRoutes(), I18N.loadUi()])
      .then(function (results) {
        var routes = results[0];
        var ui = results[1];
        loadedRoutes = routes;
        var page = I18N.findPage(routes);
        if (page) I18N.injectHreflang(page, routes);
        mountSwitcher(ui, routes, lang);
      })
      .catch(function (err) {
        console.warn("[daab-shell] i18n load failed; using fallback switcher:", err);
        mountSwitcher(null, null, lang);
      });
  }

  function boot(attempt) {
    if (!getI18n()) {
      if (attempt < 40) {
        setTimeout(function () {
          boot(attempt + 1);
        }, 25);
        return;
      }
      if (!(document.body && document.body.classList.contains("daab-gateway"))) {
        mountSwitcher(null, null, detectLang());
      }
      return;
    }
    init();
  }

  /* Bind early so footer legal clicks work even if i18n boot is delayed */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bindFooterLegalTopJump();
      boot(0);
    });
  } else {
    bindFooterLegalTopJump();
    boot(0);
  }

  function onCompactNavChange() {
    repositionSwitcher();
    if (window.DAAB_NAV && window.DAAB_NAV.syncNavHeight) {
      window.DAAB_NAV.syncNavHeight();
    }
    if (!compactNavMq.matches && window.DAAB_NAV && window.DAAB_NAV.closeMobileMenu) {
      window.DAAB_NAV.closeMobileMenu();
    }
  }

  if (typeof compactNavMq.addEventListener === "function") {
    compactNavMq.addEventListener("change", onCompactNavChange);
  } else if (typeof compactNavMq.addListener === "function") {
    compactNavMq.addListener(onCompactNavChange);
  }

  document.addEventListener("daab-primary-nav-ready", function () {
    repositionSwitcher();
    if (switcherNode) mirrorLangSwitch(switcherNode);
  });
  document.addEventListener("daab-nav-tools-mounted", repositionSwitcher);

  window.DAAB_SHELL = {
    ensureNavActions: ensureNavActions,
    repositionSwitcher: repositionSwitcher,
  };
  window.DAAB_LANG_SWITCH = {
    navigate: navigateLangSwitch
  };
})();

