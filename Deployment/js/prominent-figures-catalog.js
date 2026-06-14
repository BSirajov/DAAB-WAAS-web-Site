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
  var CARD_RENDER_BATCH = 18;
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
      searchPlaceholder: "Ad, ölkə, sahə, dövr və ya kateqoriya üzrə axtar…",
      searchAria: "Profil axtar",
      filterToggle: "Filtrlər",
      filterToggleAria: "Filtrləri göstər",
      filtersLabel: "Filtrlər",
      categoryAll: "📚 Bütün kateqoriyalar",
      categoryAzturk: "Azərbaycan və türk dünyası",
      categoryWorld: "Dünya alimləri",
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
      sortCategory: "Kateqoriya",
      sortBirth: "Tarixlər",
      groupLabel: "Qruplaşdır",
      groupNone: "Yoxdur",
      groupCategory: "Kateqoriya",
      groupPeriod: "Tarixi dövr",
      groupField: "Sahə",
      groupCountry: "Ölkə / region",
      groupOther: "Digər",
      groupCount: function (n) {
        return n + " profil";
      },
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
      cardCategory: "Kateqoriya",
      cardPeriod: "Dövr",
      cardField: "Sahə",
      cardCountry: "Ölkə",
      openProfile: "Profilə keç",
      empty: "Seçilmiş filtrlərə uyğun profil tapılmadı.",
      viewToggleAria: "Kataloq görünüşü",
      viewCards: "Kartlar",
      viewCardsTitle: "Kart görünüşü",
      viewTable: "Cədvəl",
      viewTableTitle: "Cədvəl görünüşü",
      tableName: "Ad",
      tableDates: "Tarixlər",
      tableCategory: "Kateqoriya",
      tablePeriod: "Dövr",
      tableField: "Sahə",
      tableCountry: "Ölkə",
      tableProfile: "Profil",
      tableNo: "№",
      rowsPerPageLabel: "Səhifədə sətir",
      rowsPerPageAria: "Cədvəldə göstərilən sətirlərin sayı",
      cardsPerPageLabel: "Səhifədə kart",
      cardsPerPageAria: "Kart görünüşündə göstərilən profillərin sayı",
      perPageAll: "Hamısı",
      paginationPrev: "Əvvəl",
      paginationNext: "Sonra",
    },
    en: {
      searchPlaceholder: "Search by name, country, field, period, or category…",
      searchAria: "Search profiles",
      filterToggle: "Filters",
      filterToggleAria: "Show filters",
      filtersLabel: "Filters",
      categoryAll: "📚 Category",
      categoryAzturk: "Azerbaijani & Turkic figures",
      categoryWorld: "World scientists",
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
      sortCategory: "Category",
      sortBirth: "Dates",
      groupLabel: "Group by",
      groupNone: "None",
      groupCategory: "Category",
      groupPeriod: "Period",
      groupField: "Field",
      groupCountry: "Country / region",
      groupOther: "Other",
      groupCount: function (n) {
        return n + " profile" + (n === 1 ? "" : "s");
      },
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
      cardCategory: "Category",
      cardPeriod: "Period",
      cardField: "Field",
      cardCountry: "Country",
      openProfile: "View profile",
      empty: "No profiles match the selected filters.",
      viewToggleAria: "Catalog view",
      viewCards: "Cards",
      viewCardsTitle: "Card view",
      viewTable: "Table",
      viewTableTitle: "Table view",
      tableName: "Name",
      tableDates: "Dates",
      tableCategory: "Category",
      tablePeriod: "Historical period",
      tableField: "Field",
      tableCountry: "Country",
      tableProfile: "Profile",
      tableNo: "№",
      rowsPerPageLabel: "Rows per page",
      rowsPerPageAria: "Rows shown in the table",
      cardsPerPageLabel: "Cards per page",
      cardsPerPageAria: "Cards shown in card view",
      perPageAll: "All",
      paginationPrev: "Prev",
      paginationNext: "Next",
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
  var VIEW_STORAGE_KEY = "daab-encyclopedia-view";
  var GROUP_STORAGE_KEY = "daab-encyclopedia-group";
  var PER_PAGE_TABLE_KEY = "daab-encyclopedia-per-page-table";
  var PER_PAGE_CARDS_KEY = "daab-encyclopedia-per-page-cards";
  var PER_PAGE_OPTIONS = ["20", "50", "100", "999999"];
  var GROUP_COLUMNS = ["category", "period", "field", "country"];

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

  function itemSearchText(item) {
    return norm(
      [
        item.name,
        item.dates,
        item.summary,
        item.country,
        item.field,
        item.period,
        item.region,
        item.categoryLabel,
      ].join(" ")
    );
  }

  function applyItemDataset(el, item) {
    el.id = item.id;
    el.setAttribute("data-category", item.category || "");
    el.setAttribute("data-period", item.period || "");
    el.setAttribute("data-field", item.field || "");
    el.setAttribute("data-country", item.country || "");
    el.setAttribute("data-country-name", item.country || "");
    el.setAttribute("data-region", item.region || "");
    if (item.birthYear != null) {
      el.setAttribute("data-birth-year", String(item.birthYear));
    } else {
      el.removeAttribute("data-birth-year");
    }
    el.setAttribute("data-search", itemSearchText(item));
  }

  function categoryLabelForItem(item, labels) {
    if (item.categoryLabel) return item.categoryLabel;
    if (item.category === "world") return labels.categoryWorld;
    if (item.category === "azturk") return labels.categoryAzturk;
    return "";
  }

  function renderTableCell(text, className) {
    var td = document.createElement("td");
    if (className) td.className = className;
    td.textContent = text || "—";
    return td;
  }

  function renderTableRow(item, labels) {
    var tr = document.createElement("tr");
    tr.className = "encyclopedia-row";
    applyItemDataset(tr, item);

    var noTd = document.createElement("td");
    noTd.className = "col-no";
    noTd.textContent = "—";
    tr.appendChild(noTd);

    var nameTd = document.createElement("td");
    nameTd.className = "col-name";
    var nameLink = document.createElement("a");
    nameLink.className = "row-name-link";
    nameLink.href = profileHref(item);
    nameLink.setAttribute("aria-label", labels.openProfile + ": " + item.name);
    var emojiSpan = document.createElement("span");
    emojiSpan.className = "row-emoji";
    emojiSpan.setAttribute("aria-hidden", "true");
    emojiSpan.textContent = item.emoji || "⭐";
    var nameSpan = document.createElement("span");
    nameSpan.className = "row-name";
    nameSpan.textContent = item.name;
    nameLink.appendChild(emojiSpan);
    nameLink.appendChild(nameSpan);
    nameTd.appendChild(nameLink);
    tr.appendChild(nameTd);

    tr.appendChild(renderTableCell(categoryLabelForItem(item, labels), "col-category"));
    tr.appendChild(renderTableCell(item.period, "col-period"));
    tr.appendChild(renderTableCell(item.field, "col-field"));
    tr.appendChild(renderTableCell(item.country, "col-country"));

    var profileTd = document.createElement("td");
    profileTd.className = "col-profile";
    var profileLink = document.createElement("a");
    profileLink.className = "row-profile-link";
    profileLink.href = profileHref(item);
    profileLink.textContent = labels.openProfile;
    profileTd.appendChild(profileLink);
    tr.appendChild(profileTd);

    return tr;
  }

  function renderCard(item, labels) {
    var card = document.createElement("a");
    card.className = "person-card";
    applyItemDataset(card, item);
    card.href = profileHref(item);
    card.setAttribute("aria-label", labels.openProfile + ": " + item.name);

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

  function getItemName(el) {
    var nameEl = el.querySelector(".card-name, .row-name");
    return nameEl ? nameEl.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function getSortValue(el, sortCol) {
    switch (sortCol) {
      case "period":
        return el.dataset.period || "";
      case "field":
        return el.dataset.field || "";
      case "country":
        return el.dataset.countryName || el.dataset.country || "";
      case "category":
        return el.dataset.category || "";
      case "birth":
        return parseInt(el.dataset.birthYear, 10) || 99999;
      case "name":
      default:
        return getItemName(el);
    }
  }

  function readViewState() {
    try {
      var mode = sessionStorage.getItem(VIEW_STORAGE_KEY);
      return mode === "table" ? "table" : "cards";
    } catch (e) {
      return "cards";
    }
  }

  function saveViewState(mode) {
    try {
      sessionStorage.setItem(VIEW_STORAGE_KEY, mode === "table" ? "table" : "cards");
    } catch (e) {
      /* ignore */
    }
  }

  function readSortState() {
    try {
      var raw = sessionStorage.getItem(SORT_STORAGE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || typeof s !== "object") return null;
      var col = s.sortCol;
      if (col === "group") {
        col = "category";
      }
      var dir = s.sortDir;
      if (
        col !== "name" &&
        col !== "country" &&
        col !== "field" &&
        col !== "period" &&
        col !== "birth" &&
        col !== "category"
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

  function readGroupState() {
    try {
      var col = sessionStorage.getItem(GROUP_STORAGE_KEY) || "";
      if (GROUP_COLUMNS.indexOf(col) === -1) return "";
      return col;
    } catch (e) {
      return "";
    }
  }

  function saveGroupState(groupCol) {
    try {
      if (!groupCol) {
        sessionStorage.removeItem(GROUP_STORAGE_KEY);
      } else {
        sessionStorage.setItem(GROUP_STORAGE_KEY, groupCol);
      }
    } catch (e) {
      /* ignore */
    }
  }

  function readPerPage(mode) {
    try {
      var key = mode === "table" ? PER_PAGE_TABLE_KEY : PER_PAGE_CARDS_KEY;
      var value = sessionStorage.getItem(key);
      if (value && PER_PAGE_OPTIONS.indexOf(value) >= 0) return value;
    } catch (e) {
      /* ignore */
    }
    return "50";
  }

  function savePerPage(mode, value) {
    try {
      var key = mode === "table" ? PER_PAGE_TABLE_KEY : PER_PAGE_CARDS_KEY;
      sessionStorage.setItem(key, String(value));
    } catch (e) {
      /* ignore */
    }
  }

  function getGroupKey(el, groupCol) {
    switch (groupCol) {
      case "category":
        return el.dataset.category || "";
      case "period":
        return el.dataset.period || "";
      case "field":
        return el.dataset.field || "";
      case "country":
        return el.dataset.countryName || el.dataset.country || "";
      default:
        return "";
    }
  }

  function getGroupLabel(key, groupCol, labels) {
    if (!key) return labels.groupOther;
    if (groupCol === "category") {
      if (key === "world") return labels.categoryWorld;
      if (key === "azturk") return labels.categoryAzturk;
    }
    return key;
  }

  function clearGroupChrome(grid, tableBody) {
    if (grid) {
      grid.querySelectorAll(".catalog-group-head").forEach(function (el) {
        el.remove();
      });
    }
    if (tableBody) {
      tableBody.querySelectorAll(".catalog-group-row").forEach(function (el) {
        el.remove();
      });
    }
  }

  function createCardGroupHead(label, count, labels) {
    var head = document.createElement("h3");
    head.className = "catalog-group-head";
    head.textContent = label;
    var countEl = document.createElement("span");
    countEl.className = "catalog-group-head__count";
    countEl.textContent = labels.groupCount(count);
    head.appendChild(countEl);
    return head;
  }

  function createTableGroupRow(label, count, labels, colSpan) {
    var tr = document.createElement("tr");
    tr.className = "catalog-group-row";
    var td = document.createElement("td");
    td.colSpan = colSpan;
    var labelEl = document.createElement("span");
    labelEl.className = "catalog-group-row__label";
    labelEl.textContent = label;
    var countEl = document.createElement("span");
    countEl.className = "catalog-group-row__count";
    countEl.textContent = "(" + labels.groupCount(count) + ")";
    td.appendChild(labelEl);
    td.appendChild(countEl);
    tr.appendChild(td);
    return tr;
  }

  function showAllItems(items, resultCount, noResults, countLabels) {
    items.forEach(function (el) {
      el.classList.remove("is-filtered-out", "is-match", "is-excluded");
    });
    if (resultCount && countLabels) {
      resultCount.innerHTML = countLabels.all(items.length);
    }
    if (noResults) {
      noResults.classList.remove("visible");
    }
  }

  function clearFilterInputs(
    searchInput,
    filterCategory,
    filterPeriod,
    filterField,
    filterCountry
  ) {
    if (searchInput) searchInput.value = "";
    if (filterCategory) filterCategory.value = "";
    if (filterPeriod) filterPeriod.value = "";
    if (filterField) filterField.value = "";
    if (filterCountry) filterCountry.value = "";
  }

  function syncToolbarFilterBadge() {
    if (
      window.DAAB_SCIENTISTS_TOOLBAR &&
      typeof window.DAAB_SCIENTISTS_TOOLBAR.syncAll === "function"
    ) {
      window.DAAB_SCIENTISTS_TOOLBAR.syncAll();
    }
  }

  function renderCatalogBatched(items, grid, tableBody, ui, done) {
    var index = 0;
    function batch() {
      var end = Math.min(index + CARD_RENDER_BATCH, items.length);
      for (; index < end; index++) {
        var item = items[index];
        grid.appendChild(renderCard(item, ui));
        if (tableBody) {
          tableBody.appendChild(renderTableRow(item, ui));
        }
      }
      if (index < items.length) {
        if (typeof requestAnimationFrame === "function") {
          requestAnimationFrame(batch);
        } else {
          setTimeout(batch, 0);
        }
      } else if (done) {
        done();
      }
    }
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(batch);
    } else {
      batch();
    }
  }

  function init() {
    var catalog = document.getElementById("encyclopedia-catalog");
    var grid = catalog ? catalog.querySelector(".cards-grid") : null;
    var tableBody = document.getElementById("encyclopediaTableBody");
    if (!grid || !DATA.length) return;

    var ui = t();
    var countLabels = filterCountLabels();
    var searchInput = document.getElementById("searchInput");
    var filterCategory = document.getElementById("filterCategory");
    var filterPeriod = document.getElementById("filterPeriod");
    var filterField = document.getElementById("filterField");
    var filterCountry = document.getElementById("filterCountry");
    var clearFilters = document.getElementById("clearFilters");
    var resultCount = document.getElementById("resultCount");
    var noResults = document.getElementById("no-results");
    var sortBy = document.getElementById("sortBy");
    var groupBy = document.getElementById("groupBy");
    var sortAscBtn = document.getElementById("sortAscBtn");
    var sortDescBtn = document.getElementById("sortDescBtn");
    var viewCardsBtn = document.getElementById("viewCardsBtn");
    var viewTableBtn = document.getElementById("viewTableBtn");
    var savedSort = readSortState() || defaultSortState();
    var sortCol = savedSort.sortCol;
    var sortDir = savedSort.sortDir;
    var groupCol = readGroupState();
    var viewMode = readViewState();
    var periodOptions = uniqueSorted(
      DATA.map(function (d) {
        return d.period;
      })
    );
    var fieldOptions = uniqueSorted(
      DATA.map(function (d) {
        return d.field;
      })
    );
    var countryOptions = uniqueSorted(
      DATA.map(function (d) {
        return d.country;
      })
    );
    if (catalog) {
      catalog.setAttribute("data-catalog-view", viewMode);
      catalog.setAttribute("aria-busy", "true");
    }

    renderCatalogBatched(DATA, grid, tableBody, ui, function () {
      if (catalog) {
        catalog.removeAttribute("aria-busy");
      }
      setupCatalog({
        catalog: catalog,
        grid: grid,
        tableBody: tableBody,
        ui: ui,
        countLabels: countLabels,
        searchInput: searchInput,
        filterCategory: filterCategory,
        filterPeriod: filterPeriod,
        filterField: filterField,
        filterCountry: filterCountry,
        clearFilters: clearFilters,
        resultCount: resultCount,
        noResults: noResults,
        sortBy: sortBy,
        groupBy: groupBy,
        sortAscBtn: sortAscBtn,
        sortDescBtn: sortDescBtn,
        viewCardsBtn: viewCardsBtn,
        viewTableBtn: viewTableBtn,
        viewMode: viewMode,
        sortCol: sortCol,
        sortDir: sortDir,
        groupCol: groupCol,
        periodOptions: periodOptions,
        fieldOptions: fieldOptions,
        countryOptions: countryOptions
      });
    });
  }

  function setupCatalog(ctx) {
    var catalog = ctx.catalog;
    var grid = ctx.grid;
    var tableBody = ctx.tableBody;
    var ui = ctx.ui;
    var countLabels = ctx.countLabels;
    var searchInput = ctx.searchInput;
    var filterCategory = ctx.filterCategory;
    var filterPeriod = ctx.filterPeriod;
    var filterField = ctx.filterField;
    var filterCountry = ctx.filterCountry;
    var clearFilters = ctx.clearFilters;
    var resultCount = ctx.resultCount;
    var noResults = ctx.noResults;
    var sortBy = ctx.sortBy;
    var groupBy = ctx.groupBy;
    var sortAscBtn = ctx.sortAscBtn;
    var sortDescBtn = ctx.sortDescBtn;
    var viewCardsBtn = ctx.viewCardsBtn;
    var viewTableBtn = ctx.viewTableBtn;
    var sortCol = ctx.sortCol;
    var sortDir = ctx.sortDir;
    var groupCol = ctx.groupCol || "";
    var viewMode = ctx.viewMode || "cards";
    var tableColSpan = 7;
    var page = 1;
    var perPage = 50;
    var pagination = document.getElementById("pagination");
    var perPageSel = document.getElementById("perPageSel");
    var rowsPerPageControl = document.querySelector(".rows-per-page-control");

    var cards = grid.querySelectorAll(".person-card");
    var rows = tableBody ? tableBody.querySelectorAll(".encyclopedia-row") : [];
    if (!cards.length) return;

    if (filterCategory) {
      filterCategory.innerHTML = "";
      var g0 = document.createElement("option");
      g0.value = "";
      g0.textContent = ui.categoryAll;
      filterCategory.appendChild(g0);
      [["azturk", ui.categoryAzturk], ["world", ui.categoryWorld]].forEach(function (pair) {
        var opt = document.createElement("option");
        opt.value = pair[0];
        opt.textContent = pair[1];
        filterCategory.appendChild(opt);
      });
    }

    fillSelect(filterPeriod, ui.period, ctx.periodOptions);
    fillSelect(filterField, ui.field, ctx.fieldOptions);
    fillSelect(filterCountry, ui.country, ctx.countryOptions);

    var periodHeader = document.querySelector('.encyclopedia-table th[data-col="period"]');
    if (periodHeader) periodHeader.textContent = ui.tablePeriod;
    var noHeader = document.querySelector(".encyclopedia-table th.col-no");
    if (noHeader) noHeader.textContent = ui.tableNo;
    var rowsPerPageLabel = document.querySelector(".rows-per-page-control__label");
    if (perPageSel) {
      perPageSel.value = readPerPage(viewMode);
      Array.prototype.forEach.call(perPageSel.options, function (opt) {
        if (opt.value === "999999") opt.textContent = ui.perPageAll;
      });
    }

    if (searchInput) searchInput.placeholder = ui.searchPlaceholder;
    if (searchInput) searchInput.setAttribute("aria-label", ui.searchAria);
    if (clearFilters) clearFilters.textContent = ui.clear;

    function updateViewToggleUi() {
      var cardsActive = viewMode !== "table";
      if (catalog) {
        catalog.setAttribute("data-catalog-view", cardsActive ? "cards" : "table");
      }
      if (viewCardsBtn) {
        viewCardsBtn.classList.toggle("is-active", cardsActive);
        viewCardsBtn.setAttribute("aria-pressed", cardsActive ? "true" : "false");
        viewCardsBtn.title = ui.viewCardsTitle;
        var cardsText = viewCardsBtn.querySelector(".catalog-view-toggle__text");
        if (cardsText) cardsText.textContent = ui.viewCards;
      }
      if (viewTableBtn) {
        viewTableBtn.classList.toggle("is-active", !cardsActive);
        viewTableBtn.setAttribute("aria-pressed", cardsActive ? "false" : "true");
        viewTableBtn.title = ui.viewTableTitle;
        var tableText = viewTableBtn.querySelector(".catalog-view-toggle__text");
        if (tableText) tableText.textContent = ui.viewTable;
      }
      var viewToggle = document.querySelector(".catalog-view-toggle");
      if (viewToggle) {
        viewToggle.setAttribute("aria-label", ui.viewToggleAria);
      }
      updatePerPageControlUi();
    }

    function usesPagination() {
      return !groupCol;
    }

    function updatePerPageControlUi() {
      if (rowsPerPageControl) {
        rowsPerPageControl.hidden = !usesPagination();
      }
      if (rowsPerPageLabel) {
        rowsPerPageLabel.textContent =
          viewMode === "table" ? ui.rowsPerPageLabel : ui.cardsPerPageLabel;
      }
      if (perPageSel) {
        perPageSel.setAttribute(
          "aria-label",
          viewMode === "table" ? ui.rowsPerPageAria : ui.cardsPerPageAria
        );
      }
    }

    function setRowNumber(row, n) {
      var td = row.querySelector("td.col-no");
      if (td) td.textContent = String(n);
    }

    function getVisibleTableRows() {
      if (!tableBody) return [];
      return Array.prototype.filter.call(
        tableBody.querySelectorAll(".encyclopedia-row"),
        function (row) {
          return !row.classList.contains("is-filtered-out");
        }
      );
    }

    function getVisibleCards() {
      if (!grid) return [];
      return Array.prototype.filter.call(grid.querySelectorAll(".person-card"), function (card) {
        return !card.classList.contains("is-filtered-out");
      });
    }

    function clearPaginationState() {
      Array.prototype.forEach.call(cards, function (card) {
        card.classList.remove("is-page-hidden");
      });
      if (tableBody) {
        Array.prototype.forEach.call(
          tableBody.querySelectorAll(".encyclopedia-row"),
          function (row) {
            row.classList.remove("is-page-hidden");
          }
        );
      }
      if (pagination) pagination.innerHTML = "";
    }

    function renderPagination(pages) {
      if (!pagination) return;
      if (!usesPagination() || pages <= 1) {
        pagination.innerHTML = "";
        return;
      }
      function btn(p, label, disabled, active) {
        return (
          '<button type="button" class="page-btn' +
          (active ? " active" : "") +
          (disabled ? " disabled" : "") +
          '" ' +
          (disabled ? "disabled" : "") +
          ' data-page="' +
          p +
          '">' +
          label +
          "</button>"
        );
      }
      var html = btn(page - 1, ui.paginationPrev, page === 1);
      var lo = Math.max(1, page - 2);
      var hi = Math.min(pages, page + 2);
      if (lo > 1) {
        html += btn(1, "1");
        if (lo > 2) html += '<span class="page-ellipsis">…</span>';
      }
      for (var p = lo; p <= hi; p++) html += btn(p, String(p), false, p === page);
      if (hi < pages) {
        if (hi < pages - 1) html += '<span class="page-ellipsis">…</span>';
        html += btn(pages, String(pages));
      }
      html += btn(page + 1, ui.paginationNext, page === pages);
      pagination.innerHTML = html;
      pagination.querySelectorAll(".page-btn:not(.disabled)").forEach(function (el) {
        el.addEventListener("click", function () {
          page = parseInt(el.getAttribute("data-page"), 10);
          applyCatalogPagination();
          if (catalog) {
            catalog.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        });
      });
    }

    function applyCatalogPagination() {
      if (!usesPagination()) {
        clearPaginationState();
        getVisibleTableRows().forEach(function (row, i) {
          setRowNumber(row, i + 1);
        });
        updatePerPageControlUi();
        return;
      }

      perPage = perPageSel ? parseInt(perPageSel.value, 10) || 50 : 50;
      if (perPageSel) savePerPage(viewMode, perPageSel.value);

      var pages = 1;
      var start = 0;
      var end = 0;

      if (viewMode === "table") {
        var dataRows = getVisibleTableRows();
        pages = perPage >= 999999 ? 1 : Math.ceil(dataRows.length / perPage);
        if (page > pages) page = Math.max(1, pages);
        start = (page - 1) * perPage;
        end = start + perPage;

        Array.prototype.forEach.call(cards, function (card) {
          card.classList.remove("is-page-hidden");
        });

        dataRows.forEach(function (row, i) {
          var onPage = perPage >= 999999 || (i >= start && i < end);
          row.classList.toggle("is-page-hidden", !onPage);
          if (onPage) setRowNumber(row, i + 1);
        });

        Array.prototype.forEach.call(
          tableBody.querySelectorAll(".encyclopedia-row.is-filtered-out"),
          function (row) {
            row.classList.remove("is-page-hidden");
          }
        );
      } else {
        var dataCards = getVisibleCards();
        pages = perPage >= 999999 ? 1 : Math.ceil(dataCards.length / perPage);
        if (page > pages) page = Math.max(1, pages);
        start = (page - 1) * perPage;
        end = start + perPage;

        if (tableBody) {
          Array.prototype.forEach.call(
            tableBody.querySelectorAll(".encyclopedia-row"),
            function (row) {
              row.classList.remove("is-page-hidden");
            }
          );
        }

        dataCards.forEach(function (card, i) {
          var onPage = perPage >= 999999 || (i >= start && i < end);
          card.classList.toggle("is-page-hidden", !onPage);
        });

        Array.prototype.forEach.call(
          grid.querySelectorAll(".person-card.is-filtered-out"),
          function (card) {
            card.classList.remove("is-page-hidden");
          }
        );
      }

      renderPagination(pages);
      updatePerPageControlUi();
    }

    function setViewMode(mode) {
      if (perPageSel) savePerPage(viewMode, perPageSel.value);
      viewMode = mode === "table" ? "table" : "cards";
      saveViewState(viewMode);
      page = 1;
      if (perPageSel) perPageSel.value = readPerPage(viewMode);
      updateViewToggleUi();
      applyCatalogPagination();
    }

    function updateSortUi() {
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
      updateTableSortUi();
    }

    function updateTableSortUi() {
      var table = document.querySelector(".encyclopedia-table");
      if (!table) return;
      var headers = table.querySelectorAll("thead th[data-col]");
      Array.prototype.forEach.call(headers, function (th) {
        var col = th.getAttribute("data-col");
        var active = col === sortCol;
        th.classList.toggle("asc", active && sortDir === 1);
        th.classList.toggle("desc", active && sortDir === -1);
        th.setAttribute("aria-sort", active ? (sortDir === 1 ? "ascending" : "descending") : "none");
      });
    }

    function initTableControls() {
      var table = document.querySelector(".encyclopedia-table");
      if (!table) return;
      Array.prototype.forEach.call(
        table.querySelectorAll("thead th.sortable[data-col]"),
        function (th) {
          th.addEventListener("click", function () {
            var col = th.getAttribute("data-col");
            if (!col) return;
            var nextDir = sortCol === col ? sortDir * -1 : 1;
            applySortState(col, nextDir, true);
          });
        }
      );
      if (window.DAAB_TABLE_RESIZE && typeof window.DAAB_TABLE_RESIZE.initTable === "function") {
        window.DAAB_TABLE_RESIZE.initTable(table);
      }
    }

    function compareItems(a, b) {
      if (sortCol === "birth") {
        var av = getSortValue(a, "birth");
        var bv = getSortValue(b, "birth");
        if (av !== bv) return sortDir * (av - bv);
        return sortDir * localeCompare(getItemName(a), getItemName(b));
      }
      var primary =
        sortDir * localeCompare(getSortValue(a, sortCol), getSortValue(b, sortCol));
      if (primary !== 0) return primary;
      return sortDir * localeCompare(a.id || "", b.id || "");
    }

    function appendCardAndRow(card, rowMap) {
      grid.appendChild(card);
      var row = rowMap[card.id];
      if (row && tableBody) {
        tableBody.appendChild(row);
      }
    }

    function buildVisibleGroups(visible) {
      var groups = [];
      var groupMap = {};
      visible.forEach(function (card) {
        var key = getGroupKey(card, groupCol);
        if (!groupMap[key]) {
          groupMap[key] = {
            key: key,
            label: getGroupLabel(key, groupCol, ui),
            cards: [],
          };
          groups.push(groupMap[key]);
        }
        groupMap[key].cards.push(card);
      });
      groups.sort(function (a, b) {
        return localeCompare(a.label, b.label);
      });
      return groups;
    }

    function reorderCatalog() {
      var cardList = Array.prototype.slice.call(cards);
      var rowMap = {};
      Array.prototype.forEach.call(rows, function (row) {
        rowMap[row.id] = row;
      });
      var visible = cardList.filter(function (card) {
        return !card.classList.contains("is-filtered-out");
      });
      var hidden = cardList.filter(function (card) {
        return card.classList.contains("is-filtered-out");
      });
      visible.sort(compareItems);
      hidden.sort(compareItems);
      clearGroupChrome(grid, tableBody);

      if (catalog) {
        if (groupCol) {
          catalog.setAttribute("data-catalog-group", groupCol);
        } else {
          catalog.removeAttribute("data-catalog-group");
        }
      }

      if (!groupCol) {
        visible.concat(hidden).forEach(function (card) {
          appendCardAndRow(card, rowMap);
        });
        applyCatalogPagination();
        return;
      }

      buildVisibleGroups(visible).forEach(function (group) {
        grid.appendChild(createCardGroupHead(group.label, group.cards.length, ui));
        if (tableBody) {
          tableBody.appendChild(
            createTableGroupRow(group.label, group.cards.length, ui, tableColSpan)
          );
        }
        group.cards.forEach(function (card) {
          appendCardAndRow(card, rowMap);
        });
      });

      hidden.forEach(function (card) {
        appendCardAndRow(card, rowMap);
      });

      applyCatalogPagination();
    }

    function updateGroupUi() {
      if (groupBy && groupBy.value !== groupCol) {
        groupBy.value = groupCol;
      }
      if (catalog) {
        if (groupCol) {
          catalog.setAttribute("data-catalog-group", groupCol);
        } else {
          catalog.removeAttribute("data-catalog-group");
        }
      }
    }

    function applyGroupState(nextCol, persist) {
      groupCol = GROUP_COLUMNS.indexOf(nextCol) >= 0 ? nextCol : "";
      if (persist !== false) {
        saveGroupState(groupCol);
      }
      page = 1;
      updateGroupUi();
      reorderCatalog();
    }

    function applySortState(nextCol, nextDir, persist) {
      sortCol = nextCol || "name";
      sortDir = nextDir === -1 ? -1 : 1;
      if (persist !== false) {
        saveSortState(sortCol, sortDir);
      }
      updateSortUi();
      reorderCatalog();
    }

    function setSortDir(dir) {
      applySortState(sortCol, dir === -1 ? -1 : 1, true);
    }

    function resetSort() {
      var defaults = defaultSortState();
      applySortState(defaults.sortCol, defaults.sortDir, true);
    }

    showAllItems(cards, resultCount, noResults, countLabels);
    clearFilterInputs(
      searchInput,
      filterCategory,
      filterPeriod,
      filterField,
      filterCountry
    );
    applySortState(sortCol, sortDir, false);
    applyGroupState(groupCol, false);
    updateViewToggleUi();
    initTableControls();

    if (groupBy) {
      var groupLabel = document.querySelector(".group-control__label");
      if (groupLabel) groupLabel.textContent = ui.groupLabel;
      groupBy.setAttribute("aria-label", ui.groupLabel);
      Array.prototype.forEach.call(groupBy.options, function (opt) {
        if (opt.value === "") opt.textContent = ui.groupNone;
        if (opt.value === "category") opt.textContent = ui.groupCategory;
        if (opt.value === "period") opt.textContent = ui.groupPeriod;
        if (opt.value === "field") opt.textContent = ui.groupField;
        if (opt.value === "country") opt.textContent = ui.groupCountry;
      });
    }

    if (viewCardsBtn) {
      viewCardsBtn.addEventListener("click", function () {
        setViewMode("cards");
      });
    }
    if (viewTableBtn) {
      viewTableBtn.addEventListener("click", function () {
        setViewMode("table");
      });
    }

    if (perPageSel) {
      perPageSel.addEventListener("change", function () {
        page = 1;
        applyCatalogPagination();
      });
    }

    if (!searchInput || !filterCountry) return;

    function updateFilterStyles() {
      ["filterCategory", "filterPeriod", "filterField", "filterCountry"].forEach(
        function (id) {
          var el = document.getElementById(id);
          if (!el) return;
          var wrap = el.closest(".sel-wrap");
          if (wrap) wrap.classList.toggle("active", el.value !== "");
        }
      );
    }

    function itemMatches(el, q, category, period, field, country) {
      if (category && el.dataset.category !== category) return false;
      if (period && el.dataset.period !== period) return false;
      if (field && el.dataset.field !== field) return false;
      if (country && el.dataset.country !== country) return false;
      var hay = el.dataset.search || "";
      if (q && hay.indexOf(q) === -1) return false;
      return true;
    }

    function setFilteredState(el, match) {
      el.classList.toggle("is-filtered-out", !match);
    }

    function applyFilters() {
      var q = normQuery(searchInput.value);
      var category = filterCategory ? filterCategory.value : "";
      var period = filterPeriod ? filterPeriod.value : "";
      var field = filterField ? filterField.value : "";
      var country = filterCountry.value;
      var filtering = !!(q || category || period || field || country);
      var visible = 0;
      page = 1;

      if (!filtering) {
        showAllItems(cards, resultCount, noResults, countLabels);
        Array.prototype.forEach.call(rows, function (row) {
          setFilteredState(row, true);
        });
        updateFilterStyles();
        reorderCatalog();
        syncToolbarFilterBadge();
        return;
      }

      cards.forEach(function (card) {
        var match = itemMatches(card, q, category, period, field, country);
        setFilteredState(card, match);
        if (match) visible++;
      });
      Array.prototype.forEach.call(rows, function (row) {
        setFilteredState(
          row,
          itemMatches(row, q, category, period, field, country)
        );
      });

      if (resultCount) {
        resultCount.innerHTML = countLabels.matched(visible, cards.length);
      }
      if (noResults) {
        noResults.classList.toggle("visible", visible === 0);
      }
      updateFilterStyles();
      reorderCatalog();
      syncToolbarFilterBadge();
    }

    function scrollToFirstVisible(countryName) {
      if (!countryName) return;
      var target = null;
      var list = viewMode === "table" ? rows : cards;
      Array.prototype.forEach.call(list, function (el) {
        if (target || el.classList.contains("is-filtered-out")) return;
        if (el.dataset.country === countryName) target = el;
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

    if (filterCategory) filterCategory.addEventListener("change", applyFilters);
    if (filterPeriod) filterPeriod.addEventListener("change", applyFilters);
    if (filterField) filterField.addEventListener("change", applyFilters);

    if (sortBy) {
      sortBy.addEventListener("change", function () {
        applySortState(sortBy.value, sortDir, true);
      });
    }

    if (groupBy) {
      groupBy.addEventListener("change", function () {
        applyGroupState(groupBy.value, true);
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
          filterCategory,
          filterPeriod,
          filterField,
          filterCountry
        );
        resetSort();
        applyGroupState("", true);
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
