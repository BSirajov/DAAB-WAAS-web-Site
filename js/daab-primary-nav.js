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
    forum2024: "forum2024",
    "forum-2024": "forum2024",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-official": "forumOfficial",
    "forum-program": "forumProgram",
    "forum-impressions": "forumImpressions",
    "forum-roadmap": "forumRoadmap",
    "forum-bagli-hekayeler": "forumBagliHekayeler",
    "forum-cooperation": "forumCooperation",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    charter: "charter",
    membership: "membership"
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

  function currentPageId(routes) {
    return activeI18n.getPageId(routes) || document.documentElement.getAttribute("data-daab-page-id");
  }

  function isForumNavPageId(id) {
    if (window.DAAB_NAV && typeof window.DAAB_NAV.isForumNavPageId === "function") {
      return window.DAAB_NAV.isForumNavPageId(id);
    }
    return id === "forum-2024" || (typeof id === "string" && id.indexOf("forum-") === 0);
  }

  function childLinkIsActive(page, childDef, activeId) {
    if (page.id === activeId) return true;
    if (childDef.id === "forum-2024" && isForumNavPageId(activeId) && activeId !== "activities") {
      return true;
    }
    return false;
  }

  function buildLink(page, lang, ui, activeId, className, extra) {
    var a = document.createElement("a");
    a.href = pageHref(page, lang);
    a.className = className;
    a.setAttribute("data-nav-id", page.navId || page.id);
    if (extra && extra.role) a.setAttribute("role", extra.role);
    a.textContent = labelWithIcon(ui, page.id, pageLabel(ui, lang, page.id));
    if (page.id === activeId) {
      a.classList.add("active");
      a.setAttribute("aria-current", "page");
    }
    return a;
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
      var page = pageById(routes, childDef.id);
      if (!page) return;
      var link = document.createElement("a");
      link.href = pageHref(page, lang);
      link.className = "nav-dropdown-link";
      link.setAttribute("role", "menuitem");
      link.setAttribute("data-nav-id", page.navId || page.id);

      var iconKey = childDef.labelKey || page.id;
      var title = document.createElement("span");
      title.className = "nav-dropdown-link-title";
      title.textContent = labelWithIcon(ui, iconKey, childLabel(ui, lang, childDef, page));
      link.appendChild(title);

      if (childDef.descKey) {
        var descText = label(ui, lang, childDef.descKey);
        if (descText && descText !== childDef.descKey) {
          var desc = document.createElement("span");
          desc.className = "nav-dropdown-link-desc";
          desc.textContent = descText;
          link.appendChild(desc);
        }
      }

      if (childLinkIsActive(page, childDef, activeId)) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
        groupActive = true;
      }
      panel.appendChild(link);
    });

    if (groupActive) wrap.classList.add("has-active-child");

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
        frag.appendChild(buildGroup(item, routes, lang, ui, activeId));
      }
    });

    return frag;
  }

  function applyNavAria(ui, lang) {
    var navLabels = ui.nav[lang] || ui.nav.az;
    var nav = document.querySelector(".nav-strip");
    if (nav) nav.setAttribute("aria-label", navLabels.ariaMain);
    var homeLogo = document.querySelector(".page-logo > a");
    var homeBrand = document.querySelector("a.nav-brand");
    var homeLabel = ui.nav[lang].ariaHome;
    if (homeLogo) homeLogo.setAttribute("aria-label", homeLabel);
    if (homeBrand) homeBrand.setAttribute("aria-label", homeLabel);
    var toggle = document.querySelector(".mobile-menu-toggle");
    if (toggle && !toggle.getAttribute("data-daab-menu-labels")) {
      toggle.setAttribute("data-daab-menu-labels", "1");
      toggle.setAttribute("aria-label", ui.nav[lang].menuOpen);
      toggle.setAttribute("data-label-open", ui.nav[lang].menuOpen);
      toggle.setAttribute("data-label-close", ui.nav[lang].menuClose);
    }
    var skip = document.querySelector("a.skip");
    if (skip) skip.textContent = ui.nav[lang].skip;
  }

  function staticHref(name) {
    var path = location.pathname.replace(/\\/g, "/");
    var inForum = /\/forum\/2024\//.test(path);
    var inSci = /\/scientists\//.test(path);
    var up = inForum ? "../../" : inSci ? "../" : "";
    var sci = inSci ? "" : "scientists/";
    var forum = inForum ? "" : "forum/2024/";
    var map = {
      home: up + "index.html",
      foundation: up + "foundation.html",
      mission: up + "mission.html",
      board: up + "executive-board.html",
      charter: up + "charter.html",
      list: (inSci ? "" : up + sci) + "list.html",
      profiles: (inSci ? "" : up + sci) + "profiles.html",
      activities: up + "activities.html",
      "forum-2024": up + forum + "index.html",
      membership: up + "membership.html"
    };
    return map[name] || up + "index.html";
  }

  function dropLink(href, navId, title, desc, icon) {
    var iconPart = icon ? icon + "\u00a0" : "";
    var descPart = desc
      ? '<span class="nav-dropdown-link-desc">' + desc + '</span>'
      : '';
    return (
      '<a class="nav-dropdown-link" role="menuitem" href="' + href + '" data-nav-id="' + navId + '">' +
      '<span class="nav-dropdown-link-title">' + iconPart + title + '</span>' + descPart +
      '</a>'
    );
  }

  var FALLBACK_ICONS = {
    home: "🏠",
    activities: "📰",
    activitiesNews: "📰",
    forum2024: "🎤",
    "forum-2024": "🎤",
    membership: "✒️",
    about: "🏛️",
    scientists: "🌐",
    foundation: "🏛️",
    mission: "💎",
    "executive-board": "🎓",
    charter: "📜",
    "scientists-list": "📋",
    "scientists-profiles": "👤"
  };

  function fallbackIcon(key) {
    var icon = FALLBACK_ICONS[key];
    return icon ? icon + "\u00a0" : "";
  }

  function renderStaticFallback(menu, lang) {
    var az =
      '<div class="nav-divider"></div>' +
      '<a class="nav-link" href="' + staticHref("home") + '" data-nav-id="home">' + fallbackIcon("home") + 'Ana səhifə</a>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("activities") + 'Fəaliyyətimiz <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("activities"), "activities", "Yeniliklər", "Əsas fəaliyyət və yeniliklər", FALLBACK_ICONS.activitiesNews) +
      dropLink(staticHref("forum-2024"), "forum-2024", "Forum 2024", "Forum 2024 kitabı və bölmələr", FALLBACK_ICONS["forum-2024"]) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("scientists") + 'Alimlərimiz <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("list"), "scientists-list", "Siyahı", "Bütün alimlərin siyahısı", FALLBACK_ICONS["scientists-list"]) +
      dropLink(staticHref("profiles"), "scientists-profiles", "Profillər", "Alimlərin akademik profilləri", FALLBACK_ICONS["scientists-profiles"]) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("about") + 'Haqqımızda <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("foundation"), "foundation", "Birliyin təsisi", "Yaradılma tarixi və təsis prosesi", FALLBACK_ICONS.foundation) +
      dropLink(staticHref("mission"), "mission", "Missiya və dəyərlər", "Missiya, vizyon və akademik dəyərlər", FALLBACK_ICONS.mission) +
      dropLink(staticHref("board"), "executive-board", "İdarə heyəti", "İdarə heyəti və rəhbərlik", FALLBACK_ICONS["executive-board"]) +
      dropLink(staticHref("charter"), "charter", "Nizamnamə", "Nizamnamə və idarəetmə qaydaları", FALLBACK_ICONS.charter) +
      '</div></div>' +
      '<a class="nav-link" href="' + staticHref("membership") + '" data-nav-id="membership">' + fallbackIcon("membership") + 'Üzvlük</a>';
    var en =
      '<div class="nav-divider"></div>' +
      '<a class="nav-link" href="' + staticHref("home") + '" data-nav-id="home">' + fallbackIcon("home") + 'Home</a>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("activities") + 'Activities <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("activities"), "activities", "News", "News and updates", FALLBACK_ICONS.activitiesNews) +
      dropLink(staticHref("forum-2024"), "forum-2024", "Forum 2024", "Forum 2024 book and sections", FALLBACK_ICONS["forum-2024"]) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("scientists") + 'Scientists <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("list"), "scientists-list", "Directory", "Directory of all scientists", FALLBACK_ICONS["scientists-list"]) +
      dropLink(staticHref("profiles"), "scientists-profiles", "Profiles", "Academic profiles of scientists", FALLBACK_ICONS["scientists-profiles"]) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("about") + 'About <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("foundation"), "foundation", "Foundation", "History and founding process", FALLBACK_ICONS.foundation) +
      dropLink(staticHref("mission"), "mission", "Mission &amp; values", "Mission, vision and academic values", FALLBACK_ICONS.mission) +
      dropLink(staticHref("board"), "executive-board", "Executive board", "Leadership and governance structure", FALLBACK_ICONS["executive-board"]) +
      dropLink(staticHref("charter"), "charter", "Charter", "Charter and governance rules", FALLBACK_ICONS.charter) +
      '</div></div>' +
      '<a class="nav-link" href="' + staticHref("membership") + '" data-nav-id="membership">' + fallbackIcon("membership") + 'Membership</a>';
    menu.innerHTML = lang === "en" ? en : az;
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
        applyNavAria(ui, lang);

        if (window.DAAB_NAV && typeof window.DAAB_NAV.init === "function") {
          window.DAAB_NAV.init();
        }
        document.dispatchEvent(new CustomEvent("daab-primary-nav-ready"));
      })
      .catch(function (err) {
        console.error("[daab-primary-nav] Menu build failed:", err);
        renderStaticFallback(menu, lang);
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
          renderStaticFallback(menu, lang);
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
