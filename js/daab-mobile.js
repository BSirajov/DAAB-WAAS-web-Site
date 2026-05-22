(function () {
  "use strict";

  function syncNavHeight() {
    var strip = document.querySelector(".nav-strip");
    if (!strip) return;
    var h = Math.ceil(strip.getBoundingClientRect().height);
    if (h > 0) {
      document.documentElement.style.setProperty("--daab-nav-height", h + "px");
    }
  }

  function setScrollLock(on) {
    document.body.classList.toggle("daab-scroll-lock", on);
  }

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

    function updateLock() {
      var menuOpen = menu.classList.contains("open");
      var searchOpen = document.getElementById("search-overlay")?.classList.contains("open");
      setScrollLock(menuOpen || !!searchOpen);
    }

    var observer = new MutationObserver(updateLock);
    observer.observe(menu, { attributes: true, attributeFilter: ["class"] });

    var overlay = document.getElementById("search-overlay");
    if (overlay) {
      observer.observe(overlay, { attributes: true, attributeFilter: ["class"] });
    }

    updateLock();
  }

  function initSearchOverlayA11y() {
    var overlay = document.getElementById("search-overlay");
    if (!overlay) return;

    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) {
        overlay.classList.remove("open");
        document.body.classList.remove("daab-scroll-lock");
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
