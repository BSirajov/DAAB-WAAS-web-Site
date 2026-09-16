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
    var AZ = {
      "\u0259": "e", "\u0131": "i", "\u00f6": "o", "\u00fc": "u",
      "\u011f": "g", "\u015f": "s", "\u00e7": "c",
      "\u018f": "e", "\u0130": "i", "\u00d6": "o", "\u00dc": "u",
      "\u011e": "g", "\u015e": "s", "\u00c7": "c"
    };
    return String(q || "")
      .replace(/[^\u0000-\u007f]/g, function (ch) { return AZ[ch] || ch; })
      .toLowerCase()
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  window.DAAB_SCIENTISTS_CATALOG = {
    pageLang: pageLang,
    compare: compare,
    sortValues: sortValues,
    esc: esc,
    normQuery: normQuery,
  };
})();
