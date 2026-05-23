/**
 * "In this section" sub-navigation for grouped pages (About).
 * Falls back to embedded route/label data when i18n JSON cannot be fetched.
 */
(function () {
  "use strict";

  var sectionNavInserted = false;
  var mountInFlight = false;

  var PAGE_LABEL_KEYS = {
    foundation: "foundation",
    mission: "mission",
    "executive-board": "executiveBoard",
    charter: "charter",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles"
  };

  var FALLBACK_ROUTES = {
    pages: [
      { id: "home", az: "az/index.html", en: "en/index.html", navGroup: null },
      {
        id: "foundation",
        az: "az/foundation.html",
        en: "en/foundation.html",
        navGroup: "about",
        navParent: "about"
      },
      {
        id: "mission",
        az: "az/mission.html",
        en: "en/mission.html",
        navGroup: "about",
        navParent: "about"
      },
      {
        id: "activities",
        az: "az/activities.html",
        en: "en/activities.html",
        navGroup: null
      },
      {
        id: "scientists-list",
        az: "az/scientists/list.html",
        en: "en/scientists/list.html",
        navGroup: "scientists",
        navParent: "scientists"
      },
      {
        id: "scientists-profiles",
        az: "az/scientists/profiles.html",
        en: "en/scientists/profiles.html",
        navGroup: "scientists",
        navParent: "scientists"
      },
      {
        id: "executive-board",
        az: "az/executive-board.html",
        en: "en/executive-board.html",
        navGroup: "about",
        navParent: "about"
      },
      {
        id: "charter",
        az: "az/charter.html",
        en: "en/charter.html",
        navGroup: "about",
        navParent: "about"
      },
      { id: "membership", az: "az/membership.html", en: "en/membership.html", navGroup: null }
    ]
  };

  var FALLBACK_UI = {
    sectionNav: {
      az: {
        aria: "Bu bölmədə",
        aboutTitle: "Haqqımızda",
        scientistsTitle: "Alimlərimiz"
      },
      en: {
        aria: "In this section",
        aboutTitle: "About",
        scientistsTitle: "Scientists"
      }
    },
    nav: {
      az: {
        foundation: "Birliyin təsisi",
        mission: "Missiya və dəyərlər",
        executiveBoard: "İdarə heyəti",
        charter: "Nizamnamə",
        scientistsList: "Siyahı",
        scientistsProfiles: "Profillər"
      },
      en: {
        foundation: "Foundation",
        mission: "Mission & values",
        executiveBoard: "Executive board",
        charter: "Charter",
        scientistsList: "Directory",
        scientistsProfiles: "Profiles"
      }
    }
  };

  var FALLBACK_NAV = {
    sections: {
      about: {
        landingId: "mission",
        pages: ["foundation", "mission", "executive-board", "charter"]
      },
      scientists: {
        landingId: "scientists-list",
        pages: ["scientists-list", "scientists-profiles"]
      }
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
    if (!page) return "index.html";
    var target = lang === "en" ? page.en : page.az;
    var prefix = lang + "/";
    if (target.toLowerCase().indexOf(prefix) === 0) {
      target = target.slice(prefix.length);
    }
    return target;
  }

  function findCurrentPage(I18N, routes) {
    if (I18N && typeof I18N.findPage === "function") {
      var found = I18N.findPage(routes);
      if (found) return found;
    }

    var pathKey =
      I18N && typeof I18N.currentPathKey === "function" ? I18N.currentPathKey() : "";
    if (!pathKey) return null;

    var pages = routes.pages || [];
    for (var i = 0; i < pages.length; i++) {
      var p = pages[i];
      if ((p.az && p.az.toLowerCase() === pathKey) || (p.en && p.en.toLowerCase() === pathKey)) {
        return p;
      }
    }
    return null;
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
    if (sectionNavInserted || mountInFlight) return;
    if (document.body && document.body.classList.contains("daab-gateway")) return;
    if (document.querySelector(".daab-section-nav")) {
      sectionNavInserted = true;
      return;
    }

    var I18N = getI18n();
    if (!I18N) return;

    mountInFlight = true;
    var lang = I18N.detectLang();

    loadData(I18N)
      .then(function (results) {
        if (sectionNavInserted || document.querySelector(".daab-section-nav")) {
          sectionNavInserted = true;
          return;
        }

        var routes = results[0] || FALLBACK_ROUTES;
        var ui = results[1] || FALLBACK_UI;
        var navDef = results[2] || FALLBACK_NAV;
        var page = findCurrentPage(I18N, routes);
        if (!page || !page.navGroup) return;

        var section = navDef.sections && navDef.sections[page.navGroup];
        if (!section || !section.pages || section.pages.length < 2) return;

        var main = document.getElementById("content") || document.querySelector("main.main");
        if (!main) return;

        var anchor = main.firstElementChild;
        var sectionUi = ui.sectionNav && ui.sectionNav[lang];
        var navLabels = ui.nav && ui.nav[lang];
        if (!sectionUi || !navLabels) return;

        var nav = document.createElement("nav");
        nav.className = "daab-section-nav";
        nav.setAttribute("aria-label", sectionUi.aria);

        var title = document.createElement("p");
        title.className = "daab-section-nav-title";
        title.textContent =
          sectionUi[page.navGroup + "Title"] || sectionUi.aboutTitle || page.navGroup;
        nav.appendChild(title);

        var list = document.createElement("ul");
        list.className = "daab-section-nav-list";

        section.pages.forEach(function (pid) {
          var p = pageById(routes, pid);
          if (!p) return;
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = pageHref(I18N, p, lang);
          var key = PAGE_LABEL_KEYS[pid];
          a.textContent = key ? navLabels[key] : pid;
          if (p.id === page.id) {
            a.classList.add("active");
            a.setAttribute("aria-current", "page");
          }
          li.appendChild(a);
          list.appendChild(li);
        });

        nav.appendChild(list);
        if (anchor) {
          main.insertBefore(nav, anchor);
        } else {
          main.prepend(nav);
        }
        sectionNavInserted = true;
      })
      .catch(function (err) {
        console.warn("[daab-section-nav] Mount failed:", err);
      })
      .finally(function () {
        mountInFlight = false;
      });
  }

  function boot(attempt) {
    if (sectionNavInserted || document.querySelector(".daab-section-nav")) {
      sectionNavInserted = true;
      return;
    }
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
        if (!sectionNavInserted) boot(0);
      }, 200);
      setTimeout(function () {
        if (!sectionNavInserted) boot(0);
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
