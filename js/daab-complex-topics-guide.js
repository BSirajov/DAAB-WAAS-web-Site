/**
 * Complex Topics guide: News-style sidebar switches dynamic content panels.
 * On ≤1060px the Details sidebar becomes a right-edge off-canvas drawer.
 */
(function () {
  "use strict";

  var root = document.querySelector(".ct-guide");
  if (!root) return;

  var links = Array.prototype.slice.call(
    root.querySelectorAll(".ct-guide-nav .timeline-list a[href^='#']")
  );
  var panels = Array.prototype.slice.call(
    root.querySelectorAll(".ct-guide-panels > .ct-guide-block[id]")
  );
  if (!links.length || !panels.length) return;

  var drawer = root.querySelector("#ctDetailsDrawer") || root.querySelector(".ct-guide-nav");
  var launch = root.querySelector("#ctDetailsLaunch") || root.querySelector(".ct-details-launch");
  var closeBtn = root.querySelector("#ctDetailsClose") || root.querySelector(".ct-details-close");
  var backdrop = root.querySelector("#ctDetailsBackdrop") || root.querySelector(".ct-details-backdrop");
  var html = document.documentElement;
  var lastFocus = null;
  var gestureLockUntil = 0;

  function sidebarStackMq() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.sidebarStackMq === "function") {
      return window.DAAB_DESIGN.sidebarStackMq();
    }
    return window.matchMedia("(max-width: 1060px)");
  }

  var mobileQuery = sidebarStackMq();

  function isDrawerMode() {
    return mobileQuery.matches;
  }

  function isOpen() {
    return html.classList.contains("ct-details-drawer-open");
  }

  function gestureLocked() {
    return !!(gestureLockUntil && Date.now() < gestureLockUntil);
  }

  function armGesture() {
    gestureLockUntil = Date.now() + 500;
  }

  function navTopPx() {
    var raw = "";
    try {
      raw = window.getComputedStyle(html).getPropertyValue("--daab-sticky-top-stack") || "";
    } catch (err) {
      raw = "";
    }
    var n = parseFloat(raw);
    if (!isFinite(n) || n < 1) n = 86;
    return n;
  }

  function measureDrawerBox() {
    var top = navTopPx();
    var chrome = document.getElementById("daab-top-chrome");
    if (chrome) {
      var rect = chrome.getBoundingClientRect();
      if (rect && rect.bottom > top) top = rect.bottom;
    }
    var vv = window.visualViewport;
    var offset = vv && isFinite(vv.offsetTop) && vv.offsetTop > 0 ? vv.offsetTop : 0;
    var viewH = vv && isFinite(vv.height) && vv.height > 0 ? vv.height + offset : window.innerHeight || 0;
    var layoutTop = Math.round(top + offset);
    var height = Math.round(viewH - layoutTop);
    if (!(height > 160)) {
      var fallback = Math.round((window.innerHeight || 0) - top);
      if (fallback > height) height = fallback;
    }
    if (!(height > 160)) height = 480;
    return { top: layoutTop, height: height };
  }

  var drawerBoxProps = ["top", "right", "bottom", "left", "height", "min-height", "max-height", "transform", "-webkit-transform"];

  function clearDrawerBoxInline() {
    if (!drawer) return;
    drawerBoxProps.forEach(function (prop) {
      drawer.style.removeProperty(prop);
    });
  }

  function applyDrawerBox(open) {
    if (!isDrawerMode()) {
      html.style.removeProperty("--ct-details-drawer-top");
      html.style.removeProperty("--ct-details-drawer-height");
      clearDrawerBoxInline();
      return;
    }
    var box = measureDrawerBox();
    html.style.setProperty("--ct-details-drawer-top", box.top + "px");
    html.style.setProperty("--ct-details-drawer-height", box.height + "px");
    if (!open || !drawer) {
      clearDrawerBoxInline();
      return;
    }
    drawer.style.setProperty("top", box.top + "px", "important");
    drawer.style.setProperty("right", "0px", "important");
    drawer.style.setProperty("left", "auto", "important");
    drawer.style.setProperty("bottom", "auto", "important");
    drawer.style.setProperty("height", box.height + "px", "important");
    drawer.style.setProperty("min-height", box.height + "px", "important");
    drawer.style.setProperty("max-height", box.height + "px", "important");
    drawer.style.setProperty("transform", "none", "important");
    drawer.style.setProperty("-webkit-transform", "none", "important");
  }

  function setAria(open) {
    if (launch) launch.setAttribute("aria-expanded", open ? "true" : "false");
    if (drawer) {
      if (isDrawerMode()) {
        drawer.setAttribute("aria-hidden", open ? "false" : "true");
        if (open) drawer.setAttribute("aria-modal", "true");
        else drawer.removeAttribute("aria-modal");
      } else {
        drawer.setAttribute("aria-hidden", "false");
        drawer.removeAttribute("aria-modal");
      }
    }
    if (backdrop) {
      backdrop.hidden = !open;
      backdrop.setAttribute("aria-hidden", open ? "false" : "true");
    }
  }

  function setOpen(open) {
    if (!isDrawerMode()) open = false;
    html.classList.toggle("ct-details-drawer-open", open);
    document.documentElement.classList.toggle("daab-scroll-lock", open);
    document.body.classList.toggle("daab-scroll-lock", open);
    setAria(open);
    try {
      applyDrawerBox(open);
    } catch (err) {
      /* sizing failure must not undo open state */
    }
    if (open) {
      lastFocus = document.activeElement;
      if (closeBtn) {
        try {
          closeBtn.focus();
        } catch (err2) {
          /* ignore */
        }
      }
    } else if (lastFocus && typeof lastFocus.focus === "function") {
      try {
        lastFocus.focus();
      } catch (err3) {
        /* ignore */
      }
      lastFocus = null;
    }
  }

  function closeDrawer() {
    setOpen(false);
  }

  function openDrawer() {
    setOpen(true);
  }

  function toggleDrawer() {
    if (!isDrawerMode()) return;
    setOpen(!isOpen());
  }

  function runAction(action) {
    if (gestureLocked()) return;
    armGesture();
    action();
  }

  function panelById(id) {
    for (var i = 0; i < panels.length; i++) {
      if (panels[i].id === id) return panels[i];
    }
    return null;
  }

  function setHash(id) {
    var href = "#" + id;
    if (location.hash === href) return;
    try {
      if (history.replaceState) history.replaceState(null, "", href);
    } catch (err) {
      /* ignore */
    }
  }

  function showPanel(id, opts) {
    opts = opts || {};
    var panel = panelById(id);
    if (!panel) return false;

    panels.forEach(function (el) {
      var active = el === panel;
      el.hidden = !active;
      el.classList.toggle("is-active", active);
      el.setAttribute("aria-hidden", active ? "false" : "true");
    });

    links.forEach(function (a) {
      var match = (a.getAttribute("href") || "").slice(1) === id;
      a.classList.toggle("tl-active", match);
      a.setAttribute("aria-selected", match ? "true" : "false");
      a.setAttribute("aria-current", match ? "true" : "false");
      a.setAttribute("tabindex", match ? "0" : "-1");
    });

    if (opts.updateHash !== false) setHash(id);
    if (opts.closeMenu !== false && isDrawerMode()) closeDrawer();

    if (opts.scrollIntoView) {
      var layout = root.querySelector(".ct-guide-layout");
      var target = layout || panel;
      var top =
        target.getBoundingClientRect().top +
        window.pageYOffset -
        (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--daab-sticky-top-stack")) ||
          96) -
        12;
      window.scrollTo({ top: Math.max(0, top), behavior: opts.smooth ? "smooth" : "auto" });
    }

    return true;
  }

  function idFromHash() {
    var hash = (location.hash || "").replace(/^#/, "");
    if (hash && panelById(hash)) return hash;
    var first = panels[0] && panels[0].id;
    return first || "";
  }

  panels.forEach(function (panel) {
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("tabindex", "0");
  });

  links.forEach(function (link, index) {
    link.setAttribute("tabindex", link.classList.contains("tl-active") ? "0" : "-1");
    link.addEventListener("click", function (event) {
      var href = link.getAttribute("href") || "";
      var id = href.slice(1);
      if (!panelById(id)) return;
      event.preventDefault();
      showPanel(id, { scrollIntoView: true, smooth: false });
      link.focus();
    });
    link.addEventListener("keydown", function (event) {
      var key = event.key;
      var next = -1;
      if (key === "ArrowDown" || key === "ArrowRight") next = (index + 1) % links.length;
      else if (key === "ArrowUp" || key === "ArrowLeft") next = (index - 1 + links.length) % links.length;
      else if (key === "Home") next = 0;
      else if (key === "End") next = links.length - 1;
      if (next < 0) return;
      event.preventDefault();
      var target = links[next];
      var href = target.getAttribute("href") || "";
      showPanel(href.slice(1), { scrollIntoView: false, closeMenu: false });
      target.focus();
    });
  });

  if (launch) {
    launch.addEventListener("click", function (event) {
      event.preventDefault();
      runAction(toggleDrawer);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", function (event) {
      event.preventDefault();
      runAction(closeDrawer);
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", function (event) {
      event.preventDefault();
      runAction(closeDrawer);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    if (!isOpen()) return;
    event.preventDefault();
    closeDrawer();
  });

  function onViewportChange() {
    if (!isDrawerMode()) {
      closeDrawer();
      setAria(false);
      applyDrawerBox(false);
      return;
    }
    setAria(isOpen());
    applyDrawerBox(isOpen());
  }

  if (typeof mobileQuery.addEventListener === "function") {
    mobileQuery.addEventListener("change", onViewportChange);
  } else if (typeof mobileQuery.addListener === "function") {
    mobileQuery.addListener(onViewportChange);
  }

  window.addEventListener("resize", function () {
    if (isOpen()) applyDrawerBox(true);
  });

  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", function () {
      if (isOpen()) applyDrawerBox(true);
    });
  }

  window.addEventListener("hashchange", function () {
    var id = idFromHash();
    if (id) showPanel(id, { updateHash: false, scrollIntoView: false });
  });

  var initial = showPanel(idFromHash(), {
    updateHash: false,
    scrollIntoView: false,
    closeMenu: false,
  });
  if (initial) {
    links.forEach(function (link) {
      link.setAttribute("tabindex", link.classList.contains("tl-active") ? "0" : "-1");
    });
  }

  onViewportChange();
})();

