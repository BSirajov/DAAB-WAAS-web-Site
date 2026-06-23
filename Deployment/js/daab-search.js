/**
 * WAAS / DAAB site-wide search — index-backed overlay with AZ normalization.
 */
(function (global) {
  "use strict";

  var INDEX_URL = null;
  var DEBOUNCE_MS = 80;
  var MAX_RESULTS = 24;

  var AZ_MAP = {
    "\u0259": "e", "\u0131": "i", "\u00f6": "o", "\u00fc": "u",
    "\u011f": "g", "\u015f": "s", "\u00e7": "c",
    "\u018f": "e", "\u0130": "i", "\u00d6": "o", "\u00dc": "u",
    "\u011e": "g", "\u015e": "s", "\u00c7": "c"
  };

  var state = {
    lang: "az",
    labels: null,
    entries: [],
    filtered: [],
    focusIndex: -1,
    debounceTimer: null,
    ready: false,
    indexLoading: false,
    indexLoadPromise: null
  };

  function assetRoot() {
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root != null && root !== "") {
      return root.endsWith("/") ? root : root + "/";
    }
    return "";
  }

  function detectLang() {
    var isGatewayPage = document.body && document.body.classList.contains("daab-gateway");
    var I18N = global.DAAB_I18N;
    if (isGatewayPage && I18N && I18N.readPersistedLang) {
      var saved = I18N.readPersistedLang();
      if (saved === "en" || saved === "az") return saved;
      return "az";
    }
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(location.pathname.replace(/\\/g, "/")) ? "en" : "az";
  }

  function normalizeText(text) {
    var out = String(text || "");
    out = out.replace(/<[^>]+>/g, " ");
    var i;
    for (i = 0; i < out.length; i++) {
      if (AZ_MAP[out.charAt(i)]) {
        out = out.split(out.charAt(i)).join(AZ_MAP[out.charAt(i)]);
      }
    }
    return out
      .toLowerCase()
      .replace(/[^\w\s@.-]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function highlight(text, query) {
    if (!text || !query) return escapeHtml(text);
    var words = normalizeText(query).split(/\s+/).filter(Boolean);
    if (!words.length) return escapeHtml(text);

    var src = String(text);
    var spans = [];
    var lower = normalizeText(src);
    words.forEach(function (word) {
      var start = 0;
      var idx;
      while ((idx = lower.indexOf(word, start)) !== -1) {
        spans.push([idx, idx + word.length]);
        start = idx + word.length;
      }
    });
    if (!spans.length) return escapeHtml(text);

    spans.sort(function (a, b) { return a[0] - b[0]; });
    var merged = [];
    spans.forEach(function (span) {
      var last = merged[merged.length - 1];
      if (last && span[0] <= last[1]) {
        last[1] = Math.max(last[1], span[1]);
      } else {
        merged.push([span[0], span[1]]);
      }
    });

    var out = "";
    var pos = 0;
    merged.forEach(function (span) {
      if (span[0] > pos) out += escapeHtml(src.slice(pos, span[0]));
      out += "<mark class=\"search-hl\">" + escapeHtml(src.slice(span[0], span[1])) + "</mark>";
      pos = span[1];
    });
    if (pos < src.length) out += escapeHtml(src.slice(pos));
    return out;
  }

  function resolveHref(entry) {
    var I18N = global.DAAB_I18N;
    if (!I18N || !I18N.loadRoutes) {
      return entry.anchor ? "#" + entry.anchor : "#";
    }
    return I18N.loadRoutes().then(function (routes) {
      var pages = routes.pages || [];
      var page = null;
      for (var i = 0; i < pages.length; i++) {
        if (pages[i].id === entry.pageId) {
          page = pages[i];
          break;
        }
      }
      var href = I18N.pageHref(page, entry.lang);
      if (entry.anchor) {
        href += "#" + encodeURIComponent(entry.anchor);
      }
      return href;
    });
  }

  function scoreEntry(entry, queryNorm, tokens) {
    if (entry.lang !== state.lang) return 0;
    var corpus = entry.norm || "";
    var titleNorm = normalizeText(entry.title);
    var score = entry.boost || 5;

    if (!queryNorm) return 0;
    if (titleNorm === queryNorm) return score + 40;
    if (titleNorm.indexOf(queryNorm) === 0) score += 24;
    if (corpus.indexOf(queryNorm) !== -1) score += 18;

    tokens.forEach(function (token) {
      if (!token) return;
      if (titleNorm.indexOf(token) !== -1) score += 10;
      else if (corpus.indexOf(token) !== -1) score += 4;
      else {
        var parts = corpus.split(/\s+/);
        for (var i = 0; i < parts.length; i++) {
          if (parts[i].indexOf(token) === 0) {
            score += 2;
            break;
          }
        }
      }
    });

    return score > (entry.boost || 5) ? score : 0;
  }

  function fallbackLabels(lang) {
    if (lang === "en") {
      return {
        ariaDialog: "Site search",
        placeholder: "Search pages, scientists, activities…",
        prompt: "Type to search the whole site",
        empty: "No results found. Try another keyword or spelling.",
        close: "Close",
        open: "Search site",
        hintNav: "navigate",
        hintOpen: "open",
        hintClose: "close",
        loading: "Loading search index…",
        error: "Search is temporarily unavailable.",
        shortcut: "Ctrl K"
      };
    }
    return {
      ariaDialog: "Sayt üzrə axtarış",
      placeholder: "Səhifələr, alimlər, fəaliyyətlər…",
      prompt: "Bütün sayt üzrə axtarmaq üçün yazın",
      empty: "Nəticə tapılmadı. Başqa söz və ya yazılış cəhd edin.",
      close: "Bağla",
      open: "Saytda axtar",
      hintNav: "seç",
      hintOpen: "aç",
      hintClose: "bağla",
      loading: "Axtarış indeksi yüklənir…",
      error: "Axtarış müvəqqəti olaraq əlçatan deyil.",
      shortcut: "Ctrl K"
    };
  }

  function labelsFor(lang, ui) {
    if (ui && ui.search && ui.search[lang]) {
      var base = fallbackLabels(lang);
      var patch = ui.search[lang];
      Object.keys(patch).forEach(function (k) { base[k] = patch[k]; });
      return base;
    }
    return fallbackLabels(lang);
  }

  function isGateway() {
    return !!(document.body && document.body.classList.contains("daab-gateway"));
  }

  /** Desktop pointer + hover: show Ctrl/Cmd+K chip in the nav search control. */
  function showSearchShortcutHint() {
    return window.matchMedia("(min-width: 1181px) and (hover: hover) and (pointer: fine)").matches;
  }

  function searchButtonTitle(labels) {
    if (showSearchShortcutHint()) {
      return labels.open + " (" + labels.shortcut + ")";
    }
    return labels.open;
  }

  function shortcutKbdHtml(className, labels) {
    if (!showSearchShortcutHint()) return "";
    return '<kbd class="' + className + '">' + escapeHtml(labels.shortcut) + "</kbd>";
  }

  function mountGatewayButton(labels) {
    if (document.getElementById("gateway-search-btn")) return;
    var actions = document.querySelector(".daab-gateway-actions");
    if (!actions) return;

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-secondary gateway-search-btn";
    btn.id = "gateway-search-btn";
    btn.setAttribute("aria-label", labels.open);
    btn.setAttribute("title", searchButtonTitle(labels));
    btn.innerHTML =
      '<span class="gateway-search-btn-icon" aria-hidden="true">' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">' +
      '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>' +
      "</svg></span>" +
      '<span>' + escapeHtml(labels.open) + "</span>" +
      shortcutKbdHtml("gateway-search-kbd", labels);
    actions.appendChild(btn);
  }

  var SEARCH_ICON_SVG =
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">' +
    '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>';
  var CLOSE_ICON_SVG =
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">' +
    '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';

  function searchStateHtml(kind, message) {
    return (
      '<div class="search-state search-state--' + kind + '">' +
      '<div class="search-state__icon" aria-hidden="true">' + SEARCH_ICON_SVG + "</div>" +
      '<p class="search-state__text">' + escapeHtml(message) + "</p></div>"
    );
  }

  function mountOverlay(labels) {
    if (document.getElementById("search-overlay")) return;

    var ov = document.createElement("div");
    ov.id = "search-overlay";
    ov.setAttribute("role", "dialog");
    ov.setAttribute("aria-modal", "true");
    ov.setAttribute("aria-label", labels.ariaDialog);
    ov.setAttribute("aria-hidden", "true");
    ov.innerHTML =
      '<div class="search-modal">' +
      '  <div class="search-modal__header">' +
      '    <div class="search-input-row">' +
      '      <span class="search-icon-large" aria-hidden="true">' + SEARCH_ICON_SVG + "</span>" +
      '      <input type="search" id="search-input" autocomplete="off" spellcheck="false" enterkeyhint="search" />' +
      '      <button type="button" class="search-close-btn" id="search-close-btn" aria-label="' +
      escapeHtml(labels.close) +
      '">' +
      CLOSE_ICON_SVG +
      '<span class="search-close-btn__label">Esc</span></button>' +
      "    </div>" +
      "  </div>" +
      '  <div class="search-results" id="search-results" aria-live="polite" aria-relevant="additions text"></div>' +
      '  <div class="search-hint">' +
      '    <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> ' + escapeHtml(labels.hintNav) + "</span>" +
      '    <span><kbd>&crarr;</kbd> ' + escapeHtml(labels.hintOpen) + "</span>" +
      '    <span><kbd>Esc</kbd> ' + escapeHtml(labels.hintClose) + "</span>" +
      "  </div>" +
      "</div>";

    var skip = document.querySelector("a.skip");
    if (skip && skip.parentNode) {
      skip.parentNode.insertBefore(ov, skip.nextSibling);
    } else {
      document.body.appendChild(ov);
    }
    var input = document.getElementById("search-input");
    input.placeholder = labels.placeholder;
    input.setAttribute("aria-label", labels.placeholder);
  }

  function ensureNavActions(inner) {
    if (!inner) return null;
    if (global.DAAB_SHELL && global.DAAB_SHELL.ensureNavActions) {
      return global.DAAB_SHELL.ensureNavActions(inner);
    }
    var actions = inner.querySelector(".nav-actions");
    if (!actions) {
      actions = document.createElement("div");
      actions.className = "nav-actions";
      actions.setAttribute("role", "group");
      inner.appendChild(actions);
    }
    return actions;
  }

  function navSearchButtonHtml(labels) {
    return (
      '<span class="nav-search-btn-icon" aria-hidden="true">' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">' +
      '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>' +
      "</svg></span>" +
      '<span class="nav-search-btn-label">' + escapeHtml(labels.placeholder) + "</span>" +
      shortcutKbdHtml("nav-search-kbd", labels)
    );
  }

  function refreshNavButtonLabels(labels) {
    var btn = document.getElementById("nav-search-btn");
    if (!btn) return;
    btn.setAttribute("aria-label", labels.open);
    btn.setAttribute("title", searchButtonTitle(labels));
    btn.innerHTML = navSearchButtonHtml(labels);
  }

  function refreshGatewayButtonLabels(labels) {
    var btn = document.getElementById("gateway-search-btn");
    if (!btn) return;
    btn.setAttribute("aria-label", labels.open);
    btn.setAttribute("title", searchButtonTitle(labels));
    btn.innerHTML =
      '<span class="gateway-search-btn-icon" aria-hidden="true">' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">' +
      '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>' +
      "</svg></span>" +
      '<span>' + escapeHtml(labels.open) + "</span>" +
      shortcutKbdHtml("gateway-search-kbd", labels);
  }

  function refreshSearchChromeLabels(labels) {
    var inp = document.getElementById("search-input");
    var closeBtn = document.getElementById("search-close-btn");
    var ov = document.getElementById("search-overlay");
    if (inp) {
      inp.placeholder = labels.placeholder;
      inp.setAttribute("aria-label", labels.placeholder);
    }
    if (closeBtn) closeBtn.setAttribute("aria-label", labels.close);
    if (ov) ov.setAttribute("aria-label", labels.ariaDialog);
    refreshNavButtonLabels(labels);
    refreshGatewayButtonLabels(labels);
  }

  function mountNavButton(labels) {
    var inner = document.querySelector(".nav-inner");
    if (!inner) return;

    var btn = document.getElementById("nav-search-btn");
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.className = "nav-search-btn";
      btn.id = "nav-search-btn";
      var actions = ensureNavActions(inner);
      if (actions) {
        actions.insertBefore(btn, actions.firstChild);
      } else {
        inner.appendChild(btn);
      }
    }
    refreshNavButtonLabels(labels);

    if (window.DAAB_NAV && window.DAAB_NAV.syncNavHeight) {
      window.DAAB_NAV.syncNavHeight();
    }
    if (window.DAAB_SHELL && window.DAAB_SHELL.repositionSwitcher) {
      window.DAAB_SHELL.repositionSwitcher();
    }
    document.dispatchEvent(new CustomEvent("daab-nav-tools-mounted"));
  }

  function setPrompt(res, labels, html) {
    res.innerHTML = html || searchStateHtml("prompt", labels.prompt);
  }

  function setEmpty(res, message) {
    res.innerHTML = searchStateHtml("empty", message);
  }

  function renderResults(res, items, query) {
    state.focusIndex = -1;
    if (!items.length) {
      setEmpty(res, state.labels.empty);
      return;
    }

    var pending = items.length;
    var rows = new Array(items.length);

    function finalize() {
      if (pending !== 0) return;
      var built = rows.filter(function (row) { return row; });
      if (built.length) {
        res.innerHTML = built.join("");
        updateFocus(res);
      } else {
        setEmpty(res, state.labels.empty);
      }
    }

    items.forEach(function (item, index) {
      resolveHref(item.entry).then(function (href) {
        var e = item.entry;
        rows[index] =
          '<a class="search-result-item" href="' + escapeHtml(href) + '" data-index="' + index + '">' +
          '<div class="sri-icon" aria-hidden="true">' + escapeHtml(e.icon || "📄") + "</div>" +
          '<div class="sri-body">' +
          '<div class="sri-title">' + highlight(e.title, query) + "</div>" +
          (e.summary ? '<div class="sri-desc">' + highlight(e.summary, query) + "</div>" : "") +
          "</div>" +
          '<span class="sri-tag">' + escapeHtml(e.tag || "") + "</span>" +
          "</a>";
        pending -= 1;
        finalize();
      }).catch(function () {
        pending -= 1;
        finalize();
      });
    });
  }

  function updateFocus(res) {
    var items = res.querySelectorAll(".search-result-item");
    items.forEach(function (el, i) {
      el.classList.toggle("focused", i === state.focusIndex);
      if (i === state.focusIndex) el.scrollIntoView({ block: "nearest" });
    });
  }

  function runSearch(query, res) {
    var q = query.trim();
    if (!q) {
      setPrompt(res, state.labels);
      state.filtered = [];
      return;
    }
    if (!state.ready) {
      setPrompt(
        res,
        state.labels,
        searchStateHtml("prompt", state.labels.loading)
      );
      ensureIndexLoaded().then(function () {
        runSearch(query, res);
      }).catch(function () {
        if (state.labels) {
          setEmpty(res, state.labels.error);
        }
      });
      return;
    }
    var qNorm = normalizeText(q);
    var tokens = qNorm.split(/\s+/).filter(Boolean);
    state.filtered = state.entries
      .map(function (entry) {
        return { entry: entry, score: scoreEntry(entry, qNorm, tokens) };
      })
      .filter(function (row) { return row.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, MAX_RESULTS);

    renderResults(res, state.filtered, q);
  }

  function wireUi() {
    var ov = document.getElementById("search-overlay");
    var inp = document.getElementById("search-input");
    var res = document.getElementById("search-results");
    var nb = document.getElementById("nav-search-btn") || document.getElementById("gateway-search-btn");
    var cb = document.getElementById("search-close-btn");
    if (!ov || !inp || !res) return;

    function openSearch() {
      ov.classList.add("open");
      ov.setAttribute("aria-hidden", "false");
      inp.value = "";
      state.focusIndex = -1;
      setPrompt(res, state.labels);
      if (global.DAAB_SCROLL_LOCK && typeof global.DAAB_SCROLL_LOCK.update === "function") {
        global.DAAB_SCROLL_LOCK.update();
      } else {
        document.body.classList.add("daab-scroll-lock");
      }
      ensureIndexLoaded()
        .then(function () {
          if (ov.classList.contains("open")) setPrompt(res, state.labels);
        })
        .catch(function () {
          if (state.labels && ov.classList.contains("open")) {
            setEmpty(res, state.labels.error);
          }
        });
      global.setTimeout(function () { inp.focus(); }, 40);
    }

    function closeSearch() {
      ov.classList.remove("open");
      ov.setAttribute("aria-hidden", "true");
      inp.value = "";
      state.focusIndex = -1;
      if (global.DAAB_SCROLL_LOCK && typeof global.DAAB_SCROLL_LOCK.update === "function") {
        global.DAAB_SCROLL_LOCK.update();
      } else {
        document.body.classList.remove("daab-scroll-lock");
      }
      if (nb) nb.focus();
    }

    inp.addEventListener("input", function () {
      global.clearTimeout(state.debounceTimer);
      state.debounceTimer = global.setTimeout(function () {
        runSearch(inp.value, res);
      }, DEBOUNCE_MS);
    });

    inp.addEventListener("keydown", function (e) {
      var items = res.querySelectorAll(".search-result-item");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (!items.length) return;
        state.focusIndex = Math.min(state.focusIndex + 1, items.length - 1);
        updateFocus(res);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (!items.length) return;
        state.focusIndex = Math.max(state.focusIndex - 1, 0);
        updateFocus(res);
      } else if (e.key === "Enter" && state.focusIndex >= 0 && items[state.focusIndex]) {
        e.preventDefault();
        items[state.focusIndex].click();
      } else if (e.key === "Escape") {
        closeSearch();
      }
    });

    function focusableInModal() {
      var modal = ov.querySelector(".search-modal");
      if (!modal) return [];
      var nodes = modal.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      return Array.prototype.filter.call(nodes, function (el) {
        return el.offsetParent !== null;
      });
    }

    ov.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var list = focusableInModal();
      if (!list.length) return;
      var first = list[0];
      var last = list[list.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    if (nb) nb.addEventListener("click", openSearch);
    if (cb) cb.addEventListener("click", closeSearch);
    ov.addEventListener("click", function (e) { if (e.target === ov) closeSearch(); });

    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        ov.classList.contains("open") ? closeSearch() : openSearch();
      }
      if (e.key === "Escape" && ov.classList.contains("open")) closeSearch();
    });
  }

  function loadIndex() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.loadSearchIndex) {
      return I18N.loadSearchIndex();
    }
    INDEX_URL = INDEX_URL || assetRoot() + "i18n/search-index.json";
    return fetch(INDEX_URL + "?v=6").then(function (res) {
      if (!res.ok) throw new Error("search index");
      return res.json();
    });
  }

  function ensureIndexLoaded() {
    if (state.ready) return Promise.resolve(state.entries);
    if (state.indexLoadPromise) return state.indexLoadPromise;
    state.indexLoading = true;
    state.indexLoadPromise = loadIndex()
      .then(function (data) {
        state.entries = (data && data.entries) || [];
        state.ready = true;
        state.indexLoading = false;
        return state.entries;
      })
      .catch(function (err) {
        state.indexLoading = false;
        state.indexLoadPromise = null;
        throw err;
      });
    return state.indexLoadPromise;
  }

  function shouldPreloadSearchIndex() {
    if (global.DAAB_PERF && typeof global.DAAB_PERF.heavyPreloadOk === "function") {
      return global.DAAB_PERF.heavyPreloadOk();
    }
    return true;
  }

  function scheduleIdleIndexPreload() {
    if (state.ready || state.indexLoadPromise) return;
    if (!shouldPreloadSearchIndex()) return;
    var run = function () {
      if (!shouldPreloadSearchIndex()) return;
      ensureIndexLoaded().catch(function () {});
    };
    if (global.requestIdleCallback) {
      global.requestIdleCallback(run, { timeout: 12000 });
    } else {
      global.setTimeout(run, 5000);
    }
  }

  var searchUiWired = false;

  function mountSearchChrome(labels) {
    state.labels = labels;
    mountOverlay(labels);
    if (isGateway()) mountGatewayButton(labels);
    else mountNavButton(labels);
    refreshSearchChromeLabels(labels);
    if (!searchUiWired) {
      wireUi();
      searchUiWired = true;
    }
  }

  function boot() {
    state.lang = detectLang();
    var fallbackLabels = labelsFor(state.lang, null);
    mountSearchChrome(fallbackLabels);

    var uiPromise = global.DAAB_I18N && global.DAAB_I18N.loadUi
      ? global.DAAB_I18N.loadUi().catch(function (err) {
          console.warn("[daab-search] UI labels unavailable; using fallback:", err);
          return null;
        })
      : Promise.resolve(null);

    uiPromise.then(function (ui) {
      var labels = labelsFor(state.lang, ui);
      mountSearchChrome(labels);
    });
  }

  document.addEventListener("daab-primary-nav-ready", function () {
    if (isGateway()) return;
    mountNavButton(state.labels || labelsFor(state.lang, null));
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  global.DAAB_SEARCH = {
    normalizeText: normalizeText,
    scoreEntry: scoreEntry
  };
})(typeof window !== "undefined" ? window : this);
