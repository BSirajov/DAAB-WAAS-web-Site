/**
 * Persistent contents control for left-TOC / right-article pages.
 * Desktop keeps the in-flow sticky sidebar. Small screens use a Contents
 * button and a left drawer that sits below the sticky navigation.
 *
 * iPhone 16 Pro fails in Safari, Chrome, and Edge together because all three
 * are WebKit. A tap there moves visualViewport (every iOS browser, not only
 * Safari's toolbar). The old handler treated that jump as a scroll — pointerup
 * coordinates differ by more than 12px — and setPointerCapture then suppressed
 * the click, so nothing opened. When pointerup did run, it opened the drawer
 * and the compatibility click was hit-tested again, landed on a TOC link or
 * the scrim, and closed it. The guard only ignored a click whose target was
 * still the button or the scrim.
 *
 * Bind the toggle before any positioning. Open from the native click handler
 * and from pointerup, and ignore every later event from that same gesture so
 * it cannot toggle shut. Do not call setPointerCapture, do not listen to
 * touchend, and do not preventDefault on pointerup.
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
  var listenersBound = false;
  /* While this timestamp is in the future, a follow-up event from the gesture
     that just toggled must not toggle again or activate a link underneath. */
  var gestureLockUntil = 0;
  /* Other scripts ask this before they collapse the list. It stays set only
     after an open, so a real close is not forced back open. */
  var holdOpenUntil = 0;
  var watchersBound = false;

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

  function gestureLocked() {
    return !!(gestureLockUntil && Date.now() < gestureLockUntil);
  }

  function holdingOpen() {
    return !!(holdOpenUntil && Date.now() < holdOpenUntil);
  }

  function armGesture() {
    gestureLockUntil = Date.now() + 500;
  }

  function primaryButton(event) {
    return !(event && event.button != null && event.button > 0);
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
    try {
      applyDrawerBox(open);
    } catch (err) {
      /* A sizing failure must not undo the open state. */
    }
  }

  function close() {
    holdOpenUntil = 0;
    setOpen(false);
  }

  function forceClose() {
    gestureLockUntil = 0;
    holdOpenUntil = 0;
    setOpen(false);
  }

  function toggleDrawer() {
    if (!mq.matches) return;
    var open = !widgetOpen();
    holdOpenUntil = open ? gestureLockUntil : 0;
    setOpen(open);
  }

  function runAction(action) {
    if (gestureLocked()) return;
    armGesture();
    action();
  }

  function placeChrome() {
    if (!sidebar || !backdrop || !sidebar.parentNode) return;
    if (!sidebarHome) {
      sidebarHome = {
        parent: sidebar.parentNode,
        next: sidebar.nextSibling
      };
    }
    if (mq.matches) {
      if (backdrop.parentNode !== document.body) document.body.appendChild(backdrop);
      if (sidebar.parentNode !== document.body) document.body.appendChild(sidebar);
      return;
    }
    var parent = sidebarHome.parent;
    if (!parent) return;
    var next = sidebarHome.next;
    if (next && next.parentNode === parent) {
      parent.insertBefore(backdrop, next);
      parent.insertBefore(sidebar, next);
    } else {
      parent.appendChild(backdrop);
      parent.appendChild(sidebar);
    }
  }

  var sidebarHome = null;

  function syncFromWidget() {
    if (!mq.matches) {
      applyChrome(false);
      return;
    }
    applyChrome(widgetOpen());
  }

  function safeBottomPx() {
    var raw = "";
    try {
      raw = window.getComputedStyle(document.documentElement).getPropertyValue("--daab-safe-bottom") || "";
    } catch (err) {
      raw = "";
    }
    var n = parseFloat(raw);
    if (!isFinite(n) || n < 0) return 0;
    return Math.min(80, n);
  }

  function navTopPx() {
    var raw = "";
    try {
      raw = window.getComputedStyle(document.documentElement).getPropertyValue("--daab-sticky-top-stack") || "";
    } catch (err) {
      raw = "";
    }
    var n = parseFloat(raw);
    if (!isFinite(n) || n < 1) n = 86;
    return n;
  }

  var drawerBoxProps = ["top", "right", "bottom", "left", "height", "min-height", "max-height", "transform", "-webkit-transform"];

  function clearDrawerBoxInline() {
    if (!sidebar) return;
    drawerBoxProps.forEach(function (prop) {
      sidebar.style.removeProperty(prop);
    });
  }

  /* iOS WebKit (Safari, Chrome, and Edge) paints calc(100dvh - top) as a
     hairline under the sticky header. Measure the visible space under
     #daab-top-chrome in pixels and pin the open panel to that box. */
  function measureDrawerBox() {
    var top = navTopPx();
    var chrome = document.getElementById("daab-top-chrome");
    if (chrome) {
      var rect = chrome.getBoundingClientRect();
      if (rect && rect.bottom > top) top = rect.bottom;
    }
    var vv = window.visualViewport;
    var offset = vv && isFinite(vv.offsetTop) && vv.offsetTop > 0 ? vv.offsetTop : 0;
    var viewH = vv && isFinite(vv.height) && vv.height > 0 ? vv.height + offset : (window.innerHeight || 0);
    var layoutTop = Math.round(top + offset);
    var height = Math.round(viewH - layoutTop);
    if (!(height > 160)) {
      var fallback = Math.round((window.innerHeight || 0) - top);
      if (fallback > height) height = fallback;
    }
    if (!(height > 160)) height = 480;
    return { top: layoutTop, height: height };
  }

  function applyDrawerBox(open) {
    if (!mq.matches) {
      document.documentElement.style.removeProperty("--daab-toc-drawer-top");
      document.documentElement.style.removeProperty("--daab-toc-drawer-height");
      clearDrawerBoxInline();
      if (backdrop) backdrop.style.top = "";
      return;
    }
    var box = measureDrawerBox();
    document.documentElement.style.setProperty("--daab-toc-drawer-top", box.top + "px");
    document.documentElement.style.setProperty("--daab-toc-drawer-height", box.height + "px");
    if (backdrop) backdrop.style.top = "";
    if (!open || !sidebar) {
      clearDrawerBoxInline();
      return;
    }
    sidebar.style.setProperty("top", box.top + "px", "important");
    sidebar.style.setProperty("left", "0px", "important");
    sidebar.style.setProperty("right", "auto", "important");
    sidebar.style.setProperty("bottom", "auto", "important");
    sidebar.style.setProperty("height", box.height + "px", "important");
    sidebar.style.setProperty("min-height", box.height + "px", "important");
    sidebar.style.setProperty("max-height", box.height + "px", "important");
    sidebar.style.setProperty("transform", "none", "important");
    sidebar.style.setProperty("-webkit-transform", "none", "important");
  }

  /* Keep the stylesheet `bottom`. An inline `top` taken from
     visualViewport.offsetTop + height is the layout-viewport edge, which
     iOS WebKit (every browser on the phone) still places under the browser
     UI, and it also desyncs hit testing from the painted box. */
  function pinLaunch() {
    try {
      applyDrawerBox(mq.matches && widgetOpen());
    } catch (err) {
      /* Keep the open panel even if a later button nudge fails. */
    }
    if (!launch || gestureLocked()) return;
    try {
      if (!mq.matches) {
        launch.style.top = "";
        launch.style.bottom = "";
        launch.style.transform = "";
        return;
      }
      launch.style.top = "";
      launch.style.transform = "";
      var banner = document.querySelector(".daab-cookie-banner");
      if (!banner || banner.hidden) {
        launch.style.bottom = "";
        return;
      }
      var rect = banner.getBoundingClientRect();
      if (!rect || rect.height < 1 || rect.width < 1) {
        launch.style.bottom = "";
        return;
      }
      var fromBottom = (window.innerHeight || 0) - rect.top;
      if (!(fromBottom > 0)) {
        launch.style.bottom = "";
        return;
      }
      var bottom = Math.round(Math.max(136, fromBottom + 12) + safeBottomPx());
      launch.style.bottom = bottom + "px";
    } catch (err) {
      /* A positioning failure must not skip or undo the toggle. */
    }
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

  function bindLaunch(el, action) {
    if (!el || el.getAttribute("data-daab-toc-bound")) return;
    el.setAttribute("data-daab-toc-bound", "1");
    el.onclick = function (event) {
      if (!primaryButton(event)) return;
      event.preventDefault();
      event.stopPropagation();
      if (gestureLocked()) return;
      runAction(action);
    };
    el.addEventListener("pointerup", function (event) {
      if (!primaryButton(event)) return;
      if (gestureLocked()) return;
      runAction(action);
    });
  }

  /* Capture runs before the timeline / gallery bubble listeners, which would
     toggle the same control a second time and shut the drawer. */
  function bindHamburger(el) {
    if (!el || el.getAttribute("data-daab-toc-bound")) return;
    el.setAttribute("data-daab-toc-bound", "1");
    el.addEventListener("pointerup", function (event) {
      if (!mq.matches || !primaryButton(event)) return;
      if (gestureLocked()) return;
      runAction(toggleDrawer);
    });
    el.addEventListener("click", function (event) {
      if (!mq.matches) return;
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      if (gestureLocked()) return;
      runAction(toggleDrawer);
    }, true);
  }

  function onDocumentClickCapture(event) {
    if (!gestureLocked()) return;
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
  }

  function onDocumentClickBubble() {
    window.requestAnimationFrame(function () {
      if (!mq.matches) {
        syncFromWidget();
        return;
      }
      if (holdingOpen()) {
        if (widget) widget.classList.add("events-open");
        applyChrome(true);
        return;
      }
      syncFromWidget();
    });
  }

  function bindWatchers() {
    if (watchersBound) return;
    watchersBound = true;

    function onBreakpointChange() {
      try {
        placeChrome();
      } catch (err) { /* keep the toggle */ }
      try {
        pinLaunch();
      } catch (err2) { /* keep the toggle */ }
      if (!mq.matches) forceClose();
    }

    if (typeof mq.addEventListener === "function") {
      mq.addEventListener("change", onBreakpointChange);
    } else if (typeof mq.addListener === "function") {
      mq.addListener(onBreakpointChange);
    }

    window.addEventListener("resize", pinLaunch);
    window.addEventListener("orientationchange", function () {
      window.setTimeout(pinLaunch, 80);
    });
    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", pinLaunch);
      window.visualViewport.addEventListener("scroll", pinLaunch);
    }
    if (window.MutationObserver && document.body) {
      var observer = new MutationObserver(function () {
        pinLaunch();
      });
      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["hidden"]
      });
    }
    window.addEventListener("load", pinLaunch);
  }

  function bind() {
    if (!ensureChrome()) return;

    bindLaunch(launch, toggleDrawer);
    bindLaunch(backdrop, close);
    bindHamburger(toggle);

    if (!listenersBound) {
      listenersBound = true;
      document.addEventListener("click", onDocumentClickCapture, true);
      document.addEventListener("click", onDocumentClickBubble);
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") forceClose();
      });
      sidebar.addEventListener("click", function (event) {
        if (gestureLocked()) return;
        var link = event.target.closest && event.target.closest('a[href^="#"]');
        if (link && mq.matches) {
          holdOpenUntil = 0;
          setOpen(false);
        }
      });
    }

    try {
      placeChrome();
      applyChrome(mq.matches ? widgetOpen() : false);
    } catch (err) { /* toggle is already bound */ }
    try {
      pinLaunch();
    } catch (err2) { /* toggle is already bound */ }
    try {
      bindWatchers();
    } catch (err3) { /* toggle is already bound */ }
    try {
      window.requestAnimationFrame(pinLaunch);
    } catch (err4) { /* toggle is already bound */ }
  }

  window.DAAB_TOC_DRAWER = {
    init: bind,
    bound: false,
    holdingOpen: holdingOpen
  };

  function start() {
    if (window.DAAB_TOC_DRAWER.bound) return;
    try {
      bind();
    } catch (err) {
      /* Listeners wired before positioning still work if a later step threw. */
    }
    if (sidebar && widget && launch && launch.getAttribute("data-daab-toc-bound")) {
      window.DAAB_TOC_DRAWER.bound = true;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
