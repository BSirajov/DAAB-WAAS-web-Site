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

  links.forEach(function (link) {
    link.addEventListener("click", function (event) {
      var href = link.getAttribute("href") || "";
      var id = href.slice(1);
      if (!panelById(id)) return;
      event.preventDefault();
      showPanel(id, { scrollIntoView: true, smooth: false });
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

  showPanel(idFromHash(), { updateHash: false, scrollIntoView: false, closeMenu: false });
})();
