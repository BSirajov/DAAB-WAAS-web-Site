/**
 * Mouse / keyboard resizable columns for fixed-layout catalogue tables.
 * Persists widths in localStorage (per page + column). Disabled on coarse pointers.
 */
(function (window, document) {
  "use strict";

  var STORAGE_PREFIX = "daab-table-col-width:";

  var COL_LIMITS = {
    "col-no": { min: 44, max: 88, default: 54 },
    "col-name": { min: 110, max: 480, default: 246 },
    "col-cntry": { min: 90, max: 320, default: 180 },
    "col-spec": { min: 110, max: 420, default: 246 },
    "col-degree": { min: 72, max: 220, default: 130 },
    "col-email": { min: 140, max: 520, default: 300 },
    "col-cins": { min: 0, max: 120, default: 0 },
    "col-dates": { min: 88, max: 180, default: 112 },
    "col-category": { min: 100, max: 280, default: 168 },
    "col-period": { min: 88, max: 200, default: 128 },
    "col-field": { min: 100, max: 360, default: 176 },
    "col-country": { min: 88, max: 220, default: 128 },
    "col-profile": { min: 72, max: 160, default: 96 },
  };

  function colKeyFromTh(th) {
    var list = (th.className || "").split(/\s+/);
    for (var i = 0; i < list.length; i++) {
      if (list[i].indexOf("col-") === 0) return list[i];
    }
    return null;
  }

  function isVisibleTh(th) {
    if (th.getAttribute("aria-hidden") === "true") return false;
    return window.getComputedStyle(th).display !== "none";
  }

  function storageKey(pageId, colKey) {
    return STORAGE_PREFIX + pageId + ":" + colKey;
  }

  function loadWidth(pageId, colKey) {
    try {
      var key = storageKey(pageId, colKey);
      var raw = localStorage.getItem(key);
      if (raw == null) {
        raw = sessionStorage.getItem(key);
        if (raw != null) {
          localStorage.setItem(key, raw);
          sessionStorage.removeItem(key);
        }
      }
      if (raw == null) return null;
      var n = parseInt(raw, 10);
      return isFinite(n) ? n : null;
    } catch (e) {
      return null;
    }
  }

  function saveWidth(pageId, colKey, px) {
    try {
      localStorage.setItem(storageKey(pageId, colKey), String(Math.round(px)));
    } catch (e) { /* ignore */ }
  }

  function clearWidth(pageId, colKey) {
    try {
      localStorage.removeItem(storageKey(pageId, colKey));
    } catch (e) { /* ignore */ }
  }

  function clampWidth(colKey, px) {
    var lim = COL_LIMITS[colKey] || { min: 60, max: 480, default: 120 };
    return Math.min(lim.max, Math.max(lim.min, px));
  }

  function defaultWidth(th, colKey) {
    var lim = COL_LIMITS[colKey];
    if (lim && lim.default) return lim.default;
    return th.offsetWidth || 120;
  }

  function resolveWidth(pageId, th, colKey) {
    var saved = loadWidth(pageId, colKey);
    if (saved != null) return clampWidth(colKey, saved);
    var measured = th.offsetWidth;
    if (measured > 0) return clampWidth(colKey, measured);
    return clampWidth(colKey, defaultWidth(th, colKey));
  }

  function sumColWidths(table) {
    var cols = table.querySelectorAll("colgroup col");
    var total = 0;
    for (var i = 0; i < cols.length; i++) {
      var w = parseFloat(cols[i].style.width);
      if (isFinite(w)) total += w;
    }
    return total;
  }

  function syncTableMinWidth(table) {
    var total = sumColWidths(table);
    if (total > 0) table.style.minWidth = total + "px";
  }

  function initTable(table) {
    if (!table || table.getAttribute("data-daab-resize-init") === "1") return;
    if (window.matchMedia("(pointer: coarse)").matches) return;

    var theadRow = table.querySelector("thead tr");
    if (!theadRow) return;

    var pageId =
      table.getAttribute("data-daab-resize-id") ||
      document.documentElement.getAttribute("data-daab-page-id") ||
      "table";

    var lang = (document.documentElement.lang || "en").slice(0, 2);
    var resizeLabel = lang === "az" ? "Sütun enini dəyiş" : "Resize column";

    var ths = Array.prototype.slice.call(theadRow.children);
    var visibleThs = ths.filter(isVisibleTh);

    var colgroup = table.querySelector("colgroup");
    if (!colgroup) {
      colgroup = document.createElement("colgroup");
      table.insertBefore(colgroup, table.firstChild);
    }
    colgroup.innerHTML = "";

    ths.forEach(function (th) {
      var key = colKeyFromTh(th);
      var col = document.createElement("col");
      if (key) col.setAttribute("data-col", key);

      if (!isVisibleTh(th)) {
        col.style.width = "0px";
      } else if (key) {
        col.style.width = resolveWidth(pageId, th, key) + "px";
      }
      colgroup.appendChild(col);
    });

    visibleThs.forEach(function (th, index) {
      if (index === visibleThs.length - 1) return;
      if (th.querySelector(".daab-col-resize-handle")) return;

      var handle = document.createElement("button");
      handle.type = "button";
      handle.className = "daab-col-resize-handle";
      handle.setAttribute("role", "separator");
      handle.setAttribute("aria-orientation", "vertical");
      handle.setAttribute("tabindex", "0");
      handle.setAttribute("aria-label", resizeLabel);

      handle.addEventListener("mousedown", function (ev) {
        startDrag(ev, table, th, pageId);
      });
      handle.addEventListener("dblclick", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        resetColumn(table, th, pageId);
      });
      handle.addEventListener("keydown", function (ev) {
        onHandleKey(ev, table, th, pageId);
      });
      handle.addEventListener("click", function (ev) {
        ev.stopPropagation();
      });

      th.appendChild(handle);
    });

    table.classList.add("daab-resizable-table", "daab-cols-ready");
    table.setAttribute("data-daab-resize-init", "1");
    syncTableMinWidth(table);
  }

  function colElement(table, colKey) {
    return table.querySelector('colgroup col[data-col="' + colKey + '"]');
  }

  function setColumnWidth(table, th, pageId, colKey, px, persist) {
    var col = colElement(table, colKey);
    if (!col) return;
    var w = clampWidth(colKey, px);
    col.style.width = w + "px";
    syncTableMinWidth(table);
    if (persist) saveWidth(pageId, colKey, w);
  }

  function resetColumn(table, th, pageId) {
    var colKey = colKeyFromTh(th);
    if (!colKey) return;
    clearWidth(pageId, colKey);
    setColumnWidth(table, th, pageId, colKey, defaultWidth(th, colKey), false);
  }

  function startDrag(ev, table, th, pageId) {
    if (ev.button !== 0) return;
    ev.preventDefault();
    ev.stopPropagation();

    var colKey = colKeyFromTh(th);
    if (!colKey) return;

    var col = colElement(table, colKey);
    if (!col) return;

    var startX = ev.clientX;
    var startW = parseFloat(col.style.width) || th.offsetWidth;

    document.documentElement.classList.add("daab-col-resizing");

    function onMove(e) {
      var dx = e.clientX - startX;
      setColumnWidth(table, th, pageId, colKey, startW + dx, false);
    }

    function onUp(e) {
      document.documentElement.classList.remove("daab-col-resizing");
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
      var dx = e.clientX - startX;
      setColumnWidth(table, th, pageId, colKey, startW + dx, true);
    }

    document.addEventListener("mousemove", onMove);
    document.addEventListener("mouseup", onUp);
  }

  function onHandleKey(ev, table, th, pageId) {
    var colKey = colKeyFromTh(th);
    if (!colKey) return;
    var col = colElement(table, colKey);
    if (!col) return;

    var step = ev.shiftKey ? 24 : 8;
    var current = parseFloat(col.style.width) || th.offsetWidth;
    var next = current;

    if (ev.key === "ArrowRight") next = current + step;
    else if (ev.key === "ArrowLeft") next = current - step;
    else if (ev.key === "Home") next = (COL_LIMITS[colKey] || {}).min || 60;
    else if (ev.key === "End") next = (COL_LIMITS[colKey] || {}).max || 480;
    else return;

    ev.preventDefault();
    setColumnWidth(table, th, pageId, colKey, next, true);
  }

  function initAll(root) {
    var scope = root || document;
    var tables = scope.querySelectorAll(
      "table[data-daab-resizable-table], [data-daab-page-id=\"scientists-list\"] .table-scroll > table, [data-daab-page-id=\"encyclopedia\"] .encyclopedia-table[data-daab-resizable-table]"
    );
    for (var i = 0; i < tables.length; i++) {
      initTable(tables[i]);
    }
  }

  function boot() {
    initAll(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.DAAB_TABLE_RESIZE = {
    init: initAll,
    initTable: initTable,
  };
})(window, document);
