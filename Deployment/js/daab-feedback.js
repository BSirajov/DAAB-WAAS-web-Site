/**
 * Website feedback form: validation, respectful-language check, and mail submit.
 * Language matching uses Unicode letter boundaries (see i18n/feedback-language.json).
 */
(function (root, factory) {
  var api = factory();
  root.DAAB_FEEDBACK = api;
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        api.start();
      });
    } else {
      api.start();
    }
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var MAX_FILE = 5 * 1024 * 1024;
  var FILE_EXT = { jpg: 1, jpeg: 1, png: 1, webp: 1, gif: 1, pdf: 1 };
  var sendState = "idle";
  var lexicon = [];
  var thumbUrl = "";

  var COPY = {
    az: {
      nameRequired: "Ad mütləqdir.",
      nameInvalid: "Zəhmət olmasa adı hərflərlə yazın.",
      unsafe: "Zəhmət olmasa bunu adi dildə yazın. Kod və sayta zərər verə biləcək mətn göndərilə bilməz.",
      emailInvalid: "Zəhmət olmasa etibarlı e-poçt ünvanı daxil edin.",
      emailRequired: "E-poçt ünvanı mütləqdir.",
      subjectRequired: "Mövzu mütləqdir.",
      messageRequired: "Rəy mətni mütləqdir.",
      typeRequired: "Rəyin növünü seçin.",
      urlInvalid: "Səhifə ünvanı http və ya https ilə başlamalıdır.",
      privacyRequired: "Davam etmək üçün məxfilik bildirişini təsdiq edin.",
      fileType: "Əlavə JPG, PNG, WEBP, GIF və ya PDF olmalıdır.",
      fileSize: "Əlavə 5 MB-dan böyük ola bilməz.",
      language: "Zəhmət olmasa, nəzakətli ifadələrdən istifadə edin. Göndərməzdən əvvəl işarələnmiş xanadakı təhqiramiz və ya nalayiq ifadələri düzəldin.",
      respect: "Zəhmət olmasa, nəzakətli ifadələrdən istifadə edin. Göndərməzdən əvvəl işarələnmiş xanadakı təhqiramiz və ya nalayiq ifadələri düzəldin.",
      submitting: "Göndərilir…",
      submit: "Rəyinizi göndərin",
      submitFailed: "Rəy göndərilmədi. Məlumatlarınız formada qalıb — yenidən cəhd edin.",
      phpUnavailable: "Bu baxış serveri e-poçt göndərə bilmir. Canlı saytda rəy info@daab-waas.com ünvanına çatdırılır. Məlumatlarınız formada qalıb.",
      networkError: "Bağlantı kəsildi. Məlumatlarınız formada qalıb — yenidən cəhd edin.",
      fileReady: "Göndərməyə hazırdır",
      successReply: "Göstərdiyiniz e-poçt ünvanına cavab yazacağıq."
    },
    en: {
      nameRequired: "A name is required.",
      nameInvalid: "Please enter your name using letters.",
      unsafe: "Please rewrite this in plain language. Code and other text that could harm the site cannot be sent.",
      emailInvalid: "Please enter a valid email address.",
      emailRequired: "An email address is required.",
      subjectRequired: "Subject is required.",
      messageRequired: "Your feedback is required.",
      typeRequired: "Choose a feedback type.",
      urlInvalid: "The page address must start with http:// or https://.",
      privacyRequired: "Please confirm the privacy notice before sending.",
      fileType: "The attachment must be a JPG, PNG, WEBP, GIF, or PDF file.",
      fileSize: "The attachment must be 5 MB or smaller.",
      language: "Please use respectful language. Review the highlighted field and remove any offensive or abusive wording before submitting.",
      respect: "Please use respectful language. Review the highlighted field and remove any offensive or abusive wording before submitting.",
      submitting: "Sending…",
      submit: "Send your feedback",
      submitFailed: "Your feedback could not be sent. What you entered is still in the form — please try again.",
      phpUnavailable: "This preview server cannot send email. On the live site, feedback is delivered to info@daab-waas.com. What you entered is still in the form.",
      networkError: "The connection failed. What you entered is still in the form — please try again.",
      fileReady: "Ready to submit",
      successReply: "We will reply to the email address you provided."
    }
  };

  function byId(id) {
    return document.getElementById(id);
  }

  function lang() {
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    return explicit === "az" ? "az" : "en";
  }

  function text(key) {
    var pack = COPY[lang()] || COPY.en;
    return pack[key] || COPY.en[key] || "";
  }

  function assetRoot() {
    return document.documentElement.getAttribute("data-daab-asset-root") || "../";
  }

  function isWordChar(ch) {
    return /[\p{L}\p{N}_]/u.test(ch || "");
  }

  function foldChar(ch) {
    if (ch === "İ") return "i";
    var lower = ch.toLowerCase();
    return lower.length === 1 ? lower : ch;
  }

  function charsOf(value) {
    var out = [];
    for (var i = 0; i < value.length; ) {
      var cp = value.codePointAt(i);
      var ch = String.fromCodePoint(cp);
      out.push(ch);
      i += ch.length;
    }
    return out;
  }

  function foldString(value) {
    return charsOf(value).map(foldChar).join("");
  }

  function loadTerms(data) {
    var grouped = data && data.terms ? data.terms : {};
    var seen = {};
    var terms = [];
    Object.keys(grouped).forEach(function (key) {
      (grouped[key] || []).forEach(function (term) {
        var folded = foldString(String(term || ""));
        if (folded.length < 3 || seen[folded]) return;
        seen[folded] = 1;
        terms.push(folded);
      });
    });
    return terms;
  }

  function findTermHits(foldedChars, termChars) {
    var hits = [];
    var len = termChars.length;
    if (len < 3 || len > foldedChars.length) return hits;
    var from = 0;
    while (from <= foldedChars.length - len) {
      var same = true;
      for (var i = 0; i < len; i++) {
        if (foldedChars[from + i] !== termChars[i]) {
          same = false;
          break;
        }
      }
      if (same) {
        var before = from > 0 ? foldedChars[from - 1] : "";
        var after = from + len < foldedChars.length ? foldedChars[from + len] : "";
        if (!isWordChar(before) && !isWordChar(after)) {
          hits.push({ start: from, end: from + len });
        }
        from += len;
      } else {
        from += 1;
      }
    }
    return hits;
  }

  function languageSpans(value, terms) {
    terms = terms || lexicon;
    if (!value || !terms.length) return [];
    var foldedChars = charsOf(value).map(foldChar);
    var hits = [];
    terms.forEach(function (term) {
      findTermHits(foldedChars, charsOf(term)).forEach(function (hit) {
        hits.push(hit);
      });
    });

    var collapsed = [];
    var collapsedMap = [];
    var i = 0;
    while (i < foldedChars.length) {
      var j = i + 1;
      while (j < foldedChars.length && foldedChars[j] === foldedChars[i]) j += 1;
      if (j - i >= 3) {
        collapsed.push(foldedChars[i]);
        collapsedMap.push([i, j]);
      } else {
        for (var k = i; k < j; k++) {
          collapsed.push(foldedChars[k]);
          collapsedMap.push([k, k + 1]);
        }
      }
      i = j;
    }
    terms.forEach(function (term) {
      if (term.indexOf(" ") !== -1) return;
      findTermHits(collapsed, charsOf(term)).forEach(function (hit) {
        hits.push({
          start: collapsedMap[hit.start][0],
          end: collapsedMap[hit.end - 1][1]
        });
      });
    });

    var leet = { "@": "a", "0": "o", "1": "i", "3": "e", $: "s", "5": "s", "4": "a", "7": "t" };
    var single = {};
    terms.forEach(function (term) {
      if (term.indexOf(" ") === -1) single[term] = 1;
    });
    var raw = charsOf(value);
    var tokenStart = null;
    for (var p = 0; p <= raw.length; p++) {
      var ch = p < raw.length ? raw[p] : " ";
      var isSpace = ch === " " || ch === "\n" || ch === "\t" || ch === "\r";
      if (!isSpace && tokenStart === null) tokenStart = p;
      if (isSpace && tokenStart !== null) {
        var letters = "";
        var hasSymbol = false;
        for (var t = tokenStart; t < p; t++) {
          var mapped = leet[raw[t]] || leet[foldChar(raw[t])];
          if (mapped) {
            hasSymbol = true;
            letters += mapped;
            continue;
          }
          var folded = foldChar(raw[t]);
          if (isWordChar(folded)) letters += folded;
          else hasSymbol = true;
        }
        if (hasSymbol && single[letters] && letters.length >= 3) {
          hits.push({ start: tokenStart, end: p });
        }
        tokenStart = null;
      }
    }

    hits.sort(function (a, b) {
      return b.end - b.start - (a.end - a.start) || a.start - b.start;
    });
    var kept = [];
    hits.forEach(function (hit) {
      var overlap = kept.some(function (prev) {
        return hit.start < prev.end && hit.end > prev.start;
      });
      if (!overlap) kept.push(hit);
    });
    kept.sort(function (a, b) {
      return a.start - b.start;
    });
    return kept;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function renderHighlight(field, spans) {
    var wrap = field && field.closest ? field.closest(".feedback-hl") : null;
    if (!wrap) return;
    var back = wrap.querySelector(".feedback-hl__back");
    if (!spans || !spans.length) {
      wrap.classList.remove("is-flagged");
      field.removeAttribute("aria-invalid");
      if (back) back.innerHTML = "";
      return;
    }
    var value = field.value || "";
    var chars = charsOf(value);
    var html = "";
    var cursor = 0;
    spans.forEach(function (span) {
      html += escapeHtml(chars.slice(cursor, span.start).join(""));
      html += '<mark class="feedback-lang-hit">' + escapeHtml(chars.slice(span.start, span.end).join("")) + "</mark>";
      cursor = span.end;
    });
    html += escapeHtml(chars.slice(cursor).join(""));
    if (field.tagName === "TEXTAREA") html += "\n";
    wrap.classList.add("is-flagged");
    field.setAttribute("aria-invalid", "true");
    if (back) {
      back.innerHTML = html;
      back.scrollTop = field.scrollTop;
      back.scrollLeft = field.scrollLeft;
    }
  }

  function showStatus(message, isError) {
    var box = byId("app-submit-status");
    if (!box) return;
    box.hidden = false;
    box.className = "app-submit-status" + (isError ? " app-submit-status--error" : "");
    box.textContent = message;
    box.setAttribute("role", isError ? "alert" : "status");
  }

  function clearStatus() {
    var box = byId("app-submit-status");
    if (!box) return;
    box.hidden = true;
    box.textContent = "";
    box.className = "app-submit-status";
  }

  function clearFieldNote(field) {
    if (!field) return;
    var note = field.parentNode && field.parentNode.querySelector
      ? field.parentNode.querySelector(".field-required-warning")
      : null;
    var group = field.closest ? field.closest(".field-group, .app-file-card, .opt-item") : null;
    if (!note && group) note = group.querySelector(".field-required-warning");
    if (note && note.parentNode) note.parentNode.removeChild(note);
    field.classList.remove("is-required-invalid");
  }

  function warn(field, message) {
    showStatus(message, true);
    if (!field) return;
    clearFieldNote(field);
    field.classList.add("is-required-invalid");
    field.setAttribute("aria-invalid", "true");
    var group = field.closest(".field-group, .app-file-card, .opt-item") || field.parentNode;
    var note = document.createElement("p");
    note.className = "field-required-warning";
    note.textContent = message;
    group.appendChild(note);
    try {
      field.focus({ preventScroll: true });
    } catch (e) {
      field.focus();
    }
    if (field.scrollIntoView) field.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function clearWarnings() {
    clearStatus();
    document.querySelectorAll(".field-required-warning").forEach(function (node) {
      if (node.parentNode) node.parentNode.removeChild(node);
    });
    document.querySelectorAll(".is-required-invalid, [aria-invalid='true']").forEach(function (node) {
      node.classList.remove("is-required-invalid");
      if (!node.closest(".feedback-hl.is-flagged")) node.removeAttribute("aria-invalid");
    });
  }

  function emailOk(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(value || "").trim());
  }

  function nameOk(value) {
    return /^[\p{L}\p{M}][\p{L}\p{M} .'’-]*$/u.test(String(value || "").trim());
  }

  function textUnsafe(value) {
    var text = String(value || "");
    if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/.test(text)) return true;
    if (/<\s*\/?\s*[a-z!]/i.test(text)) return true;
    if (/(?:javascript|vbscript|data)\s*:/i.test(text)) return true;
    if (/<\?(?:php|=)?|<%/i.test(text)) return true;
    if (/\bon(?:error|load|click|mouseover|focus)\s*=/i.test(text)) return true;
    if (/%3c|&#x?0*60;|&lt;/i.test(text)) return true;
    var folded = text.toLowerCase();
    return (
      /\bunion\s+select\b/.test(folded) ||
      /\bdrop\s+table\b/.test(folded) ||
      /\binsert\s+into\b/.test(folded) ||
      /\bdelete\s+from\b/.test(folded) ||
      /\binformation_schema\b/.test(folded) ||
      /\bxp_cmdshell\b/.test(folded) ||
      /\binto\s+outfile\b/.test(folded) ||
      /\bload_file\s*\(/.test(folded) ||
      /\bor\s+1\s*=\s*1\b/.test(folded) ||
      /'\s*or\b/.test(folded) ||
      /['"]\s*;\s*--/.test(folded) ||
      /\b(?:sleep|benchmark)\s*\(/.test(folded) ||
      /\b(?:exec|execute)\s*\(/.test(folded)
    );
  }

  function urlOk(value) {
    var v = String(value || "").trim();
    if (!v) return true;
    if (v.length > 500 || /\s/.test(v)) return false;
    if (/^(javascript|data):/i.test(v)) return false;
    if (v.charAt(0) === "/") return v.charAt(1) !== "/";
    try {
      var url = new URL(v);
      return url.protocol === "http:" || url.protocol === "https:";
    } catch (e) {
      return false;
    }
  }

  function selectedFile() {
    var input = byId("attachment");
    return input && input.files && input.files[0] ? input.files[0] : null;
  }

  function fileError(file) {
    if (!file) return "";
    var name = String(file.name || "");
    var ext = name.indexOf(".") >= 0 ? name.split(".").pop().toLowerCase() : "";
    if (/\.(php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i.test(name)) {
      return text("fileType");
    }
    if (!FILE_EXT[ext]) return text("fileType");
    if (file.size > MAX_FILE) return text("fileSize");
    return "";
  }

  function setFileError(message) {
    var el = byId("attachment-error");
    var card = document.querySelector(".app-file-card");
    if (el) {
      el.hidden = !message;
      el.textContent = message || "";
    }
    if (card) card.classList.toggle("is-required-invalid", !!message);
  }

  function syncFileCard() {
    var file = selectedFile();
    var status = byId("attachment-status");
    var card = document.querySelector(".app-file-card");
    if (thumbUrl) {
      URL.revokeObjectURL(thumbUrl);
      thumbUrl = "";
    }
    if (!file) {
      if (status) status.hidden = true;
      if (card) card.classList.remove("is-selected");
      setFileError("");
      return;
    }
    var error = fileError(file);
    setFileError(error);
    if (status) {
      status.hidden = false;
      var name = status.querySelector(".app-file-name");
      var ready = status.querySelector(".app-file-ready");
      if (name) name.textContent = file.name;
      if (ready) ready.textContent = error ? "" : text("fileReady");
    }
    if (card) card.classList.add("is-selected");
    var thumb = byId("attachment-thumb");
    if (thumb && /^image\//.test(file.type)) {
      thumbUrl = URL.createObjectURL(file);
      thumb.src = thumbUrl;
      thumb.hidden = false;
    } else if (thumb) {
      thumb.hidden = true;
      thumb.removeAttribute("src");
    }
  }

  function prefillUrl() {
    var field = byId("related-url");
    if (!field || field.value.trim()) return;
    var params = new URLSearchParams(window.location.search);
    var incoming = params.get("url") || params.get("page") || "";
    if (incoming && urlOk(incoming)) field.value = incoming;
  }

  function setSubmitting(on) {
    var btn = byId("appSubmitBtn");
    var form = byId("feedbackForm");
    if (btn) {
      btn.disabled = on;
      btn.classList.toggle("is-loading", on);
      btn.textContent = on ? text("submitting") : text("submit");
    }
    if (form) form.setAttribute("aria-busy", on ? "true" : "false");
  }

  function showSuccess() {
    document.querySelectorAll(".feedback-page .form-section").forEach(function (section) {
      section.hidden = true;
    });
    var success = byId("success");
    var extra = byId("success-reply");
    if (extra) extra.hidden = true;
    if (success) {
      success.classList.add("active");
      success.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function validateFields() {
    var type = byId("feedback-type");
    var subject = byId("subject");
    var message = byId("message");
    var name = byId("name");
    var email = byId("email");
    var url = byId("related-url");
    var privacy = byId("privacyconfirm");
    if (!name || !name.value.trim()) {
      warn(name, text("nameRequired"));
      return false;
    }
    if (!nameOk(name.value)) {
      warn(name, text("nameInvalid"));
      return false;
    }
    if (textUnsafe(name.value)) {
      warn(name, text("unsafe"));
      return false;
    }
    if (!email || !email.value.trim()) {
      warn(email, text("emailRequired"));
      return false;
    }
    if (!emailOk(email.value)) {
      warn(email, text("emailInvalid"));
      return false;
    }
    if (!type || !type.value) {
      warn(type, text("typeRequired"));
      return false;
    }
    if (!subject || !subject.value.trim()) {
      warn(subject, text("subjectRequired"));
      return false;
    }
    if (textUnsafe(subject.value)) {
      warn(subject, text("unsafe"));
      return false;
    }
    if (!message || !message.value.trim()) {
      warn(message, text("messageRequired"));
      return false;
    }
    if (textUnsafe(message.value)) {
      warn(message, text("unsafe"));
      return false;
    }
    if (url && url.value.trim() && !urlOk(url.value)) {
      warn(url, text("urlInvalid"));
      return false;
    }
    var uploadError = fileError(selectedFile());
    if (uploadError) {
      setFileError(uploadError);
      warn(byId("attachment-choose") || byId("attachment"), uploadError);
      return false;
    }
    if (!privacy || !privacy.checked) {
      warn(privacy, text("privacyRequired"));
      return false;
    }
    return true;
  }

  function applyLanguageCheck() {
    if (window.daabRespectOffensive) {
      var fields = [byId("name"), byId("subject"), byId("message")];
      for (var i = 0; i < fields.length; i++) {
        var current = fields[i];
        if (!current || !String(current.value || "").trim()) continue;
        if (window.daabRespectOffensive(current.value, { nameField: current.id === "name" })) {
          warn(current, text("respect"));
          return false;
        }
      }
      return true;
    }
    var subject = byId("subject");
    var message = byId("message");
    var subjectSpans = languageSpans(subject ? subject.value : "");
    var messageSpans = languageSpans(message ? message.value : "");
    renderHighlight(subject, subjectSpans);
    renderHighlight(message, messageSpans);
    if (!subjectSpans.length && !messageSpans.length) return true;
    var field = subjectSpans.length ? subject : message;
    var spans = subjectSpans.length ? subjectSpans : messageSpans;
    warn(field, text("language"));
    if (field && spans[0] && typeof field.setSelectionRange === "function") {
      try {
        var chars = charsOf(field.value || "");
        var start = 0;
        var end = 0;
        for (var i = 0; i < chars.length; i++) {
          if (i === spans[0].start) start = end;
          end += chars[i].length;
          if (i + 1 === spans[0].end) break;
        }
        if (spans[0].start === 0) start = 0;
        field.setSelectionRange(start, end);
      } catch (e) {}
    }
    return false;
  }

  function endpoint() {
    return document.documentElement.getAttribute("data-daab-form-endpoint") || "mail-feedback.php";
  }

  function submitForm(event) {
    if (event) event.preventDefault();
    if (sendState === "sending" || sendState === "sent") return;
    var honeypot = byId("website");
    if (honeypot && String(honeypot.value || "").trim()) {
      sendState = "sent";
      showSuccess();
      return;
    }
    clearWarnings();
    renderHighlight(byId("subject"), []);
    renderHighlight(byId("message"), []);
    if (!validateFields()) return;
    if (!applyLanguageCheck()) return;

    var form = byId("feedbackForm");
    var started = byId("form-started");
    var submitted = byId("submitted-at");
    var pageUrl = byId("page-url");
    if (submitted) submitted.value = new Date().toISOString();
    if (pageUrl) pageUrl.value = window.location.href;
    if (started && !started.value) started.value = String(Date.now());

    sendState = "sending";
    setSubmitting(true);
    fetch(endpoint(), {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "text/plain, */*" }
    })
      .then(function (response) {
        return response.text().then(function (body) {
          return { ok: response.ok, status: response.status, body: String(body || "") };
        });
      })
      .then(function (result) {
        var first = result.body.trim().split(/\r?\n/)[0].toLowerCase();
        if (result.ok && first === "success") {
          sendState = "sent";
          setSubmitting(false);
          showSuccess();
          return;
        }
        sendState = "idle";
        setSubmitting(false);
        if (first === "error:language") {
          var jsonLine = result.body.trim().split(/\r?\n/).slice(1).join("\n");
          var spans = {};
          try {
            var parsed = JSON.parse(jsonLine);
            spans = parsed && parsed.spans ? parsed.spans : {};
            renderHighlight(byId("subject"), spans.subject || []);
            renderHighlight(byId("message"), spans.message || []);
          } catch (e) {
            applyLanguageCheck();
          }
          warn((spans.subject && spans.subject.length) ? byId("subject") : byId("message"), text("language"));
          return;
        }
        var map = {
          "error:name": "nameRequired",
          "error:name_invalid": "nameInvalid",
          "error:unsafe": "unsafe",
          "error:respect": "respect",
          "error:email": "emailInvalid",
          "error:email_required": "emailRequired",
          "error:subject": "subjectRequired",
          "error:message": "messageRequired",
          "error:type": "typeRequired",
          "error:url": "urlInvalid",
          "error:privacy": "privacyRequired",
          "error:file_type": "fileType",
          "error:file_size": "fileSize",
          "error:file_invalid": "fileType"
        };
        if (result.status === 404 || result.status === 405 || result.status === 501) {
          showStatus(text("phpUnavailable"), true);
          return;
        }
        if (/<\?php/.test(result.body)) {
          showStatus(text("phpUnavailable"), true);
          return;
        }
        showStatus(text(map[first] || "submitFailed"), true);
      })
      .catch(function () {
        sendState = "idle";
        setSubmitting(false);
        showStatus(text("networkError"), true);
      });
  }

  function start() {
    var form = byId("feedbackForm");
    if (!form) return;
    var started = byId("form-started");
    if (started) started.value = String(Date.now());
    prefillUrl();
    form.addEventListener("submit", submitForm);
    var choose = byId("attachment-choose");
    var input = byId("attachment");
    if (choose && input) {
      choose.addEventListener("click", function () {
        input.click();
      });
    }
    document.querySelectorAll("[data-file-target='attachment']").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (input) input.click();
      });
    });
    var remove = document.querySelector(".app-file-remove");
    if (remove && input) {
      remove.addEventListener("click", function () {
        input.value = "";
        syncFileCard();
      });
    }
    if (input) input.addEventListener("change", syncFileCard);
    ["subject", "message"].forEach(function (id) {
      var field = byId(id);
      if (!field) return;
      field.addEventListener("scroll", function () {
        var back = field.parentNode.querySelector(".feedback-hl__back");
        if (back) {
          back.scrollTop = field.scrollTop;
          back.scrollLeft = field.scrollLeft;
        }
      });
      field.addEventListener("input", function () {
        var wrap = field.closest(".feedback-hl");
        if (!wrap || sendState !== "idle") return;
        if (!wrap.classList.contains("is-flagged") && !lexicon.length) return;
        renderHighlight(field, languageSpans(field.value));
        var subjectWrap = byId("subject") && byId("subject").closest(".feedback-hl");
        var messageWrap = byId("message") && byId("message").closest(".feedback-hl");
        var stillFlagged =
          (subjectWrap && subjectWrap.classList.contains("is-flagged")) ||
          (messageWrap && messageWrap.classList.contains("is-flagged"));
        if (!stillFlagged) clearWarnings();
      });
    });
    fetch(assetRoot() + "i18n/feedback-language.json?v=1")
      .then(function (res) {
        if (!res.ok) throw new Error("lexicon");
        return res.json();
      })
      .then(function (data) {
        lexicon = loadTerms(data);
      })
      .catch(function () {
        lexicon = [];
      });
  }

  return {
    start: start,
    loadTerms: loadTerms,
    languageSpans: languageSpans,
    foldString: foldString
  };
});
