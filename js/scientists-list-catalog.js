/**
 * Scientists list catalogue — filters, sort, group, cards/table views.
 * Used by az/scientists/list.html and en/scientists/list.html.
 */
(function () {
  "use strict";

  var SORT_STORAGE_KEY = "daab-scientists-list-sort";
  var GROUP_STORAGE_KEY = "daab-scientists-list-group";
  var VIEW_STORAGE_KEY = "daab-scientists-list-view";
  var SORT_COLUMNS = ["ad_soyad", "yasadigi_olke", "ixtilas", "elmi_derece", "cinsi"];
  var GROUP_COLUMNS = ["yasadigi_olke", "ixtilas", "elmi_derece", "cinsi"];

  var STRINGS = {
    az: {
      result: function (total, all) {
        var html = "<span>" + total + "</span> nəticə";
        if (total < all) html += " (" + all + " ümumi)";
        return html;
      },
      sortLabel: "Sırala",
      sortName: "Ad",
      sortCountry: "Yaşadığı Ölkə",
      sortField: "İxtisas",
      sortDegree: "Elmi dərəcə",
      sortGender: "Cins",
      sortDirAria: "Sıralama istiqaməti",
      sortAsc: "A→Z",
      sortDesc: "Z→A",
      groupLabel: "Qruplaşdır",
      groupNone: "Yoxdur",
      groupCountry: "Yaşadığı Ölkə",
      groupField: "İxtisas",
      groupDegree: "Elmi dərəcə",
      groupGender: "Cins",
      groupOther: "Digər",
      groupCount: function (n) {
        return n + " alim";
      },
      viewLabel: "Görünüş",
      viewCards: "Vərəqələr",
      viewCardsTitle: "Vərəqə görünüşü",
      viewTable: "Cədvəl",
      viewTableTitle: "Cədvəl görünüşü",
      viewToggleAria: "Kataloq görünüşü",
      paginationPrev: "Əvvəl",
      paginationNext: "Sonra",
      genderMale: "Kişi",
      genderFemale: "Qadın",
      qrTitle: "Bu alimin profil səhifəsinə keçid",
      qrAria: "Profil linkinin QR kodu",
      qrAlt: function (name) {
        return "QR kodu: " + (name || "");
      },
    },
    en: {
      result: function (total, all) {
        var html = "<span>" + total + "</span> result" + (total === 1 ? "" : "s");
        if (total < all) html += " (" + all + " total)";
        return html;
      },
      sortLabel: "Sort by",
      sortName: "Name",
      sortCountry: "Country of residence",
      sortField: "Field",
      sortDegree: "Degree",
      sortGender: "Gender",
      sortDirAria: "Sort direction",
      sortAsc: "A→Z",
      sortDesc: "Z→A",
      groupLabel: "Group by",
      groupNone: "None",
      groupCountry: "Country of residence",
      groupField: "Field",
      groupDegree: "Degree",
      groupGender: "Gender",
      groupOther: "Other",
      groupCount: function (n) {
        return n + " scientist" + (n === 1 ? "" : "s");
      },
      viewLabel: "View by",
      viewCards: "Cards",
      viewCardsTitle: "Card view",
      viewTable: "Table",
      viewTableTitle: "Table view",
      viewToggleAria: "Catalog view",
      paginationPrev: "Prev",
      paginationNext: "Next",
      genderMale: "Male",
      genderFemale: "Female",
      qrTitle: "Link to this scientist's profile page",
      qrAria: "QR code for profile link",
      qrAlt: function (name) {
        return "QR code: " + (name || "");
      },
    },
  };

  function lang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function t() {
    return STRINGS[lang()] || STRINGS.az;
  }

  function localeCollator() {
    var pageLang = lang();
    if (typeof Intl !== "undefined" && typeof Intl.Collator === "function") {
      return new Intl.Collator(pageLang === "en" ? "en" : "az", { sensitivity: "base" });
    }
    return null;
  }

  function compare(a, b) {
    var coll = window.DAAB_COLLATION;
    if (coll && typeof coll.compare === "function") {
      return coll.compare(a, b);
    }
    var intl = localeCollator();
    if (intl) return intl.compare(String(a || ""), String(b || ""));
    return String(a || "").localeCompare(String(b || ""), undefined, { sensitivity: "base" });
  }

  function sortValues(arr) {
    var coll = window.DAAB_COLLATION;
    if (coll && typeof coll.sort === "function") {
      return coll.sort(arr);
    }
    var copy = arr.slice();
    copy.sort(compare);
    return copy;
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function readSortState() {
    try {
      var raw = sessionStorage.getItem(SORT_STORAGE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || SORT_COLUMNS.indexOf(s.sortCol) === -1) return null;
      if (s.sortDir !== 1 && s.sortDir !== -1) return null;
      return { sortCol: s.sortCol, sortDir: s.sortDir };
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

  function readGroupState() {
    try {
      var col = sessionStorage.getItem(GROUP_STORAGE_KEY) || "";
      return GROUP_COLUMNS.indexOf(col) >= 0 ? col : "";
    } catch (e) {
      return "";
    }
  }

  function saveGroupState(groupCol) {
    try {
      if (!groupCol) sessionStorage.removeItem(GROUP_STORAGE_KEY);
      else sessionStorage.setItem(GROUP_STORAGE_KEY, groupCol);
    } catch (e) {
      /* ignore */
    }
  }

  function readViewState() {
    try {
      return sessionStorage.getItem(VIEW_STORAGE_KEY) === "cards" ? "cards" : "table";
    } catch (e) {
      return "table";
    }
  }

  function saveViewState(mode) {
    try {
      sessionStorage.setItem(VIEW_STORAGE_KEY, mode === "cards" ? "cards" : "table");
    } catch (e) {
      /* ignore */
    }
  }

  function groupLabelForValue(key, groupCol, labels) {
    if (!key) return labels.groupOther;
    if (groupCol === "cinsi") {
      if (key === "kişi" || key === "male") return labels.genderMale;
      if (key === "qadın" || key === "female") return labels.genderFemale;
    }
    return key;
  }

  function getGroupKey(row, groupCol) {
    if (!groupCol) return "";
    var val = row[groupCol];
    return val == null ? "" : String(val).trim();
  }

  function displayName(row) {
    var deg = (row.elmi_derece || "").trim();
    return [row.ad_soyad, deg].map(function (v) {
      return (v || "").trim();
    }).filter(Boolean).join(", ");
  }

  function init() {
    var DATA = window.SCIENTISTS_CATALOG_DATA || [];
    if (!DATA.length) return;

    var ui = t();
    var catalog = document.getElementById("scientists-catalog");
    var grid = catalog ? catalog.querySelector(".scientists-cards-grid") : null;
    var tableBody = document.getElementById("tableBody");
    var searchInput = document.getElementById("searchInput");
    var filterCountry = document.getElementById("filterCountry");
    var filterIxtilas = document.getElementById("filterIxtilas");
    var filterDegree = document.getElementById("filterDegree");
    var filterCins = document.getElementById("filterCins");
    var clearFilters = document.getElementById("clearFilters");
    var resultCount = document.getElementById("resultCount");
    var noResults = document.getElementById("noResults");
    var pagination = document.getElementById("pagination");
    var perPageSel = document.getElementById("perPageSel");
    var rowsPerPageControl = document.querySelector(".rows-per-page-control");
    var sortBy = document.getElementById("sortBy");
    var groupBy = document.getElementById("groupBy");
    var sortAscBtn = document.getElementById("sortAscBtn");
    var sortDescBtn = document.getElementById("sortDescBtn");
    var viewCardsBtn = document.getElementById("viewCardsBtn");
    var viewTableBtn = document.getElementById("viewTableBtn");

    if (!tableBody || !searchInput) return;

    var savedSort = readSortState() || { sortCol: "ad_soyad", sortDir: 1 };
    var sortCol = savedSort.sortCol;
    var sortDir = savedSort.sortDir;
    var groupCol = readGroupState();
    var viewMode = readViewState();
    var filtered = DATA.slice();
    var page = 1;
    var perPage = 50;

    var countries = sortValues(
      DATA.map(function (r) {
        return r.yasadigi_olke;
      }).filter(Boolean)
    );
    var unique = function (arr) {
      return arr.filter(function (v, i) {
        return v && arr.indexOf(v) === i;
      });
    };
    countries = sortValues(unique(countries));
    var degrees = sortValues(
      unique(
        DATA.map(function (r) {
          return (r.elmi_derece || "").trim();
        })
      )
    );
    var fields = sortValues(
      unique(
        DATA.map(function (r) {
          return (r.ixtilas || "").trim();
        })
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
    fields.forEach(function (x) {
      var o = document.createElement("option");
      o.value = x;
      o.textContent = x;
      filterIxtilas.appendChild(o);
    });

    var ms = window.DAABScientistsMultiSelect;
    var filterIds = ["filterCountry", "filterIxtilas", "filterDegree", "filterCins"];

    function getMultiFilter(id) {
      if (ms) return ms.getFilterValues(id);
      var el = document.getElementById(id);
      return el && el.value ? [el.value] : null;
    }

    function mountMultiFilters() {
      if (!ms) return;
      filterIds.forEach(function (id) {
        var el = document.getElementById(id);
        if (el) {
          ms.mount(el, {
            onChange: function () {
              applyFilters();
              updateFilterStyles();
              if (window.DAAB_SCIENTISTS_TOOLBAR) window.DAAB_SCIENTISTS_TOOLBAR.syncAll();
            },
          });
        }
      });
    }

    mountMultiFilters();

    function sortRows(rows) {
      rows.sort(function (a, b) {
        var av = a[sortCol] == null ? "" : String(a[sortCol]).trim();
        var bv = b[sortCol] == null ? "" : String(b[sortCol]).trim();
        var primary = sortDir * compare(av, bv);
        if (primary !== 0) return primary;
        return sortDir * compare(String(a.say || ""), String(b.say || ""));
      });
      return rows;
    }

    function buildGroups(rows) {
      var groups = [];
      var map = {};
      rows.forEach(function (row) {
        var key = getGroupKey(row, groupCol);
        if (!map[key]) {
          map[key] = {
            key: key,
            label: groupLabelForValue(key, groupCol, ui),
            rows: [],
          };
          groups.push(map[key]);
        }
        map[key].rows.push(row);
      });
      groups.sort(function (a, b) {
        return compare(a.label, b.label);
      });
      return groups;
    }

    function rowHTML(r, idx) {
      var email = (r.email || "").trim();
      var deg = (r.elmi_derece || "").trim();
      var nameLabel = esc(displayName(r)) || "—";
      var sayAttr = r.say != null ? ' data-scientist-say="' + esc(String(r.say)) + '"' : "";
      var emailAttr = email ? ' data-scientist-email="' + esc(email) + '"' : "";
      var nameCell =
        email || r.say != null
          ? '<button type="button" class="scientist-name-trigger"' +
            emailAttr +
            sayAttr +
            ' aria-expanded="false">' +
            nameLabel +
            "</button>"
          : nameLabel;
      return (
        "<tr>" +
        '<td class="col-no">' +
        idx +
        "</td>" +
        '<td class="col-name">' +
        nameCell +
        "</td>" +
        '<td class="col-cntry">' +
        (esc(r.yasadigi_olke) || "—") +
        "</td>" +
        '<td class="col-spec">' +
        (esc((r.ixtilas || "").trim()) || "—") +
        "</td>" +
        '<td class="col-degree">' +
        (esc(deg) || "") +
        "</td>" +
        '<td class="col-email">' +
        (email
          ? '<a class="email-link" href="mailto:' + esc(email) + '">' + esc(email) + "</a>"
          : '<span class="empty-email">—</span>') +
        "</td>" +
        '<td class="col-cins" aria-hidden="true">' +
        (esc(groupLabelForValue((r.cinsi || "").trim(), "cinsi", ui)) || "—") +
        "</td>" +
        "</tr>"
      );
    }

    function groupRowHTML(label, count) {
      return (
        '<tr class="catalog-group-row"><td colspan="7">' +
        '<span class="catalog-group-row__label">' +
        esc(label) +
        "</span>" +
        '<span class="catalog-group-row__count">(' +
        esc(ui.groupCount(count)) +
        ")</span></td></tr>"
      );
    }

    function cardInitials(name) {
      var parts = String(name || "")
        .trim()
        .split(/\s+/)
        .filter(Boolean);
      if (!parts.length) return "?";
      var first = parts[0].charAt(0);
      var last = parts.length > 1 ? parts[parts.length - 1].charAt(0) : "";
      return (first + last).toUpperCase();
    }

    function profileForRow(row) {
      var preview = window.DAABScientistsListPreview;
      if (!preview || typeof preview.lookupByKeys !== "function") return null;
      return preview.lookupByKeys((row.email || "").trim(), row.say);
    }

    function appendCardPortrait(top, row, name) {
      var profile = profileForRow(row);
      var preview = window.DAABScientistsListPreview;
      var photoUrl =
        profile && preview && typeof preview.photoUrl === "function"
          ? preview.photoUrl(profile)
          : "";

      var portrait = document.createElement("div");
      portrait.className = "scientist-card__portrait";
      var avatar = document.createElement("div");
      avatar.className = "scientist-card__avatar";

      if (photoUrl) {
        var img = document.createElement("img");
        img.src = photoUrl;
        img.alt = name || "";
        img.width = 76;
        img.height = 90;
        img.loading = "lazy";
        img.decoding = "async";
        avatar.appendChild(img);
      } else {
        avatar.classList.add("is-empty");
        avatar.setAttribute("aria-hidden", "true");
        var initials = document.createElement("span");
        initials.className = "scientist-card__initials";
        initials.textContent = cardInitials(row.ad_soyad || name);
        avatar.appendChild(initials);
      }

      portrait.appendChild(avatar);
      top.appendChild(portrait);
    }

    function appendCardQr(card, row, name) {
      var profile = profileForRow(row);
      var preview = window.DAABScientistsListPreview;
      if (!profile || !preview || typeof preview.qrUrl !== "function") return;

      var qrSrc = preview.qrUrl(profile);
      if (!qrSrc) return;

      var ui = t();
      var href =
        typeof preview.profileHref === "function"
          ? preview.profileHref(profile)
          : profile.slug
            ? "profiles.html#" + profile.slug
            : "profiles.html";

      var link = document.createElement("a");
      link.className = "scientist-card__qr-link card-qr-link";
      link.href = href;
      link.title = ui.qrTitle;
      link.setAttribute("aria-label", ui.qrAria);

      var img = document.createElement("img");
      img.className = "scientist-card__qr card-qr";
      img.src = qrSrc;
      img.width = 48;
      img.height = 48;
      img.alt = typeof ui.qrAlt === "function" ? ui.qrAlt(name) : "";
      img.decoding = "async";
      img.loading = "lazy";

      link.appendChild(img);
      card.appendChild(link);
    }

    function renderCard(row) {
      var card = document.createElement("article");
      card.className = "scientist-card";
      var email = (row.email || "").trim();
      var field = (row.ixtilas || "").trim();
      var country = row.yasadigi_olke || "";
      var deg = (row.elmi_derece || "").trim();
      var name = (row.ad_soyad || "").trim();

      var top = document.createElement("div");
      top.className = "scientist-card__top";

      appendCardPortrait(top, row, name);

      var meta = document.createElement("div");
      meta.className = "scientist-card__meta";

      if (email || row.say != null) {
        var trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "scientist-card__name scientist-name-trigger";
        trigger.textContent = name || "—";
        trigger.setAttribute("aria-expanded", "false");
        if (email) trigger.setAttribute("data-scientist-email", email);
        if (row.say != null) trigger.setAttribute("data-scientist-say", String(row.say));
        meta.appendChild(trigger);
      } else {
        var nameEl = document.createElement("div");
        nameEl.className = "scientist-card__name";
        nameEl.textContent = name || "—";
        meta.appendChild(nameEl);
      }

      if (country) {
        var countryEl = document.createElement("div");
        countryEl.className = "scientist-card__country";
        countryEl.textContent = country;
        meta.appendChild(countryEl);
      }

      if (field || deg) {
        var fieldEl = document.createElement("div");
        fieldEl.className = "scientist-card__field";
        fieldEl.textContent = [field, deg].filter(Boolean).join(" · ");
        meta.appendChild(fieldEl);
      }

      if (email) {
        var mail = document.createElement("a");
        mail.className = "scientist-card__email email-link";
        mail.href = "mailto:" + email;
        mail.textContent = email;
        meta.appendChild(mail);
      }

      top.appendChild(meta);
      card.appendChild(top);

      appendCardQr(card, row, name);

      return card;
    }

    function createCardGroupHead(label, count) {
      var head = document.createElement("h3");
      head.className = "catalog-group-head";
      head.textContent = label;
      var countEl = document.createElement("span");
      countEl.className = "catalog-group-head__count";
      countEl.textContent = ui.groupCount(count);
      head.appendChild(countEl);
      return head;
    }

    function usesPagination() {
      return viewMode === "table" && !groupCol;
    }

    function updateViewUi() {
      if (catalog) {
        catalog.setAttribute("data-catalog-view", viewMode);
        if (groupCol) catalog.setAttribute("data-catalog-group", groupCol);
        else catalog.removeAttribute("data-catalog-group");
      }
      var cardsActive = viewMode === "cards";
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
      if (rowsPerPageControl) {
        rowsPerPageControl.hidden = !usesPagination();
      }
    }

    function updateSortUi() {
      if (sortBy && sortBy.value !== sortCol) sortBy.value = sortCol;
      var ascending = sortDir === 1;
      if (sortAscBtn) {
        sortAscBtn.classList.toggle("is-active", ascending);
        sortAscBtn.setAttribute("aria-pressed", ascending ? "true" : "false");
      }
      if (sortDescBtn) {
        sortDescBtn.classList.toggle("is-active", !ascending);
        sortDescBtn.setAttribute("aria-pressed", ascending ? "false" : "true");
      }
      document.querySelectorAll("th[data-col]").forEach(function (th) {
        var col = th.getAttribute("data-col");
        var active = col === sortCol;
        th.classList.toggle("asc", active && sortDir === 1);
        th.classList.toggle("desc", active && sortDir === -1);
        th.setAttribute(
          "aria-sort",
          active ? (sortDir === 1 ? "ascending" : "descending") : "none"
        );
      });
    }

    function updateGroupUi() {
      if (groupBy && groupBy.value !== groupCol) groupBy.value = groupCol;
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
          render();
          window.scrollTo({ top: 0, behavior: "smooth" });
        });
      });
    }

    function renderCards(rows) {
      if (!grid) return;
      grid.innerHTML = "";
      if (!rows.length) return;
      if (groupCol) {
        buildGroups(rows).forEach(function (group) {
          grid.appendChild(createCardGroupHead(group.label, group.rows.length));
          group.rows.forEach(function (row) {
            grid.appendChild(renderCard(row));
          });
        });
      } else {
        rows.forEach(function (row) {
          grid.appendChild(renderCard(row));
        });
      }
    }

    function renderTable(rows) {
      if (pagination && (groupCol || viewMode === "cards")) {
        pagination.innerHTML = "";
      }
      var html = "";
      var idx = 0;
      if (groupCol) {
        buildGroups(rows).forEach(function (group) {
          html += groupRowHTML(group.label, group.rows.length);
          group.rows.forEach(function (row) {
            idx += 1;
            html += rowHTML(row, idx);
          });
        });
      } else if (usesPagination()) {
        perPage = parseInt(perPageSel.value, 10) || 50;
        var pages = perPage >= 999999 ? 1 : Math.ceil(rows.length / perPage);
        if (page > pages) page = Math.max(1, pages);
        var start = (page - 1) * perPage;
        var slice = rows.slice(start, start + perPage);
        slice.forEach(function (row, i) {
          html += rowHTML(row, start + i + 1);
        });
        renderPagination(pages);
      } else {
        rows.forEach(function (row, i) {
          html += rowHTML(row, i + 1);
        });
        if (pagination) pagination.innerHTML = "";
      }
      tableBody.innerHTML = html;
    }

    function render() {
      var total = filtered.length;
      if (resultCount) resultCount.innerHTML = ui.result(total, DATA.length);

      if (!total) {
        tableBody.innerHTML = "";
        if (grid) grid.innerHTML = "";
        if (noResults) noResults.style.display = "block";
        if (pagination) pagination.innerHTML = "";
        if (window.DAABScientistsListPreview) window.DAABScientistsListPreview.refresh();
        return;
      }

      if (noResults) noResults.style.display = "none";
      var rows = sortRows(filtered.slice());

      if (viewMode === "cards") {
        renderCards(rows);
        tableBody.innerHTML = "";
        if (pagination) pagination.innerHTML = "";
      } else {
        renderTable(rows);
        if (grid) grid.innerHTML = "";
      }

      if (window.DAABScientistsListPreview) window.DAABScientistsListPreview.refresh();
    }

    function applyFilters() {
      var q = searchInput.value.trim().toLowerCase();
      var countries = getMultiFilter("filterCountry");
      var degrees = getMultiFilter("filterDegree");
      var fieldsFilter = getMultiFilter("filterIxtilas");
      var genders = getMultiFilter("filterCins");
      var matchFn = ms ? ms.matches.bind(ms) : function (selected, value) {
        if (selected === null) return true;
        if (!selected.length) return false;
        return selected.indexOf((value == null ? "" : String(value)).trim()) !== -1;
      };
      filtered = DATA.filter(function (r) {
        if (!matchFn(countries, r.yasadigi_olke)) return false;
        if (!matchFn(degrees, (r.elmi_derece || "").trim())) return false;
        if (!matchFn(fieldsFilter, (r.ixtilas || "").trim())) return false;
        if (!matchFn(genders, (r.cinsi || "").trim())) return false;
        if (q) {
          var hay = [r.ad_soyad, r.cinsi, r.yasadigi_olke, r.ixtilas, r.elmi_derece, r.email]
            .join(" ")
            .toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });
      page = 1;
      render();
    }

    function applySortState(nextCol, nextDir, persist) {
      sortCol = SORT_COLUMNS.indexOf(nextCol) >= 0 ? nextCol : "ad_soyad";
      sortDir = nextDir === -1 ? -1 : 1;
      if (persist !== false) saveSortState(sortCol, sortDir);
      updateSortUi();
      render();
    }

    function applyGroupState(nextCol, persist) {
      groupCol = GROUP_COLUMNS.indexOf(nextCol) >= 0 ? nextCol : "";
      if (persist !== false) saveGroupState(groupCol);
      updateGroupUi();
      updateViewUi();
      page = 1;
      render();
    }

    function setViewMode(mode) {
      viewMode = mode === "cards" ? "cards" : "table";
      saveViewState(viewMode);
      updateViewUi();
      page = 1;
      render();
    }

    function updateFilterStyles() {
      filterIds.forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        var wrap = el.closest(".sel-wrap");
        if (!wrap) return;
        var active = ms ? ms.isActive(id) : el.value !== "";
        wrap.classList.toggle("active", active);
      });
    }

    if (sortBy) {
      var sortLabel = document.querySelector(".sort-control__label");
      if (sortLabel) sortLabel.textContent = ui.sortLabel;
      Array.prototype.forEach.call(sortBy.options, function (opt) {
        if (opt.value === "ad_soyad") opt.textContent = ui.sortName;
        if (opt.value === "yasadigi_olke") opt.textContent = ui.sortCountry;
        if (opt.value === "ixtilas") opt.textContent = ui.sortField;
        if (opt.value === "elmi_derece") opt.textContent = ui.sortDegree;
        if (opt.value === "cinsi") opt.textContent = ui.sortGender;
      });
    }
    if (groupBy) {
      var groupLabel = document.querySelector(".group-control__label");
      if (groupLabel) groupLabel.textContent = ui.groupLabel;
      var viewLabel = document.querySelector(".catalog-view-control__label");
      if (viewLabel) viewLabel.textContent = ui.viewLabel;
      Array.prototype.forEach.call(groupBy.options, function (opt) {
        if (opt.value === "") opt.textContent = ui.groupNone;
        if (opt.value === "yasadigi_olke") opt.textContent = ui.groupCountry;
        if (opt.value === "ixtilas") opt.textContent = ui.groupField;
        if (opt.value === "elmi_derece") opt.textContent = ui.groupDegree;
        if (opt.value === "cinsi") opt.textContent = ui.groupGender;
      });
    }

    document.querySelectorAll("th[data-col]").forEach(function (th) {
      th.addEventListener("click", function () {
        var col = th.getAttribute("data-col");
        if (!col) return;
        var nextDir = sortCol === col ? sortDir * -1 : 1;
        applySortState(col, nextDir, true);
      });
    });

    searchInput.addEventListener("input", function () {
      applyFilters();
      updateFilterStyles();
    });

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
        updateFilterStyles();
        applyFilters();
      });
    });

    ["filterCountry", "filterIxtilas", "filterDegree", "filterCins"].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("change", function () {
        applyFilters();
        updateFilterStyles();
      });
    });

    if (perPageSel) {
      perPageSel.addEventListener("change", function () {
        page = 1;
        render();
      });
    }

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
        applySortState(sortCol, 1, true);
      });
    }
    if (sortDescBtn) {
      sortDescBtn.addEventListener("click", function () {
        applySortState(sortCol, -1, true);
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

    if (clearFilters) {
      clearFilters.addEventListener("click", function () {
        searchInput.value = "";
        if (ms) {
          ms.clearAll(filterIds);
        } else {
          filterIds.forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.value = "";
          });
        }
        updateFilterStyles();
        applySortState("ad_soyad", 1, true);
        applyGroupState("", true);
        setViewMode("table");
        filtered = DATA.slice();
        page = 1;
        applyFilters();
      });
    }

    applySortState(sortCol, sortDir, false);
    applyGroupState(groupCol, false);
    setViewMode(viewMode);
    updateFilterStyles();
    applyFilters();

    if (
      window.DAAB_TABLE_RESIZE &&
      typeof window.DAAB_TABLE_RESIZE.initTable === "function"
    ) {
      var table = document.querySelector(".scientists-table-wrap table");
      if (table) window.DAAB_TABLE_RESIZE.initTable(table);
    }

    if (window.DAABScientistsListPreview && window.DAABScientistsListPreview.whenReady) {
      window.DAABScientistsListPreview.whenReady(function () {
        render();
        window.DAABScientistsListPreview.refresh();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
