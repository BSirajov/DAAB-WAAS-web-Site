/**
 * Locale-aware list sorting for DAAB pages.
 * AZ pages (data-daab-lang="az" / lang="az"): Azerbaijani alphabet order.
 * EN pages: Latin order via localeCompare('en').
 */
(function () {
  "use strict";

  var AZ_ALPHA =
    "AaBbCcÇçDdEeƏəFfGgĞğHhXxIıİiJjKkQqLlMmNnOoÖöPpRrSsŞşTtUuÜüVvYyZz";
  var AZ_ORDER = {};
  AZ_ALPHA.split("").forEach(function (ch, i) {
    AZ_ORDER[ch] = i;
  });

  function pageLang() {
    var root = document.documentElement;
    var lang = (
      root.getAttribute("data-daab-lang") ||
      root.getAttribute("lang") ||
      "az"
    ).toLowerCase();
    return lang.indexOf("en") === 0 ? "en" : "az";
  }

  function azCompare(a, b) {
    var as = String(a || "");
    var bs = String(b || "");
    var len = Math.max(as.length, bs.length);
    var i;
    for (i = 0; i < len; i++) {
      if (i >= as.length) return -1;
      if (i >= bs.length) return 1;
      var ai = AZ_ORDER[as[i]] != null ? AZ_ORDER[as[i]] : 999;
      var bi = AZ_ORDER[bs[i]] != null ? AZ_ORDER[bs[i]] : 999;
      if (ai !== bi) return ai - bi;
    }
    return 0;
  }

  function azSort(arr) {
    return arr.slice().sort(function (a, b) {
      return azCompare(a, b);
    });
  }

  function latinCompare(a, b) {
    return String(a || "").localeCompare(String(b || ""), "en", {
      sensitivity: "base",
    });
  }

  function latinSort(arr) {
    return arr.slice().sort(function (a, b) {
      return latinCompare(a, b);
    });
  }

  function compare(a, b) {
    return pageLang() === "en" ? latinCompare(a, b) : azCompare(a, b);
  }

  function sort(arr) {
    return pageLang() === "en" ? latinSort(arr) : azSort(arr);
  }

  window.DAAB_COLLATION = {
    pageLang: pageLang,
    azCompare: azCompare,
    azSort: azSort,
    latinCompare: latinCompare,
    latinSort: latinSort,
    compare: compare,
    sort: sort,
  };
})();
