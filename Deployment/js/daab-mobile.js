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
    syncNavHeight();
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
    syncNavHeight();
    window.addEventListener("resize", syncNavHeight, { passive: true });
    window.addEventListener("orientationchange", function () {
      window.setTimeout(syncNavHeight, 100);
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncNavHeight);
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
