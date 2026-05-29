(function () {
  "use strict";

  var scrollLocked = false;
  var lockedScrollY = 0;

  function isBreadcrumbNode(el) {
    if (!el) return false;
    if (el.id === "daab-breadcrumbs") return true;
    if (el.classList && el.classList.contains("daab-breadcrumbs")) return true;
    if (el.classList && el.classList.contains("forum-breadcrumbs")) return true;
    if (
      el.classList &&
      el.classList.contains("breadcrumbs") &&
      el.classList.contains("forum-breadcrumbs")
    ) {
      return true;
    }
    return false;
  }

  function findChromeBreadcrumbs() {
    var shell = document.getElementById("daab-top-chrome");
    if (shell) {
      var inShell = shell.querySelector(
        "#daab-breadcrumbs, nav.daab-breadcrumbs, .forum-breadcrumbs, .breadcrumbs.forum-breadcrumbs"
      );
      if (inShell) return inShell;
    }
    return (
      document.getElementById("daab-breadcrumbs") ||
      document.querySelector(
        ".forum-breadcrumbs, .breadcrumbs.forum-breadcrumbs, nav.daab-breadcrumbs"
      )
    );
  }

  function mountTopChrome() {
    var body = document.body;
    if (!body || body.classList.contains("daab-gateway")) return;

    var nav = document.querySelector(".nav-strip");
    if (!nav) return;

    var shell = document.getElementById("daab-top-chrome");
    if (!shell) {
      shell = document.createElement("div");
      shell.id = "daab-top-chrome";
      shell.setAttribute("data-daab-chrome", "1");
      var skip = body.querySelector(".skip");
      if (skip && skip.parentNode === body) {
        body.insertBefore(shell, skip.nextSibling);
      } else {
        body.insertBefore(shell, body.firstChild);
      }
    }

    if (nav.parentNode !== shell) {
      shell.appendChild(nav);
    }

    var crumbs = findChromeBreadcrumbs();
    if (crumbs && crumbs.parentNode !== shell) {
      shell.appendChild(crumbs);
    }

    var spacer = document.getElementById("daab-chrome-spacer");
    if (!spacer) {
      spacer = document.createElement("div");
      spacer.id = "daab-chrome-spacer";
      spacer.setAttribute("aria-hidden", "true");
    }
    if (spacer.parentNode !== body) {
      body.insertBefore(spacer, shell.nextSibling);
    } else if (spacer.previousElementSibling !== shell) {
      body.insertBefore(spacer, shell.nextSibling);
    }
  }

  function syncNavHeight() {
    mountTopChrome();
    var nav = document.querySelector(".nav-strip");
    if (!nav) return;
    var h = Math.ceil(nav.getBoundingClientRect().height);
    if (h > 0) {
      document.documentElement.style.setProperty("--daab-nav-height", h + "px");
    }
  }

  function syncBreadcrumbsHeightFallback() {
    var el = findChromeBreadcrumbs();
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

  function syncChromeSpacer() {
    var shell = document.getElementById("daab-top-chrome");
    var spacer = document.getElementById("daab-chrome-spacer");
    if (!shell || !spacer) return;
    var h = Math.ceil(shell.getBoundingClientRect().height);
    if (h > 0) {
      spacer.style.height = h + "px";
    }
  }

  function syncStickyChrome() {
    mountTopChrome();
    syncNavHeight();
    if (window.DAAB_BREADCRUMBS && typeof window.DAAB_BREADCRUMBS.syncHeight === "function") {
      window.DAAB_BREADCRUMBS.syncHeight();
    } else {
      syncBreadcrumbsHeightFallback();
    }
    syncChromeSpacer();
  }

  function applyScrollLock(on) {
    if (on === scrollLocked) return;
    scrollLocked = on;
    var root = document.documentElement;
    var body = document.body;
    if (!body) return;

    if (on) {
      lockedScrollY = window.scrollY || root.scrollTop || 0;
      root.style.setProperty("--daab-scroll-lock-y", lockedScrollY + "px");
      root.classList.add("daab-scroll-lock");
      body.classList.add("daab-scroll-lock");
      body.style.overflow = "hidden";
      body.style.touchAction = "none";
    } else {
      root.classList.remove("daab-scroll-lock");
      body.classList.remove("daab-scroll-lock");
      root.style.removeProperty("--daab-scroll-lock-y");
      body.style.overflow = "";
      body.style.touchAction = "";
      window.scrollTo(0, lockedScrollY);
    }
    syncStickyChrome();
  }

  function recomputeScrollLock() {
    var menuOpen = !!(
      document.getElementById("primaryNavMenu") &&
      document.getElementById("primaryNavMenu").classList.contains("open")
    );
    var searchOpen = !!(
      document.getElementById("search-overlay") &&
      document.getElementById("search-overlay").classList.contains("open")
    );
    applyScrollLock(menuOpen || searchOpen);
  }

  window.DAAB_SCROLL_LOCK = {
    set: applyScrollLock,
    update: recomputeScrollLock,
    isLocked: function () {
      return scrollLocked;
    },
    getScrollY: function () {
      if (scrollLocked) return lockedScrollY;
      var root = document.documentElement;
      var body = document.body;
      return window.scrollY || root.scrollTop || (body && body.scrollTop) || 0;
    }
  };

  window.DAAB_STICKY_CHROME = {
    sync: syncStickyChrome,
    syncNavHeight: syncNavHeight,
    mount: mountTopChrome
  };

  function initNavHeight() {
    syncStickyChrome();
    window.addEventListener("resize", syncStickyChrome, { passive: true });
    window.addEventListener("orientationchange", function () {
      window.setTimeout(syncStickyChrome, 100);
    });
    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", syncStickyChrome, { passive: true });
      window.visualViewport.addEventListener("scroll", syncStickyChrome, { passive: true });
    }
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncStickyChrome);
    }
    if (typeof ResizeObserver !== "undefined") {
      var shell = document.getElementById("daab-top-chrome");
      var observeTarget = shell || document.querySelector(".nav-strip");
      if (observeTarget) {
        var ro = new ResizeObserver(syncStickyChrome);
        ro.observe(observeTarget);
      }
    }
  }

  function initMobileMenuScrollLock() {
    var menu = document.getElementById("primaryNavMenu");
    if (!menu) return;

    var observer = new MutationObserver(recomputeScrollLock);
    observer.observe(menu, { attributes: true, attributeFilter: ["class"] });

    var overlay = document.getElementById("search-overlay");
    if (overlay) {
      observer.observe(overlay, { attributes: true, attributeFilter: ["class"] });
    }

    recomputeScrollLock();
  }

  function initSearchOverlayA11y() {
    var overlay = document.getElementById("search-overlay");
    if (!overlay) return;

    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) {
        overlay.classList.remove("open");
        recomputeScrollLock();
      }
    });
  }

  document.addEventListener("daab-breadcrumbs-ready", syncStickyChrome);

  function init() {
    mountTopChrome();
    initNavHeight();
    initMobileMenuScrollLock();
    initSearchOverlayA11y();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.addEventListener("load", syncStickyChrome, { passive: true });
})();
