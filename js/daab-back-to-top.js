/**
 * DAAB / WAAS — floating Go to top / Go to bottom controls for long pages.
 */
(function (global) {
  "use strict";

  var TOP_THRESHOLD_PX = 280;
  var BOTTOM_THRESHOLD_PX = 48;
  var MIN_SCROLLABLE_PX = 80;
  var MOBILE_MQ = global.matchMedia("(max-width: 1180px)");
  var stack = null;
  var topBtn = null;
  var bottomBtn = null;
  var ticking = false;
  var labels = {
    top: "Back to top",
    bottom: "Go to bottom"
  };
  var DEFAULTS = {
    en: { top: "Back to top", bottom: "Go to bottom" },
    az: { top: "Yuxarı qayıt", bottom: "Aşağı keç" }
  };

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function applyFallbackLabels() {
    var pack = DEFAULTS[detectLang()] || DEFAULTS.en;
    labels.top = pack.top;
    labels.bottom = pack.bottom;
  }

  function applyLabels(ui) {
    applyFallbackLabels();
    var lang = detectLang();
    var topBlock = ui && ui.backToTop && ui.backToTop[lang];
    var bottomBlock = ui && ui.goToBottom && ui.goToBottom[lang];
    if (topBlock && topBlock.label) labels.top = topBlock.label;
    if (bottomBlock && bottomBlock.label) labels.bottom = bottomBlock.label;
    setButtonLabel(topBtn, labels.top);
    setButtonLabel(bottomBtn, labels.bottom);
  }

  function setButtonLabel(btn, text) {
    if (!btn || !text) return;
    btn.setAttribute("aria-label", text);
    btn.setAttribute("title", text);
  }

  function getScrollY() {
    if (global.DAAB_SCROLL_LOCK && typeof global.DAAB_SCROLL_LOCK.getScrollY === "function") {
      return global.DAAB_SCROLL_LOCK.getScrollY();
    }
    var root = document.documentElement;
    var body = document.body;
    return global.scrollY || root.scrollTop || (body && body.scrollTop) || 0;
  }

  function getViewportHeight() {
    return global.innerHeight || document.documentElement.clientHeight || 0;
  }

  function getScrollHeight() {
    var root = document.documentElement;
    var body = document.body;
    return Math.max(
      root ? root.scrollHeight : 0,
      root ? root.offsetHeight : 0,
      body ? body.scrollHeight : 0,
      body ? body.offsetHeight : 0
    );
  }

  function getMaxScrollY() {
    return Math.max(0, getScrollHeight() - getViewportHeight());
  }

  function setScrollY(y) {
    var html = document.documentElement;
    var body = document.body;
    var htmlPrev = html.style.scrollBehavior;
    var bodyPrev = body ? body.style.scrollBehavior : "";
    html.style.scrollBehavior = "auto";
    if (body) body.style.scrollBehavior = "auto";
    html.scrollTop = y;
    if (body) body.scrollTop = y;
    global.scrollTo(0, y);
    html.style.scrollBehavior = htmlPrev;
    if (body) body.style.scrollBehavior = bodyPrev;
  }

  function scrollToTop() {
    setScrollY(0);
    if (topBtn) topBtn.blur();
    updateVisibility();
  }

  function scrollToBottom() {
    setScrollY(getMaxScrollY());
    if (bottomBtn) bottomBtn.blur();
    updateVisibility();
  }

  function isScrollLocked() {
    var root = document.documentElement;
    var body = document.body;
    return (
      (global.DAAB_SCROLL_LOCK && global.DAAB_SCROLL_LOCK.isLocked && global.DAAB_SCROLL_LOCK.isLocked()) ||
      (root && root.classList.contains("daab-scroll-lock")) ||
      (body && body.classList.contains("daab-scroll-lock")) ||
      (root && root.classList.contains("daab-toc-scroll-lock")) ||
      (body && body.classList.contains("daab-toc-scroll-lock"))
    );
  }

  function setVisible(btn, visible) {
    if (!btn) return;
    btn.classList.toggle("is-visible", visible);
    btn.setAttribute("aria-hidden", visible ? "false" : "true");
    btn.tabIndex = visible ? 0 : -1;
  }

  function updateVisibility() {
    var locked = isScrollLocked();
    var y = getScrollY();
    var maxY = getMaxScrollY();
    var pageScrolls = maxY > MIN_SCROLLABLE_PX;
    var showTop = !locked && pageScrolls && y > TOP_THRESHOLD_PX;
    var showBottom = !locked && pageScrolls && y < maxY - BOTTOM_THRESHOLD_PX;
    setVisible(topBtn, showTop);
    setVisible(bottomBtn, showBottom);
    if (stack) {
      stack.classList.toggle("is-active", showTop || showBottom);
    }
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    global.requestAnimationFrame(function () {
      updateVisibility();
      ticking = false;
    });
  }

  function mountTarget() {
    return document.body || document.documentElement;
  }

  function createButton(id, extraClass, direction, label, onClick) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "daab-back-to-top" + (extraClass ? " " + extraClass : "");
    btn.id = id;
    btn.setAttribute("aria-label", label);
    btn.setAttribute("title", label);
    btn.setAttribute("aria-hidden", "true");
    btn.tabIndex = -1;
    var path = direction === "down" ? "M6 9l6 6 6-6" : "M6 15l6-6 6 6";
    btn.innerHTML =
      '<svg class="daab-back-to-top__icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="' + path + '"/>' +
      "</svg>";
    btn.addEventListener("click", onClick);
    return btn;
  }

  function createControls() {
    if (stack || !mountTarget()) return;
    applyFallbackLabels();
    stack = document.createElement("div");
    stack.className = "daab-scroll-fabs";
    stack.id = "daab-scroll-fabs";
    stack.setAttribute("role", "group");
    bottomBtn = createButton(
      "daab-go-to-bottom",
      "daab-go-to-bottom",
      "down",
      labels.bottom,
      scrollToBottom
    );
    topBtn = createButton(
      "daab-back-to-top",
      "",
      "up",
      labels.top,
      scrollToTop
    );
    stack.appendChild(bottomBtn);
    stack.appendChild(topBtn);
    mountTarget().appendChild(stack);
    updateVisibility();
  }

  function watchScrollLock() {
    if (!global.MutationObserver) return;
    var observer = new MutationObserver(onScroll);
    if (document.documentElement) {
      observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    }
    if (document.body) {
      observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    }
  }

  function watchLayout() {
    if (typeof ResizeObserver === "undefined") return;
    var observer = new ResizeObserver(onScroll);
    if (document.documentElement) observer.observe(document.documentElement);
    if (document.body) observer.observe(document.body);
  }

  function init() {
    createControls();
    global.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("scroll", onScroll, { passive: true });
    global.addEventListener("resize", onScroll, { passive: true });
    global.addEventListener("orientationchange", function () {
      global.setTimeout(onScroll, 120);
    });
    if (typeof MOBILE_MQ.addEventListener === "function") {
      MOBILE_MQ.addEventListener("change", onScroll);
    }
    watchScrollLock();
    watchLayout();
    global.addEventListener("load", onScroll, { passive: true });
    global.setTimeout(onScroll, 400);

    var uiPromise =
      global.DAAB_I18N && global.DAAB_I18N.loadUi ? global.DAAB_I18N.loadUi() : Promise.resolve(null);
    uiPromise.then(function (ui) {
      applyLabels(ui);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(window);
