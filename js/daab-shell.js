/**
 * Injects language switcher and optional hreflang tags on DAAB pages.
 */
(function () {
  "use strict";

  var I18N = window.DAAB_I18N;
  if (!I18N) return;

  function buildSwitcher(ui, routes, lang) {
    var labels = ui.langSwitch[lang] || ui.langSwitch.az;
    var page = I18N.findPage(routes);
    var azUrl = I18N.getAlternateUrl("az", routes);
    var enUrl = I18N.getAlternateUrl("en", routes);

    var wrap = document.createElement("div");
    wrap.className = "daab-lang-switch";
    wrap.setAttribute("role", "navigation");
    wrap.setAttribute("aria-label", labels.label);

    var linkAz = document.createElement("a");
    linkAz.href = azUrl;
    linkAz.hreflang = "az";
    linkAz.lang = "az";
    linkAz.textContent = labels.az;
    if (lang === "az") linkAz.setAttribute("aria-current", "true");

    var sep = document.createElement("span");
    sep.className = "daab-lang-sep";
    sep.setAttribute("aria-hidden", "true");

    var linkEn = document.createElement("a");
    linkEn.href = enUrl;
    linkEn.hreflang = "en";
    linkEn.lang = "en";
    linkEn.textContent = labels.en;
    if (lang === "en") linkEn.setAttribute("aria-current", "true");

    linkAz.addEventListener("click", function () {
      I18N.persistLang("az");
    });
    linkEn.addEventListener("click", function () {
      I18N.persistLang("en");
    });

    wrap.appendChild(linkAz);
    wrap.appendChild(sep);
    wrap.appendChild(linkEn);
    return wrap;
  }

  function placeSwitcher(node) {
    var inner = document.querySelector(".nav-inner");
    if (!inner) return;
    var existing = inner.querySelector(".daab-lang-switch");
    if (existing) existing.remove();
    var menu = document.getElementById("primaryNavMenu");
    if (menu && menu.parentNode === inner) {
      inner.insertBefore(node, menu);
    } else {
      inner.appendChild(node);
    }
  }

  function maybeLocaleHint(lang) {
    if (/\/(az|en)\//.test(location.pathname)) return;
    var hint = document.getElementById("daab-locale-hint");
    if (!hint) return;
    var az = hint.querySelector("[data-locale-az]");
    var en = hint.querySelector("[data-locale-en]");
    if (lang === "az" && az) az.setAttribute("aria-current", "true");
    if (lang === "en" && en) en.setAttribute("aria-current", "true");
  }

  function init() {
    var lang = I18N.detectLang();
    document.documentElement.lang = lang;
    maybeLocaleHint(lang);

    if (document.body && document.body.classList.contains("daab-gateway")) {
      return;
    }

    Promise.all([I18N.loadRoutes(), I18N.loadUi()])
      .then(function (results) {
        var routes = results[0];
        var ui = results[1];
        var page = I18N.findPage(routes);
        if (page) I18N.injectHreflang(page, routes);
        placeSwitcher(buildSwitcher(ui, routes, lang));
      })
      .catch(function () {
        /* routes optional on offline preview */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
