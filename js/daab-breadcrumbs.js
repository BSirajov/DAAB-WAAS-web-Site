/**
 * Injects breadcrumb trail from routes + nav metadata.
 * Falls back to embedded route/label data when i18n JSON cannot be fetched.
 */
(function () {
  "use strict";

  var breadcrumbsInserted = false;
  var mountInFlight = false;

  var PAGE_LABEL_KEYS = {
    home: "home",
    foundation: "foundation",
    mission: "mission",
    activities: "activities",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    charter: "charter",
    membership: "membership"
  };

  var GROUP_LABEL_KEYS = {
    about: "about",
    scientists: "scientists"
  };

  var FALLBACK_ROUTES = {
    pages: [
      { id: "home", az: "az/index.html", en: "en/index.html", navParent: null },
      { id: "foundation", az: "az/foundation.html", en: "en/foundation.html", navParent: "about" },
      { id: "mission", az: "az/mission.html", en: "en/mission.html", navParent: "about" },
      { id: "activities", az: "az/activities.html", en: "en/activities.html", navParent: null },
      {
        id: "scientists-list",
        az: "az/scientists/list.html",
        en: "en/scientists/list.html",
        navParent: "scientists"
      },
      {
        id: "scientists-profiles",
        az: "az/scientists/profiles.html",
        en: "en/scientists/profiles.html",
        navParent: "scientists"
      },
      {
        id: "executive-board",
        az: "az/executive-board.html",
        en: "en/executive-board.html",
        navParent: "about"
      },
      { id: "charter", az: "az/charter.html", en: "en/charter.html", navParent: "about" },
      { id: "membership", az: "az/membership.html", en: "en/membership.html", navParent: null }
    ]
  };

  var FALLBACK_UI = {
    breadcrumbs: {
      az: {
        aria: "Səhifə yolu",
        home: "Ana səhifə",
        about: "Haqqımızda",
        scientists: "Alimlərimiz"
      },
      en: {
        aria: "Breadcrumb",
        home: "Home",
        about: "About",
        scientists: "Scientists"
      }
    },
    nav: {
      az: {
        home: "Ana səhifə",
        foundation: "Birliyin təsisi",
        mission: "Missiya və dəyərlər",
        activities: "Fəaliyyətimiz",
        scientistsList: "Siyahı",
        scientistsProfiles: "Profillər",
        executiveBoard: "İdarə heyəti",
        charter: "Nizamnamə",
        membership: "Üzvlük"
      },
      en: {
        home: "Home",
        foundation: "Foundation",
        mission: "Mission & values",
        activities: "Activities",
        scientistsList: "Directory",
        scientistsProfiles: "Profiles",
        executiveBoard: "Executive board",
        charter: "Charter",
        membership: "Membership"
      }
    }
  };

  var FALLBACK_NAV = {
    sections: {
      about: { landingId: "mission" },
      scientists: { landingId: "scientists-list" }
    }
  };

  function getI18n() {
    return window.DAAB_I18N || null;
  }

  function pageById(routes, id) {
    var pages = routes.pages || [];
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].id === id) return pages[i];
    }
    return null;
  }

  function pageHref(I18N, page, lang) {
    if (I18N && typeof I18N.pageHref === "function") {
      return I18N.pageHref(page, lang);
    }
    if (!page) return lang === "en" ? "index.html" : "index.html";
    var target = lang === "en" ? page.en : page.az;
    var prefix = lang + "/";
    if (target.toLowerCase().indexOf(prefix) === 0) {
      target = target.slice(prefix.length);
    }
    return target;
  }

  function t(ui, lang, section, key) {
    var block = ui[section] && ui[section][lang];
    return (block && block[key]) || key;
  }

  function pageTitle(ui, lang, pageId) {
    var key = PAGE_LABEL_KEYS[pageId];
    if (!key) return pageId;
    var navBlock = ui.nav && ui.nav[lang];
    return (navBlock && navBlock[key]) || pageId;
  }

  function sectionLanding(navDef, groupId) {
    var sec = navDef.sections && navDef.sections[groupId];
    return sec ? sec.landingId : null;
  }

  function findMountPoint() {
    var nav = document.querySelector(".nav-strip");
    if (nav && nav.parentNode) return { parent: nav.parentNode, before: nav.nextSibling };
    var main = document.getElementById("content") || document.querySelector("main");
    if (main) return { parent: main.parentNode, before: main };
    return null;
  }

  function removeBreadcrumbs() {
    document.querySelectorAll("#daab-breadcrumbs, nav.daab-breadcrumbs").forEach(function (el) {
      el.remove();
    });
  }

  function findCurrentPage(I18N, routes) {
    if (I18N && typeof I18N.findPage === "function") {
      var found = I18N.findPage(routes);
      if (found) return found;
    }

    var pathKey = I18N && typeof I18N.currentPathKey === "function" ? I18N.currentPathKey() : "";
    if (!pathKey) return null;

    var pages = routes.pages || [];
    for (var i = 0; i < pages.length; i++) {
      var p = pages[i];
      if ((p.az && p.az.toLowerCase() === pathKey) || (p.en && p.en.toLowerCase() === pathKey)) {
        return p;
      }
      if (p.legacy && p.legacy.toLowerCase() === pathKey) return p;
    }
    return null;
  }

  function buildTrail(routes, navDef, ui, lang, page, I18N) {
    if (!page || page.id === "home") return null;

    var crumbs = [];
    var home = pageById(routes, "home");
    if (home) {
      crumbs.push({
        href: pageHref(I18N, home, lang),
        text: t(ui, lang, "breadcrumbs", "home")
      });
    }

    if (page.navParent) {
      var groupKey = GROUP_LABEL_KEYS[page.navParent];
      var landingId = sectionLanding(navDef, page.navParent);
      var landing = landingId ? pageById(routes, landingId) : null;
      crumbs.push({
        href: landing ? pageHref(I18N, landing, lang) : null,
        text: groupKey ? t(ui, lang, "breadcrumbs", groupKey) : page.navParent
      });
    }

    crumbs.push({
      href: null,
      text: pageTitle(ui, lang, page.id),
      current: true
    });

    return crumbs;
  }

  function render(crumbs, ui, lang) {
    var nav = document.createElement("nav");
    nav.className = "daab-breadcrumbs";
    nav.id = "daab-breadcrumbs";
    nav.setAttribute("aria-label", t(ui, lang, "breadcrumbs", "aria"));

    var ol = document.createElement("ol");
    ol.className = "daab-breadcrumbs-list";

    crumbs.forEach(function (crumb, index) {
      var li = document.createElement("li");
      li.className = "daab-breadcrumbs-item";

      if (index > 0) {
        var sep = document.createElement("span");
        sep.className = "daab-breadcrumbs-sep";
        sep.setAttribute("aria-hidden", "true");
        sep.textContent = "›";
        li.appendChild(sep);
      }

      if (crumb.current || !crumb.href) {
        var span = document.createElement("span");
        span.className = "daab-breadcrumbs-current";
        span.setAttribute("aria-current", "page");
        span.textContent = crumb.text;
        li.appendChild(span);
      } else {
        var a = document.createElement("a");
        a.href = crumb.href;
        a.textContent = crumb.text;
        li.appendChild(a);
      }

      ol.appendChild(li);
    });

    nav.appendChild(ol);
    return nav;
  }

  function loadData(I18N) {
    if (location.protocol === "file:") {
      return Promise.resolve([FALLBACK_ROUTES, FALLBACK_UI, FALLBACK_NAV]);
    }
    return Promise.all([I18N.loadRoutes(), I18N.loadUi(), I18N.loadNav()]).catch(function () {
      return [FALLBACK_ROUTES, FALLBACK_UI, FALLBACK_NAV];
    });
  }

  function mount() {
    if (breadcrumbsInserted || mountInFlight) return;
    if (document.body && document.body.classList.contains("daab-gateway")) return;

    var I18N = getI18n();
    if (!I18N) return;

    mountInFlight = true;
    var lang = I18N.detectLang();

    loadData(I18N)
      .then(function (results) {
        if (breadcrumbsInserted) return;

        var routes = results[0] || FALLBACK_ROUTES;
        var ui = results[1] || FALLBACK_UI;
        var navDef = results[2] || FALLBACK_NAV;
        var page = findCurrentPage(I18N, routes);
        var crumbs = buildTrail(routes, navDef, ui, lang, page, I18N);
        if (!crumbs || crumbs.length < 2) return;

        var mountPoint = findMountPoint();
        if (!mountPoint) return;

        removeBreadcrumbs();
        var el = render(crumbs, ui, lang);
        mountPoint.parent.insertBefore(el, mountPoint.before);
        breadcrumbsInserted = true;
      })
      .catch(function (err) {
        console.warn("[daab-breadcrumbs] Mount failed:", err);
      })
      .finally(function () {
        mountInFlight = false;
      });
  }

  function boot(attempt) {
    if (breadcrumbsInserted) return;
    if (getI18n()) {
      mount();
      return;
    }
    if (attempt < 40) {
      setTimeout(function () {
        boot(attempt + 1);
      }, 25);
    }
  }

  document.addEventListener("daab-primary-nav-ready", function () {
    boot(0);
  });

  window.addEventListener(
    "load",
    function () {
      boot(0);
      setTimeout(function () {
        if (!breadcrumbsInserted) boot(0);
      }, 200);
      setTimeout(function () {
        if (!breadcrumbsInserted) boot(0);
      }, 800);
    },
    { once: true }
  );

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(0);
    });
  } else {
    boot(0);
  }
})();
