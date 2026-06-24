/**
 * In-page content search for activities, charter, work-done report, and application pages.
 * Search-only (no filters); styled like scientists/list.html toolbar search.
 */
(function () {
  "use strict";

  var PAGE_CFG = {
    "activities-news": {
      blocks: "article.news-card",
      navItem: ".timeline-list li",
      navTarget: function (li) {
        var a = li.querySelector('a[href^="#"]');
        return a ? a.getAttribute("href").slice(1) : "";
      },
      navText: function (li) {
        return li.textContent || "";
      },
    },
    "charter": {
      blocks: "section.charter-card",
      navItem: "#charterArticlesMenu li",
      navTarget: function (li) {
        var a = li.querySelector('a[href^="#"]');
        return a ? a.getAttribute("href").slice(1) : "";
      },
      navText: function (li) {
        return li.textContent || "";
      },
    },
    "work-done-2024-2026": {
      blocks: "section.report-section",
      navItem: ".report-toc .toc-link",
      navTarget: function (el) {
        return el.getAttribute("data-target") || "";
      },
      navText: function (el) {
        return el.textContent || "";
      },
    },
    "membership-application": {
      blocks: ".app-terms-panel, .form-section",
      navItem: "#appStepsMenu li",
      navTarget: function (li) {
        var a = li.querySelector('a[href^="#"]');
        return a ? a.getAttribute("href").slice(1) : "";
      },
      navText: function (li) {
        return li.textContent || "";
      },
    },
  };

  var STRINGS = {
    az: { clear: "Təmizlə" },
    en: { clear: "Clear" },
  };

  function norm(text) {
    return (text || "").replace(/\s+/g, " ").trim().toLocaleLowerCase();
  }

  function init() {
    var root = document.documentElement;
    var pageId = root.getAttribute("data-daab-page-id");
    var cfg = PAGE_CFG[pageId];
    if (!cfg) return;

    var lang = root.getAttribute("data-daab-lang") === "en" ? "en" : "az";
    var ui = STRINGS[lang];

    var input = document.getElementById("pageContentSearch");
    var clearBtn = document.getElementById("pageContentSearchClear");
    var emptyEl = document.getElementById("pageContentSearchEmpty");
    if (!input) return;

    var blocks = Array.prototype.slice.call(document.querySelectorAll(cfg.blocks));
    if (!blocks.length) return;

    var navItems = cfg.navItem
      ? Array.prototype.slice.call(document.querySelectorAll(cfg.navItem))
      : [];

    var blockTextCache = blocks.map(function (el) {
      return norm(el.textContent);
    });

    function findBlockForTarget(id) {
      if (!id) return null;
      var target = document.getElementById(id);
      if (!target) return null;
      for (var i = 0; i < blocks.length; i++) {
        if (blocks[i] === target || blocks[i].contains(target)) return blocks[i];
      }
      return null;
    }

    function blockMatches(block, q) {
      if (!q) return true;
      var idx = blocks.indexOf(block);
      return idx >= 0 && blockTextCache[idx].indexOf(q) !== -1;
    }

    function apply() {
      var q = norm(input.value);
      var total = 0;

      blocks.forEach(function (block, i) {
        var match = !q || blockTextCache[i].indexOf(q) !== -1;
        block.classList.toggle("page-content-search__hidden", !match);
        block.classList.toggle("page-content-search__match", !!q && match);
        if (match) total += 1;
      });

      navItems.forEach(function (item) {
        var targetId = cfg.navTarget(item);
        var textMatch = !!q && norm(cfg.navText(item)).indexOf(q) !== -1;
        var block = findBlockForTarget(targetId);
        var show = !q || textMatch || blockMatches(block, q);
        item.classList.toggle("page-content-search__hidden", !show);
      });

      if (clearBtn) clearBtn.hidden = !q;
      if (emptyEl) emptyEl.hidden = !q || total > 0;

      document.body.classList.toggle("page-content-search--active", !!q);
    }

    input.addEventListener("input", apply);
    input.addEventListener("search", apply);

    if (clearBtn) {
      clearBtn.textContent = ui.clear;
      clearBtn.addEventListener("click", function () {
        input.value = "";
        input.focus();
        apply();
      });
    }

    apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
