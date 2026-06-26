/**
 * Shared sort/compare/escape helpers for scientists list + profiles catalog scripts.
 */
(function () {
  "use strict";

  function pageLang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function localeCollator() {
    var lang = pageLang();
    if (typeof Intl !== "undefined" && typeof Intl.Collator === "function") {
      return new Intl.Collator(lang === "en" ? "en" : "az", { sensitivity: "base" });
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
    return String(a || "").localeCompare(String(b || ""), undefined, {
      sensitivity: "base",
    });
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

  function normQuery(q) {
    return String(q || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  window.DAAB_SCIENTISTS_CATALOG = {
    pageLang: pageLang,
    compare: compare,
    sortValues: sortValues,
    esc: esc,
    normQuery: normQuery,
  };
})();
