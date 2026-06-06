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
    "membership-flyer": "membershipFlyer",
    sponsors: "sponsorsProgram",
    donate: "donate",
    "sponsors-flyer": "sponsorsFlyer",
    encyclopedia: "prominentFigures",
    "industrial-revolutions": "industrialRevolutions",
    "major-scientific-inventions": "majorScientificInventions"
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
        navGroup: "forum",
        navParent: "forum"
      },
      {
        id: "scientists-profiles",
        az: "az/scientists/profiles.html",
        en: "en/scientists/profiles.html",
        navGroup: "forum",
        navParent: "forum"
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
      },
      {
        id: "sponsors",
        az: "az/sponsors.html",
        en: "en/sponsors.html",
        navGroup: "sponsorship",
        navParent: "sponsorship"
      },
      {
        id: "donate",
        az: "az/donate.html",
        en: "en/donate.html",
        navGroup: "sponsorship",
        navParent: "sponsorship"
      },
      {
        id: "sponsors-flyer",
        az: "az/sponsors_flyer.html",
        en: "en/sponsors_flyer.html",
        navGroup: "sponsorship",
        navParent: "sponsorship"
      },
      {
        id: "encyclopedia",
        az: "az/encyclopedia.html",
        en: "en/encyclopedia.html",
        navGroup: "treasury",
        navParent: "treasury"
      },
      {
        id: "industrial-revolutions",
        az: "az/industrial_revolutions.html",
        en: "en/industrial_revolutions.html",
        navGroup: "treasury",
        navParent: "treasury"
      },
      {
        id: "major-scientific-inventions",
        az: "az/major_scientific_inventions.html",
        en: "en/major_scientific_inventions.html",
        navGroup: "treasury",
        navParent: "treasury"
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
        membershipTitle: "Üzvlük",
        sponsorshipTitle: "Sponsorluq",
        treasuryTitle: "Xəzinə",
        forumPageTooltips: {
          "forum-2024": "Xaricdə yaşayan alimlərin I Forumu — sentyabr 2024",
          "forum-official": "Forumun istiqamətini müəyyən edən rəsmi çıxış və müraciətlər",
          "forum-rector-speeches": "Azərbaycan universitet rektorlarının Forum 2024 nitqləri",
          "forum-anas-leadership-speeches":
            "AMEA rəhbərliyinin Forumla bağlı görüş və nitqləri",
          "forum-program": "Bakı–Xankəndi–Şuşa forum proqramı",
          "forum-2024-presentations": "Elm, təhsil və siyasət mövzularında məruzələr",
          "forum-impressions": "İştirakçıların Forum və Qarabağ təəssüratları",
          "forum-photos-gallery": "Forumun foto-hekayəsi — açılışdan əsas görüşlərə",
          "forum-video-gallery": "Forum 2024 haqqında video reportajlar və müsahibələr",
          "forum-roadmap": "Elm, təhsil və diaspora əməkdaşlığına dair təkliflər",
          "forum-bagli-hekayeler": "Forumun ab-havasını əks etdirən ədəbi yazılar",
          "forum-cooperation": "Forumun təşkilinə dəstək verən tərəfdaşlar",
          "scientists-list": "Forumda iştirak etmiş alimlərin siyahısı",
          "scientists-profiles": "Alimlərin akademik profilləri"
        }
      },
      en: {
        aria: "In this section",
        aboutTitle: "About us",
        scientistsTitle: "Scientists",
        activitiesTitle: "Activities",
        forumTitle: "Forum 2024",
        membershipTitle: "Membership",
        sponsorshipTitle: "Sponsorship",
        treasuryTitle: "Treasury",
        forumPageTooltips: {
          "forum-2024":
            "First Forum of Azerbaijani Scientists Living Abroad — September 2024",
          "forum-official": "Official speeches and messages that shaped the Forum",
          "forum-rector-speeches":
            "Speeches by rectors of Azerbaijani universities at Forum 2024",
          "forum-anas-leadership-speeches": "Speeches by ANAS leadership at Forum 2024",
          "forum-program": "Programme of the Baku–Khankendi–Shusha forum journey",
          "forum-2024-presentations": "Presentations on science, education, policy, and more",
          "forum-impressions": "Participants' thoughts on the Forum and Karabakh visit",
          "forum-photos-gallery":
            "Photographic story of the Forum — opening to key encounters",
          "forum-video-gallery": "Video reports and interviews on Forum 2024",
          "forum-roadmap": "Ideas for science, education, and diaspora cooperation",
          "forum-bagli-hekayeler": "Literary reflections from the Forum",
          "forum-cooperation": "Partners who supported the Forum",
          "scientists-list": "Directory of scientists who took part in the Forum",
          "scientists-profiles": "Academic profiles of participating scientists"
        }
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
      membershipFlyer: "📤",
      sponsorsProgram: "🤝",
      donate: "💝",
      sponsorsFlyer: "📤"
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
        scientistsList: "Alimlərin siyahısı",
        scientistsProfiles: "Alimlərin profilləri",
        membershipWhy: "Niyə DAAB-a qoşulmalı",
        membershipTerms: "Üzvlük şərtləri",
        membershipJoin: "Bizə qoşulun",
        membershipFlyer: "Dəvət məktubu",
        sponsorsProgram: "Sponsorluq",
        donate: "İanə",
        sponsorsFlyer: "Dəvət məktubu",
        sponsorsProgramDesc: "Korporativ və proqram tərəfdaşlığı",
        donateDesc: "Fərdi, fond və xatirə ianələri",
        sponsorsFlyerDesc: "Potensial tərəfdaşlar üçün paylaşıla bilən dəvət məktubu"
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
        membershipWhy: "Why join WAAS",
        membershipTerms: "Membership terms",
        membershipJoin: "Join us",
        membershipFlyer: "Send invitation",
        sponsorsProgram: "Sponsorship",
        donate: "Donation",
        sponsorsFlyer: "Invitation letter",
        sponsorsProgramDesc: "Corporate and programme partnerships",
        donateDesc: "Individual, foundation, and memorial gifts",
        sponsorsFlyerDesc: "Printable invitation letter for potential partners"
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
          "forum-cooperation",
          "scientists-list",
          "scientists-profiles"
        ]
      },
      membership: {
        landingId: "membership-value",
        pages: ["membership-value", "membership-application", "membership-flyer"]
      },
      sponsorship: {
        landingId: "sponsors",
        pages: ["sponsors", "donate", "sponsors-flyer"]
      },
      treasury: {
        landingId: "encyclopedia",
        pages: ["encyclopedia", "industrial-revolutions", "major-scientific-inventions"]
      }
    }
  };

  /** Forum 2024 panel — three rows of pills (see daab-forum-section-nav.css). */
  var FORUM_PANEL_ROWS = [
    [
      "forum-2024",
      "forum-official",
      "forum-rector-speeches",
      "forum-anas-leadership-speeches",
      "forum-program",
      "forum-2024-presentations"
    ],
    [
      "forum-impressions",
      "forum-photos-gallery",
      "forum-video-gallery",
      "forum-roadmap",
      "forum-bagli-hekayeler",
      "forum-cooperation"
    ],
    ["scientists-list", "scientists-profiles"]
  ];

  /** Shared min-width groups for paired Forum 2024 pills. */
  var FORUM_PANEL_WIDTH_GROUPS = [
    ["forum-2024", "forum-official", "forum-photos-gallery"],
    ["forum-rector-speeches", "forum-video-gallery"],
    ["forum-anas-leadership-speeches", "forum-roadmap"],
    ["forum-program", "forum-bagli-hekayeler"],
    ["forum-cooperation", "forum-2024-presentations"],
    ["scientists-list", "scientists-profiles"]
  ];

  function forumPanelColumnWidthGroups() {
    var groups = [];
    var topRow = FORUM_PANEL_ROWS[0] || [];
    var bottomRow = FORUM_PANEL_ROWS[1] || [];
    topRow.forEach(function (topId, index) {
      var bottomId = bottomRow[index];
      if (!bottomId) return;
      groups.push([topId, bottomId]);
    });
    return groups;
  }

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

  function forumSectionPageIds() {
    var ids = [];
    FORUM_PANEL_ROWS.forEach(function (row) {
      row.forEach(function (id) {
        if (ids.indexOf(id) === -1) ids.push(id);
      });
    });
    return ids;
  }

  function isForumSectionPageId(pageId) {
    return forumSectionPageIds().indexOf(pageId) !== -1;
  }

  function forumSectionTooltip(ui, lang, pageId) {
    if (!pageId || !isForumSectionPageId(pageId)) return "";
    var sectionUi = ui.sectionNav && ui.sectionNav[lang];
    var tips = sectionUi && sectionUi.forumPageTooltips;
    return (tips && tips[pageId]) || "";
  }

  function applyForumNavLinkTooltip(a, ui, lang, pageId) {
    var tip = forumSectionTooltip(ui, lang, pageId);
    if (tip) a.setAttribute("title", tip);
  }

  function sectionNavPageTooltip(navLabels, pageId) {
    if (!navLabels || !pageId || isForumSectionPageId(pageId)) return "";
    var key = PAGE_LABEL_KEYS[pageId];
    if (!key) return "";
    return navLabels[key + "Desc"] || "";
  }

  function applySectionNavLinkTooltip(a, ui, lang, pageId, navLabels) {
    if (isForumSectionPageId(pageId)) {
      applyForumNavLinkTooltip(a, ui, lang, pageId);
      return;
    }
    var tip = sectionNavPageTooltip(navLabels, pageId);
    if (tip) a.setAttribute("title", tip);
  }

  function createSectionNavAnchor(p, currentPage, I18N, lang, ui, navLabels) {
    var a = document.createElement("a");
    a.href = pageHref(I18N, p, lang);
    a.setAttribute("data-section-nav-page", p.id);
    var key = PAGE_LABEL_KEYS[p.id];
    var fallbackNav = FALLBACK_UI.nav[lang] || {};
    var label =
      (key && navLabels[key]) ||
      (key && fallbackNav[key]) ||
      p.id;
    var icon = sectionNavIcon(ui, p.id);
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
    if (p.id === currentPage.id) {
      a.classList.add("active");
      a.setAttribute("aria-current", "page");
    }
    applySectionNavLinkTooltip(a, ui, lang, p.id, navLabels);
    return a;
  }

  function buildForumPairedList(section, routes, currentPage, I18N, lang, ui, navLabels) {
    var list = document.createElement("ul");
    list.className = "daab-section-nav-list daab-section-nav-list--forum-pairs";

    FORUM_PANEL_ROWS.forEach(function (rowIds, rowIndex) {
      var rowLi = document.createElement("li");
      rowLi.className = "daab-section-nav-row";
      rowIds.forEach(function (pid, colIndex) {
        if (section.pages.indexOf(pid) === -1) return;
        var p = pageById(routes, pid);
        if (!p) return;
        var a = createSectionNavAnchor(p, currentPage, I18N, lang, ui, navLabels);
        a.style.gridRow = String(rowIndex + 1);
        a.style.gridColumn = String(colIndex + 1);
        rowLi.appendChild(a);
      });
      if (rowLi.children.length) {
        list.appendChild(rowLi);
      }
    });

    return list;
  }

  function buildSectionNavList(section, routes, currentPage, I18N, lang, ui, navLabels, navGroup) {
    if (navGroup === "forum") {
      return buildForumPairedList(section, routes, currentPage, I18N, lang, ui, navLabels);
    }

    var list = document.createElement("ul");
    list.className = "daab-section-nav-list";

    section.pages.forEach(function (pid) {
      var p = pageById(routes, pid);
      if (!p) return;
      var li = document.createElement("li");
      li.appendChild(createSectionNavAnchor(p, currentPage, I18N, lang, ui, navLabels));
      list.appendChild(li);
    });

    return list;
  }

  var FORUM_PANEL_DESKTOP_MIN = 1080;

  function syncForumNavButtonWidths() {
    var list = document.querySelector(
      'html[data-daab-page-id^="forum-"] .daab-section-nav-list--forum-pairs'
    );
    if (!list) return;

    var links = list.querySelectorAll("a[data-section-nav-page]");
    var useDesktopWidths = window.innerWidth >= FORUM_PANEL_DESKTOP_MIN;

    links.forEach(function (a) {
      a.style.minWidth = "";
    });

    if (!useDesktopWidths) return;

    var minById = {};
    links.forEach(function (a) {
      minById[a.getAttribute("data-section-nav-page")] = 0;
    });

    function applyGroup(ids) {
      var groupLinks = ids
        .map(function (id) {
          return list.querySelector('a[data-section-nav-page="' + id + '"]');
        })
        .filter(Boolean);
      if (!groupLinks.length) return;

      var max = 0;
      groupLinks.forEach(function (a) {
        max = Math.max(max, Math.ceil(a.getBoundingClientRect().width));
      });
      if (max <= 0) return;
      ids.forEach(function (id) {
        if (minById[id] !== undefined) {
          minById[id] = Math.max(minById[id], max);
        }
      });
    }

    forumPanelColumnWidthGroups().forEach(applyGroup);
    FORUM_PANEL_WIDTH_GROUPS.forEach(applyGroup);

    links.forEach(function (a) {
      var id = a.getAttribute("data-section-nav-page");
      var min = minById[id];
      if (min > 0) {
        a.style.minWidth = min + "px";
      }
    });
  }

  var forumNavSyncTimer = 0;
  function scheduleForumNavSync() {
    if (forumNavSyncTimer) {
      window.clearTimeout(forumNavSyncTimer);
    }
    forumNavSyncTimer = window.setTimeout(function () {
      forumNavSyncTimer = 0;
      syncForumNavButtonWidths();
    }, 50);
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
    if (!a.getAttribute("data-section-nav-page")) {
      a.setAttribute("data-section-nav-page", pid);
    }
  }

  function decorateEmbeddedSectionNav(ui, routes, lang) {
    var nav = document.querySelector(".daab-section-nav");
    if (!nav) return;
    var navLabels = ui.nav && ui.nav[lang];
    var alreadyEnhanced = nav.getAttribute("data-daab-section-nav-enhanced") === "1";
    nav.querySelectorAll(".daab-section-nav-list a").forEach(function (a) {
      if (!alreadyEnhanced) {
        enhanceSectionNavLink(a, ui, routes);
      }
      var pid =
        a.getAttribute("data-section-nav-page") ||
        a.getAttribute("data-nav-id") ||
        pageIdFromHref(a.getAttribute("href"), routes);
      applySectionNavLinkTooltip(a, ui, lang, pid, navLabels);
    });
    if (!alreadyEnhanced) {
      nav.setAttribute("data-daab-section-nav-enhanced", "1");
    }
    scheduleForumNavSync();
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

  var HERO_HEADER_SEL = "header.forum-hero, header.page-hero, header.hero, section.hero";

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

        var list = buildSectionNavList(section, routes, page, I18N, lang, ui, navLabels, page.navGroup);
        nav.appendChild(list);
        if (insertPoint.before) {
          insertPoint.parent.insertBefore(nav, insertPoint.before);
        } else {
          insertPoint.parent.appendChild(nav);
        }
        sectionNavInserted = true;
        scheduleForumNavSync();
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
      var bootLang = I18N.detectLang();
      loadData(I18N)
        .then(function (results) {
          decorateEmbeddedSectionNav(
            results[1] || FALLBACK_UI,
            results[0] || FALLBACK_ROUTES,
            bootLang
          );
        })
        .catch(function () {
          decorateEmbeddedSectionNav(FALLBACK_UI, FALLBACK_ROUTES, bootLang);
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
      scheduleForumNavSync();
      setTimeout(function () {
        if (!sectionNavInserted) boot(0);
      }, 200);
      setTimeout(function () {
        if (!sectionNavInserted) boot(0);
        scheduleForumNavSync();
      }, 800);
    },
    { once: true }
  );

  window.addEventListener("resize", scheduleForumNavSync, { passive: true });
  window.addEventListener("orientationchange", scheduleForumNavSync, { passive: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(0);
    });
  } else {
    boot(0);
  }
})();
