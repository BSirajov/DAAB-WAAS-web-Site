(function () {
  "use strict";

  var DATA = window.SCIENTISTS_CATALOG_DATA || [];

  var collation = window.DAAB_COLLATION || {};
  var localeCompare =
    collation.compare ||
    function (a, b) {
      return String(a || "").localeCompare(String(b || ""), "en", {
        sensitivity: "base",
      });
    };
  var localeSort =
    collation.sort ||
    function (arr) {
      return arr.slice().sort(function (a, b) {
        return localeCompare(a, b);
      });
    };

  var SORT_STORAGE_KEY = "daab-profiles-sort";

  var COUNTRY_NAME_TO_CODE_AZ = {
    "ABŞ": "abs",
    "Almaniya": "de",
    "Avstriya": "at",
    "Birləşmiş Krallıq": "uk",
    "Koreya": "kr",
    "Estoniya": "ee",
    "Fransa": "fr",
    "Gürcüstan": "ge",
    "İsrail": "il",
    "İsveç": "se",
    "İtaliya": "it",
    "Kanada": "ca",
    "Meksika": "mx",
    "Misir": "eg",
    "Oman": "om",
    "Polşa": "pl",
    "Qazaxıstan": "kz",
    "Qırğızıstan": "kg",
    "Rusiya Federasiyası": "ru",
    "Səudiyyə Ərəbistanı": "sa",
    "Türkiyə": "tr",
    "Ukrayna": "ua",
    "Yaponiya": "jp",
  };

  function buildCountryNameToCode(cards) {
    var map = {};
    var key;
    for (key in COUNTRY_NAME_TO_CODE_AZ) {
      if (Object.prototype.hasOwnProperty.call(COUNTRY_NAME_TO_CODE_AZ, key)) {
        map[key] = COUNTRY_NAME_TO_CODE_AZ[key];
      }
    }
    cards.forEach(function (card) {
      var name = card.dataset.countryName;
      var code = card.dataset.country;
      if (name && code) map[name] = code;
    });
    return map;
  }

  function pageLang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function filterCountLabels(lang) {
    if (lang === "en") {
      return {
        all: function (n) {
          return "<span>" + n + "</span> profile" + (n === 1 ? "" : "s");
        },
        matched: function (visible, total) {
          var html =
            "<span>" +
            visible +
            "</span> matching profile" +
            (visible === 1 ? "" : "s");
          if (visible < total) html += " (" + total + " total)";
          return html;
        },
      };
    }
    return {
      all: function (n) {
        return "<span>" + n + "</span> profil";
      },
      matched: function (visible, total) {
        var html = "<span>" + visible + "</span> uyğun profil";
        if (visible < total) html += " (" + total + " ümumi)";
        return html;
      },
    };
  }

  function normQuery(q) {
    return q.toLowerCase().replace(/\s+/g, " ").trim();
  }

  function getCardName(card) {
    var el = card.querySelector(".card-name");
    if (!el) return "";
    var clone = el.cloneNode(true);
    var creds = clone.querySelectorAll(".cred");
    creds.forEach(function (node) {
      node.remove();
    });
    return clone.textContent.replace(/\s+/g, " ").trim();
  }

  function getSortValue(card, sortCol) {
    switch (sortCol) {
      case "country":
        return card.dataset.countryName || "";
      case "ixtilas":
        return card.dataset.ixtilas || "";
      case "name":
      default:
        return getCardName(card);
    }
  }

  function readSortState() {
    try {
      var raw = sessionStorage.getItem(SORT_STORAGE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || typeof s !== "object") return null;
      var col = s.sortCol;
      var dir = s.sortDir;
      if (col === "degree") {
        col = "name";
      }
      if (col !== "name" && col !== "country" && col !== "ixtilas") {
        return null;
      }
      if (dir !== 1 && dir !== -1) return null;
      return { sortCol: col, sortDir: dir };
    } catch (e) {
      return null;
    }
  }

  function saveSortState(sortCol, sortDir) {
    try {
      sessionStorage.setItem(
        SORT_STORAGE_KEY,
        JSON.stringify({ sortCol: sortCol, sortDir: sortDir })
      );
    } catch (e) {
      /* ignore */
    }
  }

  function defaultSortState() {
    return { sortCol: "name", sortDir: 1 };
  }

  function showAllCards(cards, resultCount, noResults, countLabels) {
    cards.forEach(function (card) {
      card.classList.remove("is-filtered-out", "is-match", "is-excluded");
    });
    if (resultCount && countLabels) {
      resultCount.innerHTML = countLabels.all(cards.length);
    }
    if (noResults) {
      noResults.classList.remove("visible");
    }
  }

  function clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree) {
    var ms = window.DAABScientistsMultiSelect;
    if (searchInput) searchInput.value = "";
    if (ms) {
      ms.clearAll(["filterCountry", "filterIxtilas", "filterDegree"]);
      return;
    }
    if (filterCountry) filterCountry.value = "";
    if (filterIxtilas) filterIxtilas.value = "";
    if (filterDegree) filterDegree.value = "";
  }

  function syncToolbarFilterBadge() {
    if (
      window.DAAB_SCIENTISTS_TOOLBAR &&
      typeof window.DAAB_SCIENTISTS_TOOLBAR.syncAll === "function"
    ) {
      window.DAAB_SCIENTISTS_TOOLBAR.syncAll();
    }
  }

  function buildFilterOptionsFromCards(cardNodes, filterCountry, filterIxtilas, filterDegree) {
    var countries = {};
    var degrees = {};
    var ixtisaslar = {};
    cardNodes.forEach(function (card) {
      var c = (card.dataset.countryName || "").trim();
      var d = (card.dataset.degree || "").trim();
      var x = (card.dataset.ixtilas || "").trim();
      if (c) countries[c] = 1;
      if (d) degrees[d] = 1;
      if (x) ixtisaslar[x] = 1;
    });
    localeSort(Object.keys(countries)).forEach(function (c) {
      var o = document.createElement("option");
      o.value = c;
      o.textContent = c;
      filterCountry.appendChild(o);
    });
    if (filterDegree) {
      localeSort(Object.keys(degrees)).forEach(function (d) {
        var o = document.createElement("option");
        o.value = d;
        o.textContent = d;
        filterDegree.appendChild(o);
      });
    }
    if (filterIxtilas) {
      localeSort(Object.keys(ixtisaslar)).forEach(function (x) {
        var o = document.createElement("option");
        o.value = x;
        o.textContent = x;
        filterIxtilas.appendChild(o);
      });
    }
  }

  function buildFilterOptionsFromData(filterCountry, filterIxtilas, filterDegree) {
    var countries = localeSort(
      Object.keys(
        DATA.reduce(function (acc, r) {
          if (r.yasadigi_olke) acc[r.yasadigi_olke] = 1;
          return acc;
        }, {})
      )
    );
    var degrees = localeSort(
      Array.from(
        new Set(
          DATA.map(function (r) {
            return (r.elmi_derece || "").trim();
          }).filter(Boolean)
        )
      )
    );
    var ixtisaslar = localeSort(
      Array.from(
        new Set(
          DATA.map(function (r) {
            return (r.ixtilas || "").trim();
          }).filter(Boolean)
        )
      )
    );
    countries.forEach(function (c) {
      var o = document.createElement("option");
      o.value = c;
      o.textContent = c;
      filterCountry.appendChild(o);
    });
    degrees.forEach(function (d) {
      var o = document.createElement("option");
      o.value = d;
      o.textContent = d;
      filterDegree.appendChild(o);
    });
    ixtisaslar.forEach(function (x) {
      var o = document.createElement("option");
      o.value = x;
      o.textContent = x;
      filterIxtilas.appendChild(o);
    });
  }

  function scheduleIdle(fn, timeoutMs) {
    if (typeof window.requestIdleCallback === "function") {
      window.requestIdleCallback(fn, { timeout: timeoutMs || 2000 });
      return;
    }
    window.setTimeout(fn, 0);
  }

  function hashProfileId() {
    if (window.DAAB_PROFILE_DEEPLINK && window.DAAB_PROFILE_DEEPLINK.hashId) {
      return window.DAAB_PROFILE_DEEPLINK.hashId();
    }
    if (!location.hash) return "";
    try {
      return decodeURIComponent(location.hash.slice(1));
    } catch (e) {
      return location.hash.slice(1);
    }
  }

  function spotlightCard(card) {
    if (!card) return;
    card.classList.remove("daab-profile-spotlight");
    void card.offsetWidth;
    card.classList.add("daab-profile-spotlight");
    card.addEventListener(
      "animationend",
      function onEnd() {
        card.classList.remove("daab-profile-spotlight");
        card.removeEventListener("animationend", onEnd);
      },
      { once: true }
    );
  }

  function init() {
    var searchInput = document.getElementById("searchInput");
    var filterCountry = document.getElementById("filterCountry");
    var filterIxtilas = document.getElementById("filterIxtilas");
    var filterDegree = document.getElementById("filterDegree");
    var clearFilters = document.getElementById("clearFilters");
    var resultCount = document.getElementById("resultCount");
    var noResults = document.getElementById("no-results");
    var catalog = document.getElementById("scientists-catalog");
    var grid = catalog ? catalog.querySelector(".cards-grid") : null;
    var cards = grid
      ? grid.querySelectorAll(".card")
      : document.querySelectorAll(".card");
    var sortBy = document.getElementById("sortBy");
    var sortAscBtn = document.getElementById("sortAscBtn");
    var sortDescBtn = document.getElementById("sortDescBtn");
    var savedSort = readSortState() || defaultSortState();
    var sortCol = savedSort.sortCol;
    var sortDir = savedSort.sortDir;
    var countryNameToCode = buildCountryNameToCode(cards);
    var countLabels = filterCountLabels(pageLang());

    function markProfilesReady() {
      document.documentElement.classList.add("daab-profiles-ready");
      document.documentElement.classList.remove("daab-profiles-boot");
    }

    if (!cards.length) {
      markProfilesReady();
      return;
    }

    function updateSortDirUi() {
      var ascending = sortDir === 1;
      if (sortBy && sortBy.value !== sortCol) {
        sortBy.value = sortCol;
      }
      if (sortAscBtn) {
        sortAscBtn.classList.toggle("is-active", ascending);
        sortAscBtn.setAttribute("aria-pressed", ascending ? "true" : "false");
      }
      if (sortDescBtn) {
        sortDescBtn.classList.toggle("is-active", !ascending);
        sortDescBtn.setAttribute("aria-pressed", ascending ? "false" : "true");
      }
    }

    function compareCards(a, b) {
      var primary =
        sortDir * localeCompare(getSortValue(a, sortCol), getSortValue(b, sortCol));
      if (primary !== 0) return primary;
      return sortDir * localeCompare(a.id || "", b.id || "");
    }

    function reorderCards() {
      if (!grid) return;
      var cardList = Array.prototype.slice.call(cards);
      var visible = cardList.filter(function (card) {
        return !card.classList.contains("is-filtered-out");
      });
      var hidden = cardList.filter(function (card) {
        return card.classList.contains("is-filtered-out");
      });

      function sortList(list) {
        list.sort(compareCards);
      }

      sortList(visible);
      sortList(hidden);
      var fragment = document.createDocumentFragment();
      visible.concat(hidden).forEach(function (card) {
        fragment.appendChild(card);
      });
      grid.appendChild(fragment);
    }

    function applySortState(nextCol, nextDir, persist) {
      sortCol = nextCol === "degree" ? "name" : nextCol || "name";
      sortDir = nextDir === -1 ? -1 : 1;
      if (persist !== false) {
        saveSortState(sortCol, sortDir);
      }
      updateSortDirUi();
      reorderCards();
    }

    function setSortDir(dir) {
      applySortState(sortCol, dir === -1 ? -1 : 1, true);
    }

    var profileHash = hashProfileId();

    /* Restore filters; reveal catalogue immediately unless hash deep-link boot */
    showAllCards(cards, resultCount, noResults, countLabels);
    clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree);
    if (!profileHash) {
      markProfilesReady();
      scheduleIdle(function () {
        applySortState(sortCol, sortDir, false);
      });
    } else {
      applySortState(sortCol, sortDir, false);
    }

    function revealProfileById(id) {
      if (!id) return false;
      if (window.DAAB_PROFILE_DEEPLINK && window.DAAB_PROFILE_DEEPLINK.focusProfile) {
        return window.DAAB_PROFILE_DEEPLINK.focusProfile(id);
      }
      var card = document.getElementById(id);
      if (!card || !card.classList.contains("card")) return false;

      clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree);
      showAllCards(cards, resultCount, noResults);

      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
          var target = document.getElementById(id);
          if (!target) return;
          var root = document.documentElement;
          var prevInline = root.style.scrollBehavior;
          root.style.scrollBehavior = "auto";
          var nav = document.querySelector(".nav-strip");
          var navH = nav ? nav.getBoundingClientRect().height : 86;
          var top =
            target.getBoundingClientRect().top + window.pageYOffset - navH - 20;
          window.scrollTo({ top: Math.max(0, top), behavior: "auto" });
          window.requestAnimationFrame(function () {
            root.style.scrollBehavior = prevInline;
          });
          spotlightCard(target);
        });
      });
      return true;
    }

    function handleProfileHash() {
      return revealProfileById(hashProfileId());
    }

    window.addEventListener("hashchange", function () {
      if (window.DAAB_PROFILE_DEEPLINK && window.DAAB_PROFILE_DEEPLINK.scheduleFocus) {
        window.DAAB_PROFILE_DEEPLINK.scheduleFocus();
        return;
      }
      handleProfileHash();
    });

    document.dispatchEvent(new CustomEvent("daab-profiles-catalog-ready"));
    if (profileHash && window.DAAB_PROFILE_DEEPLINK && window.DAAB_PROFILE_DEEPLINK.scheduleFocus) {
      window.DAAB_PROFILE_DEEPLINK.scheduleFocus();
    } else if (profileHash && handleProfileHash()) {
      document.dispatchEvent(new CustomEvent("daab-profile-focused"));
      markProfilesReady();
    } else if (profileHash) {
      markProfilesReady();
    }

    if (!searchInput || !filterCountry) return;

    if (DATA.length) {
      buildFilterOptionsFromData(filterCountry, filterIxtilas, filterDegree);
    } else {
      buildFilterOptionsFromCards(cards, filterCountry, filterIxtilas, filterDegree);
    }

    var ms = window.DAABScientistsMultiSelect;
    var profileFilterIds = ["filterCountry", "filterIxtilas", "filterDegree"];

    function getMultiFilter(id) {
      if (ms) return ms.getFilterValues(id);
      var el = document.getElementById(id);
      return el && el.value ? [el.value] : null;
    }

    function mountMultiFilters() {
      if (!ms) return;
      profileFilterIds.forEach(function (id) {
        var el = document.getElementById(id);
        if (el) {
          ms.mount(el, {
            onChange: function () {
              applyFilters();
            },
          });
        }
      });
    }

    mountMultiFilters();

    function updateFilterStyles() {
      profileFilterIds.forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        var wrap = el.closest(".sel-wrap");
        if (!wrap) return;
        var active = ms ? ms.isActive(id) : el.value !== "";
        wrap.classList.toggle("active", active);
      });
    }

    function cardMatches(card, q, countryCodes, degreeFilter, ixtilasFilter) {
      var code = card.dataset.country || "";
      var hay = (card.dataset.search || "").toLowerCase();
      var deg = (card.dataset.degree || "").trim();
      var ixt = (card.dataset.ixtilas || "").trim();
      var matchFn = ms ? ms.matches.bind(ms) : function (selected, value) {
        if (selected === null) return true;
        if (!selected.length) return false;
        return selected.indexOf((value == null ? "" : String(value)).trim()) !== -1;
      };
      if (countryCodes !== null) {
        if (!countryCodes.length) return false;
        if (countryCodes.indexOf(code) === -1) return false;
      }
      if (!matchFn(degreeFilter, deg)) return false;
      if (!matchFn(ixtilasFilter, ixt)) return false;
      if (q && hay.indexOf(q) === -1) return false;
      return true;
    }

    function applyFilters() {
      var q = normQuery(searchInput.value);
      var countryNames = getMultiFilter("filterCountry");
      var degreeFilter = getMultiFilter("filterDegree");
      var ixtilasFilter = getMultiFilter("filterIxtilas");
      var countryCodes = null;
      if (countryNames !== null) {
        countryCodes = countryNames
          .map(function (name) {
            return countryNameToCode[name] || "";
          })
          .filter(Boolean);
      }
      var filtering =
        !!q ||
        countryNames !== null ||
        degreeFilter !== null ||
        ixtilasFilter !== null;
      var visible = 0;

      if (!filtering) {
        showAllCards(cards, resultCount, noResults, countLabels);
        updateFilterStyles();
        reorderCards();
        syncToolbarFilterBadge();
        return;
      }

      cards.forEach(function (card) {
        var match = cardMatches(card, q, countryCodes, degreeFilter, ixtilasFilter);
        card.classList.toggle("is-filtered-out", !match);
        if (match) visible++;
      });

      if (resultCount) {
        resultCount.innerHTML = countLabels.matched(visible, cards.length);
      }
      if (noResults) {
        noResults.classList.toggle("visible", visible === 0);
      }
      updateFilterStyles();
      reorderCards();
      syncToolbarFilterBadge();
    }

    function scrollToFirstVisible(countryCode) {
      if (!countryCode) return;
      var target = null;
      cards.forEach(function (card) {
        if (target || card.classList.contains("is-filtered-out")) return;
        if (card.dataset.country === countryCode) target = card;
      });
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    function resetSort() {
      var defaults = defaultSortState();
      applySortState(defaults.sortCol, defaults.sortDir, true);
    }

    searchInput.addEventListener("input", applyFilters);

    filterCountry.addEventListener("change", function () {
      applyFilters();
      var selected = getMultiFilter("filterCountry");
      if (selected && selected.length === 1) {
        scrollToFirstVisible(countryNameToCode[selected[0]] || "");
      }
    });

    if (filterIxtilas) {
      filterIxtilas.addEventListener("change", applyFilters);
    }
    if (filterDegree) {
      filterDegree.addEventListener("change", applyFilters);
    }

    if (sortBy) {
      sortBy.addEventListener("change", function () {
        applySortState(sortBy.value, sortDir, true);
      });
    }

    if (sortAscBtn) {
      sortAscBtn.addEventListener("click", function () {
        setSortDir(1);
      });
    }
    if (sortDescBtn) {
      sortDescBtn.addEventListener("click", function () {
        setSortDir(-1);
      });
    }

    document.querySelectorAll(".sel-clear").forEach(function (btn) {
      if (!btn.getAttribute("aria-label")) {
        var tgt = document.getElementById(btn.dataset.for);
        var base = btn.getAttribute("title") || "Clear filter";
        var fname = "";
        if (tgt) {
          if (tgt.options && tgt.options[0]) fname = tgt.options[0].textContent || "";
          if (!fname) fname = tgt.getAttribute("aria-label") || "";
        }
        fname = fname.replace(/^[^\p{L}]+/u, "").trim();
        btn.setAttribute("aria-label", fname ? base + " — " + fname : base);
      }
      btn.addEventListener("click", function () {
        var targetId = btn.dataset.for;
        if (ms && targetId) {
          ms.clear(targetId);
        } else {
          var el = document.getElementById(targetId);
          if (el) {
            el.value = "";
            el.dispatchEvent(new Event("change", { bubbles: true }));
          }
        }
        applyFilters();
      });
    });

    if (clearFilters) {
      clearFilters.addEventListener("click", function () {
        clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree);
        resetSort();
        applyFilters();
      });
    }

    updateFilterStyles();
    syncToolbarFilterBadge();
    document.dispatchEvent(new CustomEvent("daab-scientists-catalog-ready"));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  function boot() {
    var catalog = document.getElementById("scientists-catalog");
    if (catalog && catalog.getAttribute("data-daab-profiles-client") === "1") {
      var grid = catalog.querySelector(".cards-grid");
      var hasCards = grid && grid.querySelector(".card");
      if (!hasCards) {
        document.addEventListener("daab-scientists-profiles-rendered", function onRendered() {
          document.removeEventListener("daab-scientists-profiles-rendered", onRendered);
          init();
        });
        document.addEventListener("daab-scientists-profiles-render-error", function onErr() {
          document.removeEventListener("daab-scientists-profiles-render-error", onErr);
          init();
        });
        return;
      }
    }
    init();
  }
})();
