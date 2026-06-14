(function () {
  "use strict";

  var searchInput = document.getElementById("inventionsSearch");
  var entries = Array.prototype.slice.call(document.querySelectorAll(".inventions-entry"));
  var categories = Array.prototype.slice.call(document.querySelectorAll(".inventions-category"));
  var widget = document.getElementById("inventionsArticlesWidget");
  var widgetBody = widget ? widget.querySelector(".widget-body") : null;
  var tocEntries = Array.prototype.slice.call(
    document.querySelectorAll(".inventions-toc-entry")
  );
  var tocCats = Array.prototype.slice.call(
    document.querySelectorAll(".inventions-toc-cat-row")
  );
  var mobileMq = window.matchMedia("(max-width: 1060px)");

  var navLinks = widget
    ? Array.prototype.slice.call(
        widget.querySelectorAll('.timeline-list a[href^="#"]')
      )
    : [];
  var linkById = {};
  var sections = [];

  navLinks.forEach(function (a) {
    var id = a.getAttribute("href").slice(1);
    if (!id) return;
    linkById[id] = a;
    var el = document.getElementById(id);
    if (el) sections.push(el);
  });

  sections.sort(function (a, b) {
    if (a === b) return 0;
    return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
  });

  var programmaticLock = false;
  var lockTimer = null;
  var scrollTick = false;
  var lastActiveId = "";

  function normalize(text) {
    return (text || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function stickyScrollOffset() {
    var root = document.documentElement;
    var style = window.getComputedStyle(root);
    var stack = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
    if (!isFinite(stack) || stack <= 0) {
      stack = parseFloat(style.getPropertyValue("--daab-nav-height"));
      if (!isFinite(stack) || stack <= 0) {
        var nav = document.querySelector(".nav-strip");
        stack = nav ? nav.getBoundingClientRect().height : 86;
      }
      var crumbsH = parseFloat(style.getPropertyValue("--daab-breadcrumbs-height"));
      if (isFinite(crumbsH) && crumbsH > 0) {
        stack += crumbsH;
      } else {
        var crumbs = document.getElementById("daab-breadcrumbs");
        if (crumbs) stack += crumbs.getBoundingClientRect().height;
      }
    }
    var gap = parseFloat(style.getPropertyValue("--daab-scroll-anchor-gap"));
    if (!isFinite(gap) || gap <= 0) gap = 20;
    return Math.ceil(stack) + gap;
  }

  function lockSpy(ms) {
    programmaticLock = true;
    clearTimeout(lockTimer);
    lockTimer = setTimeout(function () {
      programmaticLock = false;
      updateActiveFromScroll(true);
    }, ms || 900);
  }

  function applySearch() {
    if (!searchInput) return;
    var q = normalize(searchInput.value);

    entries.forEach(function (entry) {
      var hay = normalize(entry.getAttribute("data-search") || entry.textContent);
      entry.classList.toggle("is-hidden", q.length > 0 && hay.indexOf(q) === -1);
    });

    categories.forEach(function (cat) {
      var visible = cat.querySelectorAll(".inventions-entry:not(.is-hidden)").length;
      cat.classList.toggle("is-hidden", q.length > 0 && visible === 0);
    });

    tocEntries.forEach(function (item) {
      var hay = normalize(item.getAttribute("data-search") || item.textContent);
      item.classList.toggle("is-hidden", q.length > 0 && hay.indexOf(q) === -1);
    });

    tocCats.forEach(function (item) {
      var slug = item.getAttribute("data-toc-cat");
      var related = tocEntries.filter(function (e) {
        return e.getAttribute("data-toc-cat") === slug;
      });
      var anyVisible =
        !q.length ||
        related.some(function (e) {
          return !e.classList.contains("is-hidden");
        });
      item.classList.toggle("is-hidden", q.length > 0 && !anyVisible);
    });

    updateActiveFromScroll(true);
  }

  function clearActiveStates() {
    navLinks.forEach(function (l) {
      l.classList.remove("tl-active");
      l.removeAttribute("aria-current");
    });
    Array.prototype.forEach.call(
      document.querySelectorAll(".timeline-list li.toc-active"),
      function (li) {
        li.classList.remove("toc-active");
      }
    );
  }

  function scrollSidebarLinkIntoView(link) {
    if (!widgetBody || mobileMq.matches || !link) return;

    var row = link.closest("li") || link;
    var bodyRect = widgetBody.getBoundingClientRect();
    var rowRect = row.getBoundingClientRect();
    var pad = 10;

    if (rowRect.top < bodyRect.top + pad) {
      widgetBody.scrollTop += rowRect.top - bodyRect.top - pad;
    } else if (rowRect.bottom > bodyRect.bottom - pad) {
      widgetBody.scrollTop += rowRect.bottom - bodyRect.bottom + pad;
    }
  }

  function setActive(id, options) {
    options = options || {};
    var force = !!options.force;
    if (!id || (id === lastActiveId && !force)) {
      if (options.forceSidebarScroll && linkById[id]) {
        scrollSidebarLinkIntoView(linkById[id]);
      }
      return;
    }

    lastActiveId = id;
    clearActiveStates();

    var link = linkById[id];
    if (!link) return;

    link.classList.add("tl-active");
    link.setAttribute("aria-current", "true");

    var li = link.closest("li");
    if (li) li.classList.add("toc-active");

    if (li && li.classList.contains("inventions-toc-entry")) {
      var catSlug = li.getAttribute("data-toc-cat");
      if (catSlug) {
        var catRow = widget.querySelector('[data-toc-cat="' + catSlug + '"]');
        if (catRow) catRow.classList.add("toc-active");
      }
    }

    if (!options.skipSidebarScroll) {
      scrollSidebarLinkIntoView(link);
    }
  }

  function isSectionVisible(section) {
    if (!section || section.offsetParent === null) return false;
    if (section.classList.contains("is-hidden")) return false;
    return true;
  }

  function pickActiveSection() {
    if (!sections.length) return null;

    var offset = stickyScrollOffset();
    var active = null;
    var i;

    for (i = 0; i < sections.length; i += 1) {
      var section = sections[i];
      if (!isSectionVisible(section)) continue;
      var sectionTop = section.getBoundingClientRect().top;
      if (sectionTop - offset <= 2) {
        active = section;
      } else if (active) {
        break;
      }
    }

    if (active) return active;

    for (i = 0; i < sections.length; i += 1) {
      if (isSectionVisible(sections[i])) return sections[i];
    }

    return null;
  }

  function updateActiveFromScroll(force) {
    if (programmaticLock && !force) return;

    var active = pickActiveSection();
    if (active && active.id) {
      setActive(active.id, { skipSidebarScroll: false });
    }
  }

  function resolveScrollTarget(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    if (el.classList.contains("inventions-entry")) {
      return el.querySelector(".inventions-entry-title") || el;
    }
    if (el.classList.contains("inventions-category")) {
      return el.querySelector(".inventions-category-head") || el;
    }
    return el.querySelector("h2, h1") || el;
  }

  function jumpToTarget(id) {
    var target = resolveScrollTarget(id);
    if (!target) return false;

    var Pos = window.DAAB_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      return Pos.scrollToAnchor(id, false);
    }

    var root = document.documentElement;
    var prevBehavior = root.style.scrollBehavior;
    var top =
      target.getBoundingClientRect().top +
      (window.pageYOffset || root.scrollTop || 0) -
      stickyScrollOffset();

    root.style.scrollBehavior = "auto";
    window.scrollTo({ top: Math.max(0, Math.round(top)), left: 0, behavior: "auto" });
    window.requestAnimationFrame(function () {
      root.style.scrollBehavior = prevBehavior;
    });
    return true;
  }

  function scrollToSection(id) {
    if (!id || !document.getElementById(id)) return;

    lockSpy(480);
    setActive(id, { force: true, forceSidebarScroll: true });
    jumpToTarget(id);

    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#" + id);
    }

    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        setActive(id, { force: true, forceSidebarScroll: true });
      });
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", applySearch);
  }

  if (widget) {
    var toggle = widget.querySelector(".events-menu-toggle");

    if (toggle) {
      toggle.addEventListener("click", function () {
        var open = widget.classList.toggle("events-open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }

    navLinks.forEach(function (a) {
      var hrefId = a.getAttribute("href").slice(1);
      var row = a.closest("[data-toc-entry]");
      if (row && row.getAttribute("data-toc-entry") !== hrefId) {
        console.warn("TOC entry mismatch:", row.getAttribute("data-toc-entry"), hrefId);
      }
      if (hrefId && !document.getElementById(hrefId)) {
        console.warn("TOC link missing section:", hrefId);
      }

      a.addEventListener("click", function (e) {
        e.preventDefault();
        scrollToSection(hrefId);
      });
    });

    window.addEventListener(
      "scroll",
      function () {
        if (scrollTick) return;
        scrollTick = true;
        requestAnimationFrame(function () {
          scrollTick = false;
          updateActiveFromScroll(false);
        });
      },
      { passive: true }
    );

    window.addEventListener("resize", function () {
      updateActiveFromScroll(true);
    });

    mobileMq.addEventListener("change", function () {
      updateActiveFromScroll(true);
    });

    if (window.location.hash) {
      var hashId = window.location.hash.slice(1);
      if (linkById[hashId]) {
        setTimeout(function () {
          scrollToSection(hashId);
        }, 100);
      }
    } else {
      updateActiveFromScroll(true);
    }
  }
})();
