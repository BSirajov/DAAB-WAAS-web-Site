(function () {
  "use strict";

  function catalogData() {
    var en = window.PROMINENT_FIGURES_CATALOG_EN;
    if (lang() === "en" && Array.isArray(en) && en.length) {
      return en;
    }
    return window.PROMINENT_FIGURES_CATALOG || [];
  }

  var DATA = catalogData();
  var collation = window.DAAB_COLLATION || {};
  var localeCompare =
    collation.compare ||
    function (a, b) {
      return String(a || "").localeCompare(String(b || ""), "az", {
        sensitivity: "base",
      });
    };
  var localeSort =
    collation.sort ||
    function (arr, keyFn) {
      return arr.slice().sort(function (a, b) {
        return localeCompare(keyFn(a), keyFn(b));
      });
    };

  var STRINGS = {
    az: {
      searchPlaceholder: "Ad, ölkə, sahə, dövr və ya qrup üzrə axtar…",
      searchAria: "Profil axtar",
      filterToggle: "Filtrlər",
      filterToggleAria: "Filtrləri göstər",
      filtersLabel: "Filtrlər",
      groupAll: "📚 Bütün qruplar",
      groupAzturk: "Azərbaycan və türk dünyası",
      groupWorld: "Dünya alimləri",
      period: "⏳ Tarixi dövr",
      field: "🔬 Sahə",
      country: "🌍 Ölkə / region",
      region: "🏛️ Məkan / kontekst",
      clear: "Hamısını sıfırla",
      sortLabel: "Sırala",
      sortName: "Ad",
      sortPeriod: "Tarixi dövr",
      sortField: "Sahə",
      sortCountry: "Ölkə / region",
      sortBirth: "Doğum ili",
      sortAsc: "A→Z",
      sortDesc: "Z→A",
      sortDirAria: "Sıralama istiqaməti",
      allCount: function (n) {
        return "<span>" + n + "</span> profil";
      },
      matched: function (visible, total) {
        var html = "<span>" + visible + "</span> uyğun profil";
        if (visible < total) html += " (" + total + " ümumi)";
        return html;
      },
      cardGroup: "Qrup",
      cardPeriod: "Dövr",
      cardField: "Sahə",
      cardCountry: "Ölkə",
      openProfile: "Profilə keç",
      empty: "Seçilmiş filtrlərə uyğun profil tapılmadı.",
    },
    en: {
      searchPlaceholder: "Search by name, country, field, period, or group…",
      searchAria: "Search profiles",
      filterToggle: "Filters",
      filterToggleAria: "Show filters",
      filtersLabel: "Filters",
      groupAll: "📚 All groups",
      groupAzturk: "Azerbaijani & Turkic figures",
      groupWorld: "World scientists",
      period: "⏳ Historical period",
      field: "🔬 Field",
      country: "🌍 Country / region",
      region: "🏛️ Place / context",
      clear: "Clear all",
      sortLabel: "Sort by",
      sortName: "Name",
      sortPeriod: "Period",
      sortField: "Field",
      sortCountry: "Country / region",
      sortBirth: "Birth year",
      sortAsc: "A→Z",
      sortDesc: "Z→A",
      sortDirAria: "Sort direction",
      allCount: function (n) {
        return "<span>" + n + "</span> profile" + (n === 1 ? "" : "s");
      },
      matched: function (visible, total) {
        var html = "<span>" + visible + "</span> matching profile" + (visible === 1 ? "" : "s");
        if (visible < total) html += " (" + total + " total)";
        return html;
      },
      cardGroup: "Group",
      cardPeriod: "Period",
      cardField: "Field",
      cardCountry: "Country",
      openProfile: "View profile",
      empty: "No profiles match the selected filters.",
    },
  };

  function lang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function t() {
    return STRINGS[lang()] || STRINGS.az;
  }

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function uniqueSorted(values) {
    return localeSort(
      values.filter(function (v, i, arr) {
        return v && arr.indexOf(v) === i;
      }),
      function (x) {
        return x;
      }
    );
  }

  function fillSelect(sel, placeholder, values) {
    if (!sel) return;
    var current = sel.value;
    sel.innerHTML = "";
    var opt0 = document.createElement("option");
    opt0.value = "";
    opt0.textContent = placeholder;
    sel.appendChild(opt0);
    values.forEach(function (v) {
      var opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      sel.appendChild(opt);
    });
    if (values.indexOf(current) >= 0) sel.value = current;
  }

  var SORT_STORAGE_KEY = "daab-encyclopedia-sort";

  function filterCountLabels() {
    var L = t();
    return {
      all: L.allCount,
      matched: L.matched,
    };
  }

  function normQuery(q) {
    return norm(q);
  }

  function profileHref(item) {
    return item.href;
  }

  function primaryFieldTag(field) {
    if (!field) return "";
    return String(field).split("·")[0].trim();
  }

  function renderCard(item, labels) {
    var card = document.createElement("a");
    card.className = "person-card";
    card.id = item.id;
    card.href = profileHref(item);
    card.setAttribute("aria-label", labels.openProfile + ": " + item.name);
    card.setAttribute("data-group", item.group || "");
    card.setAttribute("data-period", item.period || "");
    card.setAttribute("data-field", item.field || "");
    card.setAttribute("data-country", item.country || "");
    card.setAttribute("data-country-name", item.country || "");
    card.setAttribute("data-region", item.region || "");
    if (item.birthYear != null) {
      card.setAttribute("data-birth-year", String(item.birthYear));
    }
    card.setAttribute(
      "data-search",
      norm(
        [
          item.name,
          item.dates,
          item.summary,
          item.country,
          item.field,
          item.period,
          item.region,
          item.groupLabel,
        ].join(" ")
      )
    );

    var top = document.createElement("div");
    top.className = "card-top";

    var portrait = document.createElement("div");
    portrait.className = "card-portrait";
    portrait.setAttribute("aria-hidden", "true");
    portrait.textContent = item.emoji || "⭐";
    top.appendChild(portrait);

    var meta = document.createElement("div");
    meta.className = "card-meta";

    var nameEl = document.createElement("div");
    nameEl.className = "card-name";
    nameEl.textContent = item.name;
    meta.appendChild(nameEl);

    if (item.dates) {
      var datesEl = document.createElement("div");
      datesEl.className = "card-dates";
      datesEl.textContent = item.dates;
      meta.appendChild(datesEl);
    }

    var tags = document.createElement("div");
    tags.className = "card-tags";
    if (item.country) {
      var nationTag = document.createElement("span");
      nationTag.className = "tag nation";
      nationTag.textContent = item.country;
      tags.appendChild(nationTag);
    }
    var fieldTag = primaryFieldTag(item.field);
    if (fieldTag) {
      var tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = fieldTag;
      tags.appendChild(tag);
    }
    if (tags.childNodes.length) meta.appendChild(tags);

    top.appendChild(meta);
    card.appendChild(top);

    if (item.summary) {
      var desc = document.createElement("p");
      desc.className = "card-desc";
      desc.textContent = item.summary;
      card.appendChild(desc);
    }

    var footer = document.createElement("div");
    footer.className = "card-footer";

    var fieldLine = document.createElement("span");
    fieldLine.className = "card-field";
    fieldLine.textContent = item.field || item.period || "";
    footer.appendChild(fieldLine);

    var arrow = document.createElement("span");
    arrow.className = "card-arrow";
    arrow.setAttribute("aria-hidden", "true");
    arrow.innerHTML =
      '<svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">' +
      '<path d="M5 12h14M12 5l7 7-7 7"></path></svg>';
    footer.appendChild(arrow);

    card.appendChild(footer);
    return card;
  }

  function getCardName(card) {
    var el = card.querySelector(".card-name");
    return el ? el.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function getSortValue(card, sortCol) {
    switch (sortCol) {
      case "period":
        return card.dataset.period || "";
      case "field":
        return card.dataset.field || "";
      case "country":
        return card.dataset.countryName || card.dataset.country || "";
      case "birth":
        return parseInt(card.dataset.birthYear, 10) || 99999;
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
      if (
        col !== "name" &&
        col !== "country" &&
        col !== "field" &&
        col !== "period" &&
        col !== "birth"
      ) {
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

  function clearFilterInputs(
    searchInput,
    filterGroup,
    filterPeriod,
    filterField,
    filterCountry,
    filterRegion
  ) {
    if (searchInput) searchInput.value = "";
    if (filterGroup) filterGroup.value = "";
    if (filterPeriod) filterPeriod.value = "";
    if (filterField) filterField.value = "";
    if (filterCountry) filterCountry.value = "";
    if (filterRegion) filterRegion.value = "";
  }

  function syncToolbarFilterBadge() {
    if (
      window.DAAB_SCIENTISTS_TOOLBAR &&
      typeof window.DAAB_SCIENTISTS_TOOLBAR.syncAll === "function"
    ) {
      window.DAAB_SCIENTISTS_TOOLBAR.syncAll();
    }
  }

  function init() {
    var catalog = document.getElementById("encyclopedia-catalog");
    var grid = catalog ? catalog.querySelector(".cards-grid") : null;
    if (!grid || !DATA.length) return;

    var ui = t();
    var countLabels = filterCountLabels();
    var searchInput = document.getElementById("searchInput");
    var filterGroup = document.getElementById("filterGroup");
    var filterPeriod = document.getElementById("filterPeriod");
    var filterField = document.getElementById("filterField");
    var filterCountry = document.getElementById("filterCountry");
    var filterRegion = document.getElementById("filterRegion");
    var clearFilters = document.getElementById("clearFilters");
    var resultCount = document.getElementById("resultCount");
    var noResults = document.getElementById("no-results");
    var sortBy = document.getElementById("sortBy");
    var sortAscBtn = document.getElementById("sortAscBtn");
    var sortDescBtn = document.getElementById("sortDescBtn");
    var savedSort = readSortState() || defaultSortState();
    var sortCol = savedSort.sortCol;
    var sortDir = savedSort.sortDir;

    DATA.forEach(function (item) {
      grid.appendChild(renderCard(item, ui));
    });

    var cards = grid.querySelectorAll(".person-card");
    if (!cards.length) return;

    if (filterGroup) {
      filterGroup.innerHTML = "";
      var g0 = document.createElement("option");
      g0.value = "";
      g0.textContent = ui.groupAll;
      filterGroup.appendChild(g0);
      [["azturk", ui.groupAzturk], ["world", ui.groupWorld]].forEach(function (pair) {
        var opt = document.createElement("option");
        opt.value = pair[0];
        opt.textContent = pair[1];
        filterGroup.appendChild(opt);
      });
    }

    fillSelect(
      filterPeriod,
      ui.period,
      uniqueSorted(
        DATA.map(function (d) {
          return d.period;
        })
      )
    );
    fillSelect(
      filterField,
      ui.field,
      uniqueSorted(
        DATA.map(function (d) {
          return d.field;
        })
      )
    );
    fillSelect(
      filterCountry,
      ui.country,
      uniqueSorted(
        DATA.map(function (d) {
          return d.country;
        })
      )
    );
    fillSelect(
      filterRegion,
      ui.region,
      uniqueSorted(
        DATA.map(function (d) {
          return d.region;
        })
      )
    );

    if (searchInput) searchInput.placeholder = ui.searchPlaceholder;
    if (searchInput) searchInput.setAttribute("aria-label", ui.searchAria);
    if (clearFilters) clearFilters.textContent = ui.clear;

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
      if (sortCol === "birth") {
        var av = getSortValue(a, "birth");
        var bv = getSortValue(b, "birth");
        if (av !== bv) return sortDir * (av - bv);
        return sortDir * localeCompare(getCardName(a), getCardName(b));
      }
      var primary =
        sortDir * localeCompare(getSortValue(a, sortCol), getSortValue(b, sortCol));
      if (primary !== 0) return primary;
      return sortDir * localeCompare(a.id || "", b.id || "");
    }

    function reorderCards() {
      var cardList = Array.prototype.slice.call(cards);
      var visible = cardList.filter(function (card) {
        return !card.classList.contains("is-filtered-out");
      });
      var hidden = cardList.filter(function (card) {
        return card.classList.contains("is-filtered-out");
      });
      visible.sort(compareCards);
      hidden.sort(compareCards);
      visible.concat(hidden).forEach(function (card) {
        grid.appendChild(card);
      });
    }

    function applySortState(nextCol, nextDir, persist) {
      sortCol = nextCol || "name";
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

    function resetSort() {
      var defaults = defaultSortState();
      applySortState(defaults.sortCol, defaults.sortDir, true);
    }

    showAllCards(cards, resultCount, noResults, countLabels);
    clearFilterInputs(
      searchInput,
      filterGroup,
      filterPeriod,
      filterField,
      filterCountry,
      filterRegion
    );
    applySortState(sortCol, sortDir, false);

    if (!searchInput || !filterCountry) return;

    function updateFilterStyles() {
      ["filterGroup", "filterPeriod", "filterField", "filterCountry", "filterRegion"].forEach(
        function (id) {
          var el = document.getElementById(id);
          if (!el) return;
          var wrap = el.closest(".sel-wrap");
          if (wrap) wrap.classList.toggle("active", el.value !== "");
        }
      );
    }

    function cardMatches(card, q, group, period, field, country, region) {
      if (group && card.dataset.group !== group) return false;
      if (period && card.dataset.period !== period) return false;
      if (field && card.dataset.field !== field) return false;
      if (country && card.dataset.country !== country) return false;
      if (region && card.dataset.region !== region) return false;
      var hay = card.dataset.search || "";
      if (q && hay.indexOf(q) === -1) return false;
      return true;
    }

    function applyFilters() {
      var q = normQuery(searchInput.value);
      var group = filterGroup ? filterGroup.value : "";
      var period = filterPeriod ? filterPeriod.value : "";
      var field = filterField ? filterField.value : "";
      var country = filterCountry.value;
      var region = filterRegion ? filterRegion.value : "";
      var filtering = !!(q || group || period || field || country || region);
      var visible = 0;

      if (!filtering) {
        showAllCards(cards, resultCount, noResults, countLabels);
        updateFilterStyles();
        reorderCards();
        syncToolbarFilterBadge();
        return;
      }

      cards.forEach(function (card) {
        var match = cardMatches(card, q, group, period, field, country, region);
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

    function scrollToFirstVisible(countryName) {
      if (!countryName) return;
      var target = null;
      cards.forEach(function (card) {
        if (target || card.classList.contains("is-filtered-out")) return;
        if (card.dataset.country === countryName) target = card;
      });
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    searchInput.addEventListener("input", applyFilters);

    filterCountry.addEventListener("change", function () {
      applyFilters();
      scrollToFirstVisible(filterCountry.value);
    });

    if (filterGroup) filterGroup.addEventListener("change", applyFilters);
    if (filterPeriod) filterPeriod.addEventListener("change", applyFilters);
    if (filterField) filterField.addEventListener("change", applyFilters);
    if (filterRegion) filterRegion.addEventListener("change", applyFilters);

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
      btn.addEventListener("click", function () {
        var el = document.getElementById(btn.dataset.for);
        if (el) {
          el.value = "";
          el.dispatchEvent(new Event("change", { bubbles: true }));
        }
        applyFilters();
      });
    });

    if (clearFilters) {
      clearFilters.addEventListener("click", function () {
        clearFilterInputs(
          searchInput,
          filterGroup,
          filterPeriod,
          filterField,
          filterCountry,
          filterRegion
        );
        resetSort();
        applyFilters();
      });
    }

    updateFilterStyles();
    syncToolbarFilterBadge();
    document.dispatchEvent(new CustomEvent("daab-scientists-catalog-ready"));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
