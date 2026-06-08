/**
 * Scientist profile deep links — hash navigation for QR codes and external opens.
 * Works independently of filter/sort init; includes legacy fallback by photo slug.
 */
(function (window) {
  "use strict";

  var MAX_ATTEMPTS = 60;
  var pending = false;

  function normalizeSlug(slug) {
    return String(slug || "")
      .trim()
      .toLowerCase();
  }

  function hashId() {
    if (!location.hash) return "";
    var raw = "";
    try {
      raw = decodeURIComponent(location.hash.slice(1));
    } catch (e) {
      raw = location.hash.slice(1);
    }
    return normalizeSlug(raw);
  }

  function stickyTopOffset() {
    var root = document.documentElement;
    var style = window.getComputedStyle(root);
    var stack = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
    if (isFinite(stack) && stack > 0) {
      return Math.ceil(stack) + 12;
    }
    var navH = parseFloat(style.getPropertyValue("--daab-nav-height"));
    if (!isFinite(navH) || navH <= 0) {
      var nav = document.querySelector(".nav-strip");
      navH = nav ? nav.getBoundingClientRect().height : 86;
    }
    var crumbsH = parseFloat(style.getPropertyValue("--daab-breadcrumbs-height"));
    if (!isFinite(crumbsH) || crumbsH < 0) crumbsH = 0;
    return Math.ceil(navH + crumbsH) + 20;
  }

  function findCard(slug) {
    slug = normalizeSlug(slug);
    if (!slug) return null;
    var byId = document.getElementById(slug);
    if (byId && byId.classList.contains("card")) return byId;

    var imgs = document.querySelectorAll(".card-photo img, .card-avatar img");
    var i;
    var needle = "/" + slug + ".";
    for (i = 0; i < imgs.length; i++) {
      if (imgs[i].src && imgs[i].src.indexOf(needle) !== -1) {
        var card = imgs[i].closest(".card");
        if (card) {
          if (!card.id) card.id = slug;
          if (!card.hasAttribute("tabindex")) card.setAttribute("tabindex", "-1");
          return card;
        }
      }
    }
    return null;
  }

  function clearBlockingFilters() {
    var searchInput = document.getElementById("searchInput");
    var filterCountry = document.getElementById("filterCountry");
    var filterIxtilas = document.getElementById("filterIxtilas");
    var filterDegree = document.getElementById("filterDegree");
    if (searchInput) searchInput.value = "";
    if (filterCountry) filterCountry.value = "";
    if (filterIxtilas) filterIxtilas.value = "";
    if (filterDegree) filterDegree.value = "";
    document.querySelectorAll(".card.is-filtered-out").forEach(function (card) {
      card.classList.remove("is-filtered-out", "is-match", "is-excluded");
    });
    var noResults = document.getElementById("no-results");
    if (noResults) noResults.classList.remove("visible");
  }

  function markProfilesReady() {
    document.documentElement.classList.add("daab-profiles-ready");
    document.documentElement.classList.remove("daab-profiles-boot");
  }

  function instantScrollTo(card) {
    if (!card) return;
    var root = document.documentElement;
    var prevInline = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    var top =
      card.getBoundingClientRect().top + window.pageYOffset - stickyTopOffset();
    window.scrollTo({ top: Math.max(0, top), left: 0, behavior: "auto" });
    window.requestAnimationFrame(function () {
      root.style.scrollBehavior = prevInline;
    });
  }

  function spotlight(card) {
    if (!card) return;
    card.classList.remove("daab-profile-spotlight");
    void card.offsetWidth;
    card.classList.add("daab-profile-spotlight");
    card.addEventListener(
      "animationend",
      function onEnd() {
        card.classList.remove("daab-profile-spotlight");
        card.removeEventListener("animationend", onEnd);
      },
      { once: true }
    );
  }

  function scrollAndSpotlight(slug, card) {
    instantScrollTo(card);
    spotlight(card);
    document.dispatchEvent(
      new CustomEvent("daab-profile-focused", { detail: { slug: slug } })
    );
  }

  function scheduleLayoutReflow(slug) {
    var delays = [0, 50, 150, 350];
    var i;
    for (i = 0; i < delays.length; i++) {
      (function (delay) {
        window.setTimeout(function () {
          if (normalizeSlug(hashId()) !== normalizeSlug(slug)) return;
          var card = findCard(slug);
          if (!card) return;
          instantScrollTo(card);
        }, delay);
      })(delays[i]);
    }
  }

  function focusProfile(slug) {
    slug = normalizeSlug(slug);
    if (!slug) return false;
    var card = findCard(slug);
    if (!card) return false;

    clearBlockingFilters();
    markProfilesReady();

    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        scrollAndSpotlight(slug, card);
        scheduleLayoutReflow(slug);
      });
    });

    return true;
  }

  function prepareHashNavigation() {
    if (!hashId()) return;
    document.documentElement.classList.add("daab-profiles-boot");
    if (window.history && "scrollRestoration" in window.history) {
      window.history.scrollRestoration = "manual";
    }
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  }

  function tryFocus(attempt) {
    var slug = hashId();
    if (!slug) {
      pending = false;
      markProfilesReady();
      return;
    }
    if (focusProfile(slug)) {
      pending = false;
      return;
    }
    if (attempt < MAX_ATTEMPTS) {
      window.requestAnimationFrame(function () {
        tryFocus(attempt + 1);
      });
      return;
    }
    pending = false;
    markProfilesReady();
  }

  function scheduleFocus() {
    if (!hashId()) {
      pending = false;
      markProfilesReady();
      return;
    }
    pending = true;
    tryFocus(0);
  }

  function boot() {
    if (
      document.documentElement.getAttribute("data-daab-page-id") !==
        "scientists-profiles" &&
      !document.getElementById("scientists-catalog")
    ) {
      return;
    }
    prepareHashNavigation();
  }

  document.addEventListener("daab-profiles-catalog-ready", scheduleFocus);

  window.addEventListener("hashchange", function () {
    pending = false;
    scheduleFocus();
  });

  window.addEventListener("pageshow", function () {
    if (!hashId()) return;
    pending = false;
    scheduleFocus();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.addEventListener("load", function () {
    if (!hashId()) return;
    pending = false;
    scheduleFocus();
  });

  window.DAAB_PROFILE_DEEPLINK = {
    hashId: hashId,
    normalizeSlug: normalizeSlug,
    findCard: findCard,
    focusProfile: focusProfile,
    scheduleFocus: scheduleFocus,
    markProfilesReady: markProfilesReady,
  };
})(typeof window !== "undefined" ? window : this);
