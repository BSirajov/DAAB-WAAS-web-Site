/**
 * Persistent contents control for left-TOC / right-article pages.
 * Desktop keeps the in-flow sticky sidebar. Small screens use a Contents
 * button and a left drawer that sits below the sticky navigation.
 */
(function () {
  "use strict";

  if (window.DAAB_TOC_DRAWER && window.DAAB_TOC_DRAWER.bound) return;

  var mq = window.matchMedia("(max-width: 1060px)");
  var sidebar;
  var widget;
  var launch;
  var backdrop;
  var toggle;

  function isAz() {
    var html = document.documentElement;
    var lang = (html.getAttribute("data-daab-lang") || html.lang || "").toLowerCase();
    return lang === "az" || lang.indexOf("az") === 0 || /\/az\//.test(location.pathname);
  }

  function labels() {
    return isAz()
      ? { button: "Mündəricat", aria: "Mündəricatı aç" }
      : { button: "Contents", aria: "Open contents" };
  }

  function widgetOpen() {
    return !!(widget && widget.classList.contains("events-open"));
  }

  function applyChrome(open) {
    document.documentElement.classList.toggle("daab-toc-open", open);
    document.documentElement.classList.toggle("cta-toc-open", open);
    if (launch) launch.setAttribute("aria-expanded", open ? "true" : "false");
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) backdrop.hidden = !open;
    document.body.classList.toggle("daab-toc-scroll-lock", open);
    document.body.classList.toggle("cta-toc-scroll-lock", open);
  }

  function setOpen(open) {
    if (!mq.matches) open = false;
    if (widget) widget.classList.toggle("events-open", open);
    applyChrome(open);
  }

  function close() {
    setOpen(false);
  }

  function syncFromWidget() {
    if (!mq.matches) {
      applyChrome(false);
      return;
    }
    applyChrome(widgetOpen());
  }

  function ensureChrome() {
    sidebar = document.querySelector("aside.sidebar");
    widget = sidebar && (sidebar.querySelector(".sidebar-widget") || document.getElementById("ctaTocWidget"));
    if (!sidebar || !widget) return false;

    document.documentElement.classList.add("daab-toc-page");
    toggle = sidebar.querySelector(".events-menu-toggle");

    launch =
      document.getElementById("daabTocLaunch") ||
      document.getElementById("ctaTocLaunch");
    if (!launch) {
      var copy = labels();
      launch = document.createElement("button");
      launch.type = "button";
      launch.id = "daabTocLaunch";
      launch.className = "daab-toc-launch";
      launch.setAttribute("aria-controls", sidebar.id || "daabTocPanel");
      launch.setAttribute("aria-expanded", "false");
      launch.setAttribute("aria-label", copy.aria);
      launch.innerHTML =
        '<span class="daab-toc-launch-icon" aria-hidden="true">📄</span>' +
        '<span class="daab-toc-launch-label"></span>';
      launch.querySelector(".daab-toc-launch-label").textContent = copy.button;
      if (!sidebar.id) sidebar.id = "daabTocPanel";
      document.body.appendChild(launch);
    }

    backdrop =
      document.getElementById("daabTocBackdrop") ||
      document.getElementById("ctaTocBackdrop");
    if (!backdrop) {
      backdrop = document.createElement("div");
      backdrop.id = "daabTocBackdrop";
      backdrop.className = "daab-toc-backdrop";
      backdrop.hidden = true;
      sidebar.parentNode.insertBefore(backdrop, sidebar);
    }

    return true;
  }

  function bindPress(el, action) {
    if (!el || el.getAttribute("data-daab-toc-bound")) return;
    el.setAttribute("data-daab-toc-bound", "1");
    var last = 0;
    function invoke(event) {
      var now = Date.now();
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      if (now - last < 500) return;
      last = now;
      action();
    }
    el.addEventListener("click", invoke);
    el.addEventListener(
      "touchend",
      function (event) {
        if (event.touches && event.touches.length) return;
        invoke(event);
      },
      { passive: false }
    );
  }

  function bind() {
    if (!ensureChrome()) return;

    bindPress(launch, function () {
      setOpen(!widgetOpen());
      if (widgetOpen() && toggle) {
        try {
          toggle.focus({ preventScroll: true });
        } catch (err) {
          toggle.focus();
        }
      }
    });

    bindPress(backdrop, close);

    if (toggle && !toggle.getAttribute("data-daab-toc-bound")) {
      toggle.setAttribute("data-daab-toc-bound", "1");
      var lastToggleTouch = 0;
      toggle.addEventListener(
        "touchend",
        function (event) {
          if (!mq.matches) return;
          if (event.touches && event.touches.length) return;
          event.preventDefault();
          event.stopPropagation();
          lastToggleTouch = Date.now();
          setOpen(!widgetOpen());
        },
        { capture: true, passive: false }
      );
      toggle.addEventListener(
        "click",
        function (event) {
          if (!mq.matches) return;
          event.preventDefault();
          event.stopPropagation();
          event.stopImmediatePropagation();
          if (Date.now() - lastToggleTouch < 500) return;
          setOpen(!widgetOpen());
        },
        true
      );
    }

    document.addEventListener("click", function () {
      window.requestAnimationFrame(syncFromWidget);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });

    sidebar.addEventListener("click", function (event) {
      var link = event.target.closest('a[href^="#"]');
      if (link && mq.matches) close();
    });

    function onBreakpointChange() {
      if (!mq.matches) close();
    }

    if (typeof mq.addEventListener === "function") {
      mq.addEventListener("change", onBreakpointChange);
    } else if (typeof mq.addListener === "function") {
      mq.addListener(onBreakpointChange);
    }
  }

  window.DAAB_TOC_DRAWER = { init: bind, bound: false };

  function start() {
    if (window.DAAB_TOC_DRAWER.bound) return;
    bind();
    if (sidebar && widget) window.DAAB_TOC_DRAWER.bound = true;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
