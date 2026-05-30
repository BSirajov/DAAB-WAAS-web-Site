/**
 * Membership flyer — generate PDF and open email client with invitation text.
 * mailto: cannot attach files; we download the PDF and use Web Share when available.
 */
(function () {
  "use strict";

  var HTML2PDF_URL =
    "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.2/html2pdf.bundle.min.js";

  function loadHtml2Pdf() {
    if (window.html2pdf) return Promise.resolve();
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[data-daab-html2pdf="1"]');
      if (existing) {
        existing.addEventListener("load", function () {
          resolve();
        });
        existing.addEventListener("error", reject);
        return;
      }
      var script = document.createElement("script");
      script.src = HTML2PDF_URL;
      script.defer = true;
      script.setAttribute("data-daab-html2pdf", "1");
      script.onload = function () {
        resolve();
      };
      script.onerror = function () {
        reject(new Error("Could not load PDF library"));
      };
      document.head.appendChild(script);
    });
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

  function isExportChromeNode(node) {
    if (!node || node.nodeType !== 1) return false;
    if (node.closest && node.closest("[data-flyer-export-exclude='1']")) return true;
    if (node.id === "daab-breadcrumbs") return true;
    if (node.classList && node.classList.contains("daab-breadcrumbs")) return true;
    if (node.classList && node.classList.contains("flyer-page-controls")) return true;
    return false;
  }

  function hideExportChrome() {
    var hidden = [];
    EXPORT_CHROME_SELECTORS.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (el) {
        hidden.push({ el: el, visibility: el.style.visibility });
        el.style.visibility = "hidden";
      });
    });
    return hidden;
  }

  function restoreExportChrome(hidden) {
    hidden.forEach(function (item) {
      item.el.style.visibility = item.visibility;
    });
  }

  function generatePdfBlob(sheet, filename) {
    var opt = {
      margin: [8, 8, 8, 8],
      filename: filename,
      image: { type: "jpeg", quality: 0.95 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        allowTaint: false,
        logging: false,
        letterRendering: true,
        ignoreElements: isExportChromeNode
      },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      pagebreak: { mode: ["avoid-all", "css", "legacy"] }
    };
    return window.html2pdf().set(opt).from(sheet).outputPdf("blob");
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

  function openMailto(subject, body) {
    window.location.href =
      "mailto:?subject=" +
      encodeURIComponent(subject) +
      "&body=" +
      encodeURIComponent(body);
  }

  async function sendFlyerEmail() {
    var cfg = window.DAAB_FLYER_EMAIL;
    var btn = document.getElementById("flyerSendEmailBtn");
    var sheet = getFlyerExportRoot();
    if (!cfg || !btn || !sheet) return;

    var label = btn.textContent;
    btn.disabled = true;
    btn.classList.add("flyer-btn--busy");
    btn.textContent = cfg.busyLabel || label;

    var hiddenChrome = hideExportChrome();
    try {
      await loadHtml2Pdf();
      var pdfBlob = await generatePdfBlob(sheet, cfg.pdfFilename);
      var pdfFile = new File([pdfBlob], cfg.pdfFilename, { type: "application/pdf" });

      if (navigator.share && navigator.canShare && navigator.canShare({ files: [pdfFile] })) {
        await navigator.share({
          title: cfg.subject,
          text: cfg.body,
          files: [pdfFile]
        });
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
      restoreExportChrome(hiddenChrome);
      btn.disabled = false;
      btn.classList.remove("flyer-btn--busy");
      btn.textContent = label;
    }
  }

  function init() {
    var btn = document.getElementById("flyerSendEmailBtn");
    if (!btn || btn.getAttribute("data-daab-flyer-email-init") === "1") return;
    btn.setAttribute("data-daab-flyer-email-init", "1");
    btn.addEventListener("click", function () {
      sendFlyerEmail();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
