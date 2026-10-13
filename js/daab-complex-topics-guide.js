/**
 * Complex Topics guide: News-style sidebar switches dynamic content panels.
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

  var widget = root.querySelector(".ct-guide-nav .sidebar-widget");
  var toggle = root.querySelector(".ct-guide-nav .events-menu-toggle");

  function sidebarStackMq() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.sidebarStackMq === "function") {
      return window.DAAB_DESIGN.sidebarStackMq();
    }
    return window.matchMedia("(max-width: 1060px)");
  }

  var mobileQuery = sidebarStackMq();

  function panelById(id) {
    for (var i = 0; i < panels.length; i++) {
      if (panels[i].id === id) return panels[i];
    }
    return null;
  }

  function linkById(id) {
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href") || "";
      if (href.slice(1) === id) return links[i];
    }
    return null;
  }

  function closeMenu() {
    if (!widget || !toggle) return;
    widget.classList.remove("events-open");
    toggle.setAttribute("aria-expanded", "false");
  }

  function toggleMenu() {
    if (!widget || !toggle) return;
    var open = widget.classList.toggle("events-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
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
    if (opts.closeMenu !== false && mobileQuery.matches) closeMenu();

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
      showPanel(href.slice(1), { scrollIntoView: false });
      target.focus();
    });
  });

  if (toggle && widget) {
    toggle.addEventListener("click", function (event) {
      event.preventDefault();
      toggleMenu();
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
})();
