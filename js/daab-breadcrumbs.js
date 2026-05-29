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
    activities: "activitiesNews",
    "forum-2024": "forum2024",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-official": "forumOfficial",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-program": "forumProgram",
    "forum-impressions": "forumImpressions",
    "forum-photos-gallery": "forumPhotosGallery",
    "forum-video-gallery": "forumVideoGallery",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    charter: "charter",
    membership: "membershipTerms",
    "membership-value": "membershipWhy",
    "membership-application": "membershipJoin",
    "membership-flyer": "membershipFlyer"
  };

  var GROUP_LABEL_KEYS = {
    about: "about",
    scientists: "scientists",
    activities: "activities",
    membership: "membership"
  };

  var FALLBACK_ROUTES = {
    pages: [
      { id: "home", az: "az/index.html", en: "en/index.html", navParent: null },
      { id: "foundation", az: "az/foundation.html", en: "en/foundation.html", navParent: "about" },
      { id: "mission", az: "az/mission.html", en: "en/mission.html", navParent: "about" },
      {
        id: "activities",
        az: "az/activities.html",
        en: "en/activities.html",
        navParent: "activities"
      },
      {
        id: "forum-2024",
        az: "az/forum/2024/index.html",
        en: "en/forum/2024/index.html",
        navParent: "forum"
      },
      {
        id: "forum-2024-presentations",
        az: "az/forum/2024/presentations.html",
        en: "en/forum/2024/presentations.html",
        navParent: "forum"
      },
      {
        id: "forum-official",
        az: "az/forum/2024/official.html",
        en: "en/forum/2024/official.html",
        navParent: "forum"
      },
      {
        id: "forum-rector-speeches",
        az: "az/forum/2024/rector_speeches.html",
        en: "en/forum/2024/rector_speeches.html",
        navParent: "forum"
      },
      {
        id: "forum-anas-leadership-speeches",
        az: "az/forum/2024/anas_leadership_speeches.html",
        en: "en/forum/2024/anas_leadership_speeches.html",
        navParent: "forum"
      },
      {
        id: "forum-program",
        az: "az/forum/2024/program.html",
        en: "en/forum/2024/program.html",
        navParent: "forum"
      },
      {
        id: "forum-impressions",
        az: "az/forum/2024/impressions.html",
        en: "en/forum/2024/impressions.html",
        navParent: "forum"
      },
      {
        id: "forum-photos-gallery",
        az: "az/forum/2024/photos_gallery.html",
        en: "en/forum/2024/photos_gallery.html",
        navParent: "forum"
      },
      {
        id: "forum-video-gallery",
        az: "az/forum/2024/video_gallery.html",
        en: "en/forum/2024/video_gallery.html",
        navParent: "forum"
      },
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
      {
        id: "membership-value",
        az: "az/membership_value.html",
        en: "en/membership_value.html",
        navParent: "membership"
      },
      { id: "membership", az: "az/membership.html", en: "en/membership.html", navParent: "membership" },
      {
        id: "membership-application",
        az: "az/application.html",
        en: "en/application.html",
        navParent: "membership"
      },
      {
        id: "membership-flyer",
        az: "az/membership_flyer.html",
        en: "en/membership_flyer.html",
        navParent: "membership"
      }
    ]
  };

  var FALLBACK_UI = {
    breadcrumbs: {
      az: {
        aria: "Səhifə yolu",
        home: "Ana səhifə",
        about: "Haqqımızda",
        scientists: "Alimlərimiz",
        activities: "Fəaliyyətimiz"
      },
      en: {
        aria: "Breadcrumb",
        home: "Home",
        about: "About us",
        scientists: "Scientists",
        activities: "Activities"
      }
    },
    nav: {
      az: {
        home: "Ana səhifə",
        foundation: "Birliyin təsisi",
        mission: "Missiya və dəyərlər",
        activities: "Fəaliyyətimiz",
        activitiesNews: "Yeniliklər",
        forum2024: "Forum 2024",
        forumOfficial: "Rəsmi müraciətlər",
        forumRectorSpeeches: "Rektorların nitqləri",
        forumAnasLeadershipSpeeches: "AMEA rəhbərliyinin nitqləri",
        forumProgram: "Forumun proqramı",
        forumPhotosGallery: "Foto qalereya",
        scientistsList: "Siyahı",
        scientistsProfiles: "Profillər",
        executiveBoard: "İdarə heyəti",
        charter: "Nizamnamə",
        membership: "Üzvlük",
        membershipWhy: "Niyə üzv olmalı",
        membershipTerms: "Üzvlük şərtləri",
        membershipJoin: "Bizə qoşulun",
        membershipFlyer: "Flyer paylaş"
      },
      en: {
        home: "Home",
        foundation: "Foundation",
        mission: "Mission & values",
        activities: "Activities",
        activitiesNews: "News",
        forum2024: "Forum 2024",
        forumOfficial: "Official addresses",
        forumRectorSpeeches: "Rectors' speeches",
        forumAnasLeadershipSpeeches: "Speeches by the ANAS Leadership",
        forumProgram: "Forum programme",
        forumPhotosGallery: "Photo gallery",
        forumVideoGallery: "Video gallery",
        scientistsList: "Directory",
        scientistsProfiles: "Profiles",
        executiveBoard: "Board of Directors",
        charter: "Charter",
        membership: "Membership",
        membershipWhy: "Why become a member",
        membershipTerms: "Membership terms",
        membershipJoin: "Join us",
        membershipFlyer: "Share Flyer"
      }
    }
  };

  var FALLBACK_NAV = {
    sections: {
      about: { landingId: "mission" },
      scientists: { landingId: "scientists-list" },
      activities: { landingId: "activities" },
      membership: { landingId: "membership-value" }
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

  function isBreadcrumbNode(node) {
    return (
      node &&
      (node.id === "daab-breadcrumbs" ||
        (node.classList && node.classList.contains("daab-breadcrumbs")))
    );
  }

  function findMountPoint() {
    var nav = document.querySelector(".nav-strip");
    if (nav && nav.parentNode) {
      var before = nav.nextElementSibling;
      while (isBreadcrumbNode(before)) {
        before = before.nextElementSibling;
      }
      return { parent: nav.parentNode, before: before };
    }
    var main = document.getElementById("content") || document.querySelector("main");
    if (main && main.parentNode) {
      return { parent: main.parentNode, before: main };
    }
    return null;
  }

  function removeBreadcrumbs() {
    document.querySelectorAll("#daab-breadcrumbs, nav.daab-breadcrumbs").forEach(function (el) {
      if (el.getAttribute("data-daab-breadcrumbs-static") === "1") return;
      el.remove();
    });
    document.documentElement.style.setProperty("--daab-breadcrumbs-height", "0px");
  }

  function breadcrumbsElement() {
    return (
      document.getElementById("daab-breadcrumbs") || staticBreadcrumbsNode()
    );
  }

  function syncBreadcrumbsHeight() {
    var el = breadcrumbsElement();
    if (!el) {
      document.documentElement.style.setProperty("--daab-breadcrumbs-height", "0px");
      return;
    }
    var h = Math.ceil(el.getBoundingClientRect().height);
    document.documentElement.style.setProperty(
      "--daab-breadcrumbs-height",
      h > 0 ? h + "px" : "0px"
    );
  }

  function staticBreadcrumbsNode() {
    // Some pages ship their own breadcrumb markup (e.g. forum pages).
    // If present, we should not inject a second breadcrumb trail.
    var el = document.querySelector(".breadcrumbs");
    if (!el) return null;
    if (el.id === "daab-breadcrumbs") return null;
    if (el.classList && el.classList.contains("daab-breadcrumbs")) return null;
    return el;
  }

  function adoptStaticBreadcrumbs() {
    var el = staticBreadcrumbsNode();
    if (!el) return false;
    // Remove any previously injected crumbs to avoid duplicates.
    removeBreadcrumbs();
    breadcrumbsInserted = true;
    function sync() {
      var h = Math.ceil(el.getBoundingClientRect().height);
      document.documentElement.style.setProperty("--daab-breadcrumbs-height", h > 0 ? h + "px" : "0px");
    }
    sync();
    requestAnimationFrame(sync);
    if (typeof ResizeObserver !== "undefined") {
      var ro = new ResizeObserver(sync);
      ro.observe(el);
    }
    window.addEventListener("resize", sync, { passive: true });
    document.dispatchEvent(new CustomEvent("daab-breadcrumbs-ready"));
    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
    }
    return true;
  }

  function findCurrentPage(I18N, routes) {
    if (I18N && typeof I18N.findPage === "function") {
      var found = I18N.findPage(routes);
      if (found) return found;
    }

    var pageId = document.documentElement.getAttribute("data-daab-page-id");
    if (pageId) {
      var byId = pageById(routes, pageId);
      if (byId) return byId;
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

    // For forum pages we already insert the Forum 2024 hub crumb below; adding a generic
    // "forum" group label would be redundant and confusing.
    if (page.navParent && page.navParent !== "forum") {
      var groupKey = GROUP_LABEL_KEYS[page.navParent];
      var landingId = sectionLanding(navDef, page.navParent);
      var landing = landingId ? pageById(routes, landingId) : null;
      crumbs.push({
        href: landing ? pageHref(I18N, landing, lang) : null,
        text: groupKey ? t(ui, lang, "breadcrumbs", groupKey) : page.navParent
      });
    }

    if (page.id && page.id.indexOf("forum-") === 0 && page.id !== "forum-2024") {
      var forumHub = pageById(routes, "forum-2024");
      if (forumHub) {
        crumbs.push({
          href: pageHref(I18N, forumHub, lang),
          text: pageTitle(ui, lang, "forum-2024")
        });
      }
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

  function adoptExistingBreadcrumbs() {
    var existing = document.getElementById("daab-breadcrumbs");
    if (!existing || !existing.querySelector(".daab-breadcrumbs-list")) return false;
    breadcrumbsInserted = true;
    syncBreadcrumbsHeight();
    requestAnimationFrame(syncBreadcrumbsHeight);
    document.dispatchEvent(new CustomEvent("daab-breadcrumbs-ready"));
    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
    }
    if (typeof ResizeObserver !== "undefined") {
      var ro = new ResizeObserver(syncBreadcrumbsHeight);
      ro.observe(existing);
    }
    window.addEventListener("resize", syncBreadcrumbsHeight, { passive: true });
    return true;
  }

  function mount() {
    if (breadcrumbsInserted || mountInFlight) return;
    if (document.body && document.body.classList.contains("daab-gateway")) return;
    if (adoptStaticBreadcrumbs()) return;
    if (adoptExistingBreadcrumbs()) return;

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

        removeBreadcrumbs();
        var el = render(crumbs, ui, lang);
        var mountPoint = findMountPoint();
        if (mountPoint) {
          mountPoint.parent.insertBefore(el, mountPoint.before);
        } else {
          var nav = document.querySelector(".nav-strip");
          if (nav && nav.parentNode) {
            nav.parentNode.insertBefore(el, nav.nextSibling);
          }
        }
        if (!document.getElementById("daab-breadcrumbs")) return;
        breadcrumbsInserted = true;
        syncBreadcrumbsHeight();
        document.dispatchEvent(new CustomEvent("daab-breadcrumbs-ready"));
        if (typeof ResizeObserver !== "undefined") {
          var ro = new ResizeObserver(syncBreadcrumbsHeight);
          ro.observe(el);
        }
        window.addEventListener("resize", syncBreadcrumbsHeight, { passive: true });
        if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
          window.DAAB_STICKY_CHROME.sync();
        }
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
    if (adoptStaticBreadcrumbs()) return;
    if (adoptExistingBreadcrumbs()) return;
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

  window.DAAB_BREADCRUMBS = {
    syncHeight: syncBreadcrumbsHeight
  };
})();
