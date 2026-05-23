(function () {
  "use strict";

  var MOBILE_NAV_MQ = window.matchMedia("(max-width: 1180px)");

  function isMobileNav() {
    return MOBILE_NAV_MQ.matches;
  }

  function initMobileNav() {
    var menuToggle = document.querySelector(".mobile-menu-toggle");
    var navMenu = document.getElementById("primaryNavMenu");
    if (!menuToggle || !navMenu) return;

    function closeAllDropdowns() {
      document.querySelectorAll("[data-nav-dropdown].open").forEach(function (dropdown) {
        dropdown.classList.remove("open");
        var btn = dropdown.querySelector(".nav-dropdown-toggle");
        if (btn) btn.setAttribute("aria-expanded", "false");
      });
    }

    function setBodyScrollLock(on) {
      document.body.classList.toggle("daab-scroll-lock", on);
    }

    function menuLabel(which) {
      var key = which === "close" ? "data-label-close" : "data-label-open";
      return menuToggle.getAttribute(key) || (which === "close" ? "Menyunu bağla" : "Menyunu aç");
    }

    function closeMobileMenu() {
      navMenu.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", menuLabel("open"));
      closeAllDropdowns();
      var searchOpen = document.getElementById("search-overlay")?.classList.contains("open");
      setBodyScrollLock(!!searchOpen);
    }

    menuToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = navMenu.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
      menuToggle.setAttribute("aria-label", open ? menuLabel("close") : menuLabel("open"));
      if (!open) {
        closeAllDropdowns();
      } else {
        document.querySelectorAll("[data-nav-dropdown].has-active-child").forEach(function (dropdown) {
          dropdown.classList.add("open");
          var btn = dropdown.querySelector(".nav-dropdown-toggle");
          if (btn) btn.setAttribute("aria-expanded", "true");
        });
      }
      var searchOpen = document.getElementById("search-overlay")?.classList.contains("open");
      setBodyScrollLock(open || !!searchOpen);
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
      if (event.key === "Escape") closeMobileMenu();
    });
  }

  var TOUCH_UI_MQ = window.matchMedia("(hover: none), (pointer: coarse)");

  function needsTapDropdown() {
    return isMobileNav() || TOUCH_UI_MQ.matches;
  }

  function currentNavKey() {
    var path = location.pathname.replace(/\\/g, "/");
    var page = path.split("/").pop() || "index.html";
    var navLink = document.querySelector(
      'a[data-nav-id][href$="' + page + '"], a[data-nav-id][href$="/' + page + '"]'
    );
    if (navLink) return navLink.getAttribute("data-nav-id");
    var html = document.documentElement;
    var pageId = html.getAttribute("data-daab-page-id");
    if (pageId) return pageId;
    return page;
  }

  function hrefMatchesNav(linkHref, page) {
    if (!linkHref) return false;
    var href = linkHref.split("#")[0].split("?")[0];
    if (href === page) return true;
    return href.endsWith("/" + page) || href.endsWith(page);
  }

  var dropdownToggleAttached = new WeakSet();

  function initNavDropdowns() {
    var page = location.pathname.split("/").pop() || "index.html";
    var navKey = currentNavKey();
    var dropdowns = document.querySelectorAll("[data-nav-dropdown]");

    dropdowns.forEach(function (dropdown) {
      var toggle = dropdown.querySelector(".nav-dropdown-toggle");
      var links = dropdown.querySelectorAll(".nav-dropdown-link, .nav-mega-link");
      if (!toggle) return;

      links.forEach(function (link) {
        var id = link.getAttribute("data-nav-id");
        var match = (id && id === navKey) || hrefMatchesNav(link.getAttribute("href"), page);
        if (match) {
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
          dropdown.classList.add("has-active-child");
        }
      });

      if (!dropdownToggleAttached.has(toggle)) {
        dropdownToggleAttached.add(toggle);
        /* Desktop hover opens panel; mobile & touch devices use tap */
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
      if ((id && id === navKey) || hrefMatchesNav(link.getAttribute("href"), page)) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      }
    });
  }

  var documentListenersAttached = false;
  var mobileInitialized = false;
  var menuLinkHandlerAttached = new WeakSet();

  function init() {
    if (!mobileInitialized) {
      mobileInitialized = initMobileNavOnce();
    } else {
      attachLinkCloseHandlers();
    }
    initNavDropdowns();
    attachGlobalDropdownHandlers();
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
      link.addEventListener("click", function () {
        navMenu.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        document.querySelectorAll("[data-nav-dropdown].open").forEach(function (d) {
          d.classList.remove("open");
          var btn = d.querySelector(".nav-dropdown-toggle");
          if (btn) btn.setAttribute("aria-expanded", "false");
        });
        document.body.classList.remove("daab-scroll-lock");
      });
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

  window.DAAB_NAV = { init: init };

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
})();
