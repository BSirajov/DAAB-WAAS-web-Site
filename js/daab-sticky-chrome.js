/**
 * Fixed top chrome: primary nav + breadcrumbs stay at the top on all viewports.
 * Inserts #daab-top-chrome and #daab-chrome-spacer; syncs layout CSS variables.
 */
(function () {
  "use strict";

  var chromeEl = null;
  var spacerEl = null;
  var resizeObserver = null;
  var syncScheduled = false;

  function scheduleSync() {
    if (syncScheduled) return;
    syncScheduled = true;
    window.requestAnimationFrame(function () {
      syncScheduled = false;
      sync();
    });
  }

  function rootEl() {
    return document.documentElement;
  }

  function isGateway() {
    return document.body && document.body.classList.contains("daab-gateway");
  }

  function isBreadcrumbNode(node) {
    if (!node || node.nodeType !== 1) return false;
    if (node.id === "daab-breadcrumbs") return true;
    if (node.classList && node.classList.contains("daab-breadcrumbs")) return true;
    if (node.classList && node.classList.contains("forum-breadcrumbs")) return true;
    if (node.classList && node.classList.contains("breadcrumbs")) return true;
    return false;
  }

  function breadcrumbNodes() {
    return Array.prototype.slice.call(
      document.querySelectorAll(
        "#daab-breadcrumbs, nav.daab-breadcrumbs, .forum-breadcrumbs, .breadcrumbs.forum-breadcrumbs, .breadcrumbs"
      )
    ).filter(function (el) {
      return isBreadcrumbNode(el);
    });
  }

  function ensureSpacer(parent, before) {
    spacerEl = document.getElementById("daab-chrome-spacer");
    if (spacerEl) return spacerEl;
    spacerEl = document.createElement("div");
    spacerEl.id = "daab-chrome-spacer";
    spacerEl.setAttribute("aria-hidden", "true");
    if (before) {
      parent.insertBefore(spacerEl, before);
    } else {
      parent.appendChild(spacerEl);
    }
    return spacerEl;
  }

  function mountChrome() {
    if (isGateway() || chromeEl) return;

    var nav = document.querySelector(".nav-strip");
    if (!nav || !nav.parentNode) return;

    chromeEl = document.getElementById("daab-top-chrome");
    if (!chromeEl) {
      chromeEl = document.createElement("div");
      chromeEl.id = "daab-top-chrome";
      chromeEl.setAttribute("role", "presentation");
      nav.parentNode.insertBefore(chromeEl, nav);
    }

    if (nav.parentNode !== chromeEl) {
      chromeEl.appendChild(nav);
    }

    breadcrumbNodes().forEach(function (bc) {
      if (bc.parentNode !== chromeEl) {
        chromeEl.appendChild(bc);
      }
    });

    var insertBefore =
      chromeEl.nextElementSibling && chromeEl.nextElementSibling.id !== "daab-chrome-spacer"
        ? chromeEl.nextElementSibling
        : null;
    ensureSpacer(chromeEl.parentNode, insertBefore);

    rootEl().classList.add("daab-chrome-ready");
    observeChrome();
    sync();
  }

  function observeChrome() {
    if (!chromeEl || typeof ResizeObserver === "undefined") return;
    if (resizeObserver) resizeObserver.disconnect();
    resizeObserver = new ResizeObserver(scheduleSync);
    resizeObserver.observe(chromeEl);
    chromeEl.querySelectorAll(".nav-strip, #daab-breadcrumbs, nav.daab-breadcrumbs, .breadcrumbs, .forum-breadcrumbs").forEach(function (el) {
      resizeObserver.observe(el);
    });
  }

  function measureBreadcrumbsHeight() {
    if (!chromeEl) return 0;
    var nodes = chromeEl.querySelectorAll(
      "#daab-breadcrumbs, nav.daab-breadcrumbs, .forum-breadcrumbs, .breadcrumbs.forum-breadcrumbs, .breadcrumbs"
    );
    var total = 0;
    nodes.forEach(function (el) {
      if (!isBreadcrumbNode(el)) return;
      var h = Math.ceil(el.getBoundingClientRect().height);
      if (h > total) total = h;
    });
    return total;
  }

  function sync() {
    if (isGateway()) return;

    if (!chromeEl) {
      mountChrome();
      if (!chromeEl) return;
    }

    breadcrumbNodes().forEach(function (bc) {
      if (bc.parentNode !== chromeEl) {
        chromeEl.appendChild(bc);
      }
    });

    var nav = chromeEl.querySelector(".nav-strip");
    var navH = nav ? Math.ceil(nav.getBoundingClientRect().height) : 0;
    if (navH <= 0) navH = 86;

    var bcH = measureBreadcrumbsHeight();
    var stack = navH + bcH;

    rootEl().style.setProperty("--daab-nav-height", navH + "px");
    rootEl().style.setProperty("--daab-breadcrumbs-height", bcH + "px");
    rootEl().style.setProperty("--daab-sticky-top-stack", stack + "px");

    if (spacerEl) {
      spacerEl.style.height = stack + "px";
    }
  }

  function boot() {
    if (isGateway()) return;
    mountChrome();
    sync();
  }

  window.DAAB_STICKY_CHROME = {
    mount: mountChrome,
    sync: sync,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.addEventListener("resize", scheduleSync, { passive: true });
  window.addEventListener("orientationchange", function () {
    window.setTimeout(scheduleSync, 100);
  });
  window.addEventListener("load", scheduleSync, { passive: true });

  document.addEventListener("daab-breadcrumbs-ready", scheduleSync);
  document.addEventListener("daab-primary-nav-ready", scheduleSync);
  document.addEventListener("daab-nav-tools-mounted", scheduleSync);

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(scheduleSync);
  }
})();
