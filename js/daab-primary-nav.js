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
    "forum-2026": "forum2026Year",
    encyclopedia: "prominentFigures",
    "industrial-revolutions": "industrialRevolutions",
    "major-scientific-inventions": "majorScientificInventions",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-official": "forumOfficial",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-program": "forumProgram",
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
    return page.id || childDef.labelKey;
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
    var navLabels = ui.nav[lang] || ui.nav.az;
    var nav = document.querySelector(".nav-strip");
    if (nav) nav.setAttribute("aria-label", navLabels.ariaMain);
    var homeLogo = document.querySelector(".page-logo > a");
    var homeBrand = document.querySelector("a.nav-brand");
    var homeLabel = ui.nav[lang].ariaHome;
    var homeTooltip =
      (ui.nav[lang] && ui.nav[lang].homeLogoTooltip) ||
      (lang === "en" ? "Home page" : "Ana səhifə");
    if (homeLogo) {
      homeLogo.setAttribute("aria-label", homeLabel);
      homeLogo.setAttribute("title", homeTooltip);
    }
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

  var FORUM_PAGE_FILES = {
    "forum-2024": "index.html",
    "forum-official": "official.html",
    "forum-rector-speeches": "rector_speeches.html",
    "forum-anas-leadership-speeches": "anas_leadership_speeches.html",
    "forum-program": "program.html",
    "forum-2024-presentations": "presentations.html",
    "forum-impressions": "impressions.html",
    "forum-photos-gallery": "photos_gallery.html",
    "forum-video-gallery": "video_gallery.html",
    "forum-roadmap": "roadmap.html",
    "forum-bagli-hekayeler": "stories.html",
    "forum-cooperation": "cooperation.html"
  };

  function staticHref(name) {
    var path = location.pathname.replace(/\\/g, "/");
    var inForum2024 = /\/forum\/2024\//.test(path);
    var inForum2026 = /\/forum\/2026\//.test(path);
    var inForum = inForum2024 || inForum2026;
    var inSci = /\/scientists\//.test(path);
    var inProminent = /\/prominent_figures\//.test(path);
    var up = inForum ? "../../" : inSci ? "../" : inProminent ? "../../" : "";
    var sci = inSci ? "" : "scientists/";
    var forum2024 = inForum2024 ? "" : "forum/2024/";
    var forum2026 = inForum2026 ? "" : "forum/2026/";
    if (FORUM_PAGE_FILES[name]) {
      return up + (inForum2024 ? "" : "forum/2024/") + FORUM_PAGE_FILES[name];
    }
    var map = {
      home: up + "index.html",
      foundation: up + "foundation.html",
      mission: up + "mission.html",
      board: up + "executive-board.html",
      charter: up + "charter.html",
      list: (inSci ? "" : up + sci) + "list.html",
      profiles: (inSci ? "" : up + sci) + "profiles.html",
      activities: up + "activities.html",
      encyclopedia: up + "encyclopedia.html",
      "industrial-revolutions": up + "industrial_revolutions.html",
      "major-scientific-inventions": up + "major_scientific_inventions.html",
      "forum-2024": up + forum2024 + "index.html",
      "forum-2026": up + forum2026 + "index.html",
      "membership-value": up + "membership_value.html",
      "membership-application": up + "application.html",
      "membership-flyer": up + "membership_flyer.html",
      sponsors: up + "sponsors.html",
      donate: up + "donate.html"
    };
    return map[name] || up + "index.html";
  }

  function topNavLink(navId, title, iconKey) {
    var icon = FALLBACK_ICONS[iconKey || navId] || "";
    return (
      '<a class="nav-link" href="' +
      staticHref(navId) +
      '" data-nav-id="' +
      navId +
      '">' +
      (icon ? icon + "\u00a0" : "") +
      title +
      "</a>"
    );
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
    forum2024Year: "🎤",
    forum2026Year: "🎤",
    forums: "🎤",
    "forum-2024": "🎤",
    "forum-2026": "🎤",
    encyclopedia: "👤",
    prominentFigures: "👤",
    treasury: "🏛️",
    "industrial-revolutions": "⚙️",
    industrialRevolutions: "⚙️",
    "major-scientific-inventions": "💡",
    majorScientificInventions: "💡",
    "forum-official": "🏛️",
    "forum-rector-speeches": "🎓",
    "forum-anas-leadership-speeches": "🔬",
    "forum-program": "📅",
    "forum-2024-presentations": "📊",
    "forum-impressions": "💬",
    "forum-photos-gallery": "📷",
    "forum-video-gallery": "📹",
    "forum-roadmap": "🗺️",
    "forum-bagli-hekayeler": "📖",
    "forum-cooperation": "🤝",
    membership: "✒️",
    membershipWhy: "💡",
    membershipTerms: "✒️",
    membershipJoin: "📝",
    membershipFlyer: "📤",
    sponsors: "🤝",
    sponsorsProgram: "🤝",
    donate: "💝",
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

  function forumMegaCol(heading, items, nested) {
    var wrapClass = nested ? "nav-mega-nest" : "nav-mega-links";
    var links = items
      .map(function (item) {
        return dropLink(item[0], item[1], item[2], item[3], item[4] || "");
      })
      .join("");
    return (
      '<div class="nav-mega-col">' +
      '<div class="nav-mega-heading" role="presentation">' +
      heading +
      "</div>" +
      '<div class="' +
      wrapClass +
      '">' +
      links +
      "</div></div>"
    );
  }

  function forumMegaFallback(lang) {
    var sections;
    var label;
    if (lang === "en") {
      label = fallbackIcon("forum2024Year") + "2024";
      sections = [
        [
          "Overview",
          false,
          [
            ["forum-2024", "forum-2024", "Highlights", "First Forum of Azerbaijani Scientists Living Abroad — September 2024", "forum-2024"],
            ["forum-program", "forum-program", "Programme", "Programme of the Baku–Khankendi–Shusha forum journey", "forum-program"],
          ],
        ],
        [
          "Participants",
          true,
          [
            ["list", "scientists-list", "Directory of Scientists", "Directory of all scientists", "scientists-list"],
            ["profiles", "scientists-profiles", "Profiles of Scientists", "Academic profiles of scientists", "scientists-profiles"],
          ],
        ],
        [
          "Official record",
          false,
          [
            ["forum-official", "forum-official", "Official addresses", "Official speeches and messages that shaped the Forum", "forum-official"],
            ["forum-2024-presentations", "forum-2024-presentations", "Presentations", "Presentations on science, education, policy, and more", "forum-2024-presentations"],
          ],
        ],
        [
          "Speeches",
          true,
          [
            ["forum-rector-speeches", "forum-rector-speeches", "Rectors", "Speeches by rectors of Azerbaijani universities at Forum 2024", "forum-rector-speeches"],
            ["forum-anas-leadership-speeches", "forum-anas-leadership-speeches", "Academicians", "Speeches by academicians at Forum 2024", "forum-anas-leadership-speeches"],
          ],
        ],
        [
          "Media &amp; reflections",
          false,
          [
            ["forum-photos-gallery", "forum-photos-gallery", "Photo gallery", "Photographic story of the Forum — opening to key encounters", "forum-photos-gallery"],
            ["forum-video-gallery", "forum-video-gallery", "Video gallery", "Video reports and interviews on Forum 2024", "forum-video-gallery"],
            ["forum-impressions", "forum-impressions", "Impressions", "Participants' thoughts on the Forum and Karabakh visit", "forum-impressions"],
            ["forum-bagli-hekayeler", "forum-bagli-hekayeler", "Stories", "Literary reflections from the Forum", "forum-bagli-hekayeler"],
          ],
        ],
        [
          "Outcomes &amp; partners",
          false,
          [
            ["forum-roadmap", "forum-roadmap", "Strategic roadmap", "Ideas for science, education, and diaspora cooperation", "forum-roadmap"],
            ["forum-cooperation", "forum-cooperation", "Contributions", "Partners who supported the Forum", "forum-cooperation"],
          ],
        ],
      ];
    } else {
      label = fallbackIcon("forum2024Year") + "2024";
      sections = [
        [
          "Ümumi baxış",
          false,
          [
            ["forum-2024", "forum-2024", "Forumun mənzərəsi", "Xaricdə yaşayan alimlərin I Forumu — sentyabr 2024", "forum-2024"],
            ["forum-program", "forum-program", "Proqram", "Bakı–Xankəndi–Şuşa forum proqramı", "forum-program"],
          ],
        ],
        [
          "İştirakçılar",
          true,
          [
            ["list", "scientists-list", "Alimlərin siyahısı", "Bütün alimlərin siyahısı", "scientists-list"],
            ["profiles", "scientists-profiles", "Alimlərin profilləri", "Alimlərin akademik profilləri", "scientists-profiles"],
          ],
        ],
        [
          "Rəsmi sənədlər",
          false,
          [
            ["forum-official", "forum-official", "Rəsmi müraciətlər", "Forumun istiqamətini müəyyən edən rəsmi çıxış və müraciətlər", "forum-official"],
            ["forum-2024-presentations", "forum-2024-presentations", "Məruzələr", "Elm, təhsil və siyasət mövzularında məruzələr", "forum-2024-presentations"],
          ],
        ],
        [
          "Nitqlər",
          true,
          [
            ["forum-rector-speeches", "forum-rector-speeches", "Rektorlar", "Azərbaycan universitet rektorlarının Forum 2024 nitqləri", "forum-rector-speeches"],
            ["forum-anas-leadership-speeches", "forum-anas-leadership-speeches", "Akademiklər", "Akademiklərin Forumla bağlı görüş və nitqləri", "forum-anas-leadership-speeches"],
          ],
        ],
        [
          "Media və təəssüratlar",
          false,
          [
            ["forum-photos-gallery", "forum-photos-gallery", "Foto qalereya", "Forumun foto-hekayəsi — açılışdan əsas görüşlərə", "forum-photos-gallery"],
            ["forum-video-gallery", "forum-video-gallery", "Video qalereya", "Forum 2024 haqqında video reportajlar və müsahibələr", "forum-video-gallery"],
            ["forum-impressions", "forum-impressions", "Təəssüratlar", "İştirakçıların Forum və Qarabağ təəssüratları", "forum-impressions"],
            ["forum-bagli-hekayeler", "forum-bagli-hekayeler", "Hekayələr", "Forumun ab-havasını əks etdirən ədəbi yazılar", "forum-bagli-hekayeler"],
          ],
        ],
        [
          "Nəticələr və tərəfdaşlar",
          false,
          [
            ["forum-roadmap", "forum-roadmap", "Strateji yol xəritəsi", "Elm, təhsil və diaspora əməkdaşlığına dair təkliflər", "forum-roadmap"],
            ["forum-cooperation", "forum-cooperation", "Töhfələr", "Forumun təşkilinə dəstək verən tərəfdaşlar", "forum-cooperation"],
          ],
        ],
      ];
    }
    var cols = sections
      .map(function (section) {
        var items = section[2].map(function (row) {
          return [
            staticHref(row[0]),
            row[1],
            fallbackIcon(row[4] || row[0]) + row[2],
            row[3],
          ];
        });
        return forumMegaCol(section[0], items, section[1]);
      })
      .join("");
    var yearDesc =
      lang === "en"
        ? "First Forum of Azerbaijani Scientists Living Abroad — September 2024"
        : "Xaricdə yaşayan alimlərin I Forumu — sentyabr 2024";
    return (
      '<div class="nav-dropdown nav-dropdown--mega nav-dropdown--forum nav-dropdown--nested nav-dropdown--has-mega" data-nav-dropdown data-nav-group="forum" data-has-nested-mega="1">' +
      '<button type="button" class="nav-link nav-dropdown-toggle nav-dropdown-toggle--forum-year" aria-expanded="false" aria-haspopup="true">' +
      '<span class="nav-dropdown-link-title">' +
      label +
      "</span>" +
      '<span class="nav-dropdown-link-desc">' +
      yearDesc +
      "</span>" +
      ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel nav-dropdown-panel--mega" role="menu">' +
      '<div class="nav-mega-grid">' +
      cols +
      "</div></div></div>"
    );
  }

  function forum2026LinkFallback(lang) {
    var title = "2026";
    var desc =
      lang === "en"
        ? "Second Forum of Azerbaijani Scientists Living Abroad — in preparation"
        : "Xaricdə yaşayan alimlərin II Forumu — hazırlanır";
    return dropLink(
      staticHref("forum-2026"),
      "forum-2026",
      fallbackIcon("forum2026Year") + title,
      desc,
      ""
    );
  }

  function forumsNavFallback(lang) {
    var forumsLabel =
      lang === "en"
        ? fallbackIcon("forums") + "Forums"
        : fallbackIcon("forums") + "Forumlar";
    return (
      '<div class="nav-dropdown nav-dropdown--forums" data-nav-dropdown data-nav-group="forums">' +
      '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' +
      forumsLabel +
      ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      forumMegaFallback(lang) +
      forum2026LinkFallback(lang) +
      "</div></div>"
    );
  }

  function renderStaticFallback(menu, lang) {
    var azForum = forumsNavFallback("az");
    var enForum = forumsNavFallback("en");
    var azTreasury =
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' +
      fallbackIcon("treasury") +
      'Xəzinə <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("encyclopedia"), "encyclopedia", "Görkəmli şəxsiyyətlər", "Görkəmli şəxsiyyətlər kataloqu", FALLBACK_ICONS.prominentFigures) +
      dropLink(staticHref("industrial-revolutions"), "industrial-revolutions", "Sənaye inqilabları", "Tarixi sənaye inqilablarının izləri", FALLBACK_ICONS.industrialRevolutions) +
      dropLink(staticHref("major-scientific-inventions"), "major-scientific-inventions", "Əsas elmi ixtiralar", "Elm tarixinin mühüm ixtiraları", FALLBACK_ICONS.majorScientificInventions) +
      "</div></div>";
    var enTreasury =
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' +
      fallbackIcon("treasury") +
      'Treasury <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("encyclopedia"), "encyclopedia", "Prominent Figures", "Directory of prominent figures", FALLBACK_ICONS.prominentFigures) +
      dropLink(staticHref("industrial-revolutions"), "industrial-revolutions", "Industrial Revolutions", "Landmarks of industrial history", FALLBACK_ICONS.industrialRevolutions) +
      dropLink(staticHref("major-scientific-inventions"), "major-scientific-inventions", "Major Scientific Inventions", "Key inventions that shaped science", FALLBACK_ICONS.majorScientificInventions) +
      "</div></div>";
    var az =
      '<div class="nav-divider"></div>' +
      '<a class="nav-link" href="' + staticHref("home") + '" data-nav-id="home">' + fallbackIcon("home") + 'Ana səhifə</a>' +
      topNavLink("activities", "Fəaliyyətimiz", "activities") +
      azForum +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("about") + 'Haqqımızda <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("foundation"), "foundation", "Birliyin təsisi", "Yaradılma tarixi və təsis prosesi", FALLBACK_ICONS.foundation) +
      dropLink(staticHref("mission"), "mission", "Missiya və dəyərlər", "Missiya, vizyon və akademik dəyərlər", FALLBACK_ICONS.mission) +
      dropLink(staticHref("board"), "executive-board", "İdarə heyəti", "İdarə heyəti və rəhbərlik", FALLBACK_ICONS["executive-board"]) +
      dropLink(staticHref("charter"), "charter", "Nizamnamə", "Nizamnamə və idarəetmə qaydaları", FALLBACK_ICONS.charter) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("membership") + 'Üzvlük <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("membership-value"), "membership-value", "Niyə DAAB-a qoşulmalı", "Üzvlüyün faydaları və dəyər təklifi", FALLBACK_ICONS.membershipWhy) +
      dropLink(staticHref("membership-application"), "membership-application", "Bizə qoşulun", "Onlayn üzvlük müraciət forması", FALLBACK_ICONS.membershipJoin) +
      dropLink(staticHref("membership-flyer"), "membership-flyer", "Dəvət məktubu", "Potensial üzvlər üçün çap oluna bilən flyer", FALLBACK_ICONS.membershipFlyer) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("sponsors") + 'Bizi dəstəkləyin <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("sponsors"), "sponsors", "Sponsorluq", "Korporativ və proqram tərəfdaşlığı", FALLBACK_ICONS.sponsorsProgram) +
      dropLink(staticHref("donate"), "donate", "İanə", "Fərdi, fond və xatirə ianələri", FALLBACK_ICONS.donate) +
      '</div></div>' +
      azTreasury;
    var en =
      '<div class="nav-divider"></div>' +
      '<a class="nav-link" href="' + staticHref("home") + '" data-nav-id="home">' + fallbackIcon("home") + 'Home</a>' +
      topNavLink("activities", "Activities", "activities") +
      enForum +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("about") + 'About us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("foundation"), "foundation", "Foundation", "History and founding process", FALLBACK_ICONS.foundation) +
      dropLink(staticHref("mission"), "mission", "Mission &amp; values", "Mission, vision and academic values", FALLBACK_ICONS.mission) +
      dropLink(staticHref("board"), "executive-board", "Board of Directors", "Leadership and governance structure", FALLBACK_ICONS["executive-board"]) +
      dropLink(staticHref("charter"), "charter", "Charter", "Charter and governance rules", FALLBACK_ICONS.charter) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("membership") + 'Membership <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("membership-value"), "membership-value", "Why join WAAS", "Benefits and value of WAAS membership", FALLBACK_ICONS.membershipWhy) +
      dropLink(staticHref("membership-application"), "membership-application", "Join us", "Online membership application form", FALLBACK_ICONS.membershipJoin) +
      dropLink(staticHref("membership-flyer"), "membership-flyer", "Invitation Letter", "Printable invitation letter for potential members", FALLBACK_ICONS.membershipFlyer) +
      '</div></div>' +
      '<div class="nav-dropdown" data-nav-dropdown><button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">' + fallbackIcon("sponsors") + 'Support us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>' +
      '<div class="nav-dropdown-panel" role="menu">' +
      dropLink(staticHref("sponsors"), "sponsors", "Sponsorship", "Corporate and programme partnerships", FALLBACK_ICONS.sponsorsProgram) +
      dropLink(staticHref("donate"), "donate", "Donation", "Individual, foundation, and memorial gifts", FALLBACK_ICONS.donate) +
      '</div></div>' +
      enTreasury;
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
        if (window.DAAB_NAV && typeof window.DAAB_NAV.init === "function") {
          window.DAAB_NAV.init();
        }
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
