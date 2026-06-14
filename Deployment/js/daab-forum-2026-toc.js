/**
 * Forum 2026 — build sidebar TOC from section headings + scroll-spy.
 */
(function () {
  "use strict";

  var tocList = document.getElementById("forum2026TOC");
  if (!tocList) return;

  var content = document.getElementById("content");
  if (!content) return;

  var headings = Array.prototype.slice
    .call(content.querySelectorAll("h2.card-title, h3.forum-subheading, h3.day-title"))
    .filter(function (h) {
      return !h.closest(".page-hero");
    });

  function slugify(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[ə]/g, "e")
      .replace(/[ğ]/g, "g")
      .replace(/[ü]/g, "u")
      .replace(/[ş]/g, "s")
      .replace(/[ı]/g, "i")
      .replace(/[ö]/g, "o")
      .replace(/[ç]/g, "c")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "bolme";
  }

  function uniqueId(base) {
    var id = base;
    var i = 2;
    while (document.getElementById(id)) {
      id = base + "-" + i;
      i += 1;
    }
    return id;
  }

  tocList.innerHTML = "";

  headings.forEach(function (heading) {
    if (!heading.id) {
      heading.id = uniqueId(slugify(heading.textContent || ""));
    }

    var li = document.createElement("li");
    if (heading.tagName === "H3") {
      li.className = "toc-sub";
    }

    var a = document.createElement("a");
    a.href = "#" + heading.id;
    a.textContent = heading.textContent.replace(/\s+/g, " ").trim();
    li.appendChild(a);
    tocList.appendChild(li);
  });

  var links = Array.prototype.slice.call(tocList.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  var ids = links.map(function (a) {
    return a.getAttribute("href").slice(1);
  });
  var cards = ids
    .map(function (id) {
      return document.getElementById(id);
    })
    .filter(Boolean);

  var eventsWidget = document.querySelector(".sidebar-widget");
  var eventsToggle = document.querySelector(".events-menu-toggle");

  function sidebarStackMediaQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.sidebarStackMq === "function") {
      return window.DAAB_DESIGN.sidebarStackMq();
    }
    return window.matchMedia("(max-width: 1060px)");
  }

  var mobileQuery = sidebarStackMediaQuery();

  function activate(link) {
    links.forEach(function (a) {
      a.classList.remove("tl-active");
    });
    if (link) link.classList.add("tl-active");
  }

  function closeEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    eventsWidget.classList.remove("events-open");
    eventsToggle.setAttribute("aria-expanded", "false");
  }

  function toggleEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    var open = eventsWidget.classList.toggle("events-open");
    eventsToggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function jumpToTarget(event) {
    var link = event.currentTarget;
    var id = link.getAttribute("href").slice(1);
    var target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    activate(link);
    var Pos = window.DAAB_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      Pos.scrollToAnchor(id, false);
    } else {
      target.scrollIntoView({ block: "start", behavior: "auto" });
    }
    history.pushState(null, "", link.getAttribute("href"));
    if (mobileQuery.matches) closeEventsMenu();
  }

  function onScroll() {
    var mid = window.scrollY + window.innerHeight * 0.35;
    var active = null;
    for (var i = cards.length - 1; i >= 0; i--) {
      if (cards[i] && cards[i].offsetTop <= mid) {
        active = i;
        break;
      }
    }
    activate(active !== null ? links[ids.indexOf(cards[active].id)] : null);
  }

  links.forEach(function (link) {
    link.addEventListener("click", jumpToTarget);
  });

  if (eventsToggle) {
    eventsToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      toggleEventsMenu();
    });
  }

  document.addEventListener("click", function (event) {
    if (!mobileQuery.matches || !eventsWidget || !eventsWidget.classList.contains("events-open")) {
      return;
    }
    if (eventsWidget.contains(event.target)) return;
    closeEventsMenu();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeEventsMenu();
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function syncFromHash() {
    var id = location.hash.slice(1);
    var idx = id ? ids.indexOf(id) : -1;
    if (idx === -1) {
      activate(null);
      return;
    }
    var target = document.getElementById(id);
    if (!target) return;
    activate(links[idx]);
    var Pos = window.DAAB_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      Pos.scrollToAnchor(id, false);
    } else {
      target.scrollIntoView({ block: "start", behavior: "auto" });
    }
  }

  window.addEventListener("popstate", syncFromHash);

  if (location.hash) {
    var hashId = location.hash.slice(1);
    var hashLink = links.find(function (a) {
      return a.getAttribute("href") === "#" + hashId;
    });
    if (hashLink) {
      setTimeout(function () {
        jumpToTarget({ currentTarget: hashLink, preventDefault: function () {} });
      }, 120);
    }
  }
})();
