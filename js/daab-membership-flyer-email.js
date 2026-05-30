/**
 * Membership flyer — generate PDF and open email client with invitation text.
 * PDF: off-screen A4 clone → html2canvas → jsPDF (fit entire page, no crop).
 */
(function () {
  "use strict";

  var HTML2CANVAS_URL =
    "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
  var JSPDF_URL =
    "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js";

  /* 210 mm at 96 CSS px/in — stable capture width across browsers */
  var A4_WIDTH_PX = Math.round((210 / 25.4) * 96);
  var A4_HEIGHT_PX = Math.round((297 / 25.4) * 96);
  var PDF_CAPTURE_SCALE = 2;

  function loadScript(url, id) {
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[data-daab-lib="' + id + '"]');
      if (existing) {
        if (existing.getAttribute("data-daab-loaded") === "1") {
          resolve();
          return;
        }
        existing.addEventListener("load", function () {
          resolve();
        });
        existing.addEventListener("error", reject);
        return;
      }
      var script = document.createElement("script");
      script.src = url;
      script.defer = true;
      script.setAttribute("data-daab-lib", id);
      script.onload = function () {
        script.setAttribute("data-daab-loaded", "1");
        resolve();
      };
      script.onerror = function () {
        reject(new Error("Could not load " + id));
      };
      document.head.appendChild(script);
    });
  }

  function loadPdfLibs() {
    if (window.html2canvas && getJsPDFConstructor()) {
      return Promise.resolve();
    }
    return loadScript(HTML2CANVAS_URL, "html2canvas").then(function () {
      return loadScript(JSPDF_URL, "jspdf");
    });
  }

  function getJsPDFConstructor() {
    if (window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
    if (typeof window.jsPDF === "function") return window.jsPDF;
    return null;
  }

  var EXPORT_CHROME_SELECTORS = [
    ".flyer-page-controls",
    "[data-flyer-export-exclude='1']",
    "#daab-breadcrumbs",
    "nav.daab-breadcrumbs",
    ".daab-breadcrumbs"
  ];

  function getFlyerExportRoot() {
    return document.querySelector(".flyer-sheet");
  }

  function hideExportChrome() {
    var hidden = [];
    var seen = new Set();
    EXPORT_CHROME_SELECTORS.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (el) {
        if (seen.has(el)) return;
        seen.add(el);
        hidden.push({ el: el, visibility: el.style.getPropertyValue("visibility") });
        el.style.setProperty("visibility", "hidden");
      });
    });
    return hidden;
  }

  function restoreExportChrome(hidden) {
    if (!hidden || !hidden.length) return;
    hidden.forEach(function (item) {
      if (!item.el) return;
      if (item.visibility) {
        item.el.style.setProperty("visibility", item.visibility);
      } else {
        item.el.style.removeProperty("visibility");
      }
    });
  }

  var activeExportChromeHide = null;

  function beginExportChromeHide() {
    if (activeExportChromeHide) return activeExportChromeHide;
    activeExportChromeHide = hideExportChrome();
    return activeExportChromeHide;
  }

  function endExportChromeHide() {
    if (!activeExportChromeHide) return;
    restoreExportChrome(activeExportChromeHide);
    activeExportChromeHide = null;
  }

  function waitForFonts() {
    if (document.fonts && document.fonts.ready) {
      return document.fonts.ready;
    }
    return Promise.resolve();
  }

  function waitForImages(root) {
    var imgs = root.querySelectorAll("img");
    return Promise.all(
      Array.prototype.map.call(imgs, function (img) {
        if (img.complete && img.naturalWidth > 0) return Promise.resolve();
        return new Promise(function (resolve) {
          img.addEventListener("load", resolve, { once: true });
          img.addEventListener("error", resolve, { once: true });
        });
      })
    );
  }

  function waitForLayout() {
    return new Promise(function (resolve) {
      requestAnimationFrame(function () {
        requestAnimationFrame(resolve);
      });
    });
  }

  function createExportStage(sourceSheet) {
    var existing = document.getElementById("daab-flyer-export-stage");
    if (existing) existing.remove();

    var stage = document.createElement("div");
    stage.id = "daab-flyer-export-stage";
    stage.setAttribute("aria-hidden", "true");

    var clone = sourceSheet.cloneNode(true);
    clone.removeAttribute("id");
    clone.classList.add("flyer-sheet--pdf-export");
    stage.appendChild(clone);
    document.body.appendChild(stage);

    return { stage: stage, sheet: clone };
  }

  function removeExportStage(stage) {
    if (stage && stage.parentNode) stage.parentNode.removeChild(stage);
  }

  function readBlobAsDataUrl(blob) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onload = function () {
        resolve(reader.result);
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  /** Copy pixels from the on-screen flyer (works when CORS was satisfied at load time). */
  function copyLoadedImagesFromSource(cloneRoot, sourceRoot) {
    var cloneImgs = cloneRoot.querySelectorAll("img");
    var sourceImgs = sourceRoot.querySelectorAll("img");
    Array.prototype.forEach.call(cloneImgs, function (cloneImg, index) {
      var liveImg = sourceImgs[index];
      if (!liveImg || !liveImg.complete || liveImg.naturalWidth === 0) return;
      try {
        var canvas = document.createElement("canvas");
        canvas.width = liveImg.naturalWidth;
        canvas.height = liveImg.naturalHeight;
        canvas.getContext("2d").drawImage(liveImg, 0, 0);
        cloneImg.src = canvas.toDataURL("image/png");
        cloneImg.removeAttribute("crossorigin");
      } catch (err) {
        console.warn("[daab-membership-flyer-email] copyLoadedImagesFromSource:", err);
      }
    });
  }

  /** Inline cross-origin images so html2canvas can paint them without tainting. */
  async function inlineExternalImages(root) {
    var imgs = root.querySelectorAll("img");
    var tasks = Array.prototype.map.call(imgs, async function (img) {
      var src = img.getAttribute("src") || "";
      if (!src || src.indexOf("data:") === 0) return;

      try {
        var response = await fetch(src, { mode: "cors", credentials: "omit" });
        if (!response.ok) throw new Error("HTTP " + response.status);
        var blob = await response.blob();
        img.src = await readBlobAsDataUrl(blob);
        img.removeAttribute("crossorigin");
      } catch (err) {
        console.warn("[daab-membership-flyer-email] Could not inline image:", src, err);
      }
    });
    await Promise.all(tasks);
  }

  async function captureExportCanvas(exportSheet) {
    if (!window.html2canvas) {
      throw new Error("html2canvas not available after library load");
    }

    var captureHeight = Math.max(exportSheet.scrollHeight, exportSheet.offsetHeight, 1);

    return window.html2canvas(exportSheet, {
      scale: PDF_CAPTURE_SCALE,
      useCORS: true,
      allowTaint: false,
      logging: false,
      backgroundColor: "#ffffff",
      scrollX: 0,
      scrollY: 0,
      windowWidth: Math.max(A4_WIDTH_PX + 160, 1200),
      windowHeight: Math.max(captureHeight + 200, A4_HEIGHT_PX)
    });
  }

  function canvasToA4PdfBlob(canvas) {
    var JsPDF = getJsPDFConstructor();
    if (!JsPDF) {
      throw new Error("jsPDF not available after library load");
    }

    var pdf = new JsPDF({
      unit: "mm",
      format: "a4",
      orientation: "portrait",
      compress: true
    });

    var pageW = pdf.internal.pageSize.getWidth();
    var pageH = pdf.internal.pageSize.getHeight();

    var cssW = canvas.width / PDF_CAPTURE_SCALE;
    var cssH = canvas.height / PDF_CAPTURE_SCALE;
    var imgWmm = (cssW * 25.4) / 96;
    var imgHmm = (cssH * 25.4) / 96;

    /* Fit entire capture on one A4 page (contain — never crop sides or bottom) */
    var fit = Math.min(pageW / imgWmm, pageH / imgHmm);
    var drawW = imgWmm * fit;
    var drawH = imgHmm * fit;
    var offsetX = (pageW - drawW) / 2;
    var offsetY = (pageH - drawH) / 2;

    var imgData = canvas.toDataURL("image/jpeg", 0.98);
    pdf.addImage(imgData, "JPEG", offsetX, offsetY, drawW, drawH, undefined, "FAST");

    return pdf.output("blob");
  }

  async function generatePdfBlob(sourceSheet) {
    await loadPdfLibs();
    await waitForFonts();

    var stageRef = createExportStage(sourceSheet);
    try {
      copyLoadedImagesFromSource(stageRef.sheet, sourceSheet);
      await inlineExternalImages(stageRef.sheet);
      await waitForImages(stageRef.sheet);
      await waitForLayout();

      var canvas = await captureExportCanvas(stageRef.sheet);
      return canvasToA4PdfBlob(canvas);
    } finally {
      removeExportStage(stageRef.stage);
    }
  }

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () {
      URL.revokeObjectURL(url);
    }, 120000);
  }

  function printPdfBlob(blob, filename) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(blob);
      var iframe = document.createElement("iframe");
      iframe.setAttribute("title", filename || "Flyer PDF");
      iframe.style.cssText =
        "position:fixed;right:0;bottom:0;width:0;height:0;border:0;visibility:hidden;";
      iframe.src = url;

      var cleaned = false;
      function cleanup() {
        if (cleaned) return;
        cleaned = true;
        window.setTimeout(function () {
          if (iframe.parentNode) iframe.parentNode.removeChild(iframe);
          URL.revokeObjectURL(url);
        }, 120000);
      }

      iframe.onload = function () {
        try {
          var win = iframe.contentWindow;
          if (!win) throw new Error("Print frame unavailable");
          win.focus();
          win.print();
          resolve();
          cleanup();
        } catch (err) {
          cleanup();
          var popup = window.open(url, "_blank");
          if (!popup) {
            reject(err);
            return;
          }
          popup.onload = function () {
            popup.focus();
            popup.print();
            resolve();
          };
        }
      };

      iframe.onerror = function () {
        cleanup();
        reject(new Error("Could not load PDF for printing"));
      };

      document.body.appendChild(iframe);
    });
  }

  function openMailto(subject, body) {
    window.location.href =
      "mailto:?subject=" +
      encodeURIComponent(subject) +
      "&body=" +
      encodeURIComponent(body);
  }

  function setButtonBusy(btn, busy, busyLabel) {
    if (!btn) return;
    if (busy) {
      if (!btn.dataset.daabFlyerLabel) {
        btn.dataset.daabFlyerLabel = btn.textContent;
      }
      btn.disabled = true;
      btn.classList.add("flyer-btn--busy");
      btn.textContent = busyLabel || btn.dataset.daabFlyerLabel;
      return;
    }
    btn.disabled = false;
    btn.classList.remove("flyer-btn--busy");
    if (btn.dataset.daabFlyerLabel) {
      btn.textContent = btn.dataset.daabFlyerLabel;
    }
  }

  async function sendFlyerEmail() {
    var cfg = window.DAAB_FLYER_EMAIL;
    var btn = document.getElementById("flyerSendEmailBtn");
    var sheet = getFlyerExportRoot();
    if (!cfg || !btn || !sheet) return;

    setButtonBusy(btn, true, cfg.busyLabel);

    beginExportChromeHide();
    try {
      var pdfBlob = await generatePdfBlob(sheet);
      var pdfFile = new File([pdfBlob], cfg.pdfFilename, { type: "application/pdf" });

      if (navigator.share && navigator.canShare && navigator.canShare({ files: [pdfFile] })) {
        try {
          await navigator.share({
            title: cfg.subject,
            text: cfg.body,
            files: [pdfFile]
          });
        } catch (shareErr) {
          if (shareErr && shareErr.name === "AbortError") {
            return;
          }
          throw shareErr;
        }
        return;
      }

      downloadBlob(pdfBlob, cfg.pdfFilename);
      openMailto(cfg.subject, cfg.body);
    } catch (err) {
      console.error("[daab-membership-flyer-email]", err);
      if (cfg.errorAlert) {
        window.alert(cfg.errorAlert);
      }
      openMailto(cfg.subject, cfg.body);
    } finally {
      endExportChromeHide();
      setButtonBusy(btn, false);
    }
  }

  async function printFlyerPdf() {
    var cfg = window.DAAB_FLYER_EMAIL || {};
    var btn = document.getElementById("flyerPrintPdfBtn");
    var sheet = getFlyerExportRoot();
    if (!btn || !sheet) return;

    setButtonBusy(btn, true, cfg.busyLabel);

    beginExportChromeHide();
    try {
      var pdfBlob = await generatePdfBlob(sheet);
      await printPdfBlob(pdfBlob, cfg.pdfFilename);
    } catch (err) {
      console.error("[daab-membership-flyer-email]", err);
      window.alert(
        cfg.printErrorAlert ||
          cfg.errorAlert ||
          "Could not prepare the flyer PDF for printing."
      );
    } finally {
      endExportChromeHide();
      setButtonBusy(btn, false);
    }
  }

  function initPrintChromeHandlers() {
    if (!document.querySelector(".flyer-sheet")) return;
    if (window.__daabFlyerPrintHandlersInit) return;
    window.__daabFlyerPrintHandlersInit = true;

    function onBeforePrint() {
      beginExportChromeHide();
    }

    function onAfterPrint() {
      endExportChromeHide();
    }

    window.addEventListener("beforeprint", onBeforePrint);
    window.addEventListener("afterprint", onAfterPrint);

    if (window.matchMedia) {
      var printMq = window.matchMedia("print");
      var onPrintMq = function (event) {
        if (event.matches) {
          onBeforePrint();
        } else {
          onAfterPrint();
        }
      };
      if (typeof printMq.addEventListener === "function") {
        printMq.addEventListener("change", onPrintMq);
      } else if (typeof printMq.addListener === "function") {
        printMq.addListener(onPrintMq);
      }
    }
  }

  function init() {
    initPrintChromeHandlers();

    var shareBtn = document.getElementById("flyerSendEmailBtn");
    if (shareBtn && shareBtn.getAttribute("data-daab-flyer-email-init") !== "1") {
      shareBtn.setAttribute("data-daab-flyer-email-init", "1");
      shareBtn.addEventListener("click", function () {
        sendFlyerEmail();
      });
    }

    var printBtn = document.getElementById("flyerPrintPdfBtn");
    if (printBtn && printBtn.getAttribute("data-daab-flyer-print-init") !== "1") {
      printBtn.setAttribute("data-daab-flyer-print-init", "1");
      printBtn.addEventListener("click", function () {
        printFlyerPdf();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
