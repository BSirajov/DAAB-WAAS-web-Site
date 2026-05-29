/**
 * Scientist profile card preview on scientists/list.html (hover, focus, touch).
 * Loads i18n/scientists-profiles.json once; single fixed popover, no layout shift.
 */
(function (window, document) {
  "use strict";

  var CRED = {
    PhD: "Ph.D.",
    "Prof.Dr.": "Prof. Dr.",
    "Ed.D.": "Ed.D.",
    "Dr.": "Dr.",
  };

  var LABELS = {
    az: { field: "İxtisas:", email: "E-poçt:", view: "Tam profil ↗", preview: "Profil önizləməsi" },
    en: { field: "Field:", email: "Email:", view: "View full profile ↗", preview: "Profile preview" },
  };

  var SHOW_DELAY = 160;
  var HIDE_DELAY = 120;
  var GAP = 10;
  var VIEWPORT_PAD = 12;

  var lang = (document.documentElement.getAttribute("data-daab-lang") || document.documentElement.lang || "az")
    .slice(0, 2)
    .toLowerCase();
  if (lang !== "en") lang = "az";
  var labels = LABELS[lang];

  var assetRoot = document.documentElement.getAttribute("data-daab-asset-root") || "../../";
  var profilesUrl = assetRoot + "i18n/scientists-profiles.json";

  var byEmail = Object.create(null);
  var bySay = Object.create(null);
  var htmlCache = Object.create(null);
  var loadPromise = null;

  var popover = null;
  var activeTrigger = null;
  var activeKey = null;
  var showTimer = null;
  var hideTimer = null;
  var hoverPreview = true;
  var tapPreview = false;
  var pinnedTouch = false;

  function updatePointerMode() {
    try {
      hoverPreview = window.matchMedia("(hover: hover)").matches;
      tapPreview = window.matchMedia("(hover: none)").matches;
    } catch (e) {
      hoverPreview = true;
      tapPreview = false;
    }
  }

  function slugFromPhoto(photo) {
    var p = (photo || "").trim();
    var i = p.lastIndexOf("/");
    if (i >= 0) p = p.slice(i + 1);
    var dot = p.lastIndexOf(".");
    return dot > 0 ? p.slice(0, dot) : p;
  }

  function azUpperName(name) {
    return String(name || "")
      .trim()
      .toUpperCase()
      .replace(/I/g, "İ");
  }

  function enUpperName(name) {
    return String(name || "")
      .trim()
      .toUpperCase();
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function bioLeadText(html) {
    if (!html) return "";
    var tmp = document.createElement("div");
    tmp.innerHTML = html;
    var lead = tmp.querySelector(".bio-lead") || tmp.querySelector("p.bio");
    return lead ? lead.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function localizeProfile(p) {
    var degree = (p.degree || "").trim();
    return {
      slug: slugFromPhoto(p.photo),
      photo: (p.photo || "").trim(),
      email: (p.email || "").trim(),
      say: p.say,
      name: lang === "en" ? p.name_en || p.name : p.name,
      country: lang === "en" ? p.country_en || p.country_az : p.country_az || p.country,
      field: lang === "en" ? p.field_en || p.field_az : p.field_az || p.field,
      title: lang === "en" ? p.title_en || p.title_az || p.title : p.title_az || p.title,
      degree: degree,
      cred: CRED[degree] || degree,
      bioLead: bioLeadText(lang === "en" ? p.bio_html_en || p.bio_html_az : p.bio_html_az || p.bio_html),
    };
  }

  function indexProfiles(list) {
    var i;
    for (i = 0; i < list.length; i++) {
      var loc = localizeProfile(list[i]);
      if (loc.email) byEmail[loc.email.toLowerCase()] = loc;
      if (loc.say != null) bySay[String(loc.say)] = loc;
    }
  }

  function loadProfiles() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(profilesUrl, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("profiles fetch failed");
        return res.json();
      })
      .then(function (data) {
        indexProfiles(data.profiles || []);
      })
      .catch(function () {
        /* list still works without previews */
      });
    return loadPromise;
  }

  function lookupProfile(trigger) {
    var email = (trigger.getAttribute("data-scientist-email") || "").toLowerCase();
    var say = trigger.getAttribute("data-scientist-say");
    if (email && byEmail[email]) return byEmail[email];
    if (say != null && bySay[String(say)]) return bySay[String(say)];
    return null;
  }

  function fallbackFromRow(trigger) {
    var tr = trigger.closest("tr");
    if (!tr) return null;
    var cells = tr.querySelectorAll("td");
    if (cells.length < 5) return null;
    return {
      slug: "",
      photo: "",
      email: (trigger.getAttribute("data-scientist-email") || "").trim(),
      name: trigger.textContent.replace(/\s+/g, " ").trim(),
      country: cells[2] ? cells[2].textContent.trim() : "",
      field: cells[3] ? cells[3].textContent.trim() : "",
      title: "",
      degree: cells[4] ? cells[4].textContent.trim() : "",
      cred: "",
      bioLead: "",
    };
  }

  function buildCardHtml(profile) {
    var key = profile.email || "say-" + profile.say;
    if (htmlCache[key]) return htmlCache[key];

    var nameHeading =
      lang === "en" ? enUpperName(profile.name) : azUpperName(profile.name);
    var credHtml = profile.cred
      ? ' <span class="cred">' + esc(profile.cred) + "</span>"
      : "";
    var photoHtml = profile.photo
      ? '<img src="' +
        esc(assetRoot + "images/scientists-photos/" + profile.photo) +
        '" alt="' +
        esc(profile.name) +
        '" width="88" height="88" decoding="async" loading="lazy"/>'
      : "";
    var emailRow = profile.email
      ? '<a class="scientist-preview-card__email" href="mailto:' +
        esc(profile.email) +
        '">' +
        esc(profile.email) +
        "</a>"
      : '<span class="scientist-preview-card__meta-value">—</span>';
    var profileHref = profile.slug
      ? "profiles.html#" + profile.slug
      : "profiles.html";
    var leadHtml = profile.bioLead
      ? '<p class="scientist-preview-card__lead">' + esc(profile.bioLead) + "</p>"
      : "";

    htmlCache[key] =
      '<article class="scientist-preview-card">' +
      '<div class="scientist-preview-card__inner">' +
      '<div class="scientist-preview-card__portrait">' +
      '<div class="scientist-preview-card__avatar">' +
      photoHtml +
      "</div></div>" +
      '<div class="scientist-preview-card__body">' +
      '<p class="scientist-preview-card__name">' +
      esc(nameHeading) +
      credHtml +
      "</p>" +
      (profile.country
        ? '<p class="scientist-preview-card__country">' + esc(profile.country) + "</p>"
        : "") +
      (profile.title
        ? '<p class="scientist-preview-card__title">' + esc(profile.title) + "</p>"
        : "") +
      '<div class="scientist-preview-card__meta">' +
      '<div class="scientist-preview-card__meta-row"><span class="scientist-preview-card__meta-label">' +
      esc(labels.field) +
      '</span><span class="scientist-preview-card__meta-value">' +
      esc(profile.field || "—") +
      "</span></div>" +
      '<div class="scientist-preview-card__meta-row"><span class="scientist-preview-card__meta-label">' +
      esc(labels.email) +
      "</span>" +
      emailRow +
      "</div></div>" +
      leadHtml +
      "</div></div>" +
      '<div class="scientist-preview-card__footer">' +
      '<a class="scientist-preview-card__link" href="' +
      esc(profileHref) +
      '">' +
      esc(labels.view) +
      "</a></div></article>";

    return htmlCache[key];
  }

  function ensurePopover() {
    if (popover) return popover;
    popover = document.createElement("div");
    popover.id = "scientistListPreview";
    popover.className = "scientist-list-preview";
    popover.setAttribute("role", "region");
    popover.setAttribute("aria-hidden", "true");
    document.body.appendChild(popover);
    popover.addEventListener("mouseenter", cancelHide);
    popover.addEventListener("mouseleave", scheduleHide);
    popover.addEventListener("focusin", cancelHide);
    popover.addEventListener("focusout", onPopoverFocusOut);
    return popover;
  }

  function stickyTopInset() {
    var root = document.documentElement;
    var style = window.getComputedStyle(root);
    var stack = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
    if (!isFinite(stack) || stack <= 0) {
      var nav = parseFloat(style.getPropertyValue("--daab-nav-height"));
      var bc = parseFloat(style.getPropertyValue("--daab-breadcrumbs-height"));
      stack = (isFinite(nav) ? nav : 86) + (isFinite(bc) ? bc : 0);
    }
    return Math.ceil(stack) + VIEWPORT_PAD;
  }

  function positionPopover(trigger) {
    if (!popover || !trigger) return;
    var rect = trigger.getBoundingClientRect();
    var popRect = popover.getBoundingClientRect();
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var topMin = stickyTopInset();
    var maxH = vh - topMin - VIEWPORT_PAD;
    popover.style.maxHeight = Math.max(160, maxH) + "px";

    var w = popRect.width || Math.min(352, vw - VIEWPORT_PAD * 2);
    var h = popover.offsetHeight || 280;

    var placeBelow = rect.bottom + GAP + h <= vh - VIEWPORT_PAD;
    var top = placeBelow ? rect.bottom + GAP : rect.top - GAP - h;
    if (top < topMin) top = topMin;
    if (top + h > vh - VIEWPORT_PAD) top = Math.max(topMin, vh - VIEWPORT_PAD - h);

    var left = rect.left;
    if (left + w > vw - VIEWPORT_PAD) left = vw - VIEWPORT_PAD - w;
    if (left < VIEWPORT_PAD) left = VIEWPORT_PAD;

    popover.style.left = Math.round(left) + "px";
    popover.style.top = Math.round(top) + "px";
  }

  function setExpanded(trigger, on) {
    if (!trigger) return;
    trigger.setAttribute("aria-expanded", on ? "true" : "false");
    var id = popover ? popover.id : "scientistListPreview";
    if (on) trigger.setAttribute("aria-describedby", id);
    else trigger.removeAttribute("aria-describedby");
  }

  function show(trigger) {
    if (!trigger) return;
    var profile = lookupProfile(trigger) || fallbackFromRow(trigger);
    if (!profile) return;

    cancelTimers();
    var el = ensurePopover();
    var key = (trigger.getAttribute("data-scientist-email") || "") + "-" + trigger.getAttribute("data-scientist-say");
    if (activeKey !== key) {
      el.innerHTML = buildCardHtml(profile);
      activeKey = key;
    }

    if (activeTrigger && activeTrigger !== trigger) setExpanded(activeTrigger, false);
    activeTrigger = trigger;
    setExpanded(trigger, true);

    el.hidden = false;
    el.setAttribute("aria-hidden", "false");
    el.setAttribute("aria-label", labels.preview + ": " + (profile.name || ""));
    el.classList.add("is-visible");
    void el.offsetHeight;
    positionPopover(trigger);
  }

  function hide() {
    cancelTimers();
    if (!popover) return;
    popover.classList.remove("is-visible");
    popover.setAttribute("aria-hidden", "true");
    if (activeTrigger) setExpanded(activeTrigger, false);
    activeTrigger = null;
    activeKey = null;
    pinnedTouch = false;
  }

  function cancelTimers() {
    if (showTimer) {
      window.clearTimeout(showTimer);
      showTimer = null;
    }
    if (hideTimer) {
      window.clearTimeout(hideTimer);
      hideTimer = null;
    }
  }

  function scheduleShow(trigger) {
    cancelTimers();
    if (tapPreview && pinnedTouch && activeTrigger === trigger) return;
    showTimer = window.setTimeout(function () {
      showTimer = null;
      show(trigger);
    }, tapPreview && !hoverPreview ? 0 : SHOW_DELAY);
  }

  function scheduleHide() {
    cancelTimers();
    if (tapPreview && pinnedTouch) return;
    hideTimer = window.setTimeout(function () {
      hideTimer = null;
      hide();
    }, HIDE_DELAY);
  }

  function cancelHide() {
    if (hideTimer) {
      window.clearTimeout(hideTimer);
      hideTimer = null;
    }
  }

  function containsRelated(node, root) {
    return node && root && (node === root || root.contains(node));
  }

  function onTriggerFocusOut(e) {
    var next = e.relatedTarget;
    if (containsRelated(next, popover) || containsRelated(next, e.currentTarget)) return;
    scheduleHide();
  }

  function onPopoverFocusOut(e) {
    var next = e.relatedTarget;
    if (containsRelated(next, popover) || containsRelated(next, activeTrigger)) return;
    scheduleHide();
  }

  function onDocumentPointerDown(e) {
    if (!touchMode || !popover || popover.hidden) return;
    var t = e.target;
    if (containsRelated(t, popover) || (activeTrigger && containsRelated(t, activeTrigger))) return;
    hide();
  }

  function onTriggerClick(e, trigger) {
    if (!tapPreview) return;
    e.preventDefault();
    if (activeTrigger === trigger && popover && popover.classList.contains("is-visible")) {
      hide();
      return;
    }
    pinnedTouch = true;
    show(trigger);
  }

  function onKeyDown(e) {
    if (e.key === "Escape" && popover && popover.classList.contains("is-visible")) {
      e.preventDefault();
      hide();
      if (activeTrigger) activeTrigger.focus();
    }
  }

  function bindTable() {
    var tbody = document.getElementById("tableBody");
    if (!tbody || tbody.dataset.previewBound === "1") return;
    tbody.dataset.previewBound = "1";

    tbody.addEventListener("pointerover", function (e) {
      if (!hoverPreview || e.pointerType === "touch") return;
      var trg = e.target.closest(".scientist-name-trigger");
      if (!trg || !tbody.contains(trg)) return;
      scheduleShow(trg);
    });

    tbody.addEventListener("pointerout", function (e) {
      if (!hoverPreview || e.pointerType === "touch") return;
      var trg = e.target.closest(".scientist-name-trigger");
      if (!trg) return;
      var rel = e.relatedTarget;
      if (containsRelated(rel, trg) || containsRelated(rel, popover)) return;
      scheduleHide();
    });

    tbody.addEventListener("focusin", function (e) {
      var trg = e.target.closest(".scientist-name-trigger");
      if (!trg || !tbody.contains(trg)) return;
      scheduleShow(trg);
    });

    tbody.addEventListener("focusout", onTriggerFocusOut);

    tbody.addEventListener("click", function (e) {
      var trg = e.target.closest(".scientist-name-trigger");
      if (!trg || !tbody.contains(trg)) return;
      onTriggerClick(e, trg);
    });
  }

  function onScrollOrResize() {
    if (popover && popover.classList.contains("is-visible") && activeTrigger) {
      positionPopover(activeTrigger);
    }
  }

  function init() {
    updatePointerMode();
    try {
      window.matchMedia("(hover: hover)").addEventListener("change", updatePointerMode);
    } catch (e) {
      /* ignore */
    }
    loadProfiles().then(bindTable);
    bindTable();
    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("pointerdown", onDocumentPointerDown, true);
    window.addEventListener("resize", onScrollOrResize, { passive: true });
    window.addEventListener("scroll", onScrollOrResize, { passive: true, capture: true });
  }

  window.DAABScientistsListPreview = {
    refresh: function () {
      bindTable();
      if (activeTrigger && !document.body.contains(activeTrigger)) hide();
      else if (activeTrigger && popover && popover.classList.contains("is-visible")) {
        positionPopover(activeTrigger);
      }
    },
  };

  function boot() {
    if (!document.getElementById("tableBody")) {
      document.addEventListener("DOMContentLoaded", init, { once: true });
      return;
    }
    init();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})(window, document);
