/**
 * DAAB / WAAS — shared Print / PDF control.
 * Waits for page images (including lazy ones) before opening the print dialog.
 */
(function (global) {
  "use strict";

  var DEFAULTS = {
    en: {
      label: "Print / PDF",
      title: "Open the browser print dialog and choose Save as PDF.",
      preparing: "Preparing images…"
    },
    az: {
      label: "Çap et / PDF",
      title: "Brauzerin çap pəncərəsini açın və «PDF kimi yadda saxla» seçin.",
      preparing: "Şəkillər hazırlanır…"
    }
  };

  var btn = null;
  var copy = {
    label: DEFAULTS.en.label,
    title: DEFAULTS.en.title,
    preparing: DEFAULTS.en.preparing
  };
  var nativePrint = global.print ? global.print.bind(global) : function () {};
  var busy = false;
  var warmed = false;

  function detectLang() {
    var I18N = global.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
  }

  function applyFallback() {
    var pack = DEFAULTS[detectLang()] || DEFAULTS.en;
    copy.label = pack.label;
    copy.title = pack.title;
    copy.preparing = pack.preparing;
  }

  function applyLabels(ui) {
    applyFallback();
    var lang = detectLang();
    var block = ui && ui.printPdf && ui.printPdf[lang];
    if (block && block.label) copy.label = block.label;
    if (block && block.title) copy.title = block.title;
    if (block && block.preparing) copy.preparing = block.preparing;
    if (!btn || busy) return;
    btn.textContent = copy.label;
    btn.setAttribute("aria-label", copy.title);
    btn.setAttribute("title", copy.title);
  }

  function isChromeImage(img) {
    return !!(
      img.closest &&
      img.closest(
        "#daab-top-chrome, .nav-strip, .skip, .daab-lang-switch, .daab-page-search, #search-overlay"
      )
    );
  }

  function printableImages() {
    return Array.prototype.filter.call(document.images || [], function (img) {
      return img && !isChromeImage(img);
    });
  }

  function wakeImage(img) {
    var dataSrc = img.getAttribute("data-src");
    var dataSrcset = img.getAttribute("data-srcset");
    if (dataSrc && !img.getAttribute("src")) img.src = dataSrc;
    if (dataSrcset && !img.getAttribute("srcset")) img.srcset = dataSrcset;
    img.loading = "eager";
    img.setAttribute("loading", "eager");
    img.decoding = "sync";
    if (img.hasAttribute("decoding")) img.setAttribute("decoding", "sync");
    if (!img.complete && img.src) {
      var src = img.getAttribute("src");
      img.removeAttribute("src");
      img.src = src;
    }
    wrapForPageBreak(img);
  }

  function wrapForPageBreak(img) {
    var parent = img.parentNode;
    if (!parent || parent.classList.contains("daab-print-figure")) return;
    if (img.closest(".daab-print-header")) return;
    var wrap = document.createElement("div");
    wrap.className = "daab-print-figure";
    parent.insertBefore(wrap, img);
    wrap.appendChild(img);
  }

  function waitForImage(img) {
    return new Promise(function (resolve) {
      var settled = false;
      function done() {
        if (settled) return;
        settled = true;
        resolve();
      }

      function finishDecode() {
        if (typeof img.decode === "function" && img.naturalWidth > 0) {
          img.decode().then(done, done);
        } else {
          done();
        }
      }

      if (img.complete && img.naturalWidth > 0) {
        finishDecode();
        return;
      }
      img.addEventListener("load", finishDecode, { once: true });
      img.addEventListener("error", done, { once: true });
      global.setTimeout(done, 12000);
    });
  }

  function prepareImages() {
    var images = printableImages();
    images.forEach(wakeImage);
    document.documentElement.classList.add("daab-print-images-ready");
    return Promise.all(images.map(waitForImage)).then(function () {
      warmed = true;
    });
  }

  function setBusy(on) {
    busy = !!on;
    document.documentElement.classList.toggle("daab-print-busy", busy);
    if (!btn) return;
    btn.disabled = busy;
    btn.setAttribute("aria-busy", busy ? "true" : "false");
    btn.textContent = busy ? copy.preparing : copy.label;
  }

  function printNow() {
    nativePrint();
  }

  function startPrint() {
    if (busy) return Promise.resolve();
    setBusy(true);
    return prepareImages()
      .catch(function () {})
      .then(function () {
        printNow();
      })
      .finally(function () {
        global.setTimeout(function () {
          setBusy(false);
        }, 400);
      });
  }

  function shouldMountButton() {
    var root = document.documentElement;
    if (!root || root.getAttribute("data-daab-print") !== "1") return false;
    if (document.querySelector(".report-print-btn")) return false;
    return true;
  }

  function createButton() {
    if (btn || !shouldMountButton()) return;
    applyFallback();
    btn = document.createElement("button");
    btn.type = "button";
    btn.className = "report-print-btn";
    btn.id = "daab-print-pdf";
    btn.textContent = copy.label;
    btn.setAttribute("aria-label", copy.title);
    btn.setAttribute("title", copy.title);
    (document.body || document.documentElement).appendChild(btn);
  }

  function bindExistingButton() {
    if (btn) return;
    btn = document.querySelector(".report-print-btn");
    if (!btn) return;
    btn.removeAttribute("onclick");
  }

  function onPrintClick(event) {
    var target = event.target && event.target.closest ? event.target.closest(".report-print-btn") : null;
    if (!target) return;
    event.preventDefault();
    event.stopPropagation();
    startPrint();
  }

  function warmupIdle() {
    if (warmed) return;
    var run = function () {
      prepareImages();
    };
    if (global.requestIdleCallback) {
      global.requestIdleCallback(run, { timeout: 2500 });
    } else {
      global.setTimeout(run, 800);
    }
  }

  function init() {
    createButton();
    bindExistingButton();
    applyFallback();
    if (btn) {
      btn.textContent = copy.label;
      btn.setAttribute("aria-label", copy.title);
      btn.setAttribute("title", copy.title);
    }

    document.addEventListener("click", onPrintClick, true);
    document.addEventListener("beforeprint", function () {
      printableImages().forEach(wakeImage);
    });

    global.print = function () {
      startPrint();
    };

    var uiPromise =
      global.DAAB_I18N && global.DAAB_I18N.loadUi ? global.DAAB_I18N.loadUi() : Promise.resolve(null);
    uiPromise.then(function (ui) {
      applyLabels(ui);
    });

    warmupIdle();
  }

  global.DAAB_PRINT_PDF = {
    print: startPrint,
    prepareImages: prepareImages
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(window);
