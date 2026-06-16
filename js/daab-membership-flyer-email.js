/**
 * Membership / sponsorship flyer — PDF export (Print/Share).
 * html2canvas + jsPDF load on first PDF action (not on page load).
 */
(function () {
  "use strict";

  var A4_WIDTH_PX = Math.round((210 / 25.4) * 96);
  var PDF_CAPTURE_SCALE = 2;
  var EXPORT_CLASS = "flyer-sheet--pdf-export";
  var exportBusy = false;
  var pendingShareBlob = null;
  var pdfLibsPromise = null;

  function assetRoot() {
    var html = document.documentElement;
    var fromAttr = html && html.getAttribute("data-daab-asset-root");
    if (fromAttr) return fromAttr;
    var path = (location.pathname || "").replace(/\\/g, "/");
    if (/\/(az|en)\/forum\//.test(path)) return "../../../";
    if (/\/(az|en)\//.test(path)) return "../";
    return "";
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[src="' + src + '"]');
      if (existing) {
        if (existing.getAttribute("data-daab-loaded") === "1") {
          resolve();
          return;
        }
        existing.addEventListener("load", function () { resolve(); }, { once: true });
        existing.addEventListener("error", function () { reject(fail("Script failed: " + src)); }, { once: true });
        return;
      }
      var script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.onload = function () {
        script.setAttribute("data-daab-loaded", "1");
        resolve();
      };
      script.onerror = function () {
        reject(fail("Script failed: " + src));
      };
      document.head.appendChild(script);
    });
  }

  function ensurePdfLibs() {
    if (libsReady()) return Promise.resolve();
    if (pdfLibsPromise) return pdfLibsPromise;
    var root = assetRoot();
    pdfLibsPromise = loadScript(root + "js/vendor/html2canvas.min.js").then(function () {
      return loadScript(root + "js/vendor/jspdf.umd.min.js");
    });
    return pdfLibsPromise;
  }

  function getFlyerCfg() {
    return window.DAAB_FLYER_EMAIL || {};
  }

  function getFlyerExportRoot() {
    return document.querySelector(".flyer-sheet");
  }

  function getJsPDFConstructor() {
    if (window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
    if (typeof window.jsPDF === "function") return window.jsPDF;
    return null;
  }

  function libsReady() {
    return !!(window.html2canvas && getJsPDFConstructor());
  }

  function fail(message) {
    return new Error(message);
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      window.setTimeout(resolve, ms);
    });
  }

  function waitForLayout() {
    return new Promise(function (resolve) {
      requestAnimationFrame(function () {
        requestAnimationFrame(resolve);
      });
    });
  }

  function waitForFonts() {
    if (document.fonts && document.fonts.ready) {
      return Promise.race([document.fonts.ready, wait(8000)]);
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

  var EXPORT_CHROME_SELECTORS = [
    "#daab-breadcrumbs",
    "nav.daab-breadcrumbs",
    ".daab-breadcrumbs"
  ];

  var activeExportChromeHide = null;

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
    if (!hidden) return;
    hidden.forEach(function (item) {
      if (!item.el) return;
      if (item.visibility) item.el.style.setProperty("visibility", item.visibility);
      else item.el.style.removeProperty("visibility");
    });
  }

  function beginExportChromeHide() {
    if (!activeExportChromeHide) activeExportChromeHide = hideExportChrome();
    return activeExportChromeHide;
  }

  function endExportChromeHide() {
    if (!activeExportChromeHide) return;
    restoreExportChrome(activeExportChromeHide);
    activeExportChromeHide = null;
  }

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
        console.warn("[daab-membership-flyer-email] image copy:", err);
      }
    });
  }

  function createExportClone(sourceSheet) {
    var existing = document.getElementById("daab-flyer-export-stage");
    if (existing) existing.remove();

    var stage = document.createElement("div");
    stage.id = "daab-flyer-export-stage";
    stage.setAttribute("aria-hidden", "true");

    var clone = sourceSheet.cloneNode(true);
    clone.removeAttribute("id");
    clone.classList.add(EXPORT_CLASS);
    copyLoadedImagesFromSource(clone, sourceSheet);
    stage.appendChild(clone);
    document.body.appendChild(stage);
    return { stage: stage, sheet: clone };
  }

  function removeExportStage(stage) {
    if (stage && stage.parentNode) stage.parentNode.removeChild(stage);
  }

  function measureSheet(sheet) {
    sheet.style.setProperty("height", "auto", "important");
    sheet.style.setProperty("overflow", "visible", "important");
    return {
      width: Math.max(sheet.offsetWidth, sheet.scrollWidth, A4_WIDTH_PX),
      height: Math.max(sheet.scrollHeight, sheet.offsetHeight, sheet.getBoundingClientRect().height, 1)
    };
  }

  function captureSheet(sheet, opts) {
    var dims = measureSheet(sheet);
    return window.html2canvas(sheet, {
      scale: PDF_CAPTURE_SCALE,
      useCORS: true,
      allowTaint: !!(opts && opts.allowTaint),
      logging: false,
      backgroundColor: "#ffffff",
      scrollX: 0,
      scrollY: 0,
      width: dims.width,
      height: dims.height,
      windowWidth: dims.width,
      windowHeight: dims.height + 32,
      x: 0,
      y: 0
    });
  }

  async function captureExportCanvas(exportSheet) {
    try {
      return await captureSheet(exportSheet, { allowTaint: false });
    } catch (err) {
      console.warn("[daab-membership-flyer-email] strict capture failed, retrying:", err);
      return captureSheet(exportSheet, { allowTaint: true });
    }
  }

  function canvasToA4PdfBlob(canvas) {
    var JsPDF = getJsPDFConstructor();
    if (!JsPDF) throw fail("jsPDF library is not loaded.");

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
    var fit = Math.min(pageW / imgWmm, pageH / imgHmm);
    var drawW = imgWmm * fit;
    var drawH = imgHmm * fit;

    pdf.addImage(
      canvas.toDataURL("image/jpeg", 0.98),
      "JPEG",
      (pageW - drawW) / 2,
      (pageH - drawH) / 2,
      drawW,
      drawH,
      undefined,
      "FAST"
    );

    return pdf.output("blob");
  }

  async function generatePdfBlob(sourceSheet) {
    await ensurePdfLibs();

    await waitForFonts();
    var stageRef = createExportClone(sourceSheet);
    try {
      await waitForImages(stageRef.sheet);
      await waitForLayout();
      await wait(150);
      await waitForLayout();

      var dims = measureSheet(stageRef.sheet);
      if (dims.height < 200) {
        throw fail("Flyer layout was not ready for export (height=" + dims.height + ").");
      }

      var canvas = await captureExportCanvas(stageRef.sheet);
      if (!canvas || canvas.width < 10 || canvas.height < 10) {
        throw fail("PDF capture returned an empty image.");
      }
      return canvasToA4PdfBlob(canvas);
    } finally {
      removeExportStage(stageRef.stage);
    }
  }

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = filename || "flyer.pdf";
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () {
      URL.revokeObjectURL(url);
    }, 180000);
    return url;
  }

  function preparePrintWindow() {
    var win = window.open("", "_blank");
    if (!win) return null;
    try {
      win.document.title = "Preparing PDF…";
      win.document.body.style.cssText = "font-family:Arial,sans-serif;padding:24px;";
      win.document.body.innerHTML = "<p>Preparing flyer PDF for print…</p>";
    } catch (err) {
      // Ignore cross-window write issues and continue.
    }
    return win;
  }

  function openPdfInPrintWindow(printWin, blob) {
    if (!printWin || printWin.closed) return false;
    var url = URL.createObjectURL(blob);
    try {
      var doc = printWin.document;
      doc.open();
      doc.write(
        "<!doctype html><html><head><meta charset=\"utf-8\"><title>Flyer PDF</title>" +
          "<style>html,body{height:100%;margin:0;background:#111}#pdf{width:100%;height:100%;border:0}</style>" +
          "</head><body><iframe id=\"pdf\" src=\"" +
          url +
          "\" title=\"Flyer PDF\"></iframe></body></html>"
      );
      doc.close();

      var printed = false;
      var triggerPrint = function () {
        if (printed || printWin.closed) return;
        printed = true;
        try {
          var frameWin = frame && frame.contentWindow ? frame.contentWindow : null;
          if (frameWin) {
            frameWin.focus();
            frameWin.print();
            return;
          }
          printWin.focus();
          printWin.print();
        } catch (err) {
          console.warn("[daab-membership-flyer-email] print:", err);
        }
      };
      var frame = doc.getElementById("pdf");
      if (frame && typeof frame.addEventListener === "function") {
        frame.addEventListener(
          "load",
          function () {
            // Let built-in PDF viewer settle before opening print dialog.
            window.setTimeout(triggerPrint, 400);
          },
          { once: true }
        );
      }
      // Fallback for browsers where iframe load isn't fired for PDF viewers.
      window.setTimeout(triggerPrint, 2500);
      window.setTimeout(function () {
        URL.revokeObjectURL(url);
      }, 300000);
      return true;
    } catch (err) {
      console.warn("[daab-membership-flyer-email] print window:", err);
      try {
        printWin.close();
      } catch (closeErr) {
        // Ignore close failures.
      }
      URL.revokeObjectURL(url);
      return false;
    }
  }

  function buildPdfFile(pdfBlob, cfg) {
    var filename = cfg.pdfFilename || "flyer.pdf";
    return new File([pdfBlob], filename, { type: "application/pdf" });
  }

  function isShareContextSecure() {
    if (window.isSecureContext) return true;
    var host = (window.location && window.location.hostname) || "";
    return host === "localhost" || host === "127.0.0.1" || host === "::1";
  }

  function canSharePdfFile(pdfFile) {
    if (!navigator.share || !pdfFile || !isShareContextSecure()) return false;
    if (typeof navigator.canShare !== "function") return true;
    try {
      // Some browsers return false negatives here; we still try navigator.share() next.
      return navigator.canShare({ files: [pdfFile] });
    } catch (err) {
      return true;
    }
  }

  async function openNativeShareSheet(pdfFile, cfg) {
    return navigator.share({
      title: cfg.subject || "",
      text: cfg.body || "",
      files: [pdfFile]
    });
  }

  async function sharePdfNative(pdfBlob, cfg) {
    var filename = cfg.pdfFilename || "flyer.pdf";
    var pdfFile = buildPdfFile(pdfBlob, cfg);
    var fallbackMsg =
      cfg.shareFallbackAlert ||
      cfg.printFallbackAlert ||
      "Sharing is not available here. The PDF was downloaded instead.";

    if (!navigator.share) {
      downloadBlob(pdfBlob, filename);
      window.alert(fallbackMsg);
      return;
    }

    if (!isShareContextSecure()) {
      downloadBlob(pdfBlob, filename);
      window.alert(
        cfg.shareSecureContextAlert ||
          "Sharing requires a secure connection (HTTPS). The PDF was downloaded instead."
      );
      return;
    }

    try {
      var shareStarted = Date.now();
      await openNativeShareSheet(pdfFile, cfg);
      pendingShareBlob = null;
      return;
    } catch (err) {
      if (err && err.name === "AbortError") {
        // If sheet opened and user cancelled, stop quietly.
        if (Date.now() - shareStarted > 500) {
          pendingShareBlob = null;
          return;
        }
        // Quick AbortError often means user activation expired before sheet opened.
        pendingShareBlob = pdfBlob;
        window.alert(
          cfg.shareReadyConfirm ||
            "PDF is ready. Tap Share once more to open the system sharing menu."
        );
        return;
      }

      if (err && err.name === "NotAllowedError") {
        pendingShareBlob = pdfBlob;
        window.alert(
          cfg.shareReadyConfirm ||
            "PDF is ready. Tap Share once more to open the system sharing menu."
        );
        return;
      }

      // canShare false or TypeError may still indicate unsupported file sharing.
      if (
        (typeof navigator.canShare === "function" && !canSharePdfFile(pdfFile)) ||
        (err && (err.name === "TypeError" || err.name === "DataError"))
      ) {
        pendingShareBlob = null;
        downloadBlob(pdfBlob, filename);
        window.alert(fallbackMsg);
        return;
      }

      console.warn("[daab-membership-flyer-email] share:", err);
      throw err;
    }
  }

  function setButtonBusy(btn, busy, busyLabel) {
    if (!btn) return;
    if (busy) {
      if (!btn.dataset.daabFlyerLabel) btn.dataset.daabFlyerLabel = btn.textContent;
      btn.disabled = true;
      btn.classList.add("flyer-btn--busy");
      btn.textContent = busyLabel || btn.dataset.daabFlyerLabel;
      return;
    }
    btn.disabled = false;
    btn.classList.remove("flyer-btn--busy");
    if (btn.dataset.daabFlyerLabel) btn.textContent = btn.dataset.daabFlyerLabel;
  }

  function showError(cfg, key, err) {
    console.error("[daab-membership-flyer-email]", err);
    var msg =
      cfg[key] ||
      cfg.errorAlert ||
      (err && err.message) ||
      "Could not create the flyer PDF.";
    window.alert(msg);
  }

  async function withExportLock(fn) {
    if (exportBusy) return;
    exportBusy = true;
    try {
      return await fn();
    } finally {
      exportBusy = false;
    }
  }

  async function sendFlyerEmail() {
    var cfg = getFlyerCfg();
    var btn = document.getElementById("flyerSendEmailBtn");
    var sheet = getFlyerExportRoot();
    if (!btn || !sheet) return;

    if (pendingShareBlob) {
      var retryBlob = pendingShareBlob;
      try {
        await sharePdfNative(retryBlob, cfg);
      } catch (retryErr) {
        showError(cfg, "errorAlert", retryErr);
      }
      return;
    }

    var pdfBlob = null;
    await withExportLock(async function () {
      setButtonBusy(btn, true, cfg.busyLabel);
      try {
        pdfBlob = await generatePdfBlob(sheet);
      } catch (err) {
        showError(cfg, "errorAlert", err);
      } finally {
        setButtonBusy(btn, false);
      }
    });

    if (!pdfBlob) return;

    try {
      await sharePdfNative(pdfBlob, cfg);
    } catch (err) {
      showError(cfg, "errorAlert", err);
    }
  }

  async function printFlyerPdf() {
    var cfg = getFlyerCfg();
    var btn = document.getElementById("flyerPrintPdfBtn");
    var sheet = getFlyerExportRoot();
    if (!btn || !sheet) return;

    await withExportLock(async function () {
      setButtonBusy(btn, true, cfg.busyLabel);
      beginExportChromeHide();
      try {
        var pdfBlob = await generatePdfBlob(sheet);
        // Deterministic single-page export from jsPDF pipeline.
        downloadBlob(pdfBlob, cfg.pdfFilename);
      } catch (err) {
        showError(cfg, "printErrorAlert", err);
      } finally {
        endExportChromeHide();
        setButtonBusy(btn, false);
      }
    });
  }

  function init() {
    if (!document.querySelector(".flyer-sheet")) return;

    var shareBtn = document.getElementById("flyerSendEmailBtn");
    if (shareBtn && shareBtn.getAttribute("data-daab-flyer-email-init") !== "1") {
      shareBtn.setAttribute("data-daab-flyer-email-init", "1");
      shareBtn.addEventListener("click", function () {
        sendFlyerEmail().catch(function (err) {
          showError(getFlyerCfg(), "errorAlert", err);
        });
      });
    }

    var printBtn = document.getElementById("flyerPrintPdfBtn");
    if (printBtn && printBtn.getAttribute("data-daab-flyer-print-init") !== "1") {
      printBtn.setAttribute("data-daab-flyer-print-init", "1");
      printBtn.addEventListener("click", function () {
        printFlyerPdf().catch(function (err) {
          showError(getFlyerCfg(), "printErrorAlert", err);
        });
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
