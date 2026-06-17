/**
 * Work-done report — sidebar TOC scroll + active section highlight.
 */
(function () {
  "use strict";

  var root = document.querySelector(".work-done-report");
  if (!root) return;

  function scrollOffset() {
    var nav = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue("--daab-nav-height") || "64",
      10
    );
    var crumbs = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue("--daab-breadcrumbs-height") || "0",
      10
    );
    return nav + crumbs + 16;
  }

  function scrollToTarget(id) {
    var el = document.getElementById(id);
    if (!el) return;
    var top = el.getBoundingClientRect().top + window.pageYOffset - scrollOffset();
    window.scrollTo({ top: top, behavior: "smooth" });
    try {
      if (history && history.replaceState) {
        history.replaceState(null, "", "#" + encodeURIComponent(id));
      }
    } catch (e) {}
  }

  var buttons = Array.prototype.slice.call(root.querySelectorAll(".toc-link[data-target]"));
  buttons.forEach(function (btn) {
    btn.addEventListener("click", function (ev) {
      ev.preventDefault();
      scrollToTarget(btn.getAttribute("data-target"));
    });
  });

  var targets = buttons
    .map(function (btn) {
      return document.getElementById(btn.getAttribute("data-target"));
    })
    .filter(Boolean);

  if ("IntersectionObserver" in window && targets.length) {
    var byId = {};
    buttons.forEach(function (btn) {
      byId[btn.getAttribute("data-target")] = btn;
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            buttons.forEach(function (btn) {
              btn.classList.remove("active");
            });
            var active = byId[entry.target.id];
            if (active) active.classList.add("active");
          }
        });
      },
      { root: null, rootMargin: "-12% 0px -68% 0px", threshold: 0.01 }
    );
    targets.forEach(function (el) {
      observer.observe(el);
    });
  }

  window.addEventListener("load", function () {
    var id = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (id) {
      setTimeout(function () {
        scrollToTarget(id);
      }, 180);
    }
  });
})();
