/**
 * DAAB / WAAS — floating back-to-top control for long pages.
 */
(function (global) {
  "use strict";

  var THRESHOLD_PX = 280;
  var MOBILE_MQ = global.matchMedia("(max-width: 1180px)");
  var btn = null;
  var ticking = false;
  var labels = { label: "Back to top" };

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function applyLabels(ui) {
    var lang = detectLang();
    var block = ui && ui.backToTop && ui.backToTop[lang];
    if (block && block.label) labels.label = block.label;
    if (!btn) return;
    btn.setAttribute("aria-label", labels.label);
    btn.setAttribute("title", labels.label);
  }

  function getScrollY() {
    if (global.DAAB_SCROLL_LOCK && typeof global.DAAB_SCROLL_LOCK.getScrollY === "function") {
      return global.DAAB_SCROLL_LOCK.getScrollY();
    }
    var root = document.documentElement;
    var body = document.body;
    return global.scrollY || root.scrollTop || (body && body.scrollTop) || 0;
  }

  function scrollToTop() {
    var html = document.documentElement;
    var body = document.body;
    var htmlPrev = html.style.scrollBehavior;
    var bodyPrev = body ? body.style.scrollBehavior : "";
    html.style.scrollBehavior = "auto";
    if (body) body.style.scrollBehavior = "auto";
    html.scrollTop = 0;
    if (body) body.scrollTop = 0;
    global.scrollTo(0, 0);
    html.style.scrollBehavior = htmlPrev;
    if (body) body.style.scrollBehavior = bodyPrev;
    if (btn) btn.blur();
    updateVisibility();
  }

  function isScrollLocked() {
    var root = document.documentElement;
    var body = document.body;
    return (
      (global.DAAB_SCROLL_LOCK && global.DAAB_SCROLL_LOCK.isLocked && global.DAAB_SCROLL_LOCK.isLocked()) ||
      (root && root.classList.contains("daab-scroll-lock")) ||
      (body && body.classList.contains("daab-scroll-lock"))
    );
  }

  function updateVisibility() {
    if (!btn) return;
    var show = getScrollY() > THRESHOLD_PX;
    var locked = isScrollLocked();
    var visible = show && !locked;
    btn.classList.toggle("is-visible", visible);
    btn.setAttribute("aria-hidden", visible ? "false" : "true");
    btn.tabIndex = visible ? 0 : -1;
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
    return document.documentElement || document.body;
  }

  function createButton() {
    if (btn || !mountTarget()) return;
    btn = document.createElement("button");
    btn.type = "button";
    btn.className = "daab-back-to-top";
    btn.id = "daab-back-to-top";
    btn.setAttribute("aria-label", labels.label);
    btn.setAttribute("title", labels.label);
    btn.setAttribute("aria-hidden", "true");
    btn.tabIndex = -1;
    btn.innerHTML =
      '<svg class="daab-back-to-top__icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M12 5.2 6.1 11.1l1.4 1.4L11 9V18h2V9l3.5 3.5 1.4-1.4L12 5.2z"/>' +
      "</svg>";
    btn.addEventListener("click", scrollToTop);
    mountTarget().appendChild(btn);
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

  function init() {
    createButton();
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
