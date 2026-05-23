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

  var COUNTRY_NAME_TO_CODE = {
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
      case "degree":
        return card.dataset.degree || "";
      case "name":
      default:
        return getCardName(card);
    }
  }

  function showAllCards(cards, resultCount, noResults) {
    cards.forEach(function (card) {
      card.classList.remove("is-filtered-out", "is-match", "is-excluded");
    });
    if (resultCount) {
      resultCount.innerHTML =
        "<span>" + cards.length + "</span> profil";
    }
    if (noResults) {
      noResults.classList.remove("visible");
    }
  }

  function clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree) {
    if (searchInput) searchInput.value = "";
    if (filterCountry) filterCountry.value = "";
    if (filterIxtilas) filterIxtilas.value = "";
    if (filterDegree) filterDegree.value = "";
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
    var sortCol = sortBy ? sortBy.value : "name";
    var sortDir = 1;

    if (!cards.length) return;

    function updateSortDirUi() {
      var ascending = sortDir === 1;
      if (sortAscBtn) {
        sortAscBtn.classList.toggle("is-active", ascending);
        sortAscBtn.setAttribute("aria-pressed", ascending ? "true" : "false");
      }
      if (sortDescBtn) {
        sortDescBtn.classList.toggle("is-active", !ascending);
        sortDescBtn.setAttribute("aria-pressed", ascending ? "false" : "true");
      }
    }

    function setSortDir(dir) {
      sortDir = dir === -1 ? -1 : 1;
      updateSortDirUi();
      reorderCards();
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
        list.sort(function (a, b) {
          return (
            sortDir *
            localeCompare(getSortValue(a, sortCol), getSortValue(b, sortCol))
          );
        });
      }

      sortList(visible);
      sortList(hidden);
      visible.concat(hidden).forEach(function (card) {
        grid.appendChild(card);
      });
    }

    /* Always restore full catalogue on load */
    showAllCards(cards, resultCount, noResults);
    clearFilterInputs(searchInput, filterCountry, filterIxtilas, filterDegree);
    updateSortDirUi();
    reorderCards();

    if (!searchInput || !filterCountry) return;

    if (DATA.length) {
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

    function updateFilterStyles() {
      ["filterCountry", "filterIxtilas", "filterDegree"].forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        var wrap = el.closest(".sel-wrap");
        if (wrap) wrap.classList.toggle("active", el.value !== "");
      });
    }

    function cardMatches(card, q, countryCode, degree, ixtilas) {
      var code = card.dataset.country || "";
      var hay = (card.dataset.search || "").toLowerCase();
      var deg = (card.dataset.degree || "").trim();
      var ixt = (card.dataset.ixtilas || "").trim();
      if (countryCode && countryCode !== code) return false;
      if (degree && deg !== degree) return false;
      if (ixtilas && ixt !== ixtilas) return false;
      if (q && hay.indexOf(q) === -1) return false;
      return true;
    }

    function applyFilters() {
      var q = normQuery(searchInput.value);
      var cntry = filterCountry.value;
      var degree = filterDegree ? filterDegree.value : "";
      var ixtilas = filterIxtilas ? filterIxtilas.value : "";
      var countryCode = cntry ? COUNTRY_NAME_TO_CODE[cntry] || "" : "";
      var filtering = !!(q || cntry || degree || ixtilas);
      var visible = 0;

      if (!filtering) {
        showAllCards(cards, resultCount, noResults);
        updateFilterStyles();
        reorderCards();
        return;
      }

      cards.forEach(function (card) {
        var match = cardMatches(card, q, countryCode, degree, ixtilas);
        card.classList.toggle("is-filtered-out", !match);
        if (match) visible++;
      });

      if (resultCount) {
        resultCount.innerHTML =
          "<span>" +
          visible +
          "</span> uyğun profil" +
          (visible < cards.length ? " (" + cards.length + " ümumi)" : "");
      }
      if (noResults) {
        noResults.classList.toggle("visible", visible === 0);
      }
      updateFilterStyles();
      reorderCards();
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
      sortCol = "name";
      sortDir = 1;
      if (sortBy) sortBy.value = "name";
      updateSortDirUi();
      reorderCards();
    }

    searchInput.addEventListener("input", applyFilters);

    filterCountry.addEventListener("change", function () {
      applyFilters();
      scrollToFirstVisible(COUNTRY_NAME_TO_CODE[filterCountry.value] || "");
    });

    if (filterIxtilas) {
      filterIxtilas.addEventListener("change", applyFilters);
    }
    if (filterDegree) {
      filterDegree.addEventListener("change", applyFilters);
    }

    if (sortBy) {
      sortBy.addEventListener("change", function () {
        sortCol = sortBy.value;
        reorderCards();
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
        if (el) el.value = "";
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
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
