/**
 * Sticky in-page search — mounts below nav + breadcrumbs in #daab-top-chrome.
 * Filter mode for structured pages; find-in-page for other content pages.
 */
(function (global) {
  "use strict";

  var SKIP_PAGE_IDS = {
    "membership-flyer": 1,
    "sponsors-flyer": 1,
    "scientists-list": 1,
    "scientists-profiles": 1,
  };

  var PAGE_CFG = {
    "activities-news": {
      blocks: "article.news-card",
      navItem: ".timeline-list li",
      navTarget: navHrefTarget,
      navText: textOf,
    },
    charter: {
      blocks: "section.charter-card",
      navItem: "#charterArticlesMenu li",
      navTarget: navHrefTarget,
      navText: textOf,
    },
    "work-done-2024-2026": {
      blocks: "section.report-section",
      navItem: ".report-toc .toc-link",
      navTarget: function (el) {
        return el.getAttribute("data-target") || hrefTarget(el);
      },
      navText: textOf,
    },
    "membership-application": {
      blocks: ".app-terms-panel, .form-section",
      navItem: "#appStepsMenu li",
      navTarget: navHrefTarget,
      navText: textOf,
    },
    "forum-2026-register": {
      blocks: ".form-section",
      navItem: "#appStepsMenu li",
      navTarget: navHrefTarget,
      navText: textOf,
    },
    "complex-topics-approach": {
      blocks: "section.cta-card",
      navItem: ".cta-toc-item",
      navTarget: navHrefTarget,
      navText: function (li) {
        var t = li.querySelector(":scope > a .cta-toc-text, :scope > a");
        return (t || li).textContent || "";
      },
    },
    "complex-topics-informatics": {
      blocks: "section.cta-card",
      navItem: ".cta-toc-item",
      navTarget: navHrefTarget,
      navText: function (li) {
        var t = li.querySelector(":scope > a .cta-toc-text, :scope > a");
        return (t || li).textContent || "";
      },
    },
    "forum-2026": {
      blocks: "article.news-card",
      navItem: "#forum2026TOC li",
      navTarget: navHrefTarget,
      navText: textOf,
    },
  };

  var DISCOVER_BLOCKS = [
    "article.news-card",
    "section.charter-card",
    "section.report-section",
    "section.cta-card",
    ".form-section",
    ".app-terms-panel",
    "article.core-card",
    ".page-card",
  ].join(", ");

  var DEFAULTS = {
    az: {
      label: "Bu səhifədə axtar",
      placeholder: "Bu səhifədə axtar…",
      clear: "Təmizlə",
      empty: "Nəticə tapılmadı.",
      next: "Növbəti",
      prev: "Əvvəlki",
      count: "{current} / {total}",
    },
    en: {
      label: "Search this page",
      placeholder: "Search this page…",
      clear: "Clear",
      empty: "No results found.",
      next: "Next",
      prev: "Previous",
      count: "{current} / {total}",
    },
  };

  var PLACEHOLDERS = {
    charter: { az: "Nizamnamədə axtar…", en: "Search charter articles…" },
    "activities-news": { az: "Yeniliklərdə axtar…", en: "Search news…" },
    "work-done-2024-2026": { az: "Hesabatda axtar…", en: "Search this report…" },
    "membership-application": { az: "Müraciət formasında axtar…", en: "Search this form…" },
    "forum-2026-register": { az: "Qeydiyyat formasında axtar…", en: "Search this form…" },
    home: { az: "Bölmələrdə axtar…", en: "Search sections…" },
    "forum-2024": { az: "Bölmələrdə axtar…", en: "Search sections…" },
  };

  var AZ_FOLD = {
    "\u0259": "e",
    "\u0131": "i",
    "\u00f6": "o",
    "\u00fc": "u",
    "\u011f": "g",
    "\u015f": "s",
    "\u00e7": "c",
    "\u018f": "e",
    "\u0130": "i",
    "\u00d6": "o",
    "\u00dc": "u",
    "\u011e": "g",
    "\u015e": "s",
    "\u00c7": "c",
  };

  var SEARCH_ICON =
    '<svg fill="none" height="15" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="15" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" x2="16.65" y1="21" y2="16.65"></line></svg>';

  var ui = null;
  var input = null;
  var clearBtn = null;
  var prevBtn = null;
  var nextBtn = null;
  var statusEl = null;
  var emptyEl = null;
  var bar = null;
  var mode = "find";
  var cfg = null;
  var blocks = [];
  var navItems = [];
  var blockTextCache = [];
  var hits = [];
  var hitIndex = -1;
  var applyTimer = 0;

  function navHrefTarget(el) {
    var a = el.matches && el.matches("a[href^='#']") ? el : el.querySelector("a[href^='#']");
    return hrefTarget(a);
  }

  function hrefTarget(el) {
    if (!el) return "";
    var href = el.getAttribute("href") || "";
    return href.charAt(0) === "#" ? href.slice(1) : "";
  }

  function textOf(el) {
    return el ? el.textContent || "" : "";
  }

  function detectLang() {
    if (global.DAAB_I18N && typeof global.DAAB_I18N.detectLang === "function") {
      return global.DAAB_I18N.detectLang();
    }
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function strings() {
    var lang = detectLang();
    var pack = Object.assign({}, DEFAULTS[lang] || DEFAULTS.en);
    var block = ui && ui.pageSearch && ui.pageSearch[lang];
    if (block) {
      Object.keys(pack).forEach(function (key) {
        if (block[key]) pack[key] = block[key];
      });
    }
    var pageId = document.documentElement.getAttribute("data-daab-page-id") || "";
    var ph = PLACEHOLDERS[pageId];
    if (ph && ph[lang]) pack.placeholder = ph[lang];
    return pack;
  }

  function shouldSkip() {
    if (document.body && document.body.classList.contains("daab-gateway")) return true;
    var pageId = document.documentElement.getAttribute("data-daab-page-id") || "";
    return !!SKIP_PAGE_IDS[pageId];
  }

  function contentRoot() {
    return (
      document.getElementById("content") ||
      document.querySelector("main.main, main") ||
      document.body
    );
  }

  function foldAz(text) {
    return String(text || "").replace(/[^\u0000-\u007f]/g, function (ch) {
      return AZ_FOLD[ch] || ch;
    });
  }

  function norm(text) {
    return foldAz(text)
      .toLowerCase()
      .replace(/\u0307/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function foldForIndex(text) {
    return foldAz(text).toLowerCase();
  }

  function resolveMode() {
    var pageId = document.documentElement.getAttribute("data-daab-page-id") || "";
    if (document.getElementById("cardSearch")) {
      mode = "hub";
      cfg = {
        blocks: ".page-card",
        navItem: "",
        navTarget: function () { return ""; },
        navText: textOf,
      };
      return;
    }
    if (PAGE_CFG[pageId]) {
      mode = "filter";
      cfg = PAGE_CFG[pageId];
      return;
    }
    var found = Array.prototype.slice.call(document.querySelectorAll(DISCOVER_BLOCKS));
    found = found.filter(function (el) {
      return !el.closest(".sidebar, .cta-toc, .report-toc, .nav-strip, #daab-top-chrome, footer");
    });
    if (found.length >= 2) {
      mode = "filter";
      cfg = {
        blocks: DISCOVER_BLOCKS,
        navItem: ".sidebar .timeline-list li, .cta-toc-item, .report-toc .toc-link",
        navTarget: navHrefTarget,
        navText: textOf,
      };
      return;
    }
    mode = "find";
    cfg = null;
  }

  function collectBlocks() {
    if (mode === "find") {
      blocks = [];
      navItems = [];
      blockTextCache = [];
      return;
    }
    blocks = Array.prototype.slice.call(document.querySelectorAll(cfg.blocks)).filter(function (el) {
      return !el.closest("#daab-top-chrome, .daab-page-search, footer");
    });
    blockTextCache = blocks.map(function (el) {
      return norm(el.textContent);
    });
    navItems = cfg.navItem
      ? Array.prototype.slice.call(document.querySelectorAll(cfg.navItem))
      : [];
  }

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
    if (!q || !block) return !q;
    var idx = blocks.indexOf(block);
    return idx >= 0 && blockTextCache[idx].indexOf(q) !== -1;
  }

  function searchScope() {
    var root = contentRoot();
    if (!root) return null;
    var clone = root;
    return clone;
  }

  function unwrapHits(root) {
    if (!root) return;
    var marks = root.querySelectorAll("mark.daab-page-search-hit");
    for (var i = marks.length - 1; i >= 0; i--) {
      var mark = marks[i];
      var parent = mark.parentNode;
      if (!parent) continue;
      while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
      parent.removeChild(mark);
      parent.normalize();
    }
  }

  function highlightQuery(root, q) {
    unwrapHits(root);
    hits = [];
    hitIndex = -1;
    if (!q || !root) return;

    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !norm(node.nodeValue)) return NodeFilter.FILTER_REJECT;
        var p = node.parentNode;
        if (!p || /^(SCRIPT|STYLE|NOSCRIPT|TEXTAREA|INPUT|SELECT|OPTION)$/i.test(p.nodeName)) {
          return NodeFilter.FILTER_REJECT;
        }
        if (
          p.closest(
            "#daab-top-chrome, .daab-page-search, .sidebar, .cta-toc, .report-toc, footer, .nav-strip, .page-content-search__hidden"
          )
        ) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(function (node) {
      var text = node.nodeValue;
      var lower = foldForIndex(text);
      var idx = 0;
      var pos;
      var pieces = [];
      while ((pos = lower.indexOf(q, idx)) !== -1) {
        if (pos > idx) pieces.push(document.createTextNode(text.slice(idx, pos)));
        var mark = document.createElement("mark");
        mark.className = "daab-page-search-hit";
        mark.textContent = text.slice(pos, pos + q.length);
        pieces.push(mark);
        hits.push(mark);
        idx = pos + q.length;
      }
      if (!pieces.length) return;
      if (idx < text.length) pieces.push(document.createTextNode(text.slice(idx)));
      var frag = document.createDocumentFragment();
      pieces.forEach(function (piece) {
        frag.appendChild(piece);
      });
      node.parentNode.replaceChild(frag, node);
    });
  }

  function showHit(index) {
    if (!hits.length) return;
    if (index < 0) index = hits.length - 1;
    if (index >= hits.length) index = 0;
    hits.forEach(function (hit) {
      hit.classList.remove("is-current");
    });
    hitIndex = index;
    var current = hits[hitIndex];
    current.classList.add("is-current");
    current.scrollIntoView({ block: "center", inline: "nearest", behavior: "smooth" });
    updateStatus();
  }

  function updateStatus() {
    var s = strings();
    if (!statusEl) return;
    if (mode === "hub") {
      statusEl.hidden = true;
      statusEl.textContent = "";
      return;
    }
    var q = norm(input && input.value);
    if (!q) {
      statusEl.hidden = true;
      statusEl.textContent = "";
      return;
    }
    statusEl.hidden = false;
    if (!hits.length) {
      statusEl.textContent = s.empty;
      return;
    }
    statusEl.textContent = s.count
      .replace("{current}", String(hitIndex + 1))
      .replace("{total}", String(hits.length));
  }

  function applyFilter(q) {
    var total = 0;
    blocks.forEach(function (block, i) {
      var match = !q || blockTextCache[i].indexOf(q) !== -1;
      block.classList.toggle("page-content-search__hidden", !match);
      block.classList.toggle("page-content-search__match", !!q && match);
      if (match) total += 1;
    });

    var liveNav = cfg.navItem
      ? Array.prototype.slice.call(document.querySelectorAll(cfg.navItem))
      : navItems;
    liveNav.forEach(function (item) {
      var targetId = cfg.navTarget(item);
      var textMatch = !!q && norm(cfg.navText(item)).indexOf(q) !== -1;
      var block = findBlockForTarget(targetId);
      var show = !q || textMatch || blockMatches(block, q);
      item.classList.toggle("page-content-search__hidden", !show);
    });

    if (emptyEl) emptyEl.hidden = !q || total > 0;
  }

  function applyHub(q) {
    var hub = document.getElementById("cardSearch");
    if (hub && hub.value !== (input ? input.value : "")) {
      hub.value = input.value;
      hub.dispatchEvent(new Event("input", { bubbles: true }));
    }
    var visible = 0;
    document.querySelectorAll(".page-card").forEach(function (card) {
      if (card.style.display !== "none" && !card.classList.contains("page-content-search__hidden")) {
        visible += 1;
      }
    });
    var hubEmpty = document.getElementById("cardSearchEmpty");
    if (hubEmpty) hubEmpty.hidden = !q || visible !== 0;
    if (emptyEl && emptyEl !== hubEmpty) emptyEl.hidden = !q || visible !== 0;
  }

  function apply() {
    if (!input) return;
    var q = norm(input.value);
    if (clearBtn) clearBtn.hidden = !q;
    if (prevBtn) prevBtn.hidden = mode === "hub" || !q;
    if (nextBtn) nextBtn.hidden = mode === "hub" || !q;
    document.body.classList.toggle("page-content-search--active", !!q);
    document.documentElement.classList.toggle("daab-page-search-active", !!q);

    if (mode === "hub") {
      applyHub(q);
      return;
    }
    if (mode === "filter") {
      unwrapHits(searchScope());
      if (!blocks.length) collectBlocks();
      applyFilter(q);
      highlightQuery(searchScope(), q);
      if (q && hits.length) showHit(0);
      else updateStatus();
      return;
    }

    if (emptyEl) emptyEl.hidden = true;
    highlightQuery(searchScope(), q);
    if (q && hits.length) showHit(0);
    else updateStatus();
  }

  function scheduleApply() {
    if (applyTimer) global.clearTimeout(applyTimer);
    applyTimer = global.setTimeout(apply, 40);
  }

  function applyLabels() {
    var s = strings();
    if (!input) return;
    input.setAttribute("aria-label", s.label);
    input.setAttribute("placeholder", s.placeholder);
    if (bar) bar.setAttribute("aria-label", s.label);
    if (clearBtn) clearBtn.textContent = s.clear;
    if (prevBtn) {
      prevBtn.setAttribute("aria-label", s.prev);
      prevBtn.setAttribute("title", s.prev);
    }
    if (nextBtn) {
      nextBtn.setAttribute("aria-label", s.next);
      nextBtn.setAttribute("title", s.next);
    }
    if (emptyEl && !emptyEl.querySelector("svg")) {
      emptyEl.textContent = s.empty;
    } else if (emptyEl) {
      var label = emptyEl.querySelector("[data-daab-page-search-empty-text]");
      if (label) label.textContent = s.empty;
    }
    updateStatus();
  }

  function retireLegacyInput() {
    var old = document.getElementById("pageContentSearch");
    if (!old) return;
    old.removeAttribute("id");
    old.setAttribute("data-daab-page-search-legacy", "1");
    old.tabIndex = -1;
    old.setAttribute("aria-hidden", "true");
  }

  function ensureEmpty() {
    emptyEl = document.getElementById("pageContentSearchEmpty");
    if (emptyEl || mode === "find" || mode === "hub") return;
    emptyEl = document.createElement("div");
    emptyEl.id = "pageContentSearchEmpty";
    emptyEl.className = "no-results page-content-search__empty";
    emptyEl.hidden = true;
    emptyEl.innerHTML =
      SEARCH_ICON + '<span data-daab-page-search-empty-text></span>';
    var main = contentRoot();
    if (main && main.parentNode) main.parentNode.insertBefore(emptyEl, main);
  }

  function mountBar() {
    bar = document.getElementById("daab-page-search");
    if (bar) {
      input = document.getElementById("pageContentSearch");
      clearBtn = document.getElementById("pageContentSearchClear");
      prevBtn = document.getElementById("pageContentSearchPrev");
      nextBtn = document.getElementById("pageContentSearchNext");
      statusEl = document.getElementById("pageContentSearchStatus");
      return;
    }

    retireLegacyInput();

    bar = document.createElement("div");
    bar.id = "daab-page-search";
    bar.className = "daab-page-search";
    bar.setAttribute("role", "search");

    var inner = document.createElement("div");
    inner.className = "daab-page-search__inner";

    var field = document.createElement("div");
    field.className = "daab-page-search__field";
    field.innerHTML = SEARCH_ICON;

    input = document.createElement("input");
    input.type = "search";
    input.id = "pageContentSearch";
    input.autocomplete = "off";
    input.setAttribute("enterkeyhint", "search");

    field.appendChild(input);

    statusEl = document.createElement("p");
    statusEl.id = "pageContentSearchStatus";
    statusEl.className = "daab-page-search__status";
    statusEl.setAttribute("aria-live", "polite");
    statusEl.hidden = true;

    prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.id = "pageContentSearchPrev";
    prevBtn.className = "daab-page-search__nav";
    prevBtn.hidden = true;
    prevBtn.innerHTML =
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>';

    nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.id = "pageContentSearchNext";
    nextBtn.className = "daab-page-search__nav";
    nextBtn.hidden = true;
    nextBtn.innerHTML =
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';

    clearBtn = document.createElement("button");
    clearBtn.type = "button";
    clearBtn.id = "pageContentSearchClear";
    clearBtn.className = "daab-page-search__clear btn-clear";
    clearBtn.hidden = true;

    inner.appendChild(field);
    inner.appendChild(statusEl);
    inner.appendChild(prevBtn);
    inner.appendChild(nextBtn);
    inner.appendChild(clearBtn);
    bar.appendChild(inner);

    var chrome = document.getElementById("daab-top-chrome");
    if (chrome) {
      chrome.appendChild(bar);
    } else {
      var nav = document.querySelector(".nav-strip");
      if (nav && nav.parentNode) {
        if (nav.nextSibling) nav.parentNode.insertBefore(bar, nav.nextSibling);
        else nav.parentNode.appendChild(bar);
      } else {
        document.body.insertBefore(bar, document.body.firstChild);
      }
    }
  }

  function bind() {
    input.addEventListener("input", scheduleApply);
    input.addEventListener("search", scheduleApply);
    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        input.value = "";
        apply();
        event.preventDefault();
        return;
      }
      if (event.key === "Enter" && hits.length) {
        event.preventDefault();
        showHit(event.shiftKey ? hitIndex - 1 : hitIndex + 1);
      }
    });

    clearBtn.addEventListener("click", function () {
      input.value = "";
      input.focus();
      apply();
    });
    prevBtn.addEventListener("click", function () {
      showHit(hitIndex - 1);
    });
    nextBtn.addEventListener("click", function () {
      showHit(hitIndex + 1);
    });
  }

  function notifyChrome() {
    document.documentElement.classList.add("daab-page-search-ready");
    document.dispatchEvent(new CustomEvent("daab-page-search-ready"));
    if (global.DAAB_STICKY_CHROME && typeof global.DAAB_STICKY_CHROME.sync === "function") {
      global.DAAB_STICKY_CHROME.sync();
    }
  }

  function waitForChrome(done) {
    if (document.getElementById("daab-top-chrome") || document.documentElement.classList.contains("daab-chrome-ready")) {
      done();
      return;
    }
    var n = 0;
    var t = global.setInterval(function () {
      n += 1;
      if (document.getElementById("daab-top-chrome") || n > 40) {
        global.clearInterval(t);
        done();
      }
    }, 50);
  }

  function boot() {
    if (shouldSkip() || document.getElementById("daab-page-search")) return;
    resolveMode();
    if (mode === "filter" || mode === "hub") collectBlocks();
    if (mode === "filter" && !blocks.length && !document.getElementById("cardSearch")) {
      mode = "find";
      cfg = null;
    }
    if (mode === "find" && !contentRoot()) return;

    waitForChrome(function () {
      if (shouldSkip()) return;
      resolveMode();
      collectBlocks();
      if (mode === "filter" && !blocks.length) mode = "find";
      mountBar();
      ensureEmpty();
      applyLabels();
      bind();
      apply();
      notifyChrome();
    });
  }

  function init() {
    var uiPromise =
      global.DAAB_I18N && global.DAAB_I18N.loadUi ? global.DAAB_I18N.loadUi() : Promise.resolve(null);
    uiPromise
      .then(function (data) {
        ui = data;
      })
      .catch(function () {
        ui = null;
      })
      .then(function () {
        boot();
        applyLabels();
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(window);
