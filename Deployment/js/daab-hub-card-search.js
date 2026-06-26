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

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var visible = 0;

      cards.forEach(function (card) {
        var hay = ((card.dataset.title || "") + " " + card.innerText).toLowerCase();
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
