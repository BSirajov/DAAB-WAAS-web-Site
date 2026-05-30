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
    if (id === "forum-2024" && isForumNavPageId(navKey) && navKey !== "activities") {
      return true;
    }
    /* When data-daab-page-id is set, match by id only (see comment above navLinkIsActive). */
    if (pageIdAttr) return false;
    return hrefMatchesNav(href, relPath);
  }

  var dropdownToggleAttached = new WeakSet();

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
        }
      });

      if (!dropdownToggleAttached.has(toggle)) {
        dropdownToggleAttached.add(toggle);
        toggle.addEventListener("click", function (event) {
          if (!needsTapDropdown()) return;
          event.preventDefault();
          event.stopPropagation();
          var willOpen = !dropdown.classList.contains("open");
          document.querySelectorAll("[data-nav-dropdown].open").forEach(function (other) {
            if (other === dropdown) return;
            other.classList.remove("open");
            var otherToggle = other.querySelector(".nav-dropdown-toggle");
            if (otherToggle) otherToggle.setAttribute("aria-expanded", "false");
          });
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

  function injectNavBrandQr() {
    if (document.body && document.body.classList.contains("daab-gateway")) return;
    var brand = document.querySelector("a.nav-brand");
    if (!brand || document.querySelector(".nav-brand-qr-link")) return;

    var root = document.documentElement.getAttribute("data-daab-asset-root") || "";
    var lang = document.documentElement.getAttribute("data-daab-lang");
    if (lang !== "en") lang = "az";
    var isEn = lang === "en";
    var imgSrc = root + "images/qr/home-" + (isEn ? "en" : "az") + ".png";
    var href = isEn ? "https://daab-waas.com/en/" : "https://daab-waas.com/az/";
    var label = isEn
      ? "QR code for the WAAS home page — daab-waas.com"
      : "DAAB ana səhifəsi üçün QR kod — daab-waas.com";

    var block = document.createElement("div");
    block.className = "nav-brand-block";
    var parent = brand.parentNode;
    if (!parent) return;
    parent.insertBefore(block, brand);
    block.appendChild(brand);

    var qrLink = document.createElement("a");
    qrLink.className = "nav-brand-qr-link";
    qrLink.href = href;
    qrLink.rel = "noopener noreferrer";
    qrLink.setAttribute("aria-label", label);
    qrLink.title = "daab-waas.com";

    var img = document.createElement("img");
    img.className = "nav-brand-qr-img";
    img.src = imgSrc;
    img.alt = "";
    img.width = 44;
    img.height = 44;
    img.loading = "lazy";
    img.decoding = "async";
    qrLink.appendChild(img);
    block.appendChild(qrLink);
    scheduleNavHeightSync();
  }

  function init() {
    if (!mobileInitialized) {
      mobileInitialized = initMobileNavOnce();
    } else {
      attachLinkCloseHandlers();
    }
    initNavDropdowns();
    attachGlobalDropdownHandlers();
    attachViewportListeners();
    injectNavBrandQr();
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
    injectNavBrandQr: injectNavBrandQr,
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
    injectNavBrandQr();
    scheduleNavHeightSync();
  });

  function bootNavBrandQr() {
    injectNavBrandQr();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootNavBrandQr);
  } else {
    bootNavBrandQr();
  }

  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) {
      initNavDropdowns();
    }
  });
})();
