/**
 * Builds primary navigation from i18n/nav.json, routes.json, and ui.json.
 */
(function () {
  "use strict";

  /** Set in init(); used by helpers below. */
  var activeI18n = null;

  var PAGE_LABEL_KEYS = {
    home: "home",
    foundation: "foundation",
    mission: "mission",
    activities: "activities",
    activitiesNews: "activitiesNews",
    "activities-news": "activitiesNews",
    "work-done-2024-2026": "activitiesWorkDone2024",
    forum2024: "forum2024",
    "forum-2024": "forum2024",
    "forum-2026": "forum2026Year",
    encyclopedia: "prominentFigures",
    "industrial-revolutions": "industrialRevolutions",
    "major-scientific-inventions": "majorScientificInventions",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-official": "forumOfficial",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-program": "forumProgram",
    "forum-logistics": "forumLogistics",
    "forum-sessions-organization": "forumSessionsOrganization",
    "forum-impressions": "forumImpressions",
    "forum-roadmap": "forumRoadmap",
    "forum-bagli-hekayeler": "forumBagliHekayeler",
    "forum-cooperation": "forumCooperation",
    "forum-photos-gallery": "forumPhotosGallery",
    "forum-video-gallery": "forumVideoGallery",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    charter: "charter",
    membership: "membershipTerms",
    "membership-value": "membershipWhy",
    "membership-application": "membershipJoin",
    "membership-flyer": "membershipFlyer",
    sponsors: "sponsorsProgram",
    donate: "donate",
    "sponsors-flyer": "sponsorsFlyer"
  };

  function pageById(routes, id) {
    var pages = routes.pages || [];
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].id === id) return pages[i];
    }
    return null;
  }

  function pageHref(page, lang) {
    return activeI18n.pageHref(page, lang);
  }

  function label(ui, lang, key) {
    var nav = ui.nav[lang] || ui.nav.az;
    return nav[key] || key;
  }

  function navIcon(ui, key) {
    var icons = ui.navIcons || {};
    var icon = icons[key];
    return icon ? icon + "\u00a0" : "";
  }

  function labelWithIcon(ui, key, text) {
    return navIcon(ui, key) + text;
  }

  function pageLabel(ui, lang, pageId) {
    var key = PAGE_LABEL_KEYS[pageId];
    return key ? label(ui, lang, key) : pageId;
  }

  function childLabel(ui, lang, childDef, page) {
    var key = childDef.labelKey || PAGE_LABEL_KEYS[page.id] || page.id;
    return label(ui, lang, key);
  }

  function childIconKey(childDef, page) {
    if (childDef.labelKey) return childDef.labelKey;
    if (page && page.id) return page.id;
    if (childDef.id) return childDef.id;
    return "";
  }

  function currentPageId(routes) {
    var explicit = document.documentElement.getAttribute("data-daab-page-id");
    if (explicit) return explicit;
    return activeI18n.getPageId(routes);
  }

  function isForumNavPageId(id) {
    if (window.DAAB_NAV && typeof window.DAAB_NAV.isForumNavPageId === "function") {
      return window.DAAB_NAV.isForumNavPageId(id);
    }
    return id === "forum-2024" || (typeof id === "string" && id.indexOf("forum-") === 0);
  }

  function childLinkIsActive(page, childDef, activeId) {
    if (!activeId) return false;
    if (childDef.id === activeId || page.id === activeId) return true;
    if (childDef.id === "activities-news" && activeId === "activities") return true;
    if (childDef.id === "encyclopedia" && activeId === "prominent-figure") return true;
    return false;
  }

  function forumPageNavDesc(ui, lang, pageId) {
    var sectionUi = ui.sectionNav && ui.sectionNav[lang];
    var tips = sectionUi && sectionUi.forumPageTooltips;
    return (tips && tips[pageId]) || "";
  }

  function linkDescription(ui, lang, childDef, page) {
    if (childDef.descKey) {
      var fromKey = label(ui, lang, childDef.descKey);
      if (fromKey && fromKey !== childDef.descKey) return fromKey;
    }
    if (page) {
      var fromTooltip = forumPageNavDesc(ui, lang, page.id);
      if (fromTooltip) return fromTooltip;
    }
    return "";
  }

  function buildLink(page, lang, ui, activeId, className, extra) {
    var a = document.createElement("a");
    a.href = pageHref(page, lang);
    a.className = className;
    a.setAttribute("data-nav-id", page.id);
    if (extra && extra.role) a.setAttribute("role", extra.role);
    a.textContent = labelWithIcon(ui, page.id, pageLabel(ui, lang, page.id));
    if (page.id === activeId) {
      a.classList.add("active");
      a.setAttribute("aria-current", "page");
    }
    return a;
  }

  var navPanelSeq = 0;
  function associatePanel(toggle, panel) {
    if (!panel.id) panel.id = "daab-nav-panel-" + (++navPanelSeq);
    toggle.setAttribute("aria-controls", panel.id);
  }

  /**
   * Unified dropdown renderer. Every group — whether marked `mega` or `dropdown`
   * in nav.json — gets the same panel/link styling. Descriptions are optional.
   */
  function buildGroup(item, routes, lang, ui, activeId) {
    var wrap = document.createElement("div");
    wrap.className = "nav-dropdown";
    wrap.setAttribute("data-nav-dropdown", "");

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-link nav-dropdown-toggle";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-haspopup", "true");
    toggle.appendChild(
      document.createTextNode(labelWithIcon(ui, item.labelKey, label(ui, lang, item.labelKey)))
    );
    var caret = document.createElement("span");
    caret.className = "nav-dropdown-caret";
    caret.setAttribute("aria-hidden", "true");
    toggle.appendChild(document.createTextNode(" "));
    toggle.appendChild(caret);

    var panel = document.createElement("div");
    panel.className = "nav-dropdown-panel";
    panel.setAttribute("role", "menu");

    var children = item.children || [];
    var groupActive = false;
    children.forEach(function (childDef) {
      if (childDef.type === "section") return;
      var page = pageById(routes, childDef.id);
      if (!page) return;
      var link = document.createElement("a");
      link.href = pageHref(page, lang);
      link.className = "nav-dropdown-link";
      link.setAttribute("role", "menuitem");
      link.setAttribute("data-nav-id", childDef.id);

      var iconKey = childIconKey(childDef, page);
      var title = document.createElement("span");
      title.className = "nav-dropdown-link-title";
      title.textContent = labelWithIcon(ui, iconKey, childLabel(ui, lang, childDef, page));
      link.appendChild(title);

      var descText = linkDescription(ui, lang, childDef, page);
      if (descText) {
        var desc = document.createElement("span");
        desc.className = "nav-dropdown-link-desc";
        desc.textContent = descText;
        link.appendChild(desc);
      }

      if (childLinkIsActive(page, childDef, activeId)) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
        groupActive = true;
      }
      panel.appendChild(link);
    });

    if (groupActive) wrap.classList.add("has-active-child");

    associatePanel(toggle, panel);
    wrap.appendChild(toggle);
    wrap.appendChild(panel);
    return wrap;
  }

  function buildForumYearToggle(toggle, item, lang, ui) {
    toggle.classList.add("nav-dropdown-toggle--forum-year");

    var title = document.createElement("span");
    title.className = "nav-dropdown-link-title";
    title.textContent = labelWithIcon(ui, item.labelKey, label(ui, lang, item.labelKey));
    toggle.appendChild(title);

    if (item.descKey) {
      var desc = document.createElement("span");
      desc.className = "nav-dropdown-link-desc";
      desc.textContent = label(ui, lang, item.descKey);
      toggle.appendChild(desc);
    }

    toggle.appendChild(document.createTextNode(" "));
    var caret = document.createElement("span");
    caret.className = "nav-dropdown-caret";
    caret.setAttribute("aria-hidden", "true");
    toggle.appendChild(caret);
  }

  function buildMegaGroup(item, routes, lang, ui, activeId, nested) {
    var isNested = !!nested;
    var wrap = document.createElement("div");
    wrap.className =
      "nav-dropdown nav-dropdown--mega nav-dropdown--forum" +
      (isNested ? " nav-dropdown--nested nav-dropdown--has-mega" : "");
    wrap.setAttribute("data-nav-dropdown", "");
    wrap.setAttribute("data-nav-group", item.id || "forum");
    if (isNested) {
      wrap.setAttribute("data-has-nested-mega", "1");
    }

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-link nav-dropdown-toggle";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-haspopup", "true");
    if (isNested && item.descKey) {
      buildForumYearToggle(toggle, item, lang, ui);
    } else {
      toggle.appendChild(
        document.createTextNode(labelWithIcon(ui, item.labelKey, label(ui, lang, item.labelKey)))
      );
      var caret = document.createElement("span");
      caret.className = "nav-dropdown-caret";
      caret.setAttribute("aria-hidden", "true");
      toggle.appendChild(document.createTextNode(" "));
      toggle.appendChild(caret);
    }

    var panel = document.createElement("div");
    panel.className = "nav-dropdown-panel nav-dropdown-panel--mega";
    panel.setAttribute("role", "menu");

    var grid = document.createElement("div");
    grid.className = "nav-mega-grid";
    panel.appendChild(grid);

    var groupActive = false;
    (item.children || []).forEach(function (sectionDef) {
      if (sectionDef.type !== "section") return;

      var col = document.createElement("div");
      col.className = "nav-mega-col";

      if (sectionDef.labelKey) {
        var heading = document.createElement("div");
        heading.className = "nav-mega-heading";
        heading.setAttribute("role", "presentation");
        heading.textContent = label(ui, lang, sectionDef.labelKey);
        col.appendChild(heading);
      }

      var linksWrap = document.createElement("div");
      linksWrap.className = sectionDef.nested ? "nav-mega-nest" : "nav-mega-links";
      col.appendChild(linksWrap);

      (sectionDef.children || []).forEach(function (childDef) {
        var page = pageById(routes, childDef.id);
        if (!page) return;

        var link = document.createElement("a");
        link.href = pageHref(page, lang);
        link.className = "nav-dropdown-link";
        link.setAttribute("role", "menuitem");
        link.setAttribute("data-nav-id", childDef.id);

        var iconKey = childIconKey(childDef, page);
        var title = document.createElement("span");
        title.className = "nav-dropdown-link-title";
        title.textContent = labelWithIcon(ui, iconKey, childLabel(ui, lang, childDef, page));
        link.appendChild(title);

        var descText = linkDescription(ui, lang, childDef, page);
        if (descText) {
          var desc = document.createElement("span");
          desc.className = "nav-dropdown-link-desc";
          desc.textContent = descText;
          link.appendChild(desc);
        }

        if (childLinkIsActive(page, childDef, activeId)) {
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
          groupActive = true;
        }

        linksWrap.appendChild(link);
      });

      if (linksWrap.children.length) {
        grid.appendChild(col);
      }
    });

    if (groupActive) wrap.classList.add("has-active-child");

    associatePanel(toggle, panel);
    wrap.appendChild(toggle);
    wrap.appendChild(panel);
    return wrap;
  }

  function buildForumsPanelLink(panel, childDef, page, lang, ui, activeId) {
    var link = document.createElement("a");
    link.href = pageHref(page, lang);
    link.className = "nav-dropdown-link nav-dropdown-link--forum-year";
    link.setAttribute("role", "menuitem");
    link.setAttribute("data-nav-id", childDef.id || page.id);

    var labelKey = childDef.labelKey || page.id;
    var title = document.createElement("span");
    title.className = "nav-dropdown-link-title";
    title.textContent = labelWithIcon(ui, labelKey, label(ui, lang, labelKey));
    link.appendChild(title);

    var descText = linkDescription(ui, lang, childDef, page);
    if (descText) {
      var desc = document.createElement("span");
      desc.className = "nav-dropdown-link-desc";
      desc.textContent = descText;
      link.appendChild(desc);
    }

    if (childLinkIsActive(page, childDef, activeId)) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
      panel.appendChild(link);
      return true;
    }

    panel.appendChild(link);
    return false;
  }

  function buildForumsGroup(item, routes, lang, ui, activeId) {
    var wrap = document.createElement("div");
    wrap.className = "nav-dropdown nav-dropdown--forums";
    wrap.setAttribute("data-nav-dropdown", "");
    wrap.setAttribute("data-nav-group", item.id || "forums");

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-link nav-dropdown-toggle";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-haspopup", "true");
    toggle.appendChild(
      document.createTextNode(labelWithIcon(ui, item.labelKey, label(ui, lang, item.labelKey)))
    );
    var caret = document.createElement("span");
    caret.className = "nav-dropdown-caret";
    caret.setAttribute("aria-hidden", "true");
    toggle.appendChild(document.createTextNode(" "));
    toggle.appendChild(caret);

    var panel = document.createElement("div");
    panel.className = "nav-dropdown-panel";
    panel.setAttribute("role", "menu");

    var groupActive = false;
    (item.children || []).forEach(function (child) {
      if (child.type === "group" && child.style === "mega") {
        var nestedMega = buildMegaGroup(child, routes, lang, ui, activeId, true);
        panel.appendChild(nestedMega);
        if (nestedMega.classList.contains("has-active-child")) {
          groupActive = true;
        }
        return;
      }
      if (!child.id) return;
      var page = pageById(routes, child.id);
      if (!page) return;
      if (buildForumsPanelLink(panel, child, page, lang, ui, activeId)) {
        groupActive = true;
      }
    });

    if (!panel.children.length) {
      return buildMegaGroup(item, routes, lang, ui, activeId, false);
    }

    if (groupActive) {
      wrap.classList.add("has-active-child");
    }

    associatePanel(toggle, panel);
    wrap.appendChild(toggle);
    wrap.appendChild(panel);
    return wrap;
  }

  function buildMenu(navDef, routes, lang, ui, activeId) {
    var frag = document.createDocumentFragment();
    var divider = document.createElement("div");
    divider.className = "nav-divider";
    frag.appendChild(divider);

    (navDef.primary || []).forEach(function (item) {
      if (item.type === "page") {
        var page = pageById(routes, item.id);
        if (!page) return;
        var cls = item.emphasis === "cta" ? "nav-link nav-link-cta" : "nav-link";
        frag.appendChild(buildLink(page, lang, ui, activeId, cls));
        return;
      }
      if (item.type === "group") {
        if (item.id === "forums") {
          frag.appendChild(buildForumsGroup(item, routes, lang, ui, activeId));
        } else if (item.style === "mega") {
          frag.appendChild(buildMegaGroup(item, routes, lang, ui, activeId, false));
        } else {
          frag.appendChild(buildGroup(item, routes, lang, ui, activeId));
        }
      }
    });

    return frag;
  }

  function applyNavAria(ui, lang) {
    var navLabels = (ui && ui.nav && (ui.nav[lang] || ui.nav.az)) || null;
    if (!navLabels) return;
    var nav = document.querySelector(".nav-strip");
    if (nav && navLabels.ariaMain) nav.setAttribute("aria-label", navLabels.ariaMain);
    var homeLogo = document.querySelector(".page-logo > a");
    var homeBrand = document.querySelector("a.nav-brand");
    var homeLabel = navLabels.ariaHome;
    var homeTooltip =
      navLabels.homeLogoTooltip ||
      (lang === "en" ? "Home page" : "Ana səhifə");
    if (homeLogo) {
      if (homeLabel) homeLogo.setAttribute("aria-label", homeLabel);
      homeLogo.setAttribute("title", homeTooltip);
    }
    if (homeBrand && homeLabel) homeBrand.setAttribute("aria-label", homeLabel);
    var toggle = document.querySelector(".mobile-menu-toggle");
    if (toggle && !toggle.getAttribute("data-daab-menu-labels")) {
      toggle.setAttribute("data-daab-menu-labels", "1");
      if (navLabels.menuOpen) {
        toggle.setAttribute("aria-label", navLabels.menuOpen);
        toggle.setAttribute("data-label-open", navLabels.menuOpen);
      }
      if (navLabels.menuClose) toggle.setAttribute("data-label-close", navLabels.menuClose);
    }
    var skip = document.querySelector("a.skip");
    if (skip && navLabels.skip) skip.textContent = navLabels.skip;
  }

  function homeHref() {
    var path = location.pathname.replace(/\\/g, "/");
    if (/\/forum\/202[46]\//.test(path) || /\/prominent_figures\//.test(path)) {
      return "../../index.html";
    }
    if (/\/scientists\//.test(path)) {
      return "../index.html";
    }
    return "index.html";
  }

  function renderMinimalFallback(menu, lang) {
    var title = lang === "en" ? "Home" : "Ana səhifə";
    menu.innerHTML =
      '<div class="nav-divider"></div>' +
      '<a class="nav-link" href="' +
      homeHref() +
      '" data-nav-id="home">🏠\u00a0' +
      title +
      "</a>";
    menu.setAttribute("data-daab-nav-ready", "1");
    if (window.DAAB_NAV && typeof window.DAAB_NAV.init === "function") {
      window.DAAB_NAV.init();
    }
  }

  function init(i18nApi) {
    activeI18n = i18nApi;
    if (document.body && document.body.classList.contains("daab-gateway")) return;

    var menu = document.getElementById("primaryNavMenu");
    if (!menu) return;

    var lang = activeI18n.detectLang();

    Promise.all([activeI18n.loadRoutes(), activeI18n.loadUi(), activeI18n.loadNav()])
      .then(function (results) {
        var routes = results[0];
        var ui = results[1];
        var navDef = results[2];
        var activeId = currentPageId(routes);

        while (menu.firstChild) menu.removeChild(menu.firstChild);
        menu.appendChild(buildMenu(navDef, routes, lang, ui, activeId));
        menu.setAttribute("data-daab-nav-ready", "1");
        applyNavAria(ui, lang);

        if (window.DAAB_NAV && typeof window.DAAB_NAV.init === "function") {
          window.DAAB_NAV.init();
        }
        document.dispatchEvent(new CustomEvent("daab-primary-nav-ready"));
      })
      .catch(function (err) {
        console.error("[daab-primary-nav] Menu build failed:", err);
        renderMinimalFallback(menu, lang);
        document.dispatchEvent(new CustomEvent("daab-primary-nav-ready"));
      });
  }

  function boot(attempt) {
    var api = window.DAAB_I18N;
    if (!api) {
      if (attempt < 40) {
        setTimeout(function () {
          boot(attempt + 1);
        }, 25);
      } else {
        var menu = document.getElementById("primaryNavMenu");
        if (menu) {
          var lang =
            document.documentElement.getAttribute("data-daab-lang") === "en" ? "en" : "az";
          renderMinimalFallback(menu, lang);
          document.dispatchEvent(new CustomEvent("daab-primary-nav-ready"));
        }
      }
      return;
    }
    init(api);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(0);
    });
  } else {
    boot(0);
  }
})();
