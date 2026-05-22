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

    function closeMobileMenu() {
      navMenu.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Menyunu aç");
      closeAllDropdowns();
      var searchOpen = document.getElementById("search-overlay")?.classList.contains("open");
      setBodyScrollLock(!!searchOpen);
    }

    menuToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = navMenu.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
      menuToggle.setAttribute("aria-label", open ? "Menyunu bağla" : "Menyunu aç");
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

  function initNavDropdowns() {
    var page = location.pathname.split("/").pop() || "index.html";
    var dropdowns = document.querySelectorAll("[data-nav-dropdown]");

    dropdowns.forEach(function (dropdown) {
      var toggle = dropdown.querySelector(".nav-dropdown-toggle");
      var links = dropdown.querySelectorAll(".nav-dropdown-link");
      if (!toggle) return;

      links.forEach(function (link) {
        if (link.getAttribute("href") === page) {
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
          dropdown.classList.add("has-active-child");
        }
      });

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
    });

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

  function init() {
    initMobileNav();
    initNavDropdowns();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
