/**
 * Injects language switcher and optional hreflang tags on DAAB pages.
 */
(function () {
  "use strict";

  function navCompactMediaQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.navCompactMq === "function") {
      return window.DAAB_DESIGN.navCompactMq();
    }
    return window.matchMedia("(max-width: 1180px)");
  }

  var compactNavMq = navCompactMediaQuery();
  var switcherNode = null;

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

  function navigateLangSwitch(url, lang) {
    var I18N = getI18n();
    var Pos = window.DAAB_LANG_POSITION;
    if (I18N) I18N.persistLang(lang);
    var target = url;
    if (Pos) target = Pos.decorateAlternateUrl(url, lang);
    location.assign(target);
  }

  function buildSwitcher(ui, routes, lang) {
    var labels = resolveLabels(ui, lang);
    var urls = resolveUrls(routes, lang);
    var I18N = getI18n();
    var Pos = window.DAAB_LANG_POSITION;
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

    if (I18N) {
      linkAz.addEventListener("click", function (ev) {
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button !== 0) {
          I18N.persistLang("az");
          if (Pos) linkAz.href = Pos.decorateAlternateUrl(urls.az, "az");
          return;
        }
        ev.preventDefault();
        navigateLangSwitch(urls.az, "az");
      });
      if (!(pairMode === "az-only")) {
        linkEn.addEventListener("click", function (ev) {
          if (linkEn.classList.contains("daab-lang-link--disabled")) {
            ev.preventDefault();
            return;
          }
          if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button !== 0) {
            I18N.persistLang("en");
            if (Pos) linkEn.href = Pos.decorateAlternateUrl(urls.en, "en");
            return;
          }
          ev.preventDefault();
          navigateLangSwitch(urls.en, "en");
        });
      } else {
        linkEn.addEventListener("click", function (ev) {
          ev.preventDefault();
        });
      }
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
    try {
      placeSwitcher(buildSwitcher(ui, routes, lang));
    } catch (err) {
      console.warn("[daab-shell] Switcher build failed:", err);
      placeSwitcher(buildSwitcher(null, null, lang));
    }
  }

  function repositionSwitcher() {
    if (switcherNode) placeSwitcher(switcherNode);
  }

  function init() {
    var I18N = getI18n();
    if (!I18N) return;

    var lang = detectLang();
    document.documentElement.lang = lang;

    if (document.body && document.body.classList.contains("daab-gateway")) {
      return;
    }

    Promise.all([I18N.loadRoutes(), I18N.loadUi()])
      .then(function (results) {
        var routes = results[0];
        var ui = results[1];
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(0);
    });
  } else {
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

  document.addEventListener("daab-primary-nav-ready", repositionSwitcher);
  document.addEventListener("daab-nav-tools-mounted", repositionSwitcher);

  window.DAAB_SHELL = {
    ensureNavActions: ensureNavActions,
    repositionSwitcher: repositionSwitcher,
  };
})();