/**
 * Touch-friendly tip toggle for pills / formats / core items on Complex Topics.
 * Hover and keyboard focus keep working; coarse pointers can tap to open/close.
 */
(function () {
  "use strict";

  if (!document.documentElement || document.documentElement.getAttribute("data-daab-page-id") !== "complex-topics") {
    return;
  }

  var TIP_HOSTS = ".ct-core-item";
  var hosts = Array.prototype.slice.call(document.querySelectorAll(TIP_HOSTS));
  if (!hosts.length) return;

  function coarsePointer() {
    try {
      return window.matchMedia("(hover: none), (pointer: coarse)").matches;
    } catch (err) {
      return "ontouchstart" in window;
    }
  }

  function closeAll(except) {
    hosts.forEach(function (el) {
      if (el === except) return;
      el.classList.remove("is-tip-open");
      el.removeAttribute("aria-expanded");
    });
  }

  function toggleTip(host) {
    var open = !host.classList.contains("is-tip-open");
    closeAll(open ? host : null);
    host.classList.toggle("is-tip-open", open);
    if (open) host.setAttribute("aria-expanded", "true");
    else host.removeAttribute("aria-expanded");
  }

  hosts.forEach(function (host) {
    host.addEventListener("click", function (event) {
      if (!coarsePointer()) return;
      if (event.target.closest("a, button, input, label")) return;
      event.preventDefault();
      toggleTip(host);
    });

    host.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;
      if (!host.classList.contains("is-tip-open")) return;
      host.classList.remove("is-tip-open");
      host.removeAttribute("aria-expanded");
    });
  });

  document.addEventListener("click", function (event) {
    if (!coarsePointer()) return;
    if (event.target.closest(TIP_HOSTS)) return;
    closeAll(null);
  });
})();
