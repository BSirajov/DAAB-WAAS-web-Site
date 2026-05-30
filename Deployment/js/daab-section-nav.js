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
    activities: "activitiesNews",
    "forum-2024": "forum2024",
    "forum-2024-presentations": "forum2024",
    "forum-official": "forumOfficial",
    "forum-program": "forumProgram",
    "forum-impressions": "forumImpressions",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-roadmap": "forumRoadmap",
    "forum-bagli-hekayeler": "forumBagliHekayeler",
    "forum-cooperation": "forumCooperation",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-photos-gallery": "forumPhotosGallery",
    "forum-video-gallery": "forumVideoGallery",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    membership: "membershipTerms",
    "membership-value": "membershipWhy",
    "membership-application": "membershipJoin",
    "membership-flyer": "membershipFlyer"
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
        navGroup: "activities",
        navParent: "activities"
      },
      {
        id: "forum-2024",
        az: "az/forum/2024/index.html",
        en: "en/forum/2024/index.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-2024-presentations",
        az: "az/forum/2024/presentations.html",
        en: "en/forum/2024/presentations.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-official",
        az: "az/forum/2024/official.html",
        en: "en/forum/2024/official.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-rector-speeches",
        az: "az/forum/2024/rector_speeches.html",
        en: "en/forum/2024/rector_speeches.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-anas-leadership-speeches",
        az: "az/forum/2024/anas_leadership_speeches.html",
        en: "en/forum/2024/anas_leadership_speeches.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-program",
        az: "az/forum/2024/program.html",
        en: "en/forum/2024/program.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-impressions",
        az: "az/forum/2024/impressions.html",
        en: "en/forum/2024/impressions.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-photos-gallery",
        az: "az/forum/2024/photos_gallery.html",
        en: "en/forum/2024/photos_gallery.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-video-gallery",
        az: "az/forum/2024/video_gallery.html",
        en: "en/forum/2024/video_gallery.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-roadmap",
        az: "az/forum/2024/roadmap.html",
        en: "en/forum/2024/roadmap.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-bagli-hekayeler",
        az: "az/forum/2024/stories.html",
        en: "en/forum/2024/stories.html",
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "forum-cooperation",
        az: "az/forum/2024/cooperation.html",
        en: "en/forum/2024/cooperation.html",
        navGroup: "forum",
        navParent: "forum"
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
      {
        id: "membership-value",
        az: "az/membership_value.html",
        en: "en/membership_value.html",
        navGroup: "membership",
        navParent: "membership"
      },
      { id: "membership", az: "az/membership.html", en: "en/membership.html", navGroup: "membership", navParent: "membership" },
      {
        id: "membership-application",
        az: "az/application.html",
        en: "en/application.html",
        navGroup: "membership",
        navParent: "membership"
      },
      {
        id: "membership-flyer",
        az: "az/membership_flyer.html",
        en: "en/membership_flyer.html",
        navGroup: "membership",
        navParent: "membership"
      }
    ]
  };

  var FALLBACK_UI = {
    sectionNav: {
      az: {
        aria: "Bu bölmədə",
        aboutTitle: "Haqqımızda",
        scientistsTitle: "Alimlərimiz",
        activitiesTitle: "Fəaliyyətimiz",
        forumTitle: "Forum 2024",
        membershipTitle: "Üzvlük"
      },
      en: {
        aria: "In this section",
        aboutTitle: "About us",
        scientistsTitle: "Scientists",
        activitiesTitle: "Activities",
        forumTitle: "Forum 2024",
        membershipTitle: "Membership"
      }
    },
    navIcons: {
      "forum-2024": "🎤",
      "forum-official": "🏛️",
      "forum-program": "📅",
      "forum-2024-presentations": "📊",
      "forum-impressions": "💬",
      "forum-roadmap": "🗺️",
      "forum-bagli-hekayeler": "📖",
      "forum-cooperation": "🤝",
      "forum-rector-speeches": "🎓",
      "forum-anas-leadership-speeches": "🔬",
      "forum-photos-gallery": "📷",
      "forum-video-gallery": "📹",
      activities: "📰",
      activitiesNews: "📰",
      foundation: "🏛️",
      mission: "💎",
      "executive-board": "🎓",
      charter: "📜",
      "scientists-list": "📋",
      "scientists-profiles": "👤",
      membershipWhy: "💡",
      membershipTerms: "✒️",
      membershipJoin: "📝",
      membershipFlyer: "📤"
    },
    nav: {
      az: {
        foundation: "Birliyin təsisi",
        mission: "Missiya və dəyərlər",
        executiveBoard: "İdarə heyəti",
        charter: "Nizamnamə",
        activitiesNews: "Yeniliklər",
        forum2024: "Forum 2024",
        forumOfficial: "Rəsmi müraciətlər",
        forumProgram: "Proqram",
        forum2024Presentations: "Məruzələr",
        forumImpressions: "Təəssüratlar",
        forumRoadmap: "Strateji yol xəritəsi",
        forumBagliHekayeler: "Hekayələr",
        forumCooperation: "Töhfələr",
        forumRectorSpeeches: "Rektorlar",
        forumAnasLeadershipSpeeches: "AMEA rəhbərliyi",
        forumPhotosGallery: "Foto qalereya",
        forumVideoGallery: "Video qalereya",
        scientistsList: "Siyahı",
        scientistsProfiles: "Profillər",
        membershipWhy: "Niyə üzv olmalı",
        membershipTerms: "Üzvlük şərtləri",
        membershipJoin: "Bizə qoşulun",
        membershipFlyer: "Dəvət göndərin"
      },
      en: {
        foundation: "Foundation",
        mission: "Mission & values",
        executiveBoard: "Board of Directors",
        charter: "Charter",
        activitiesNews: "News",
        forum2024: "Forum 2024",
        forumOfficial: "Official addresses",
        forumProgram: "Programme",
        forum2024Presentations: "Presentations",
        forumImpressions: "Impressions",
        forumRoadmap: "Strategic roadmap",
        forumBagliHekayeler: "Stories",
        forumCooperation: "Contributions",
        forumRectorSpeeches: "Rectors",
        forumAnasLeadershipSpeeches: "ANAS Leadership",
        forumPhotosGallery: "Photo gallery",
        forumVideoGallery: "Video gallery",
        scientistsList: "Directory",
        scientistsProfiles: "Profiles",
        membershipWhy: "Why become a member",
        membershipTerms: "Membership terms",
        membershipJoin: "Join us",
        membershipFlyer: "Send invite"
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
      },
      activities: {
        landingId: "activities",
        pages: ["activities", "forum-2024"]
      },
      forum: {
        landingId: "forum-2024",
        pages: [
          "forum-2024",
          "forum-official",
          "forum-rector-speeches",
          "forum-anas-leadership-speeches",
          "forum-program",
          "forum-2024-presentations",
          "forum-impressions",
          "forum-photos-gallery",
          "forum-video-gallery",
          "forum-roadmap",
          "forum-bagli-hekayeler",
          "forum-cooperation"
        ]
      },
      membership: {
        landingId: "membership-value",
        pages: ["membership-value", "membership", "membership-application", "membership-flyer"]
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

  function sectionNavIcon(ui, pageId) {
    var icons = (ui && ui.navIcons) || {};
    if (icons[pageId]) return icons[pageId];
    var labelKey = PAGE_LABEL_KEYS[pageId];
    if (labelKey && icons[labelKey]) return icons[labelKey];
    return "";
  }

  function pageIdFromHref(href, routes) {
    if (!href || !routes) return "";
    var linkPath = href.split("#")[0].split("?")[0].replace(/\\/g, "/").toLowerCase();
    var linkFile = linkPath.split("/").pop() || linkPath;
    var pages = routes.pages || [];
    var i;
    for (i = 0; i < pages.length; i++) {
      var p = pages[i];
      var az = (p.az || "").toLowerCase();
      var en = (p.en || "").toLowerCase();
      if (
        az === linkPath ||
        en === linkPath ||
        az.endsWith("/" + linkPath) ||
        en.endsWith("/" + linkPath) ||
        az.split("/").pop() === linkFile ||
        en.split("/").pop() === linkFile
      ) {
        return p.id;
      }
    }
    return "";
  }

  function enhanceSectionNavLink(a, ui, routes) {
    if (!a || a.querySelector(".daab-section-nav-icon")) return;
    var pid = a.getAttribute("data-nav-id") || pageIdFromHref(a.getAttribute("href"), routes);
    if (!pid) return;
    var icon = sectionNavIcon(ui, pid);
    if (!icon) return;
    var labelText = a.textContent.trim();
    a.textContent = "";
    var iconEl = document.createElement("span");
    iconEl.className = "daab-section-nav-icon";
    iconEl.setAttribute("aria-hidden", "true");
    iconEl.textContent = icon;
    var labelEl = document.createElement("span");
    labelEl.className = "daab-section-nav-label";
    labelEl.textContent = labelText;
    a.appendChild(iconEl);
    a.appendChild(labelEl);
    if (!a.getAttribute("data-nav-id")) {
      a.setAttribute("data-nav-id", pid);
    }
  }

  function decorateEmbeddedSectionNav(ui, routes) {
    var nav = document.querySelector(".daab-section-nav");
    if (!nav || nav.getAttribute("data-daab-section-nav-enhanced") === "1") return;
    nav.querySelectorAll(".daab-section-nav-list a").forEach(function (a) {
      enhanceSectionNavLink(a, ui, routes);
    });
    nav.setAttribute("data-daab-section-nav-enhanced", "1");
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

  var HERO_HEADER_SEL = "header.forum-hero, header.page-hero, header.hero";

  /**
   * Place section pills below the page title/hero band, not above it (and not under breadcrumbs only).
   */
  function findSectionNavInsertPoint(main) {
    var i;
    var heroSel = HERO_HEADER_SEL.split(", ");
    for (i = 0; i < heroSel.length; i++) {
      var inMain = main.querySelector(":scope > " + heroSel[i]);
      if (inMain) {
        return { parent: main, before: inMain.nextSibling };
      }
    }

    var contentWrap = main.closest(".content-wrap");
    if (contentWrap && contentWrap.parentNode) {
      var heroBeforeWrap = contentWrap.previousElementSibling;
      if (heroBeforeWrap && heroBeforeWrap.matches(HERO_HEADER_SEL)) {
        return { parent: contentWrap.parentNode, before: contentWrap };
      }
    }

    var prev = main.previousElementSibling;
    if (prev && prev.matches && prev.matches(HERO_HEADER_SEL)) {
      return { parent: main.parentNode, before: main };
    }

    return { parent: main, before: main.firstElementChild };
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

        var insertPoint = findSectionNavInsertPoint(main);
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
          var fallbackNav = FALLBACK_UI.nav[lang] || {};
          var label =
            (key && navLabels[key]) ||
            (key && fallbackNav[key]) ||
            pid;
          var icon = sectionNavIcon(ui, pid);
          if (icon) {
            var iconEl = document.createElement("span");
            iconEl.className = "daab-section-nav-icon";
            iconEl.setAttribute("aria-hidden", "true");
            iconEl.textContent = icon;
            a.appendChild(iconEl);
          }
          var labelEl = document.createElement("span");
          labelEl.className = "daab-section-nav-label";
          labelEl.textContent = label;
          a.appendChild(labelEl);
          if (p.id === page.id) {
            a.classList.add("active");
            a.setAttribute("aria-current", "page");
          }
          li.appendChild(a);
          list.appendChild(li);
        });

        nav.appendChild(list);
        if (insertPoint.before) {
          insertPoint.parent.insertBefore(nav, insertPoint.before);
        } else {
          insertPoint.parent.appendChild(nav);
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
    }
    var I18N = getI18n();
    if (I18N && document.querySelector(".daab-section-nav")) {
      loadData(I18N)
        .then(function (results) {
          decorateEmbeddedSectionNav(results[1] || FALLBACK_UI, results[0] || FALLBACK_ROUTES);
        })
        .catch(function () {
          decorateEmbeddedSectionNav(FALLBACK_UI, FALLBACK_ROUTES);
        });
    }
    if (sectionNavInserted) return;
    if (I18N) {
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
