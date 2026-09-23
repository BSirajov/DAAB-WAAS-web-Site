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

  /**
   * Tab order follows DOM: menu, breadcrumbs, in-page search.
   * Flex `order` keeps the same visual stack. Avoid moving nodes that
   * are already in place so ResizeObserver does not loop.
   */
  function orderChrome(nav) {
    if (!chromeEl) return nav || null;
    nav = nav || chromeEl.querySelector(".nav-strip") || document.querySelector(".nav-strip");
    var crumbs = breadcrumbNodes();
    var search = document.getElementById("daab-page-search");

    if (nav && chromeEl.firstElementChild !== nav) {
      chromeEl.insertBefore(nav, chromeEl.firstChild);
    }

    var cursor = nav && nav.parentNode === chromeEl ? nav.nextElementSibling : chromeEl.firstElementChild;
    crumbs.forEach(function (bc) {
      if (bc !== cursor) chromeEl.insertBefore(bc, cursor);
      cursor = bc.nextElementSibling;
    });

    var tools = document.querySelector(".sitemap-controls");
    if (tools) {
      var beforeTools = search && search.parentNode === chromeEl ? search : cursor;
      if (tools.parentNode !== chromeEl || (beforeTools && tools.nextElementSibling !== beforeTools && tools !== beforeTools)) {
        chromeEl.insertBefore(tools, beforeTools);
      }
    }

    if (search && chromeEl.lastElementChild !== search) {
      chromeEl.appendChild(search);
    }
    return nav;
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

    orderChrome(nav);

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
    chromeEl.querySelectorAll(".nav-strip, #daab-breadcrumbs, nav.daab-breadcrumbs, .breadcrumbs, .forum-breadcrumbs, #daab-page-search, .sitemap-controls").forEach(function (el) {
      resizeObserver.observe(el);
    });
  }

  function measureSitemapControlsHeight() {
    if (!chromeEl) return 0;
    var tools = chromeEl.querySelector(".sitemap-controls");
    if (!tools) return 0;
    var style = window.getComputedStyle(tools);
    if (style.display === "none" || style.visibility === "hidden") return 0;
    return Math.ceil(tools.getBoundingClientRect().height);
  }

  function measureSearchHeight() {
    if (!chromeEl) return 0;
    var search = chromeEl.querySelector("#daab-page-search");
    if (!search) return 0;
    var style = window.getComputedStyle(search);
    if (style.display === "none" || style.visibility === "hidden") return 0;
    return Math.ceil(search.getBoundingClientRect().height);
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

    var nav = orderChrome();
    var navH = nav ? Math.ceil(nav.getBoundingClientRect().height) : 0;
    if (navH <= 0) navH = 86;

    var bcH = measureBreadcrumbsHeight();
    var toolsH = measureSitemapControlsHeight();
    var searchH = measureSearchHeight();
    var stack = navH + bcH + toolsH + searchH;

    rootEl().style.setProperty("--daab-nav-height", navH + "px");
    rootEl().style.setProperty("--daab-breadcrumbs-height", bcH + "px");
    rootEl().style.setProperty("--daab-page-search-height", searchH + "px");
    rootEl().style.setProperty("--daab-sticky-top-stack", stack + "px");

    if (spacerEl) {
      spacerEl.style.height = stack + "px";
    }
  }

  function detectLang() {
    if (window.DAAB_I18N && typeof window.DAAB_I18N.detectLang === "function") {
      return window.DAAB_I18N.detectLang();
    }
    var explicit = rootEl().getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function assetRoot() {
    var root = rootEl().getAttribute("data-daab-asset-root");
    if (root == null || root === "") return "";
    return root.endsWith("/") ? root : root + "/";
  }

  function orgName(lang) {
    return lang === "az"
      ? "Dünya Azərbaycanlı Alimlər Birliyi"
      : "World Association of Azerbaijani Scientists";
  }

  function applyPrintHeaderName(name) {
    var title = document.querySelector(".daab-print-header__name");
    if (title && name) title.textContent = name;
  }

  function mountPrintHeader() {
    if (isGateway() || document.getElementById("daab-print-sheet")) return;
    var pageId = rootEl().getAttribute("data-daab-page-id") || "";
    if (pageId === "membership-flyer" || pageId === "sponsors-flyer") return;
    if (!document.body) return;

    var lang = detectLang();

    var table = document.createElement("table");
    table.id = "daab-print-sheet";
    table.className = "daab-print-sheet";
    table.setAttribute("role", "presentation");

    var thead = document.createElement("thead");
    thead.className = "daab-print-sheet__head";
    thead.setAttribute("aria-hidden", "true");

    var headRow = document.createElement("tr");
    var headCell = document.createElement("td");

    var header = document.createElement("div");
    header.id = "daab-print-header";
    header.className = "daab-print-header";

    var img = document.createElement("img");
    img.className = "daab-print-header__logo";
    img.src = assetRoot() + "images/daab-logo.png";
    img.alt = "";

    var name = document.createElement("p");
    name.className = "daab-print-header__name";
    name.textContent = orgName(lang);

    header.appendChild(img);
    header.appendChild(name);
    headCell.appendChild(header);
    headRow.appendChild(headCell);
    thead.appendChild(headRow);

    var tbody = document.createElement("tbody");
    tbody.className = "daab-print-sheet__body-group";
    var bodyRow = document.createElement("tr");
    var bodyCell = document.createElement("td");
    bodyCell.className = "daab-print-sheet__body";

    while (document.body.firstChild) {
      bodyCell.appendChild(document.body.firstChild);
    }

    bodyRow.appendChild(bodyCell);
    tbody.appendChild(bodyRow);
    table.appendChild(thead);
    table.appendChild(tbody);
    document.body.appendChild(table);
    rootEl().classList.add("daab-print-header-ready");

    if (window.DAAB_I18N && window.DAAB_I18N.loadUi) {
      window.DAAB_I18N.loadUi().then(function (ui) {
        var block = ui && ui.printHeader && ui.printHeader[lang];
        if (block && block.name) applyPrintHeaderName(block.name);
      });
    }
  }

  function boot() {
    if (isGateway()) return;
    mountChrome();
    mountPrintHeader();
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
  document.addEventListener("daab-page-search-ready", function () {
    observeChrome();
    scheduleSync();
  });

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(scheduleSync);
  }
})();
