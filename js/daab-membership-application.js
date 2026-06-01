/**
 * Multi-step membership application form (AZ).
 */
(function () {
  "use strict";

  var totalSections = 4;
  var currentSection = 1;

  function byId(id) {
    return document.getElementById(id);
  }

  function updateProgress(n) {
    var i;
    var el;
    for (i = 1; i <= totalSections; i++) {
      el = byId("prog-" + i);
      if (!el) continue;
      el.classList.remove("active", "done");
      if (i < n) el.classList.add("done");
      else if (i === n) el.classList.add("active");
    }
  }

  function showSection(n) {
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.classList.remove("active");
    });
    var sec = byId("sec-" + n);
    if (sec) sec.classList.add("active");
    updateProgress(n);
    currentSection = n;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function goTo(n) {
    if (n <= currentSection) showSection(n);
  }

  function next(n) {
    if (n < totalSections) showSection(n + 1);
  }

  function prev(n) {
    if (n > 1) showSection(n - 1);
  }

  function submitForm() {
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.classList.remove("active");
      s.hidden = true;
    });
    var success = byId("success");
    var progress = document.querySelector(".application-page .app-progress-bar");
    var stepNav = document.querySelector(".application-page .app-steps-nav");
    if (success) success.classList.add("active");
    if (progress) progress.hidden = true;
    if (stepNav) stepNav.hidden = true;
    document.querySelectorAll(".application-page .prog-step").forEach(function (el) {
      el.classList.remove("active");
      el.classList.add("done");
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function bindRadioHighlight() {
    document.querySelectorAll('.application-page .opt-item input[type="radio"]').forEach(function (radio) {
      radio.addEventListener("change", function () {
        var name = radio.getAttribute("name");
        document.querySelectorAll('.application-page .opt-item input[name="' + name + '"]').forEach(function (r) {
          var item = r.closest(".opt-item");
          if (item) item.classList.remove("selected");
        });
        var parent = radio.closest(".opt-item");
        if (parent) parent.classList.add("selected");
      });
    });
  }

  function setActiveStepButton(targetId) {
    document.querySelectorAll(".application-page .app-step-btn").forEach(function (btn) {
      var isActive = btn.getAttribute("data-target") === targetId;
      btn.classList.toggle("active", isActive);
      if (isActive) btn.setAttribute("aria-current", "step");
      else btn.removeAttribute("aria-current");
    });
  }

  function currentVisibleSectionId() {
    var sections = Array.prototype.slice.call(document.querySelectorAll(".application-page .form-section"));
    if (!sections.length) return null;
    var refY = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--daab-nav-height")) || 72) + 120;
    var active = sections[0];
    sections.forEach(function (sec) {
      if (sec.hidden) return;
      if (sec.getBoundingClientRect().top <= refY) active = sec;
    });
    return active ? active.id : null;
  }

  function initStepNavigation() {
    var buttons = Array.prototype.slice.call(document.querySelectorAll(".application-page .app-step-btn"));
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var targetId = btn.getAttribute("data-target");
        var section = byId(targetId);
        if (!section) return;
        section.scrollIntoView({ behavior: "smooth", block: "start" });
        setActiveStepButton(targetId);
      });
    });

    var ticking = false;
    function syncActiveFromScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var id = currentVisibleSectionId();
        if (id) setActiveStepButton(id);
        ticking = false;
      });
    }

    window.addEventListener("scroll", syncActiveFromScroll, { passive: true });
    window.addEventListener("resize", syncActiveFromScroll, { passive: true });
    syncActiveFromScroll();
  }

  function initBackToStepsButtons() {
    var topButtons = Array.prototype.slice.call(document.querySelectorAll(".application-page .app-step-top"));
    if (!topButtons.length) return;

    topButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var targetId = btn.getAttribute("data-target");
        var target = byId(targetId);
        if (!target) return;
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  window.daabApplicationGoTo = goTo;
  window.daabApplicationNext = next;
  window.daabApplicationPrev = prev;
  window.daabApplicationSubmit = submitForm;

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.classList.contains("application-page")) return;
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.hidden = false;
    });
    var stepNav = document.querySelector(".application-page .app-steps-nav");
    if (stepNav) stepNav.hidden = false;
    bindRadioHighlight();
    initStepNavigation();
    initBackToStepsButtons();
    updateProgress(1);
  });
})();
