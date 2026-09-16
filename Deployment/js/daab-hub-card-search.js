/**
 * Hub card filter for home and Forum 2024 index pages (#cardSearch).
 */
(function () {
  "use strict";

  function init() {
    var input = document.getElementById("cardSearch");
    if (!input) return;

    var cards = Array.prototype.slice.call(document.querySelectorAll(".page-card"));
    if (!cards.length) return;

    var emptyState = document.getElementById("cardSearchEmpty");
    var groups = document.querySelectorAll(".forum-hub-group, .forum-participants-panel");
    var isForumHub = groups.length > 0;
    var showDisplay = isForumHub ? "" : "flex";

    function fold(text) {
      var AZ = {
        "\u0259": "e", "\u0131": "i", "\u00f6": "o", "\u00fc": "u",
        "\u011f": "g", "\u015f": "s", "\u00e7": "c",
        "\u018f": "e", "\u0130": "i", "\u00d6": "o", "\u00dc": "u",
        "\u011e": "g", "\u015e": "s", "\u00c7": "c"
      };
      return String(text || "")
        .replace(/[^\u0000-\u007f]/g, function (ch) { return AZ[ch] || ch; })
        .toLowerCase()
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/\s+/g, " ")
        .trim();
    }

    input.addEventListener("input", function () {
      var q = fold(input.value);
      var visible = 0;

      cards.forEach(function (card) {
        var hay = fold((card.dataset.title || "") + " " + card.innerText);
        var match = !q || hay.indexOf(q) !== -1;
        card.style.display = match ? showDisplay : "none";
        if (match) visible += 1;
      });

      if (isForumHub) {
        groups.forEach(function (group) {
          var anyVisible = Array.prototype.some.call(
            group.querySelectorAll(".page-card"),
            function (card) {
              return card.style.display !== "none";
            }
          );
          group.hidden = !!q && !anyVisible;
        });
      }

      if (emptyState) {
        emptyState.hidden = !q || visible !== 0;
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
