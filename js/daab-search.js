/**
 * Site-wide search overlay — URL-aware for legacy, /az/, and /en/ trees.
 */
(function () {
  "use strict";

  function detectContext() {
    var path = location.pathname.replace(/\\/g, "/");
    if (/\/az\/scientists\//.test(path)) return "az-scientists";
    if (/\/az\//.test(path)) return "az";
    if (/\/en\/scientists\//.test(path)) return "en-scientists";
    if (/\/en\//.test(path)) return "en";
    return "legacy";
  }

  function urls(ctx) {
    if (ctx === "az-scientists") {
      return {
        home: "../index.html",
        mission: "../mission.html",
        activities: "../activities.html",
        foundation: "../foundation.html",
        scientists: "list.html",
        board: "../executive-board.html",
        charter: "../charter.html",
        membership: "../membership.html"
      };
    }
    if (ctx === "az") {
      return {
        home: "index.html",
        mission: "mission.html",
        activities: "activities.html",
        foundation: "foundation.html",
        scientists: "scientists/list.html",
        board: "executive-board.html",
        charter: "charter.html",
        membership: "membership.html"
      };
    }
    if (ctx === "en-scientists") {
      return {
        home: "../index.html",
        mission: "../mission.html",
        activities: "../activities.html",
        foundation: "../foundation.html",
        scientists: "list.html",
        board: "../executive-board.html",
        charter: "../charter.html",
        membership: "../membership.html"
      };
    }
    if (ctx === "en") {
      return {
        home: "index.html",
        mission: "mission.html",
        activities: "activities.html",
        foundation: "foundation.html",
        scientists: "scientists/list.html",
        board: "executive-board.html",
        charter: "charter.html",
        membership: "membership.html"
      };
    }
    return {
      home: "index.html",
      mission: "mission_vision_values_az.html",
      activities: "activities_az.html",
      foundation: "foundation_az.html",
      scientists: "scientists_list_view_az.html",
      board: "executive_board_az.html",
      charter: "charter_az.html",
      membership: "membership_terms_az.html"
    };
  }

  function buildPages(ctx) {
    var u = urls(ctx);
    if (ctx === "en" || ctx === "en-scientists") {
      return [
        { title: "Home", desc: "WAAS website main entry", icon: "🏠", tag: "Main", url: u.home, kw: ["home", "daab", "index"] },
        { title: "Mission, Vision & Values", desc: "Strategic direction and values", icon: "💎", tag: "About", url: u.mission, kw: ["mission", "vision", "values"] },
        { title: "Activities", desc: "Events and initiatives", icon: "📰", tag: "Activities", url: u.activities, kw: ["activities", "events", "conference"] },
        { title: "Foundation", desc: "Establishment of the association", icon: "🏛️", tag: "Foundation", url: u.foundation, kw: ["foundation", "founding", "istanbul"] },
        { title: "Scientists", desc: "Directory of Azerbaijani scientists", icon: "🌐", tag: "Catalogue", url: u.scientists, kw: ["scientists", "scholars", "directory"] },
        { title: "Executive Board", desc: "Leadership and governance", icon: "🎓", tag: "Governance", url: u.board, kw: ["board", "executive", "leadership"] },
        { title: "Charter", desc: "Governing documents", icon: "📜", tag: "Charter", url: u.charter, kw: ["charter", "statute", "rules"] },
        { title: "Membership", desc: "How to join WAAS", icon: "✒️", tag: "Membership", url: u.membership, kw: ["membership", "application"] }
      ];
    }
    return [
      { title: "Ana Səhifə", desc: "DAAB website main entry page", icon: "🏠", tag: "Main", url: u.home, kw: ["home", "daab", "index", "ana səhifə"] },
      { title: "Missiya, Vizyon və Dəyərlər", desc: "Strategic direction, purpose and institutional values", icon: "💎", tag: "About", url: u.mission, kw: ["mission", "vision", "values", "missiya", "vizyon", "dəyərlər"] },
      { title: "Fəaliyyətimiz", desc: "Scientific, academic and cultural events chronicle", icon: "📰", tag: "Activities", url: u.activities, kw: ["activities", "events", "fəaliyyət", "tədbirlər"] },
      { title: "Birliyin Təsisi", desc: "Təsis zərurəti və İstanbul təsis görüşü", icon: "🏛️", tag: "Foundation", url: u.foundation, kw: ["founding", "təsis", "istanbul"] },
      { title: "Alimlərimiz", desc: "Catalogue of Azerbaijani scientists worldwide", icon: "🌐", tag: "Catalogue", url: u.scientists, kw: ["scientists", "alimlər", "kataloq"] },
      { title: "İdarə Heyəti", desc: "Leadership board and contact", icon: "🎓", tag: "Governance", url: u.board, kw: ["board", "idarə", "rəhbərlik"] },
      { title: "Nizamnamə", desc: "Official DAAB charter in Azerbaijani", icon: "📜", tag: "Charter", url: u.charter, kw: ["charter", "nizamnamə"] },
      { title: "Üzvlük Şərtləri", desc: "Requirements and application procedure", icon: "✒️", tag: "Membership", url: u.membership, kw: ["membership", "üzvlük", "müraciət"] }
    ];
  }

  function init() {
    var ov = document.getElementById("search-overlay");
    var inp = document.getElementById("search-input");
    var res = document.getElementById("search-results");
    var nb = document.getElementById("nav-search-btn");
    var cb = document.getElementById("search-close-btn");
    if (!ov || !inp || !res) return;

    var PAGES = buildPages(detectContext());
    var fi = -1;

    function openSearch() {
      ov.classList.add("open");
      inp.value = "";
      fi = -1;
      res.innerHTML = '<div class="search-prompt">Axtarmaq üçün yuxarıdakı xanaya mətn daxil edin</div>';
      setTimeout(function () { inp.focus(); }, 50);
      document.body.classList.add("daab-scroll-lock");
    }

    function closeSearch() {
      ov.classList.remove("open");
      inp.value = "";
      fi = -1;
      document.body.classList.remove("daab-scroll-lock");
    }

    function score(p, q) {
      var ql = q.toLowerCase();
      var corpus = [p.title, p.desc, p.tag].concat(p.kw).join(" ").toLowerCase();
      if (corpus.indexOf(ql) !== -1) return 10;
      var words = ql.split(/\s+/).filter(Boolean);
      var s = 0;
      words.forEach(function (w) {
        if (corpus.indexOf(w) !== -1) s += 2;
        else if (corpus.split(/\s+/).some(function (cw) { return cw.indexOf(w) === 0; })) s += 1;
      });
      return s;
    }

    function updateFocus() {
      var items = res.querySelectorAll(".search-result-item");
      items.forEach(function (el, i) {
        el.classList.toggle("focused", i === fi);
        if (i === fi) el.scrollIntoView({ block: "nearest" });
      });
    }

    function renderResults(pages) {
      fi = -1;
      if (!pages.length) {
        res.innerHTML = '<div class="search-empty">Nəticə tapılmadı. Başqa söz cəhd edin.</div>';
        return;
      }
      res.innerHTML = pages.map(function (p) {
        return '<a class="search-result-item" href="' + p.url + '"><div class="sri-icon">' + p.icon +
          '</div><div class="sri-body"><div class="sri-title">' + p.title + '</div><div class="sri-desc">' + p.desc +
          '</div></div><span class="sri-tag">' + p.tag + "</span></a>";
      }).join("");
      updateFocus();
    }

    inp.addEventListener("input", function () {
      var q = inp.value.trim();
      if (!q) {
        res.innerHTML = '<div class="search-prompt">Axtarmaq üçün yuxarıdakı xanaya mətn daxil edin</div>';
        fi = -1;
        return;
      }
      renderResults(
        PAGES.map(function (p) { return { p: p, s: score(p, q) }; })
          .filter(function (x) { return x.s > 0; })
          .sort(function (a, b) { return b.s - a.s; })
          .map(function (x) { return x.p; })
      );
    });

    inp.addEventListener("keydown", function (e) {
      var items = res.querySelectorAll(".search-result-item");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        fi = Math.min(fi + 1, items.length - 1);
        updateFocus();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        fi = Math.max(fi - 1, 0);
        updateFocus();
      } else if (e.key === "Enter" && fi >= 0 && items[fi]) {
        items[fi].click();
      } else if (e.key === "Escape") {
        closeSearch();
      }
    });

    if (nb) nb.addEventListener("click", openSearch);
    if (cb) cb.addEventListener("click", closeSearch);
    ov.addEventListener("click", function (e) { if (e.target === ov) closeSearch(); });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        ov.classList.contains("open") ? closeSearch() : openSearch();
      }
      if (e.key === "Escape" && ov.classList.contains("open")) closeSearch();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
