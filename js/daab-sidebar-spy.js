/**
 * Shared sidebar scroll-spy for .timeline-list anchor navigation.
 */
(function (window) {
  "use strict";

  function defaultActivate(links, activeLink) {
    links.forEach(function (link) {
      link.classList.remove("tl-active");
    });
    if (activeLink) activeLink.classList.add("tl-active");
  }

  function scrollSpyFromLinks(links, options) {
    var opts = options || {};
    var onActivate = opts.onActivate || defaultActivate.bind(null, links);
    var scrollFraction = typeof opts.scrollFraction === "number" ? opts.scrollFraction : 0.35;

    var ids = links
      .map(function (link) {
        return link.getAttribute("href").slice(1);
      })
      .filter(Boolean);
    var cards = ids
      .map(function (id) {
        return document.getElementById(id);
      })
      .filter(Boolean);

    function updateActive() {
      var mid = window.scrollY + window.innerHeight * scrollFraction;
      var activeIndex = -1;
      for (var i = cards.length - 1; i >= 0; i--) {
        if (cards[i] && cards[i].offsetTop <= mid) {
          activeIndex = i;
          break;
        }
      }
      onActivate(activeIndex >= 0 ? links[activeIndex] : null);
    }

    function scrollToId(id, behavior) {
      var target = document.getElementById(id);
      if (!target) return;
      var Pos = window.DAAB_LANG_POSITION;
      if (Pos && Pos.scrollToAnchor) {
        Pos.scrollToAnchor(id, false);
        return;
      }
      target.scrollIntoView({ block: "start", behavior: behavior || "auto" });
    }

    return {
      cards: cards,
      updateActive: updateActive,
      scrollToId: scrollToId,
      bind: function () {
        window.addEventListener("scroll", updateActive, { passive: true });
        updateActive();
      },
    };
  }

  window.DAAB_SIDEBAR_SPY = {
    fromTimelineLinks: scrollSpyFromLinks,
  };
})(window);
