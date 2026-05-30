(function () {
  "use strict";

  var scrollLocked = false;
  var lockedScrollY = 0;

  function syncNavHeight() {
    var strip = document.querySelector(".nav-strip");
    if (!strip) return;
    var h = Math.ceil(strip.getBoundingClientRect().height);
    if (h > 0) {
      document.documentElement.style.setProperty("--daab-nav-height", h + "px");
    }
  }

  function syncBreadcrumbsHeight() {
    if (window.DAAB_BREADCRUMBS && typeof window.DAAB_BREADCRUMBS.syncHeight === "function") {
      window.DAAB_BREADCRUMBS.syncHeight();
      return;
    }
    var el =
      document.querySelector(".breadcrumbs.forum-breadcrumbs") ||
      document.querySelector(".forum-breadcrumbs");
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

  function syncLayoutHeights() {
    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
      return;
    }
    syncNavHeight();
    syncBreadcrumbsHeight();
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
      body.style.position = "fixed";
      body.style.top = "-" + lockedScrollY + "px";
      body.style.left = "0";
      body.style.right = "0";
      body.style.width = "100%";
    } else {
      root.classList.remove("daab-scroll-lock");
      body.classList.remove("daab-scroll-lock");
      root.style.removeProperty("--daab-scroll-lock-y");
      body.style.position = "";
      body.style.top = "";
      body.style.left = "";
      body.style.right = "";
      body.style.width = "";
      var y = lockedScrollY;
      window.scrollTo(0, y);
    }
    syncLayoutHeights();
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
      return (
        window.scrollY ||
        root.scrollTop ||
        (body && body.scrollTop) ||
        0
      );
    },
  };

  function initNavHeight() {
    syncLayoutHeights();
    window.addEventListener("resize", syncLayoutHeights, { passive: true });
    window.addEventListener("orientationchange", function () {
      window.setTimeout(syncLayoutHeights, 100);
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncLayoutHeights);
    }
    document.addEventListener("daab-breadcrumbs-ready", syncLayoutHeights);
    window.addEventListener("load", syncLayoutHeights, { passive: true });
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

  function init() {
    initNavHeight();
    initMobileMenuScrollLock();
    initSearchOverlayA11y();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.addEventListener("load", syncNavHeight, { passive: true });
})();
