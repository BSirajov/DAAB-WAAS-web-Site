(function () {
  "use strict";

  function navCompactMediaQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.navCompactMq === "function") {
      return window.DAAB_DESIGN.navCompactMq();
    }
    return window.matchMedia("(max-width: 1180px)");
  }

  var MOBILE_NAV_MQ = navCompactMediaQuery();

  function isMobileNav() {
    return MOBILE_NAV_MQ.matches;
  }

  var menuToggleRef = null;
  var navMenuRef = null;

  function closeAllDropdowns() {
    document.querySelectorAll("[data-nav-dropdown].open").forEach(function (dropdown) {
      dropdown.classList.remove("open");
      var btn = dropdown.querySelector(".nav-dropdown-toggle");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function setBodyScrollLock(on) {
    if (window.DAAB_SCROLL_LOCK && typeof window.DAAB_SCROLL_LOCK.set === "function") {
      window.DAAB_SCROLL_LOCK.set(on);
      return;
    }
    document.body.classList.toggle("daab-scroll-lock", on);
  }

  function syncScrollLockFromUi() {
    if (window.DAAB_SCROLL_LOCK && typeof window.DAAB_SCROLL_LOCK.update === "function") {
      window.DAAB_SCROLL_LOCK.update();
      return;
    }
    var searchOpen = document.getElementById("search-overlay")?.classList.contains("open");
    var menuOpen = navMenuRef?.classList.contains("open");
    setBodyScrollLock(!!(menuOpen || searchOpen));
  }

  function menuLabel(toggle, which) {
    var key = which === "close" ? "data-label-close" : "data-label-open";
    return toggle.getAttribute(key) || (which === "close" ? "Menyunu bağla" : "Menyunu aç");
  }

  function closeMobileMenu() {
    var menuToggle = menuToggleRef || document.querySelector(".mobile-menu-toggle");
    var navMenu = navMenuRef || document.getElementById("primaryNavMenu");
    if (!menuToggle || !navMenu) return;

    navMenu.classList.remove("open");
    document.querySelector(".nav-strip")?.classList.remove("is-menu-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", menuLabel(menuToggle, "open"));
    closeAllDropdowns();
    syncScrollLockFromUi();
  }

  function syncNavHeight() {
    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
      return;
    }
    var strip = document.querySelector(".nav-strip");
    if (!strip) return;
    var h = Math.ceil(strip.getBoundingClientRect().height);
    if (h > 0) {
      document.documentElement.style.setProperty("--daab-nav-height", h + "px");
    }
  }

  var resizeTimer = 0;
  function onViewportChange() {
    syncNavHeight();
    document.querySelectorAll(".nav-dropdown--forums .nav-dropdown--nested.is-forum-mega-open").forEach(function (nested) {
      nested.classList.remove("is-forum-mega-open");
    });
    if (!isMobileNav()) {
      closeMobileMenu();
    }
  }

  function scheduleNavHeightSync() {
    if (resizeTimer) window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(syncNavHeight, 50);
  }

  function initMobileNav() {
    var menuToggle = document.querySelector(".mobile-menu-toggle");
    var navMenu = document.getElementById("primaryNavMenu");
    if (!menuToggle || !navMenu) return;

    menuToggleRef = menuToggle;
    navMenuRef = navMenu;

    menuToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = navMenu.classList.toggle("open");
      var root = document.documentElement;
      if (open) {
        var scrollY = window.scrollY || root.scrollTop || 0;
        root.style.setProperty("--daab-scroll-lock-y", scrollY + "px");
      }
      document.querySelector(".nav-strip")?.classList.toggle("is-menu-open", open);
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
      menuToggle.setAttribute("aria-label", open ? menuLabel(menuToggle, "close") : menuLabel(menuToggle, "open"));
      if (!open) {
        closeAllDropdowns();
      } else {
        document.querySelectorAll("[data-nav-dropdown].has-active-child").forEach(function (dropdown) {
          dropdown.classList.add("open");
          var btn = dropdown.querySelector(".nav-dropdown-toggle");
          if (btn) btn.setAttribute("aria-expanded", "true");
        });
      }
      syncScrollLockFromUi();
      scheduleNavHeightSync();
    });

    navMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMobileMenu);
    });

    document.addEventListener("click", function (event) {
      if (!navMenu.classList.contains("open")) return;
      if (navMenu.contains(event.target) || menuToggle.contains(event.target)) return;
      closeMobileMenu();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navMenu.classList.contains("open")) {
        closeMobileMenu();
      }
    });
  }

  var TOUCH_UI_MQ = window.matchMedia("(hover: none), (pointer: coarse)");

  function needsTapDropdown() {
    return isMobileNav() || TOUCH_UI_MQ.matches;
  }

  function siteRelativePath() {
    var path = location.pathname.replace(/\\/g, "/");
    var m = path.match(/\/(az|en)\/(.+)$/i);
    if (m) return m[2].toLowerCase();
    var base = path.split("/").pop() || "";
    return base ? base.toLowerCase() : "index.html";
  }

  function currentNavKey() {
    var pageId = (document.documentElement.getAttribute("data-daab-page-id") || "").trim();
    if (pageId) return pageId;

    var rel = siteRelativePath();
    var file = rel.split("/").pop() || "index.html";
    var navLinks = document.querySelectorAll("a[data-nav-id]");
    var i;
    for (i = 0; i < navLinks.length; i++) {
      var href = navLinks[i].getAttribute("href");
      if (!href) continue;
      href = href.split("#")[0].split("?")[0].replace(/\\/g, "/").toLowerCase();
      if (href === rel || href.endsWith("/" + rel)) {
        return navLinks[i].getAttribute("data-nav-id");
      }
    }
    if (rel.indexOf("/") === -1) {
      for (i = 0; i < navLinks.length; i++) {
        if (hrefMatchesNav(navLinks[i].getAttribute("href"), file)) {
          return navLinks[i].getAttribute("data-nav-id");
        }
      }
    }
    return file;
  }

  function hrefMatchesNav(linkHref, pagePath) {
    if (!linkHref || !pagePath) return false;
    var href = linkHref.split("#")[0].split("?")[0].replace(/\\/g, "/").toLowerCase();
    pagePath = pagePath.replace(/\\/g, "/").toLowerCase();
    if (href === pagePath) return true;
    /* Locale home is index.html only — not forum/.../index.html or other nested index pages. */
    if (pagePath === "index.html") return false;
    if (href.endsWith("/" + pagePath)) return true;
    return false;
  }

  /** Forum hub + forum content pages (forum-official, forum-program, …). */
  function isForumNavPageId(id) {
    return id === "forum-2024" || (typeof id === "string" && id.indexOf("forum-") === 0);
  }

  /** Membership submenu pages (value, terms, application). */
  function isMembershipNavPageId(id) {
    return (
      id === "membership" ||
      id === "membership-value" ||
      id === "membership-application"
    );
  }

  function clearNavActiveStates() {
    var menu = document.getElementById("primaryNavMenu");
    var scope = menu ? menu.querySelectorAll("a.active, a[aria-current]") : document.querySelectorAll(".nav-menu a.active, .nav-menu a[aria-current]");
    scope.forEach(function (link) {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    });
    document.querySelectorAll("[data-nav-dropdown].has-active-child").forEach(function (dropdown) {
      dropdown.classList.remove("has-active-child");
    });
  }

  /**
   * Match nav link to current page. When data-daab-page-id is set, use ids only
   * (avoids false positives from many pages named index.html).
   */
  function navLinkIsActive(id, href, navKey, pageIdAttr, relPath) {
    if (!navKey) return false;
    if (id && id === navKey) return true;
    /* When data-daab-page-id is set, match by id only (see comment above navLinkIsActive). */
    if (pageIdAttr) return false;
    return hrefMatchesNav(href, relPath);
  }

  var dropdownToggleAttached = new WeakSet();
  var forumsSubmenuAttached = new WeakSet();
  var FORUM_MEGA_CLOSE_DELAY_MS = 200;

  function setForumMegaOpen(nested, open) {
    if (!nested) return;
    nested.classList.toggle("is-forum-mega-open", !!open);
    if (!needsTapDropdown()) {
      var btn = nested.querySelector(":scope > .nav-dropdown-toggle");
      if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
  }

  function closeForumsNestedMega(exceptDropdown) {
    document.querySelectorAll(".nav-dropdown--forums .nav-dropdown--nested").forEach(function (nested) {
      if (exceptDropdown && nested === exceptDropdown) return;
      nested.classList.remove("open");
      nested.classList.remove("is-forum-mega-open");
      var btn = nested.querySelector(":scope > .nav-dropdown-toggle");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  /**
   * Forums submenu: show the 2024 mega panel only while the pointer is on 2024
   * (or its mega grid). Hide immediately when moving to leaf items such as 2026.
   */
  function initForumsSubmenuBehavior() {
    document.querySelectorAll(".nav-dropdown--forums").forEach(function (forumsDrop) {
      if (forumsSubmenuAttached.has(forumsDrop)) return;

      var panel = forumsDrop.querySelector(":scope > .nav-dropdown-panel");
      if (!panel) return;

      var megaNested = panel.querySelector(":scope > .nav-dropdown--nested.nav-dropdown--has-mega");
      if (!megaNested) return;

      forumsSubmenuAttached.add(forumsDrop);

      var leafLinks = panel.querySelectorAll(":scope > .nav-dropdown-link--forum-year");
      var closeTimer = 0;

      function cancelCloseTimer() {
        if (!closeTimer) return;
        window.clearTimeout(closeTimer);
        closeTimer = 0;
      }

      function openMegaNow() {
        if (needsTapDropdown()) return;
        cancelCloseTimer();
        setForumMegaOpen(megaNested, true);
      }

      function closeMegaNow() {
        cancelCloseTimer();
        setForumMegaOpen(megaNested, false);
        if (needsTapDropdown()) {
          megaNested.classList.remove("open");
          var btn = megaNested.querySelector(":scope > .nav-dropdown-toggle");
          if (btn) btn.setAttribute("aria-expanded", "false");
        }
      }

      function scheduleCloseMega() {
        if (needsTapDropdown()) return;
        cancelCloseTimer();
        closeTimer = window.setTimeout(function () {
          closeTimer = 0;
          setForumMegaOpen(megaNested, false);
        }, FORUM_MEGA_CLOSE_DELAY_MS);
      }

      function isInsideMegaZone(node) {
        return !!(node && megaNested.contains(node));
      }

      if (!needsTapDropdown()) {
        megaNested.addEventListener("mouseenter", openMegaNow);

        var megaPanel = megaNested.querySelector(":scope > .nav-dropdown-panel--mega");
        if (megaPanel) {
          megaPanel.addEventListener("mouseenter", openMegaNow);
        }

        megaNested.addEventListener("mouseleave", function (event) {
          if (isInsideMegaZone(event.relatedTarget)) return;
          scheduleCloseMega();
        });

        panel.addEventListener("mouseleave", function (event) {
          if (isInsideMegaZone(event.relatedTarget)) return;
          if (event.relatedTarget && panel.contains(event.relatedTarget)) return;
          closeMegaNow();
        });
      }

      leafLinks.forEach(function (link) {
        if (dropdownToggleAttached.has(link)) return;
        dropdownToggleAttached.add(link);

        link.addEventListener("mouseenter", closeMegaNow);
        link.addEventListener("focus", closeMegaNow);
        link.addEventListener("click", function () {
          closeForumsNestedMega(null);
        });
      });
    });
  }

  function closeSiblingDropdowns(dropdown) {
    var parent = dropdown.parentElement;
    if (!parent) return;
    Array.prototype.forEach.call(parent.children, function (child) {
      if (child === dropdown || !child.matches || !child.matches("[data-nav-dropdown]")) return;
      child.classList.remove("open");
      var btn = child.querySelector(":scope > .nav-dropdown-toggle");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function markAncestorDropdownsActive(dropdown) {
    var node = dropdown.parentElement;
    while (node) {
      var parentDropdown = node.closest ? node.closest("[data-nav-dropdown]") : null;
      if (!parentDropdown || parentDropdown === dropdown) break;
      parentDropdown.classList.add("has-active-child");
      node = parentDropdown.parentElement;
      dropdown = parentDropdown;
    }
  }

  function initNavDropdowns() {
    var pageIdAttr = (document.documentElement.getAttribute("data-daab-page-id") || "").trim() || null;
    var navKey = currentNavKey();
    var relPath = siteRelativePath();
    var dropdowns = document.querySelectorAll("[data-nav-dropdown]");

    clearNavActiveStates();

    dropdowns.forEach(function (dropdown) {
      var toggle = dropdown.querySelector(".nav-dropdown-toggle");
      var links = dropdown.querySelectorAll(".nav-dropdown-link, .nav-mega-link");
      if (!toggle) return;

      links.forEach(function (link) {
        var id = link.getAttribute("data-nav-id");
        var href = link.getAttribute("href");
        if (navLinkIsActive(id, href, navKey, pageIdAttr, relPath)) {
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
          dropdown.classList.add("has-active-child");
          markAncestorDropdownsActive(dropdown);
        }
      });

      if (!dropdownToggleAttached.has(toggle)) {
        dropdownToggleAttached.add(toggle);
        toggle.addEventListener("click", function (event) {
          if (!needsTapDropdown()) return;
          event.preventDefault();
          event.stopPropagation();
          var willOpen = !dropdown.classList.contains("open");
          closeSiblingDropdowns(dropdown);
          dropdown.classList.toggle("open", willOpen);
          toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
        });
      }
    });

    document.querySelectorAll(".nav-menu > a.nav-link[data-nav-id]").forEach(function (link) {
      var id = link.getAttribute("data-nav-id");
      var href = link.getAttribute("href");
      if (navLinkIsActive(id, href, navKey, pageIdAttr, relPath)) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      }
    });
  }

  var documentListenersAttached = false;
  var mobileInitialized = false;
  var menuLinkHandlerAttached = new WeakSet();
  var viewportListenersAttached = false;

  function attachViewportListeners() {
    if (viewportListenersAttached) return;
    viewportListenersAttached = true;

    if (typeof MOBILE_NAV_MQ.addEventListener === "function") {
      MOBILE_NAV_MQ.addEventListener("change", onViewportChange);
    } else if (typeof MOBILE_NAV_MQ.addListener === "function") {
      MOBILE_NAV_MQ.addListener(onViewportChange);
    }

    window.addEventListener("resize", scheduleNavHeightSync, { passive: true });
    window.addEventListener("orientationchange", scheduleNavHeightSync, { passive: true });

    if (typeof ResizeObserver !== "undefined") {
      var strip = document.querySelector(".nav-strip");
      if (strip) {
        var ro = new ResizeObserver(scheduleNavHeightSync);
        ro.observe(strip);
      }
    }
  }

  function wrapFooterContactColumn(contactCol) {
    if (!contactCol || contactCol.querySelector(".footer-contact-layout")) return;
    contactCol.classList.add("footer-col--contact");
    var nodes = Array.prototype.slice.call(contactCol.childNodes);
    var existingQr = contactCol.querySelector(".footer-home-qr");
    var layout = document.createElement("div");
    layout.className = "footer-contact-layout";
    var details = document.createElement("div");
    details.className = "footer-contact-details";
    nodes.forEach(function (node) {
      if (node.nodeType === 1 && node.classList && node.classList.contains("footer-home-qr")) return;
      details.appendChild(node);
    });
    layout.appendChild(details);
    if (existingQr) layout.insertBefore(existingQr, details);
    contactCol.appendChild(layout);
  }

  function injectFooterHomeQr() {
    if (document.body && document.body.classList.contains("daab-gateway")) return;
    var footer = document.querySelector("footer.footer-pro");
    if (!footer) return;
    var contactCol = footer.querySelector(".footer-grid > .footer-col:first-child");
    if (!contactCol) return;

    wrapFooterContactColumn(contactCol);

    var layout = contactCol.querySelector(".footer-contact-layout");
    if (!layout || layout.querySelector(".footer-home-qr")) return;
    var details = layout.querySelector(".footer-contact-details");
    if (!details) return;

    var root = document.documentElement.getAttribute("data-daab-asset-root") || "";
    var lang = document.documentElement.getAttribute("data-daab-lang");
    if (lang !== "en") lang = "az";
    var isEn = lang === "en";
    var imgSrc = root + "images/qr/home-" + (isEn ? "en" : "az") + ".png";
    var href = isEn ? "https://daab-waas.com/en/" : "https://daab-waas.com/az/";
    var label = isEn
      ? "QR code for the WAAS home page — daab-waas.com"
      : "DAAB ana səhifəsi üçün QR kod — daab-waas.com";

    var wrap = document.createElement("div");
    wrap.className = "footer-home-qr";

    var qrLink = document.createElement("a");
    qrLink.className = "footer-home-qr-link";
    qrLink.href = href;
    qrLink.rel = "noopener noreferrer";
    qrLink.target = "_blank";
    qrLink.setAttribute("aria-label", label);
    qrLink.title = "daab-waas.com";

    var img = document.createElement("img");
    img.className = "footer-home-qr-img";
    img.src = imgSrc;
    img.alt = "";
    img.loading = "lazy";
    img.decoding = "async";
    qrLink.appendChild(img);
    wrap.appendChild(qrLink);
    layout.insertBefore(wrap, details);
  }

  function init() {
    if (!mobileInitialized) {
      mobileInitialized = initMobileNavOnce();
    } else {
      attachLinkCloseHandlers();
    }
    initNavDropdowns();
    initForumsSubmenuBehavior();
    attachGlobalDropdownHandlers();
    attachViewportListeners();
    injectFooterHomeQr();
    scheduleNavHeightSync();
  }

  function initMobileNavOnce() {
    var menuToggle = document.querySelector(".mobile-menu-toggle");
    var navMenu = document.getElementById("primaryNavMenu");
    if (!menuToggle || !navMenu) return false;
    initMobileNav();
    return true;
  }

  function attachLinkCloseHandlers() {
    var navMenu = document.getElementById("primaryNavMenu");
    var menuToggle = document.querySelector(".mobile-menu-toggle");
    if (!navMenu || !menuToggle) return;
    navMenu.querySelectorAll("a").forEach(function (link) {
      if (menuLinkHandlerAttached.has(link)) return;
      menuLinkHandlerAttached.add(link);
      link.addEventListener("click", closeMobileMenu);
    });
  }

  function attachGlobalDropdownHandlers() {
    if (documentListenersAttached) return;
    documentListenersAttached = true;

    document.addEventListener("click", function (event) {
      if (!needsTapDropdown()) return;
      document.querySelectorAll("[data-nav-dropdown].open").forEach(function (dropdown) {
        if (!dropdown.contains(event.target)) {
          dropdown.classList.remove("open");
          var btn = dropdown.querySelector(".nav-dropdown-toggle");
          if (btn) btn.setAttribute("aria-expanded", "false");
        }
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;
      document.querySelectorAll("[data-nav-dropdown].open").forEach(function (dropdown) {
        dropdown.classList.remove("open");
        var btn = dropdown.querySelector(".nav-dropdown-toggle");
        if (btn) btn.setAttribute("aria-expanded", "false");
      });
    });
  }

  window.DAAB_NAV = {
    init: init,
    injectFooterHomeQr: injectFooterHomeQr,
    closeMobileMenu: closeMobileMenu,
    syncNavHeight: syncNavHeight,
    currentNavKey: currentNavKey,
    isForumNavPageId: isForumNavPageId,
    isMembershipNavPageId: isMembershipNavPageId
  };

  function maybeAutoInit() {
    if (document.documentElement.getAttribute("data-daab-nav-mount") === "1") {
      return;
    }
    init();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", maybeAutoInit);
  } else {
    maybeAutoInit();
  }

  window.addEventListener("load", scheduleNavHeightSync, { once: true });
  document.addEventListener("daab-primary-nav-ready", function () {
    initNavDropdowns();
    initForumsSubmenuBehavior();
    injectFooterHomeQr();
    scheduleNavHeightSync();
  });

  function bootFooterHomeQr() {
    injectFooterHomeQr();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootFooterHomeQr);
  } else {
    bootFooterHomeQr();
  }

  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) {
      initNavDropdowns();
    }
  });
})();
