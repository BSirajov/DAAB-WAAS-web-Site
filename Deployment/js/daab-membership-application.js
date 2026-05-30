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
    });
    var success = byId("success");
    var progress = document.querySelector(".application-page .app-progress-bar");
    if (success) success.classList.add("active");
    if (progress) progress.hidden = true;
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

  window.daabApplicationGoTo = goTo;
  window.daabApplicationNext = next;
  window.daabApplicationPrev = prev;
  window.daabApplicationSubmit = submitForm;

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.classList.contains("application-page")) return;
    bindRadioHighlight();
    updateProgress(1);
  });
})();
