/**
 * Cookie consent (KVKK-aligned): essential always on; analytics opt-in.
 * Storage key: daab-cookie-consent
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "daab-cookie-consent";
  var CSS_HREF = "css/daab-cookie-banner.css?v=3";
  var bannerEl = null;
  var previouslyFocused = null;
  var keydownBound = false;

  function assetRoot() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.assetRoot) return I18N.assetRoot();
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root != null && root !== "") {
      return root.endsWith("/") ? root : root + "/";
    }
    return "";
  }

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function readConsent() {
    try {
      var raw = global.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data || typeof data !== "object") return null;
      return {
        essential: true,
        analytics: !!data.analytics,
        ts: data.ts || 0
      };
    } catch (e) {
      return null;
    }
  }

  function writeConsent(analytics) {
    var payload = {
      essential: true,
      analytics: !!analytics,
      ts: Date.now()
    };
    try {
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) {
      /* ignore quota / private mode */
    }
    try {
      global.dispatchEvent(
        new CustomEvent("daab-cookie-consent", { detail: payload })
      );
    } catch (e2) {
      /* older browsers */
    }
    return payload;
  }

  function hasAnalyticsConsent() {
    var c = readConsent();
    return !!(c && c.analytics);
  }

  function ensureCss() {
    if (document.getElementById("daab-cookie-banner-css")) return;
    var link = document.createElement("link");
    link.id = "daab-cookie-banner-css";
    link.rel = "stylesheet";
    link.href = assetRoot() + CSS_HREF;
    document.head.appendChild(link);
  }

  function t(lang) {
    var root = assetRoot();
    if (lang === "en") {
      return {
        title: "Cookies and privacy",
        text:
          "We use essential cookies to run this site. Optional analytics cookies (Google Analytics) help us understand visits and are used only with your consent, in line with Turkish KVKK requirements. See our " +
          '<a href="' +
          root +
          'en/cookies.html#page-title">Cookie policy</a> and <a href="' +
          root +
          'en/privacy.html#page-title">Privacy notice</a>.',
        accept: "Accept all",
        reject: "Essential only",
        prefs: "Preferences",
        save: "Save choices",
        essential: "Essential cookies (required)",
        essentialHelp: "Security, language preference, and basic site functions.",
        analytics: "Analytics cookies (optional)",
        analyticsHelp: "Google Analytics — visit statistics only if you allow."
      };
    }
    return {
      title: "Kukilər və məxfilik",
      text:
        "Saytın işləməsi üçün zəruri kukilərdən istifadə edirik. İstəyə bağlı analitika kukiləri (Google Analytics) yalnız sizin razılığınızla işə düşür və KVKK tələblərinə uyğun tətbiq olunur. Ətraflı məlumat: " +
        '<a href="' +
        root +
        'az/cookies.html#page-title">Kuki siyasəti</a> və <a href="' +
        root +
        'az/privacy.html#page-title">Məxfilik bildirişi</a>.',
      accept: "Hamısını qəbul et",
      reject: "Yalnız zəruri",
      prefs: "Seçimlər",
      save: "Seçimləri saxla",
      essential: "Zəruri kukilər (məcburi)",
      essentialHelp: "Təhlükəsizlik, dil seçimi və saytın əsas funksiyaları.",
      analytics: "Analitika kukiləri (istəyə bağlı)",
      analyticsHelp: "Google Analytics — yalnız icazə versəniz, statistika üçün."
    };
  }

  function focusableIn(root) {
    if (!root) return [];
    return Array.prototype.slice
      .call(
        root.querySelectorAll(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
      )
      .filter(function (el) {
        if (el.hidden || el.getAttribute("aria-hidden") === "true") return false;
        var style = global.getComputedStyle ? global.getComputedStyle(el) : null;
        if (style && (style.visibility === "hidden" || style.display === "none")) return false;
        return true;
      });
  }

  function onBannerKeydown(e) {
    if (!bannerEl || bannerEl.hidden) return;
    if (e.key === "Escape") {
      e.preventDefault();
      writeConsent(false);
      hideBanner();
      return;
    }
    if (e.key !== "Tab") return;
    var list = focusableIn(bannerEl);
    if (!list.length) return;
    var first = list[0];
    var last = list[list.length - 1];
    if (e.shiftKey) {
      if (document.activeElement === first || !bannerEl.contains(document.activeElement)) {
        e.preventDefault();
        last.focus();
      }
    } else if (document.activeElement === last || !bannerEl.contains(document.activeElement)) {
      e.preventDefault();
      first.focus();
    }
  }

  function bindKeydown() {
    if (keydownBound) return;
    document.addEventListener("keydown", onBannerKeydown, true);
    keydownBound = true;
  }

  function unbindKeydown() {
    if (!keydownBound) return;
    document.removeEventListener("keydown", onBannerKeydown, true);
    keydownBound = false;
  }

  function hideBanner() {
    if (bannerEl) bannerEl.hidden = true;
    unbindKeydown();
    if (previouslyFocused && typeof previouslyFocused.focus === "function") {
      try {
        previouslyFocused.focus();
      } catch (e) {
        /* ignore */
      }
    }
    previouslyFocused = null;
  }

  function showBanner(forcePrefs) {
    ensureCss();
    var lang = detectLang();
    var copy = t(lang);
    if (!bannerEl) {
      bannerEl = document.createElement("div");
      bannerEl.className = "daab-cookie-banner";
      bannerEl.setAttribute("role", "dialog");
      bannerEl.setAttribute("aria-modal", "true");
      bannerEl.setAttribute("aria-live", "polite");
      bannerEl.setAttribute("aria-label", copy.title);
      document.body.appendChild(bannerEl);
    }
    bannerEl.hidden = false;
    bannerEl.setAttribute("aria-modal", "true");
    bannerEl.setAttribute("aria-label", copy.title);
    bannerEl.innerHTML =
      '<p class="daab-cookie-banner__title" id="daab-cookie-banner-title"></p>' +
      '<p class="daab-cookie-banner__text"></p>' +
      '<div class="daab-cookie-banner__prefs" hidden></div>' +
      '<div class="daab-cookie-banner__actions"></div>';

    bannerEl.querySelector(".daab-cookie-banner__title").textContent = copy.title;
    bannerEl.querySelector(".daab-cookie-banner__text").innerHTML = copy.text;
    bannerEl.setAttribute("aria-labelledby", "daab-cookie-banner-title");

    var prefs = bannerEl.querySelector(".daab-cookie-banner__prefs");
    prefs.innerHTML =
      '<label class="daab-cookie-banner__pref">' +
      '<input type="checkbox" checked disabled data-daab-cookie="essential"/>' +
      "<span><strong></strong><br/><span data-help></span></span></label>" +
      '<label class="daab-cookie-banner__pref">' +
      '<input type="checkbox" data-daab-cookie="analytics"/>' +
      "<span><strong></strong><br/><span data-help></span></span></label>";
    var labels = prefs.querySelectorAll(".daab-cookie-banner__pref");
    labels[0].querySelector("strong").textContent = copy.essential;
    labels[0].querySelector("[data-help]").textContent = copy.essentialHelp;
    labels[1].querySelector("strong").textContent = copy.analytics;
    labels[1].querySelector("[data-help]").textContent = copy.analyticsHelp;
    var analyticsBox = prefs.querySelector('[data-daab-cookie="analytics"]');
    var existing = readConsent();
    analyticsBox.checked = !!(existing && existing.analytics);

    var actions = bannerEl.querySelector(".daab-cookie-banner__actions");
    actions.innerHTML = "";
    function btn(label, className, onClick) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "daab-cookie-banner__btn" + (className ? " " + className : "");
      b.textContent = label;
      b.addEventListener("click", onClick);
      actions.appendChild(b);
      return b;
    }

    btn(copy.reject, "", function () {
      writeConsent(false);
      hideBanner();
    });
    btn(copy.prefs, "", function () {
      prefs.hidden = !prefs.hidden;
      if (!prefs.hidden) {
        try {
          analyticsBox.focus();
        } catch (e) {
          /* ignore */
        }
      }
    });
    btn(copy.accept, "daab-cookie-banner__btn--primary", function () {
      writeConsent(true);
      hideBanner();
    });
    btn(copy.save, "", function () {
      writeConsent(!!analyticsBox.checked);
      hideBanner();
    });

    if (forcePrefs) prefs.hidden = false;

    previouslyFocused = document.activeElement;
    bindKeydown();
    var first = focusableIn(bannerEl)[0];
    if (first) {
      try {
        first.focus();
      } catch (e3) {
        /* ignore */
      }
    }
  }

  function init() {
    if (!readConsent()) showBanner(false);
  }

  global.DAAB_COOKIE = {
    STORAGE_KEY: STORAGE_KEY,
    read: readConsent,
    hasAnalyticsConsent: hasAnalyticsConsent,
    openSettings: function () {
      showBanner(true);
    },
    acceptAll: function () {
      writeConsent(true);
      hideBanner();
    },
    rejectOptional: function () {
      writeConsent(false);
      hideBanner();
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : this);
