/**
 * Sitemap page: filter, chip jump, search/cookie actions, suggest chips.
 */
(function () {
  "use strict";

  function normalize(text) {
    return String(text || "")
      .toLocaleLowerCase("az")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/ə/g, "e")
      .replace(/ı/g, "i")
      .replace(/ö/g, "o")
      .replace(/ü/g, "u")
      .replace(/ğ/g, "g")
      .replace(/ş/g, "s")
      .replace(/ç/g, "c")
      .trim();
  }

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function cssPx(name, fallback) {
    var raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    var n = parseFloat(raw);
    return Number.isFinite(n) ? n : fallback;
  }

  function chromeOffset() {
    var stack = cssPx("--daab-sticky-top-stack", 0);
    if (stack > 0) return stack;
    return cssPx("--daab-nav-height", 72) + cssPx("--daab-breadcrumbs-height", 0);
  }

  ready(function () {
    var root = document.documentElement;
    if (root.getAttribute("data-daab-page-id") !== "sitemap") return;

    var input = document.getElementById("sitemap-filter");
    var clearBtn = document.getElementById("sitemap-filter-clear");
    var countEl = document.getElementById("sitemap-count");
    var emptyEl = document.getElementById("sitemap-empty");
    var chips = Array.prototype.slice.call(document.querySelectorAll(".sitemap-chip"));
    var sections = Array.prototype.slice.call(document.querySelectorAll(".sitemap-section"));
    var startBlock = document.querySelector(".sitemap-start");
    var links = Array.prototype.slice.call(
      document.querySelectorAll(".sitemap-section .sitemap-link, .sitemap-start .sitemap-link")
    );
    if (!input) return;

    var totalLabel = countEl ? countEl.getAttribute("data-label-template") || "{n}" : "{n}";
    var totalPages = links.length;

    function setCount(visible) {
      if (!countEl) return;
      countEl.textContent = totalLabel.replace("{n}", String(visible)).replace("{t}", String(totalPages));
    }

    function applyFilter() {
      var q = normalize(input.value);
      var visibleLinks = 0;

      links.forEach(function (link) {
        var hay = link.getAttribute("data-search") || normalize(link.textContent);
        var match = !q || hay.indexOf(q) !== -1;
        var item = link.closest("li");
        link.hidden = !match;
        if (item) item.hidden = !match;
        if (match) visibleLinks += 1;
      });

      sections.forEach(function (section) {
        var visibleInSection = section.querySelectorAll(".sitemap-grid > li:not([hidden])").length;
        var cta = section.querySelector(".sitemap-cta");
        var ctaMatch = true;
        if (cta && q) {
          var ctaHay = cta.getAttribute("data-search") || normalize(cta.textContent);
          ctaMatch = ctaHay.indexOf(q) !== -1;
          cta.hidden = !ctaMatch;
          if (ctaMatch) visibleLinks += 1;
        } else if (cta) {
          cta.hidden = false;
        }
        section.hidden = visibleInSection === 0 && !(cta && ctaMatch && !cta.hidden);
        var meta = section.querySelector(".sitemap-section__meta");
        if (meta) {
          var tpl = meta.getAttribute("data-count-template") || "{n}";
          meta.textContent = tpl.replace("{n}", String(visibleInSection));
        }
      });

      if (startBlock) {
        var startVisible = startBlock.querySelectorAll(".sitemap-grid > li:not([hidden])").length;
        startBlock.hidden = startVisible === 0 && !!q;
      }

      if (clearBtn) clearBtn.hidden = !q;
      if (emptyEl) emptyEl.classList.toggle("is-visible", visibleLinks === 0);
      setCount(visibleLinks);
    }

    function syncActiveChip(hashId) {
      var hash = (hashId || location.hash || "").replace(/^#/, "");
      chips.forEach(function (chip) {
        var target = (chip.getAttribute("href") || "").replace(/^#/, "");
        var active = !!hash && target === hash;
        chip.classList.toggle("is-active", active);
        if (active) chip.setAttribute("aria-current", "true");
        else chip.removeAttribute("aria-current");
      });
      sections.forEach(function (section) {
        section.classList.toggle("is-target", !!hash && section.id === hash);
      });
    }

    function jumpToSection(id) {
      var section = document.getElementById(id);
      if (!section || section.hidden) return;
      var head = section.querySelector(".sitemap-section__head") || section;
      var top = head.getBoundingClientRect().top + window.pageYOffset - chromeOffset();
      window.scrollTo(0, Math.max(0, Math.round(top)));
    }

    function goToSection(id) {
      if (!id) return;
      if (history.replaceState) history.replaceState(null, "", "#" + id);
      else location.hash = id;
      syncActiveChip(id);
      window.requestAnimationFrame(function () {
        jumpToSection(id);
        window.requestAnimationFrame(function () {
          jumpToSection(id);
        });
      });
    }

    function openSiteSearch() {
      if (window.DAAB_SEARCH && typeof window.DAAB_SEARCH.open === "function") {
        window.DAAB_SEARCH.open();
        return;
      }
      var btn =
        document.getElementById("nav-search-btn") ||
        document.getElementById("gateway-search-btn");
      if (btn) btn.click();
    }

    function openCookieSettings() {
      if (window.DAAB_COOKIE && typeof window.DAAB_COOKIE.openSettings === "function") {
        window.DAAB_COOKIE.openSettings();
      }
    }

    input.addEventListener("input", applyFilter);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && input.value) {
        input.value = "";
        applyFilter();
      }
    });

    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        input.value = "";
        input.focus();
        applyFilter();
      });
    }

    document.querySelectorAll(".sitemap-suggest").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var term = btn.getAttribute("data-suggest") || btn.textContent || "";
        input.value = term;
        applyFilter();
        input.focus();
      });
    });

    var openSearchBtn = document.getElementById("sitemap-open-search");
    if (openSearchBtn) {
      openSearchBtn.addEventListener("click", function (e) {
        e.preventDefault();
        openSiteSearch();
      });
    }

    document.querySelectorAll("[data-sitemap-action]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        var action = el.getAttribute("data-sitemap-action");
        if (action === "search") {
          e.preventDefault();
          openSiteSearch();
        } else if (action === "cookies") {
          e.preventDefault();
          openCookieSettings();
        }
      });
    });

    chips.forEach(function (chip) {
      chip.addEventListener("click", function (e) {
        var href = chip.getAttribute("href") || "";
        if (href.charAt(0) !== "#") return;
        e.preventDefault();
        goToSection(href.slice(1));
      });
    });

    window.addEventListener("hashchange", function () {
      var id = (location.hash || "").replace(/^#/, "");
      if (id) goToSection(id);
      else syncActiveChip("");
    });

    applyFilter();

    if (window.DAAB_STICKY_CHROME && typeof window.DAAB_STICKY_CHROME.sync === "function") {
      window.DAAB_STICKY_CHROME.sync();
    }

    var initial = (location.hash || "").replace(/^#/, "");
    if (initial) {
      window.setTimeout(function () {
        goToSection(initial);
      }, 0);
    } else {
      syncActiveChip("");
    }
  });
})();
