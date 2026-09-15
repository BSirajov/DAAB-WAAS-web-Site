/**
 * Multi-step membership application form (AZ).
 */
(function () {
  "use strict";

  var totalSections = 5;

  function countFormSections() {
    var n = document.querySelectorAll(".application-page .form-section").length;
    return n > 0 ? n : 5;
  }
  var currentSection = 1;
  var cityCache = Object.create(null);
  // Capitals and local-name aliases the remote city API sometimes omits or buries.
  var CITY_GUARANTEES = {
    AT: [
      { name: "Vienna", aliases: ["Wien", "Wien Stadt", "Vienna", "Vyana", "Viyana", "Vena"] },
      { name: "Wien", aliases: ["Vienna", "Wien Stadt"] },
    ],
  };
  // Codes come from the shared js/daab-country-codes.js module.
  var COUNTRY_CODES = window.DAAB_COUNTRY_CODES || [];

  function closeOpenPickersExcept(keepPicker) {
    document.querySelectorAll(".phone-code-picker.is-open").forEach(function (p) {
      if (keepPicker && p === keepPicker) return;
      p.classList.remove("is-open");
      var pnl = p.querySelector(".phone-code-picker-panel");
      var b = p.querySelector(".phone-code-picker-btn");
      if (pnl) pnl.hidden = true;
      if (b) b.setAttribute("aria-expanded", "false");
    });
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function formKind() {
    var kind = document.documentElement.getAttribute("data-daab-form-kind");
    if (kind && kind.trim()) return kind.trim();
    var pageId = document.documentElement.getAttribute("data-daab-page-id");
    if (pageId === "forum-2026-register") return "forum-2026";
    return "membership";
  }

  function isForumRegister() {
    return formKind() === "forum-2026";
  }

  function mainFormEl() {
    return byId("forumRegisterForm") || byId("mainForm");
  }

  function detectLang() {
    // Canonical detection lives in js/daab-i18n.js (DAAB_I18N.detectLang).
    // Delegate to it when present; the inline fallback only covers the
    // (unexpected) case where daab-i18n.js failed to load.
    var I18N = window.DAAB_I18N;
    if (I18N && I18N.detectLang) return I18N.detectLang();
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "az" || explicit === "en") return explicit;
    return /\/en(\/|$)/.test(String(location.pathname).replace(/\\/g, "/")) ? "en" : "az";
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

  function applyForumIdentityValidity() {
    var requiredText = [
      ["fathername", "fatherNameRequired"],
      ["birthcountry", "birthCountryRequired"],
      ["citizenship", "citizenshipRequired"],
      ["country", "residenceCountryRequired"],
    ];
    applyDobValidity();
    requiredText.forEach(function (pair) {
      var el = byId(pair[0]);
      if (!el) return;
      el.setCustomValidity(String(el.value || "").trim() ? "" : uiText(pair[1]));
    });
    var genderFirst = byId("gender-male");
    if (genderFirst) {
      genderFirst.setCustomValidity(getRadioValue("gender") ? "" : uiText("genderRequired"));
    }
  }

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function parseDobDisplay(value) {
    var raw = String(value || "").trim();
    var m = raw.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (!m) return null;
    var day = parseInt(m[1], 10);
    var month = parseInt(m[2], 10);
    var year = parseInt(m[3], 10);
    if (year < 1900) return null;
    var dt = new Date(year, month - 1, day);
    if (dt.getFullYear() !== year || dt.getMonth() !== month - 1 || dt.getDate() !== day) return null;
    var today = new Date();
    today.setHours(23, 59, 59, 999);
    if (dt > today) return null;
    return {
      day: day,
      month: month,
      year: year,
      iso: year + "-" + pad2(month) + "-" + pad2(day),
      display: pad2(day) + "/" + pad2(month) + "/" + year,
    };
  }

  function normalizeDobTypedValue(raw) {
    var text = String(raw || "").trim();
    var iso = text.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (iso) {
      var parsedIso = parseDobDisplay(iso[3] + "/" + iso[2] + "/" + iso[1]);
      return parsedIso ? parsedIso.display : formatDobDigits(iso[3] + iso[2] + iso[1]);
    }
    var loose = text.match(/^(\d{1,2})[./-](\d{1,2})[./-](\d{4})$/);
    if (loose) {
      var parsedLoose = parseDobDisplay(pad2(loose[1]) + "/" + pad2(loose[2]) + "/" + loose[3]);
      return parsedLoose ? parsedLoose.display : formatDobDigits(loose[1] + loose[2] + loose[3]);
    }
    return formatDobDigits(text);
  }

  function formatDobDigits(raw) {
    var digits = String(raw || "").replace(/\D/g, "").slice(0, 8);
    if (digits.length <= 2) return digits;
    if (digits.length <= 4) return digits.slice(0, 2) + "/" + digits.slice(2);
    return digits.slice(0, 2) + "/" + digits.slice(2, 4) + "/" + digits.slice(4);
  }

  function applyDobValidity() {
    var dob = byId("dob");
    if (!dob) return;
    var value = String(dob.value || "").trim();
    if (!value) {
      dob.setCustomValidity(uiText("dobRequired"));
      return;
    }
    dob.setCustomValidity(parseDobDisplay(value) ? "" : uiText("dobInvalid"));
  }

  function initDobField() {
    var dob = byId("dob");
    var picker = byId("dob_picker");
    var calendarBtn = byId("dob_calendar_btn");
    if (!dob) return;

    var today = new Date();
    if (picker) {
      picker.setAttribute("max", today.getFullYear() + "-" + pad2(today.getMonth() + 1) + "-" + pad2(today.getDate()));
      picker.setAttribute("min", "1900-01-01");
    }
    if (calendarBtn) {
      calendarBtn.setAttribute("aria-label", uiText("dobCalendar"));
    }

    function syncPickerFromText() {
      if (!picker) return;
      var parsed = parseDobDisplay(dob.value);
      picker.value = parsed ? parsed.iso : "";
    }

    function openDobPicker() {
      if (!picker) return;
      syncPickerFromText();
      if (typeof picker.showPicker === "function") {
        try {
          picker.showPicker();
          return;
        } catch (err) {}
      }
      try {
        picker.focus();
        picker.click();
      } catch (err2) {}
    }

    dob.addEventListener("input", function () {
      var start = dob.selectionStart;
      var before = dob.value;
      var next = formatDobDigits(dob.value);
      if (next !== before) {
        dob.value = next;
        if (typeof start === "number") {
          var added = next.length - before.length;
          var pos = Math.max(0, start + added);
          try {
            dob.setSelectionRange(pos, pos);
          } catch (err) {}
        }
      }
      syncPickerFromText();
      applyDobValidity();
    });

    dob.addEventListener("blur", function () {
      var normalized = normalizeDobTypedValue(dob.value);
      if (normalized) dob.value = normalized;
      syncPickerFromText();
      applyDobValidity();
    });

    dob.addEventListener("paste", function (e) {
      var pasted = "";
      if (e.clipboardData) pasted = e.clipboardData.getData("text");
      if (!pasted) return;
      e.preventDefault();
      dob.value = normalizeDobTypedValue(pasted);
      syncPickerFromText();
      applyDobValidity();
    });

    if (calendarBtn) {
      calendarBtn.addEventListener("click", function (e) {
        e.preventDefault();
        openDobPicker();
      });
    }

    if (picker) {
      picker.addEventListener("change", function () {
        var iso = String(picker.value || "").trim();
        var parts = iso.match(/^(\d{4})-(\d{2})-(\d{2})$/);
        if (!parts) return;
        dob.value = parts[3] + "/" + parts[2] + "/" + parts[1];
        applyDobValidity();
        dob.dispatchEvent(new Event("change", { bubbles: true }));
      });
    }

    applyDobValidity();
  }

  function initForumIdentityValidation() {
    initDobField();
    ["fathername", "dob", "birthcountry", "citizenship", "country"].forEach(function (id) {
      var el = byId(id);
      if (!el) return;
      el.addEventListener("input", applyForumIdentityValidity);
      el.addEventListener("change", applyForumIdentityValidity);
      el.addEventListener("blur", applyForumIdentityValidity);
    });
    document.querySelectorAll('.application-page input[name="gender"]').forEach(function (radio) {
      radio.addEventListener("change", applyForumIdentityValidity);
    });
    applyForumIdentityValidity();
  }

  function validateForm() {
    var form = mainFormEl();
    if (!form) return true;
    applyForumIdentityValidity();
    var emailInput = byId("email");
    if (emailInput && !isEmailValid(emailInput.value || "")) {
      emailInput.reportValidity();
      return false;
    }
    if (!form.checkValidity()) {
      form.reportValidity();
      return false;
    }
    return true;
  }

  function isEmailValid(value) {
    var normalized = String(value || "").trim();
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(normalized);
  }

  function initEmailValidation() {
    var emailInput = byId("email");
    if (!emailInput) return;
    var lang = detectLang();
    var invalidMessage =
      lang === "az"
        ? "Zəhmət olmasa etibarlı e-məktub ünvanı daxil edin."
        : "Please enter a valid email address.";

    function applyEmailValidity() {
      if (!emailInput.value.trim()) {
        emailInput.setCustomValidity("");
        return;
      }
      emailInput.setCustomValidity(isEmailValid(emailInput.value) ? "" : invalidMessage);
    }

    emailInput.addEventListener("input", applyEmailValidity);
    emailInput.addEventListener("blur", applyEmailValidity);
    applyEmailValidity();
  }

  function getFormEndpoint() {
    var attr = document.documentElement.getAttribute("data-daab-form-endpoint");
    if (attr && attr.trim()) return attr.trim();
    var cfg = (typeof window !== "undefined" && window.DAAB_APPLICATION_CONFIG) || {};
    if (cfg.submitEndpoint && String(cfg.submitEndpoint).trim()) {
      return String(cfg.submitEndpoint).trim();
    }
    if (cfg.formspreeEndpoint && String(cfg.formspreeEndpoint).trim()) {
      return String(cfg.formspreeEndpoint).trim();
    }
    return "mail.php";
  }

  function isPhpMailEndpoint(endpoint) {
    return /\.php(\?|#|$)/i.test(String(endpoint || ""));
  }

  function isPhpHandlerUnavailable(statusCode, statusText, body) {
    if (statusCode === 404 || statusCode === 405 || statusCode === 501) return true;
    var text = String(statusText || "") + " " + String(body || "");
    return /not implemented|unsupported method|php mail handler required/i.test(text);
  }

  function buildFormDataForPhp(payload) {
    var fd = new FormData();
    Object.keys(payload).forEach(function (key) {
      if (key.charAt(0) === "_") return;
      var val = payload[key];
      if (val == null || val === "") return;
      fd.append(key, String(val));
    });
    if (isForumRegister()) {
      var cv = getSelectedUploadFile("cv");
      var photo = getSelectedUploadFile("photo");
      if (cv) fd.append("cv_file", cv, cv.name);
      if (photo) fd.append("photo_file", photo, photo.name);
    }
    return fd;
  }

  function uiText(key) {
    var lang = detectLang();
    var strings = {
      az: {
        submitting: "Göndərilir…",
        submit: "✓ Göndər",
        sciRequired: "Ən azı bir elmi sahə seçin.",
        sciLimitExceeded: "Siz ən çox iki elm sahəsi seçə bilərsiniz. Başqa birini seçməzdən əvvəl mövcud seçimlərdən birini ləğv edin.",
        degreeRequired: "Akademik dərəcənizi seçin.",
        titleRequired: "Akademik titulunuzu seçin.",
        genderRequired: "Cinsinizi seçin.",
        fatherNameRequired: "Atanızın adını daxil edin.",
        dobRequired: "Doğum tarixinizi daxil edin.",
        dobInvalid: "Tarixi dd/mm/yyyy formatında daxil edin.",
        dobCalendar: "Təqvimi aç",
        birthCountryRequired: "Doğulduğunuz ölkəni seçin.",
        citizenshipRequired: "Vətəndaşlığınızı seçin.",
        residenceCountryRequired: "Yaşadığınız ölkəni seçin.",
        privacyRequired: "Davam etmək üçün məxfilik bildirişi ilə razılaşmalısınız.",
        fileCvRequired: "CV faylını seçin.",
        filePhotoRequired: "Fotoşəkil seçin.",
        fileCvType: "CV PDF və ya DOCX formatında olmalıdır.",
        filePhotoType: "Foto JPG və ya PNG formatında olmalıdır.",
        fileCvSize: "CV faylı çox böyükdür (ən çox 8 MB).",
        filePhotoSize: "Fotoşəkil çox böyükdür (ən çox 5 MB).",
        fileCvInvalid: "CV faylı oxuna bilmədi. Başqa fayl seçin.",
        filePhotoInvalid: "Fotoşəkil oxuna bilmədi. Başqa fayl seçin.",
        fileAttachFailed: "Fayllar e-məktuba əlavə edilə bilmədi. Yenidən cəhd edin və ya info@daab-waas.com ünvanına yazın.",
        noEndpoint: isForumRegister()
          ? "Qeydiyyat serveri hələ konfiqurasiya edilməyib. Zəhmət olmasa birbaşa info@daab-waas.com ünvanına yazın."
          : "Müraciət serveri hələ konfiqurasiya edilməyib. Zəhmət olmasa birbaşa info@daab-waas.com ünvanına yazın.",
        submitFailed: isForumRegister()
          ? "Qeydiyyat göndərilmədi. Bir az sonra yenidən cəhd edin və ya info@daab-waas.com ünvanına yazın."
          : "Müraciət göndərilmədi. Bir az sonra yenidən cəhd edin və ya info@daab-waas.com ünvanına yazın.",
        networkError: "Şəbəkə xətası. İnternet bağlantınızı yoxlayın və yenidən cəhd edin.",
        expandSection: "Bölməni aç",
        collapseSection: "Bölməni yığ",
        phpUnavailable: isForumRegister()
          ? "Bu server qeydiyyatı göndərə bilmir (PHP mail işləyicisi lazımdır). Canlı saytda göndərin, və ya məlumatlarınızı info@daab-waas.com ünvanına yazın."
          : "Bu server müraciəti göndərə bilmir (PHP mail işləyicisi lazımdır). Canlı saytda göndərin, və ya məlumatlarınızı info@daab-waas.com ünvanına yazın.",
      },
      en: {
        submitting: "Submitting…",
        submit: "✓ Submit Application",
        sciRequired: "Select at least one scientific field.",
        sciLimitExceeded: "You can select up to two scientific fields. Deselect one of your current choices before selecting another.",
        degreeRequired: "Please select your academic degree.",
        titleRequired: "Please select your academic title.",
        genderRequired: "Please select your gender.",
        fatherNameRequired: "Please enter your father’s name.",
        dobRequired: "Please enter your date of birth.",
        dobInvalid: "Enter the date as dd/mm/yyyy.",
        dobCalendar: "Open calendar",
        birthCountryRequired: "Please select your country of birth.",
        citizenshipRequired: "Please select your citizenship.",
        residenceCountryRequired: "Please select your country of residence.",
        privacyRequired: "Please accept the privacy notice to continue.",
        fileCvRequired: "Please select a CV file.",
        filePhotoRequired: "Please select a photo.",
        fileCvType: "The CV must be a PDF or DOCX file.",
        filePhotoType: "The photo must be a JPG or PNG image.",
        fileCvSize: "The CV is too large (maximum 8 MB).",
        filePhotoSize: "The photo is too large (maximum 5 MB).",
        fileCvInvalid: "The CV file could not be read. Please choose another file.",
        filePhotoInvalid: "The photo could not be read. Please choose another file.",
        fileAttachFailed: "The files could not be attached to the registration email. Please try again or write to info@daab-waas.com.",
        noEndpoint: isForumRegister()
          ? "The registration backend is not configured yet. Please email info@daab-waas.com directly."
          : "The application backend is not configured yet. Please email info@daab-waas.com directly.",
        submitFailed: isForumRegister()
          ? "Could not submit your registration. Please try again or email info@daab-waas.com."
          : "Could not submit your application. Please try again or email info@daab-waas.com.",
        networkError: "Network error. Check your connection and try again.",
        expandSection: "Expand section",
        collapseSection: "Collapse section",
        phpUnavailable: isForumRegister()
          ? "This server cannot send registrations (a PHP mail handler is required). Submit on the live website, or email your details to info@daab-waas.com."
          : "This server cannot send applications (a PHP mail handler is required). Submit on the live website, or email your details to info@daab-waas.com.",
      },
    };
    return (strings[lang] || strings.en)[key] || key;
  }

  function showSubmitError(message, options) {
    var opts = options || {};
    var box = byId("app-submit-status");
    if (!box) return;
    box.hidden = false;
    box.className = "app-submit-status app-submit-status--error";
    box.textContent = message;
    if (opts.alert) {
      box.setAttribute("role", "alert");
      box.setAttribute("aria-live", "assertive");
    } else {
      box.setAttribute("role", "status");
      box.setAttribute("aria-live", "polite");
    }
  }

  function clearSubmitStatus() {
    var box = byId("app-submit-status");
    if (!box) return;
    box.hidden = true;
    box.textContent = "";
    box.className = "app-submit-status";
    box.setAttribute("role", "status");
    box.setAttribute("aria-live", "polite");
    var sciFieldset = byId("sci-fields");
    if (sciFieldset) sciFieldset.removeAttribute("aria-invalid");
  }

  function setSubmitting(isSubmitting) {
    var btn = byId("appSubmitBtn");
    if (!btn) return;
    btn.disabled = isSubmitting;
    btn.classList.toggle("is-loading", isSubmitting);
    btn.textContent = isSubmitting ? uiText("submitting") : uiText("submit");
  }

  function getRadioValue(name) {
    var el = document.querySelector('.application-page input[name="' + name + '"]:checked');
    return el ? el.value : "";
  }

  function getSciValues() {
    return Array.prototype.map.call(
      document.querySelectorAll('.application-page input[name="sci"]:checked'),
      function (el) {
        return el.value;
      }
    );
  }

  function getCvConfirmValue() {
    var field = byId("cvconfirm");
    if (!field) return "";
    if (field.type === "checkbox") return field.checked ? "yes" : "";
    return String(field.value || "").trim();
  }

  function getPrivacyConfirmValue() {
    var field = byId("privacyconfirm");
    if (!field) return "";
    if (field.type === "checkbox") return field.checked ? "yes" : "";
    return String(field.value || "").trim();
  }

  var FORUM_CV_MAX_BYTES = 8 * 1024 * 1024;
  var FORUM_PHOTO_MAX_BYTES = 5 * 1024 * 1024;
  var photoPreviewUrl = "";

  function fileExtension(name) {
    var value = String(name || "");
    var dot = value.lastIndexOf(".");
    return dot >= 0 ? value.slice(dot + 1).toLowerCase() : "";
  }

  function uploadInputId(kind) {
    return kind === "photo" ? "photofile" : "cvfile";
  }

  function getSelectedUploadFile(kind) {
    var input = byId(uploadInputId(kind));
    return input && input.files && input.files[0] ? input.files[0] : null;
  }

  function setFileCardError(kind, message) {
    var box = byId(uploadInputId(kind) + "-error");
    if (!box) return;
    if (!message) {
      box.hidden = true;
      box.textContent = "";
      return;
    }
    box.hidden = false;
    box.textContent = message;
  }

  function revokePhotoPreview() {
    var thumb = byId("photofile-thumb");
    if (photoPreviewUrl) {
      URL.revokeObjectURL(photoPreviewUrl);
      photoPreviewUrl = "";
    }
    if (thumb) {
      thumb.hidden = true;
      thumb.removeAttribute("src");
      thumb.alt = "";
    }
  }

  function showPhotoPreview(file) {
    var thumb = byId("photofile-thumb");
    if (!thumb || !file) return;
    revokePhotoPreview();
    photoPreviewUrl = URL.createObjectURL(file);
    thumb.src = photoPreviewUrl;
    thumb.alt = file.name || uiText("filePhotoRequired");
    thumb.hidden = false;
  }

  function setFileCardSelected(kind, file) {
    var card = document.querySelector('.app-file-card[data-file-kind="' + kind + '"]');
    var status = byId(uploadInputId(kind) + "-status");
    var nameEl = status ? status.querySelector(".app-file-name") : null;
    if (card) card.classList.toggle("is-selected", !!file);
    if (!status) return;
    if (!file) {
      status.hidden = true;
      if (nameEl) nameEl.textContent = "";
      if (kind === "photo") revokePhotoPreview();
      return;
    }
    if (nameEl) nameEl.textContent = file.name;
    status.hidden = false;
    if (kind === "photo") showPhotoPreview(file);
  }

  function validateSelectedFile(kind, file) {
    if (!file) return uiText(kind === "photo" ? "filePhotoRequired" : "fileCvRequired");
    var ext = fileExtension(file.name);
    if (kind === "photo") {
      if (ext !== "jpg" && ext !== "jpeg" && ext !== "png") return uiText("filePhotoType");
      if (file.size > FORUM_PHOTO_MAX_BYTES) return uiText("filePhotoSize");
    } else {
      if (ext !== "pdf" && ext !== "docx") return uiText("fileCvType");
      if (file.size > FORUM_CV_MAX_BYTES) return uiText("fileCvSize");
    }
    if (!file.size) return uiText(kind === "photo" ? "filePhotoInvalid" : "fileCvInvalid");
    return "";
  }

  function applyUploadSelection(kind) {
    var file = getSelectedUploadFile(kind);
    if (!file) {
      setFileCardSelected(kind, null);
      setFileCardError(kind, "");
      return false;
    }
    var error = validateSelectedFile(kind, file);
    if (error) {
      var input = byId(uploadInputId(kind));
      if (input) input.value = "";
      setFileCardSelected(kind, null);
      setFileCardError(kind, error);
      return false;
    }
    setFileCardError(kind, "");
    setFileCardSelected(kind, file);
    return true;
  }

  function clearUploadSelection(kind) {
    var input = byId(uploadInputId(kind));
    if (input) input.value = "";
    setFileCardSelected(kind, null);
    setFileCardError(kind, "");
  }

  function openUploadPicker(inputId) {
    var input = byId(inputId);
    if (input) input.click();
  }

  function initFileUploads() {
    if (!isForumRegister()) return;
    var root = byId("app-file-uploads");
    if (!root) return;
    root.addEventListener("click", function (e) {
      var choose = e.target.closest(".app-file-choose, .app-file-replace");
      if (choose) {
        openUploadPicker(choose.getAttribute("data-file-target"));
        return;
      }
      var remove = e.target.closest(".app-file-remove");
      if (remove) clearUploadSelection(remove.getAttribute("data-file-kind"));
    });
    ["cv", "photo"].forEach(function (kind) {
      var input = byId(uploadInputId(kind));
      if (!input) return;
      input.addEventListener("change", function () {
        applyUploadSelection(kind);
      });
    });
  }

  function validateFileUploads() {
    if (!isForumRegister() || !byId("app-file-uploads")) return true;
    var firstError = "";
    var firstKind = "";
    ["cv", "photo"].forEach(function (kind) {
      var error = validateSelectedFile(kind, getSelectedUploadFile(kind));
      setFileCardError(kind, error);
      if (error && !firstError) {
        firstError = error;
        firstKind = kind;
      }
    });
    if (!firstError) return true;
    showSubmitError(firstError, { alert: true });
    var card = document.querySelector('.app-file-card[data-file-kind="' + firstKind + '"]');
    if (card) card.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }

  function uploadErrorFromStatus(status) {
    var map = {
      "error:cv_missing": "fileCvRequired",
      "error:cv_type": "fileCvType",
      "error:cv_size": "fileCvSize",
      "error:cv_invalid": "fileCvInvalid",
      "error:photo_missing": "filePhotoRequired",
      "error:photo_type": "filePhotoType",
      "error:photo_size": "filePhotoSize",
      "error:photo_invalid": "filePhotoInvalid",
      "error:attach": "fileAttachFailed",
    };
    return map[status] ? uiText(map[status]) : "";
  }

  function validatePrivacyConfirm() {
    var field = byId("privacyconfirm");
    if (!field) return true;
    if (field.checked) {
      field.setCustomValidity("");
      return true;
    }
    field.setCustomValidity(uiText("privacyRequired"));
    showSubmitError(uiText("privacyRequired"), { alert: true });
    try {
      field.focus({ preventScroll: true });
    } catch (e) {
      field.focus();
    }
    field.scrollIntoView({ behavior: "smooth", block: "center" });
    field.reportValidity();
    return false;
  }

  var SCI_FIELD_LIMIT = 2;

  function showSciLimitMessage() {
    var box = byId("sci-fields-limit");
    if (!box) return;
    box.hidden = false;
    box.textContent = uiText("sciLimitExceeded");
  }

  function hideSciLimitMessage() {
    var box = byId("sci-fields-limit");
    if (!box) return;
    box.hidden = true;
    box.textContent = "";
  }

  function initSciFieldLimit() {
    if (!isForumRegister()) return;
    var fieldset = byId("sci-fields");
    if (!fieldset) return;
    fieldset.addEventListener("change", function (e) {
      var target = e.target;
      if (!target || target.name !== "sci" || target.type !== "checkbox") return;
      if (!target.checked) {
        hideSciLimitMessage();
        return;
      }
      var selected = fieldset.querySelectorAll('input[name="sci"]:checked');
      if (selected.length > SCI_FIELD_LIMIT) {
        target.checked = false;
        showSciLimitMessage();
        return;
      }
      hideSciLimitMessage();
    });
  }

  function validateSciSelection() {
    if (getSciValues().length > 0) return true;
    var sciFieldset = byId("sci-fields");
    if (sciFieldset) sciFieldset.setAttribute("aria-invalid", "true");
    showSubmitError(uiText("sciRequired"), { alert: true });
    var sec = sciFieldset && sciFieldset.closest
      ? sciFieldset.closest(".form-section")
      : byId("sec-4") || byId("sec-3");
    if (sec) sec.scrollIntoView({ behavior: "smooth", block: "start" });
    return false;
  }

  function validateRadioGroup(name, messageKey, focusId) {
    if (getRadioValue(name)) return true;
    showSubmitError(uiText(messageKey), { alert: true });
    var focusEl = byId(focusId) || document.querySelector(
      '.application-page input[name="' + name + '"]'
    );
    if (focusEl) {
      try {
        focusEl.focus({ preventScroll: true });
      } catch (e) {
        focusEl.focus();
      }
      focusEl.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    return false;
  }

  function getCityValue() {
    var manual = byId("city_manual");
    if (manual && !manual.hidden) {
      return String(manual.value || "").trim();
    }
    var citySelect = byId("city");
    return (citySelect && citySelect.value.trim()) || "";
  }

  function buildSubmissionPayload() {
    var lang = detectLang();
    var firstName = (byId("name") && byId("name").value.trim()) || "";
    var lastName = (byId("surname") && byId("surname").value.trim()) || "";
    var email = (byId("email") && byId("email").value.trim()) || "";
    var phoneCode = (byId("phone_code") && byId("phone_code").value.trim()) || "";
    var phoneNumber = (byId("phone") && byId("phone").value.trim()) || "";
    var fullName = (firstName + " " + lastName).trim();

    var subjectPrefix = isForumRegister()
      ? lang === "az"
        ? "Forum 2026 iştirakçı qeydiyyatı — "
        : "Forum 2026 participant registration — "
      : lang === "az"
        ? "DAAB üzvlük — "
        : "WAAS Membership — ";
    var affiliation = (byId("currentjob") && byId("currentjob").value.trim()) || "";
    var fieldOfStudyEl = byId("fieldofstudy");

    var payload = {
      _subject: subjectPrefix + fullName,
      form_kind: formKind(),
      locale: lang,
      submitted_at: new Date().toISOString(),
      page_url: location.href,
      email: email,
      first_name: firstName,
      last_name: lastName,
      full_name: fullName,
      father_name: (byId("fathername") && byId("fathername").value.trim()) || "",
      date_of_birth: (byId("dob") && byId("dob").value.trim()) || "",
      country_of_birth: (byId("birthcountry") && byId("birthcountry").value.trim()) || "",
      citizenship: (byId("citizenship") && byId("citizenship").value.trim()) || "",
      gender: getRadioValue("gender"),
      country: (byId("country") && byId("country").value.trim()) || "",
      city: getCityValue(),
      phone_code: phoneCode,
      phone_number: phoneNumber,
      phone_full: phoneCode && phoneNumber ? phoneCode + " " + phoneNumber : phoneNumber,
      university: (byId("university") && byId("university").value.trim()) || "",
      degree: getRadioValue("degree"),
      degree_institution: (byId("deginst") && byId("deginst").value.trim()) || "",
      academic_title: getRadioValue("title"),
      title_institution: (byId("titinst") && byId("titinst").value.trim()) || "",
      affiliation: affiliation,
      current_job: affiliation,
      previous_jobs: (byId("prevjobs") && byId("prevjobs").value.trim()) || "",
      contributions: (byId("contributions") && byId("contributions").value.trim()) || "",
      sci_fields: getSciValues().join(", "),
      sci_fields_count: String(getSciValues().length),
      additional_info: (byId("addinfo") && byId("addinfo").value.trim()) || "",
      cv_confirm: getCvConfirmValue(),
      privacy_confirm: getPrivacyConfirmValue(),
    };
    if (fieldOfStudyEl) {
      payload.field_of_study = fieldOfStudyEl.value.trim();
    }
    return payload;
  }

  function showSuccessScreen() {
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.classList.remove("active");
      s.hidden = true;
    });
    var success = byId("success");
    var progress = document.querySelector(".application-page .app-progress-bar");
    var sidebar = document.querySelector(".application-page .application-sidebar");
    if (success) success.classList.add("active");
    if (progress) progress.hidden = true;
    if (sidebar) sidebar.hidden = true;
    document.querySelectorAll(".application-page .prog-step").forEach(function (el) {
      el.classList.remove("active");
      el.classList.add("done");
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function postApplication(payload) {
    var endpoint = getFormEndpoint();
    if (isPhpMailEndpoint(endpoint)) {
      return fetch(endpoint, {
        method: "POST",
        body: buildFormDataForPhp(payload),
        headers: {
          Accept: "text/plain, */*",
        },
      }).then(function (response) {
        return response.text().then(function (text) {
          var status = String(text || "").trim().toLowerCase();
          if (!response.ok || status !== "success") {
            if (isPhpHandlerUnavailable(response.status, status, text)) {
              throw new Error(uiText("phpUnavailable"));
            }
            throw new Error(
              uploadErrorFromStatus(status) ||
                (status === "error" ? uiText("submitFailed") : uiText("submitFailed"))
            );
          }
          return { ok: true };
        });
      });
    }
    return fetch(endpoint, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }).then(function (response) {
      return response
        .json()
        .catch(function () {
          return {};
        })
        .then(function (body) {
          if (!response.ok) {
            var detail =
              (body && (body.error || body.message)) ||
              response.status + " " + response.statusText;
            throw new Error(String(detail));
          }
          return body;
        });
    });
  }

  function submitForm() {
    clearSubmitStatus();
    var honeypot = byId("website");
    if (honeypot && String(honeypot.value || "").trim()) {
      showSuccessScreen();
      return;
    }
    if (!validateForm()) return;
    if (document.querySelector('.application-page input[name="degree"]')) {
      if (!validateRadioGroup("degree", "degreeRequired", "deg1")) return;
    }
    if (document.querySelector('.application-page input[name="title"]')) {
      if (!validateRadioGroup("title", "titleRequired", "tit1")) return;
    }
    if (document.querySelector('.application-page input[name="gender"]')) {
      if (!validateRadioGroup("gender", "genderRequired", "gender-male")) return;
    }
    if (byId("sci-fields")) {
      if (!validateSciSelection()) return;
    }
    if (!validateFileUploads()) return;
    if (!validatePrivacyConfirm()) return;

    setSubmitting(true);
    var payload = buildSubmissionPayload();

    postApplication(payload)
      .then(function () {
        showSuccessScreen();
      })
      .catch(function (err) {
        var msg = uiText("submitFailed");
        var detail = err && err.message ? String(err.message) : "";
        if (
          detail === uiText("phpUnavailable") ||
          /405|501|404/.test(detail) ||
          /failed to fetch|networkerror|load failed/i.test(detail)
        ) {
          msg = isPhpMailEndpoint(getFormEndpoint())
            ? uiText("phpUnavailable")
            : uiText("networkError");
        }
        showSubmitError(msg);
      })
      .finally(function () {
        setSubmitting(false);
      });
  }

  function buildLocalizedCountries(lang) {
    var formatter =
      typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function"
        ? new Intl.DisplayNames([lang], { type: "region" })
        : null;
    var enFormatter =
      typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function"
        ? new Intl.DisplayNames(["en"], { type: "region" })
        : null;
    var collator =
      typeof Intl !== "undefined" && typeof Intl.Collator === "function"
        ? new Intl.Collator(lang, { sensitivity: "base" })
        : null;

    var azNames = window.DAAB_COUNTRY_NAMES_AZ || {};
    var countries = COUNTRY_CODES.map(function (code) {
      var azName = azNames[code];
      var intlName = formatter ? formatter.of(code) || code : code;
      return {
        code: code,
        name: lang === "az" && azName ? azName : intlName,
        englishName: enFormatter ? enFormatter.of(code) || code : code,
      };
    });
    countries.sort(function (a, b) {
      if (collator) return collator.compare(a.name, b.name);
      return String(a.name).localeCompare(String(b.name), lang);
    });
    return { countries: countries, collator: collator };
  }

  function fillCountrySelect(select, countries, placeholderText) {
    select.innerHTML = "";
    var placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = placeholderText;
    select.appendChild(placeholder);
    countries.forEach(function (entry) {
      var option = document.createElement("option");
      option.value = entry.name;
      option.setAttribute("data-code", entry.code);
      option.setAttribute("data-country-en", entry.englishName);
      option.textContent = entry.name;
      select.appendChild(option);
    });
    select.selectedIndex = 0;
  }

  function enhanceCountryPicker(select, config) {
    if (!select || select.getAttribute("data-country-picker-ready") === "1") return;
    select.setAttribute("data-country-picker-ready", "1");

    var placeholderText = config.placeholderText || "";
    var searchPlaceholder = config.searchPlaceholder || "";
    var noResultsText = config.noResultsText || "";
    var lang = config.lang || "en";
    var fieldGroup = select.closest(".field-group");
    if (!fieldGroup) return;

    var picker = document.createElement("div");
    picker.className = "phone-code-picker country-picker";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = select.id ? select.id + "_picker" : "country_picker";
    btn.className = "phone-code-picker-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute(
      "aria-label",
      (fieldGroup.querySelector("label.field-label") &&
        fieldGroup.querySelector("label.field-label").textContent.trim()) ||
        placeholderText
    );

    var valueWrap = document.createElement("span");
    valueWrap.className = "phone-code-picker-value";

    var flagImg = document.createElement("img");
    flagImg.className = "phone-code-flag";
    flagImg.alt = "";
    flagImg.setAttribute("aria-hidden", "true");
    flagImg.width = 20;
    flagImg.height = 15;
    flagImg.hidden = true;

    var labelSpan = document.createElement("span");
    labelSpan.className = "phone-code-picker-text";
    labelSpan.textContent = placeholderText;

    valueWrap.appendChild(flagImg);
    valueWrap.appendChild(labelSpan);
    btn.appendChild(valueWrap);

    var chevron = document.createElement("span");
    chevron.className = "phone-code-picker-chevron";
    chevron.setAttribute("aria-hidden", "true");
    btn.appendChild(chevron);

    var panel = document.createElement("div");
    panel.className = "phone-code-picker-panel country-picker-panel";
    panel.hidden = true;

    var searchWrap = document.createElement("div");
    searchWrap.className = "country-picker-search-wrap";
    var search = document.createElement("input");
    search.type = "search";
    search.className = "country-picker-search";
    search.setAttribute("autocomplete", "off");
    search.setAttribute("spellcheck", "false");
    search.setAttribute("aria-label", searchPlaceholder);
    search.placeholder = searchPlaceholder;
    searchWrap.appendChild(search);

    var list = document.createElement("ul");
    list.className = "phone-code-picker-list";
    list.setAttribute("role", "listbox");
    if (btn.id) list.id = btn.id + "_list";
    btn.setAttribute("aria-controls", list.id);

    var empty = document.createElement("div");
    empty.className = "country-picker-empty";
    empty.hidden = true;
    empty.textContent = noResultsText;

    Array.prototype.forEach.call(select.options, function (opt) {
      if (!opt.value) return;
      var countryCode = opt.getAttribute("data-code") || "";
      var li = document.createElement("li");
      li.className = "phone-code-picker-option country-picker-option";
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      li.setAttribute("data-value", opt.value);
      li.setAttribute("data-code", countryCode);
      li.setAttribute("data-country-en", opt.getAttribute("data-country-en") || "");
      li.setAttribute("data-label", opt.textContent);

      var img = document.createElement("img");
      img.className = "phone-code-flag";
      img.src = phoneFlagSrc(countryCode);
      img.alt = "";
      img.setAttribute("aria-hidden", "true");
      img.width = 20;
      img.height = 15;
      img.loading = "lazy";
      img.decoding = "async";

      var text = document.createElement("span");
      text.className = "phone-code-picker-option-text";
      text.textContent = opt.textContent;

      li.appendChild(img);
      li.appendChild(text);
      list.appendChild(li);
    });

    panel.appendChild(searchWrap);
    panel.appendChild(list);
    panel.appendChild(empty);

    select.classList.add("phone-code-picker-native");
    select.parentNode.insertBefore(picker, select);
    picker.appendChild(select);
    picker.appendChild(btn);
    picker.appendChild(panel);

    var label = fieldGroup.querySelector('label[for="' + select.id + '"]');
    if (label) {
      label.setAttribute("for", btn.id);
      label.addEventListener("click", function (e) {
        e.preventDefault();
        btn.focus();
        if (panel.hidden) openPanel();
      });
    }

    function optionNodes() {
      return list.querySelectorAll(".country-picker-option");
    }

    function syncFromSelect() {
      var opt = select.options[select.selectedIndex];
      btn.disabled = select.disabled;
      if (!opt || !opt.value) {
        flagImg.hidden = true;
        flagImg.removeAttribute("src");
        labelSpan.textContent = placeholderText;
        btn.classList.remove("has-value");
        optionNodes().forEach(function (li) {
          li.classList.remove("is-selected", "is-active");
          li.setAttribute("aria-selected", "false");
        });
        return;
      }
      btn.classList.add("has-value");
      var cc = opt.getAttribute("data-code");
      if (cc) {
        flagImg.src = phoneFlagSrc(cc);
        flagImg.hidden = false;
      } else {
        flagImg.hidden = true;
      }
      labelSpan.textContent = opt.textContent;
      optionNodes().forEach(function (li) {
        var selected = li.getAttribute("data-value") === opt.value;
        li.classList.toggle("is-selected", selected);
        li.classList.toggle("is-active", selected);
        li.setAttribute("aria-selected", selected ? "true" : "false");
      });
    }

    function closeOtherCountryPickers() {
      closeOpenPickersExcept(picker);
    }

    function visibleOptions() {
      return Array.prototype.filter.call(optionNodes(), function (li) {
        return !li.classList.contains("is-filtered-out");
      });
    }

    function applyFilter() {
      var query = String(search.value || "").trim().toLocaleLowerCase(lang);
      var shown = 0;
      optionNodes().forEach(function (li) {
        var hay = [
          li.getAttribute("data-label") || "",
          li.getAttribute("data-country-en") || "",
          li.getAttribute("data-code") || "",
        ]
          .join(" ")
          .toLocaleLowerCase(lang);
        var match = !query || hay.indexOf(query) !== -1;
        li.classList.toggle("is-filtered-out", !match);
        if (match) shown += 1;
      });
      empty.hidden = shown > 0;
      list.hidden = shown === 0;
    }

    function closePanel() {
      panel.hidden = true;
      picker.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      search.value = "";
      applyFilter();
    }

    function openPanel() {
      if (select.disabled) return;
      closeOtherCountryPickers();
      search.value = "";
      applyFilter();
      panel.hidden = false;
      picker.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      var selected = list.querySelector(".country-picker-option.is-selected");
      optionNodes().forEach(function (li) {
        li.classList.toggle("is-active", li === selected);
      });
      try {
        search.focus({ preventScroll: true });
      } catch (e) {
        search.focus();
      }
      if (selected) selected.scrollIntoView({ block: "nearest" });
    }

    function chooseOption(li) {
      if (!li) return;
      var value = li.getAttribute("data-value");
      var i;
      for (i = 0; i < select.options.length; i++) {
        if (select.options[i].value === value) {
          select.selectedIndex = i;
          break;
        }
      }
      select.dispatchEvent(new Event("change", { bubbles: true }));
      syncFromSelect();
      closePanel();
      btn.focus();
    }

    function moveActive(delta) {
      var items = visibleOptions();
      if (!items.length) return;
      var current = list.querySelector(".country-picker-option.is-active:not(.is-filtered-out)");
      var index = current ? items.indexOf(current) : -1;
      var next = items[(index + delta + items.length) % items.length];
      items.forEach(function (li) {
        li.classList.toggle("is-active", li === next);
      });
      if (next) next.scrollIntoView({ block: "nearest" });
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      if (panel.hidden) openPanel();
      else closePanel();
    });

    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (panel.hidden) openPanel();
      }
    });

    search.addEventListener("input", applyFilter);
    search.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveActive(1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        moveActive(-1);
      } else if (e.key === "Enter") {
        e.preventDefault();
        var active = list.querySelector(".country-picker-option.is-active:not(.is-filtered-out)");
        chooseOption(active || visibleOptions()[0]);
      } else if (e.key === "Escape") {
        e.preventDefault();
        closePanel();
        btn.focus();
      }
    });

    list.addEventListener("click", function (e) {
      var li = e.target.closest(".country-picker-option");
      if (!li || li.classList.contains("is-filtered-out")) return;
      chooseOption(li);
    });

    select.addEventListener("invalid", function () {
      if (panel.hidden) {
        try {
          btn.focus({ preventScroll: true });
        } catch (err) {
          btn.focus();
        }
        btn.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });

    document.addEventListener("click", function (e) {
      if (picker.contains(e.target)) return;
      if (label && label.contains(e.target)) return;
      closePanel();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) {
        closePanel();
        btn.focus();
      }
    });

    select.addEventListener("change", syncFromSelect);
    syncFromSelect();
  }

  function initCountryDropdowns() {
    var lang = detectLang();
    var localized = buildLocalizedCountries(lang);
    var texts = {
      en: {
        countryPlaceholder: "Select country",
        birthCountryPlaceholder: "Select country of birth",
        citizenshipPlaceholder: "Select citizenship",
        countrySearchPlaceholder: "Search country",
        countryNoResults: "No countries found",
        cityDisabledPlaceholder: "Select country first",
        cityPlaceholder: "Select city",
        cityLoadingPlaceholder: "Loading cities...",
        cityUnavailablePlaceholder: "No cities available — type your city below",
        citySearchPlaceholder: "Search city",
        cityNoResults: "No cities found",
      },
      az: {
        countryPlaceholder: "Ölkə seçin",
        birthCountryPlaceholder: "Doğulduğunuz ölkəni seçin",
        citizenshipPlaceholder: "Vətəndaşlığınızı seçin",
        countrySearchPlaceholder: "Ölkə axtarın",
        countryNoResults: "Ölkə tapılmadı",
        cityDisabledPlaceholder: "Əvvəlcə ölkə seçin",
        cityPlaceholder: "Şəhər seçin",
        cityLoadingPlaceholder: "Şəhərlər yüklənir...",
        cityUnavailablePlaceholder: "Şəhərlər tapılmadı — aşağıda şəhəri yazın",
        citySearchPlaceholder: "Şəhər axtarın",
        cityNoResults: "Şəhər tapılmadı",
      },
    };
    var t = texts[lang] || texts.en;
    var placeholderById = {
      country: t.countryPlaceholder,
      birthcountry: t.birthCountryPlaceholder,
      citizenship: t.citizenshipPlaceholder,
    };

    document.querySelectorAll("select[data-country-select]").forEach(function (select) {
      var placeholder = placeholderById[select.id] || t.countryPlaceholder;
      fillCountrySelect(select, localized.countries, placeholder);
      enhanceCountryPicker(select, {
        placeholderText: placeholder,
        searchPlaceholder: t.countrySearchPlaceholder,
        noResultsText: t.countryNoResults,
        lang: lang,
      });
    });

    initResidenceCityPicker(t, localized.collator, lang);
  }

  function initResidenceCityPicker(t, collator, lang) {
    var countrySelect = byId("country");
    var citySelect = byId("city");
    var cityManual = byId("city_manual");
    if (!countrySelect || !citySelect) return;
    var cityRequestSeq = 0;

    function hideCityManual() {
      if (!cityManual) return;
      cityManual.hidden = true;
      cityManual.required = false;
      cityManual.setAttribute("aria-hidden", "true");
      cityManual.value = "";
    }

    function showCityManual() {
      if (!cityManual) return;
      cityManual.hidden = false;
      cityManual.required = true;
      cityManual.removeAttribute("aria-hidden");
      citySelect.required = false;
    }

    function resetCitySelect() {
      hideCityManual();
      citySelect.required = true;
      citySelect.disabled = true;
      citySelect.innerHTML = "";
      var option = document.createElement("option");
      option.value = "";
      option.textContent = t.cityDisabledPlaceholder;
      citySelect.appendChild(option);
    }

    function showCityLoading() {
      hideCityManual();
      citySelect.required = true;
      citySelect.disabled = true;
      citySelect.innerHTML = "";
      var option = document.createElement("option");
      option.value = "";
      option.textContent = t.cityLoadingPlaceholder;
      citySelect.appendChild(option);
    }

    function selectedCountryCode() {
      var selected = countrySelect.options[countrySelect.selectedIndex];
      return selected ? selected.getAttribute("data-code") || "" : "";
    }

    function aliasesForCity(countryCode, cityName) {
      var extras = CITY_GUARANTEES[countryCode] || [];
      var key = String(cityName || "").toLocaleLowerCase(lang);
      var i;
      for (i = 0; i < extras.length; i++) {
        if (String(extras[i].name).toLocaleLowerCase(lang) === key) {
          return (extras[i].aliases || []).join(" ");
        }
      }
      return "";
    }

    function pinGuaranteedCities(countryCode, cityList) {
      var extras = CITY_GUARANTEES[countryCode] || [];
      if (!extras.length) return cityList;
      var pinOrder = extras.map(function (entry) {
        return String(entry.name).toLocaleLowerCase(lang);
      });
      var pinSet = Object.create(null);
      pinOrder.forEach(function (key) {
        pinSet[key] = true;
      });
      var pinned = [];
      var rest = [];
      cityList.forEach(function (name) {
        if (pinSet[String(name).toLocaleLowerCase(lang)]) pinned.push(name);
        else rest.push(name);
      });
      pinned.sort(function (a, b) {
        return (
          pinOrder.indexOf(String(a).toLocaleLowerCase(lang)) -
          pinOrder.indexOf(String(b).toLocaleLowerCase(lang))
        );
      });
      return pinned.concat(rest);
    }

    function mergeGuaranteedCities(countryCode, rawList) {
      var extras = CITY_GUARANTEES[countryCode] || [];
      var merged = Array.isArray(rawList) ? rawList.slice() : [];
      extras.forEach(function (entry) {
        if (entry && entry.name) merged.push(entry.name);
      });
      return pinGuaranteedCities(countryCode, normalizeCityList(merged));
    }

    function populateCitySelect(cityList) {
      citySelect.innerHTML = "";

      if (!Array.isArray(cityList) || cityList.length === 0) {
        var unavailable = document.createElement("option");
        unavailable.value = "";
        unavailable.textContent = t.cityUnavailablePlaceholder;
        citySelect.appendChild(unavailable);
        citySelect.disabled = true;
        showCityManual();
        if (citySelect._daabRebuildCityPicker) citySelect._daabRebuildCityPicker();
        return;
      }

      hideCityManual();
      citySelect.disabled = false;
      citySelect.required = true;
      var placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = t.cityPlaceholder;
      citySelect.appendChild(placeholder);

      var countryCode = selectedCountryCode();
      cityList.forEach(function (cityName) {
        var option = document.createElement("option");
        option.value = cityName;
        option.textContent = cityName;
        var aliases = aliasesForCity(countryCode, cityName);
        if (aliases) option.setAttribute("data-aliases", aliases);
        citySelect.appendChild(option);
      });
      if (citySelect._daabRebuildCityPicker) citySelect._daabRebuildCityPicker();
    }

    function normalizeCityList(rawList) {
      if (!Array.isArray(rawList)) return [];
      var map = Object.create(null);
      var items = [];
      rawList.forEach(function (city) {
        var name = String(city || "").trim();
        if (!name) return;
        var key = name.toLocaleLowerCase(lang);
        if (map[key]) return;
        map[key] = true;
        items.push(name);
      });
      items.sort(function (a, b) {
        if (collator) return collator.compare(a, b);
        return a.localeCompare(b, lang);
      });
      return items;
    }

    function fetchCitiesByCountryEnglishName(countryEnglishName, countryCode) {
      if (cityCache[countryEnglishName]) {
        return Promise.resolve(cityCache[countryEnglishName]);
      }
      return fetch("https://countriesnow.space/api/v0.1/countries/cities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ country: countryEnglishName }),
      })
        .then(function (response) {
          if (!response.ok) throw new Error("city-fetch-failed");
          return response.json();
        })
        .then(function (payload) {
          var list = mergeGuaranteedCities(countryCode, payload && payload.data);
          cityCache[countryEnglishName] = list;
          return list;
        })
        .catch(function () {
          return mergeGuaranteedCities(countryCode, []);
        });
    }

    function resetCitySelectAndPicker() {
      resetCitySelect();
      if (citySelect._daabRebuildCityPicker) citySelect._daabRebuildCityPicker();
    }

    function showCityLoadingAndPicker() {
      showCityLoading();
      if (citySelect._daabRebuildCityPicker) citySelect._daabRebuildCityPicker();
    }

    countrySelect.addEventListener("change", function () {
      cityRequestSeq += 1;
      var requestId = cityRequestSeq;
      var selected = countrySelect.options[countrySelect.selectedIndex];
      var countryEnglishName = selected ? selected.getAttribute("data-country-en") : null;
      var countryCode = selected ? selected.getAttribute("data-code") || "" : "";
      if (!countryEnglishName) {
        resetCitySelectAndPicker();
        return;
      }
      showCityLoadingAndPicker();
      fetchCitiesByCountryEnglishName(countryEnglishName, countryCode).then(function (cityList) {
        if (requestId !== cityRequestSeq) return;
        populateCitySelect(cityList);
      });
    });

    enhanceCityPicker(citySelect, {
      placeholderText: t.cityPlaceholder,
      disabledPlaceholder: t.cityDisabledPlaceholder,
      searchPlaceholder: t.citySearchPlaceholder,
      noResultsText: t.cityNoResults,
      lang: lang,
    });
    resetCitySelectAndPicker();
  }

  function enhanceCityPicker(select, config) {
    if (!select || select.getAttribute("data-city-picker-ready") === "1") return;
    select.setAttribute("data-city-picker-ready", "1");

    var placeholderText = config.placeholderText || "";
    var disabledPlaceholder = config.disabledPlaceholder || placeholderText;
    var searchPlaceholder = config.searchPlaceholder || "";
    var noResultsText = config.noResultsText || "";
    var lang = config.lang || "en";
    var fieldGroup = select.closest(".field-group");
    if (!fieldGroup) return;

    var picker = document.createElement("div");
    picker.className = "phone-code-picker country-picker city-picker";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = select.id ? select.id + "_picker" : "city_picker";
    btn.className = "phone-code-picker-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute(
      "aria-label",
      (fieldGroup.querySelector("label.field-label") &&
        fieldGroup.querySelector("label.field-label").textContent.trim()) ||
        placeholderText
    );

    var valueWrap = document.createElement("span");
    valueWrap.className = "phone-code-picker-value";
    var labelSpan = document.createElement("span");
    labelSpan.className = "phone-code-picker-text";
    labelSpan.textContent = disabledPlaceholder;
    valueWrap.appendChild(labelSpan);
    btn.appendChild(valueWrap);

    var chevron = document.createElement("span");
    chevron.className = "phone-code-picker-chevron";
    chevron.setAttribute("aria-hidden", "true");
    btn.appendChild(chevron);

    var panel = document.createElement("div");
    panel.className = "phone-code-picker-panel country-picker-panel";
    panel.hidden = true;

    var searchWrap = document.createElement("div");
    searchWrap.className = "country-picker-search-wrap";
    var search = document.createElement("input");
    search.type = "search";
    search.className = "country-picker-search";
    search.setAttribute("autocomplete", "off");
    search.setAttribute("spellcheck", "false");
    search.setAttribute("aria-label", searchPlaceholder);
    search.placeholder = searchPlaceholder;
    searchWrap.appendChild(search);

    var list = document.createElement("ul");
    list.className = "phone-code-picker-list";
    list.setAttribute("role", "listbox");
    if (btn.id) list.id = btn.id + "_list";
    btn.setAttribute("aria-controls", list.id);

    var empty = document.createElement("div");
    empty.className = "country-picker-empty";
    empty.hidden = true;
    empty.textContent = noResultsText;

    panel.appendChild(searchWrap);
    panel.appendChild(list);
    panel.appendChild(empty);

    select.classList.add("phone-code-picker-native");
    select.parentNode.insertBefore(picker, select);
    picker.appendChild(select);
    picker.appendChild(btn);
    picker.appendChild(panel);

    var label = fieldGroup.querySelector('label[for="' + select.id + '"]');
    if (label) {
      label.setAttribute("for", btn.id);
      label.addEventListener("click", function (e) {
        e.preventDefault();
        if (select.disabled) return;
        btn.focus();
        if (panel.hidden) openPanel();
      });
    }

    function optionNodes() {
      return list.querySelectorAll(".country-picker-option");
    }

    function buttonLabel() {
      if (select.disabled) {
        var first = select.options[0];
        return (first && first.textContent) || disabledPlaceholder;
      }
      var opt = select.options[select.selectedIndex];
      if (opt && opt.value) return opt.textContent;
      return placeholderText;
    }

    function syncFromSelect() {
      var opt = select.options[select.selectedIndex];
      btn.disabled = !!select.disabled;
      labelSpan.textContent = buttonLabel();
      if (!opt || !opt.value || select.disabled) {
        btn.classList.remove("has-value");
        optionNodes().forEach(function (li) {
          li.classList.remove("is-selected", "is-active");
          li.setAttribute("aria-selected", "false");
        });
        return;
      }
      btn.classList.add("has-value");
      optionNodes().forEach(function (li) {
        var selected = li.getAttribute("data-value") === opt.value;
        li.classList.toggle("is-selected", selected);
        li.classList.toggle("is-active", selected);
        li.setAttribute("aria-selected", selected ? "true" : "false");
      });
    }

    function rebuildOptions() {
      list.innerHTML = "";
      Array.prototype.forEach.call(select.options, function (opt) {
        if (!opt.value) return;
        var li = document.createElement("li");
        li.className = "phone-code-picker-option country-picker-option";
        li.setAttribute("role", "option");
        li.setAttribute("aria-selected", "false");
        li.setAttribute("data-value", opt.value);
        li.setAttribute("data-label", opt.textContent);
        li.setAttribute("data-aliases", opt.getAttribute("data-aliases") || "");
        var text = document.createElement("span");
        text.className = "phone-code-picker-option-text";
        text.textContent = opt.textContent;
        li.appendChild(text);
        list.appendChild(li);
      });
      search.value = "";
      applyFilter();
      syncFromSelect();
    }

    function visibleOptions() {
      return Array.prototype.filter.call(optionNodes(), function (li) {
        return !li.classList.contains("is-filtered-out");
      });
    }

    function applyFilter() {
      var query = String(search.value || "").trim().toLocaleLowerCase(lang);
      var shown = 0;
      optionNodes().forEach(function (li) {
        var hay = [li.getAttribute("data-label") || "", li.getAttribute("data-aliases") || ""]
          .join(" ")
          .toLocaleLowerCase(lang);
        var match = !query || hay.indexOf(query) !== -1;
        li.classList.toggle("is-filtered-out", !match);
        if (match) shown += 1;
      });
      empty.hidden = shown > 0;
      list.hidden = shown === 0;
    }

    function closePanel() {
      panel.hidden = true;
      picker.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      search.value = "";
      applyFilter();
    }

    function openPanel() {
      if (select.disabled) return;
      closeOpenPickersExcept(picker);
      search.value = "";
      applyFilter();
      panel.hidden = false;
      picker.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      var selected = list.querySelector(".country-picker-option.is-selected");
      optionNodes().forEach(function (li) {
        li.classList.toggle("is-active", li === selected);
      });
      try {
        search.focus({ preventScroll: true });
      } catch (e) {
        search.focus();
      }
      if (selected) selected.scrollIntoView({ block: "nearest" });
    }

    function chooseOption(li) {
      if (!li) return;
      var value = li.getAttribute("data-value");
      var i;
      for (i = 0; i < select.options.length; i++) {
        if (select.options[i].value === value) {
          select.selectedIndex = i;
          break;
        }
      }
      select.dispatchEvent(new Event("change", { bubbles: true }));
      syncFromSelect();
      closePanel();
      btn.focus();
    }

    function moveActive(delta) {
      var items = visibleOptions();
      if (!items.length) return;
      var current = list.querySelector(".country-picker-option.is-active:not(.is-filtered-out)");
      var index = current ? items.indexOf(current) : -1;
      var next = items[(index + delta + items.length) % items.length];
      items.forEach(function (li) {
        li.classList.toggle("is-active", li === next);
      });
      if (next) next.scrollIntoView({ block: "nearest" });
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      if (select.disabled) return;
      if (panel.hidden) openPanel();
      else closePanel();
    });

    btn.addEventListener("keydown", function (e) {
      if (select.disabled) return;
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (panel.hidden) openPanel();
      }
    });

    search.addEventListener("input", applyFilter);
    search.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveActive(1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        moveActive(-1);
      } else if (e.key === "Enter") {
        e.preventDefault();
        var active = list.querySelector(".country-picker-option.is-active:not(.is-filtered-out)");
        chooseOption(active || visibleOptions()[0]);
      } else if (e.key === "Escape") {
        e.preventDefault();
        closePanel();
        btn.focus();
      }
    });

    list.addEventListener("click", function (e) {
      var li = e.target.closest(".country-picker-option");
      if (!li || li.classList.contains("is-filtered-out")) return;
      chooseOption(li);
    });

    select.addEventListener("invalid", function () {
      if (panel.hidden) {
        try {
          btn.focus({ preventScroll: true });
        } catch (err) {
          btn.focus();
        }
        btn.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });

    document.addEventListener("click", function (e) {
      if (picker.contains(e.target)) return;
      if (label && label.contains(e.target)) return;
      closePanel();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) {
        closePanel();
        btn.focus();
      }
    });

    select.addEventListener("change", syncFromSelect);
    select._daabRebuildCityPicker = rebuildOptions;
    rebuildOptions();
  }

  function initPhoneCodeDropdown() {
    var phoneCodeSelect = byId("phone_code");
    var localPhoneInput = byId("phone");
    if (!phoneCodeSelect || !localPhoneInput) return;

    var lang = detectLang();
    var texts = {
      en: {
        placeholder: "Select area code",
        searchPlaceholder: "Search country or code",
        noResults: "No area codes found",
        error: "Enter local phone number only (without country code)."
      },
      az: {
        placeholder: "Kod seçin",
        searchPlaceholder: "Ölkə və ya kod axtarın",
        noResults: "Kod tapılmadı",
        error: "Yalnız yerli telefon nömrəsini daxil edin (ölkə kodu olmadan)."
      }
    };
    var t = texts[lang] || texts.en;
    var phoneCodes = window.DAAB_PHONE_CODES || [];
    var formatter =
      typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function"
        ? new Intl.DisplayNames([lang], { type: "region" })
        : null;
    var enFormatter =
      typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function"
        ? new Intl.DisplayNames(["en"], { type: "region" })
        : null;
    var collator =
      typeof Intl !== "undefined" && typeof Intl.Collator === "function"
        ? new Intl.Collator(lang, { sensitivity: "base" })
        : null;
    var azNames = window.DAAB_COUNTRY_NAMES_AZ || {};

    function localizedCountryName(code) {
      if (code === "TR") return lang === "az" ? "Türkiyə" : "Türkiye";
      if (lang === "az" && azNames[code]) return azNames[code];
      return formatter ? (formatter.of(code) || code) : code;
    }

    function englishCountryName(code) {
      if (code === "TR") return "Türkiye";
      return enFormatter ? (enFormatter.of(code) || code) : code;
    }

    function validateLocalPhone() {
      var value = String(localPhoneInput.value || "").trim();
      if (value.indexOf("+") === 0) {
        localPhoneInput.setCustomValidity(t.error);
      } else {
        localPhoneInput.setCustomValidity("");
      }
    }

    localPhoneInput.addEventListener("input", validateLocalPhone);
    localPhoneInput.addEventListener("blur", validateLocalPhone);

    var entries = phoneCodes.map(function (pair) {
      var code = pair[0];
      var dialCode = pair[1];
      return {
        countryCode: code,
        countryName: localizedCountryName(code),
        englishName: englishCountryName(code),
        dialCode: dialCode
      };
    });

    entries.sort(function (a, b) {
      if (a.countryName === b.countryName) {
        return a.dialCode.localeCompare(b.dialCode);
      }
      if (collator) return collator.compare(a.countryName, b.countryName);
      return a.countryName.localeCompare(b.countryName);
    });

    phoneCodeSelect.innerHTML = "";
    var placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = t.placeholder;
    phoneCodeSelect.appendChild(placeholder);

    entries.forEach(function (entry) {
      var option = document.createElement("option");
      option.value = entry.dialCode;
      option.setAttribute("data-country-code", entry.countryCode);
      option.setAttribute("data-country-en", entry.englishName);
      option.textContent = entry.countryName + " (" + entry.dialCode + ")";
      phoneCodeSelect.appendChild(option);
    });
    phoneCodeSelect.disabled = false;
    enhancePhoneCodePicker(phoneCodeSelect, {
      placeholderText: t.placeholder,
      searchPlaceholder: t.searchPlaceholder,
      noResultsText: t.noResults,
      lang: lang,
    });
  }

  function phoneFlagAssetRoot() {
    var I18N = window.DAAB_I18N;
    if (I18N && typeof I18N.assetRoot === "function") return I18N.assetRoot();
    var root = document.documentElement.getAttribute("data-daab-asset-root");
    if (root != null && root !== "") return root.endsWith("/") ? root : root + "/";
    return "../";
  }

  function phoneFlagSrc(countryCode) {
    if (typeof window.DAAB_PHONE_FLAG_SRC === "function") {
      return window.DAAB_PHONE_FLAG_SRC(phoneFlagAssetRoot(), countryCode);
    }
    return (
      phoneFlagAssetRoot() +
      "images/flags/4x3/" +
      String(countryCode || "").toLowerCase() +
      ".svg"
    );
  }

  function enhancePhoneCodePicker(select, config) {
    if (!select || select.getAttribute("data-phone-code-picker-ready") === "1") return;
    select.setAttribute("data-phone-code-picker-ready", "1");

    var placeholderText = (config && config.placeholderText) || "";
    var searchPlaceholder = (config && config.searchPlaceholder) || "";
    var noResultsText = (config && config.noResultsText) || "";
    var lang = (config && config.lang) || "en";
    var fieldGroup = select.closest(".field-group");
    if (!fieldGroup) return;

    var picker = document.createElement("div");
    picker.className = "phone-code-picker";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = select.id ? select.id + "_picker" : "phone_code_picker";
    btn.className = "phone-code-picker-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute(
      "aria-label",
      (fieldGroup.querySelector("label.field-label") &&
        fieldGroup.querySelector("label.field-label").textContent.trim()) ||
        "Phone country code"
    );

    var valueWrap = document.createElement("span");
    valueWrap.className = "phone-code-picker-value";

    var flagImg = document.createElement("img");
    flagImg.className = "phone-code-flag";
    flagImg.alt = "";
    flagImg.setAttribute("aria-hidden", "true");
    flagImg.width = 20;
    flagImg.height = 15;
    flagImg.hidden = true;

    var labelSpan = document.createElement("span");
    labelSpan.className = "phone-code-picker-text";
    labelSpan.textContent = placeholderText;

    valueWrap.appendChild(flagImg);
    valueWrap.appendChild(labelSpan);
    btn.appendChild(valueWrap);

    var chevron = document.createElement("span");
    chevron.className = "phone-code-picker-chevron";
    chevron.setAttribute("aria-hidden", "true");
    btn.appendChild(chevron);

    var panel = document.createElement("div");
    panel.className = "phone-code-picker-panel";
    panel.hidden = true;

    var searchWrap = document.createElement("div");
    searchWrap.className = "country-picker-search-wrap";
    var search = document.createElement("input");
    search.type = "search";
    search.className = "country-picker-search";
    search.setAttribute("autocomplete", "off");
    search.setAttribute("spellcheck", "false");
    search.setAttribute("aria-label", searchPlaceholder);
    search.placeholder = searchPlaceholder;
    searchWrap.appendChild(search);

    var list = document.createElement("ul");
    list.className = "phone-code-picker-list";
    list.setAttribute("role", "listbox");
    if (btn.id) list.id = btn.id + "_list";
    btn.setAttribute("aria-controls", list.id);

    var empty = document.createElement("div");
    empty.className = "country-picker-empty";
    empty.hidden = true;
    empty.textContent = noResultsText;

    Array.prototype.forEach.call(select.options, function (opt) {
      if (!opt.value) return;
      var countryCode = opt.getAttribute("data-country-code") || "";
      var li = document.createElement("li");
      li.className = "phone-code-picker-option country-picker-option";
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      li.setAttribute("data-value", opt.value);
      li.setAttribute("data-country-code", countryCode);
      li.setAttribute("data-label", opt.textContent);
      li.setAttribute("data-country-en", opt.getAttribute("data-country-en") || "");
      li.setAttribute("data-dial", String(opt.value || "").replace(/^\+/, ""));

      var img = document.createElement("img");
      img.className = "phone-code-flag";
      img.src = phoneFlagSrc(countryCode);
      img.alt = "";
      img.setAttribute("aria-hidden", "true");
      img.width = 20;
      img.height = 15;
      img.loading = "lazy";
      img.decoding = "async";

      var text = document.createElement("span");
      text.className = "phone-code-picker-option-text";
      text.textContent = opt.textContent;

      li.appendChild(img);
      li.appendChild(text);
      list.appendChild(li);
    });

    panel.appendChild(searchWrap);
    panel.appendChild(list);
    panel.appendChild(empty);

    select.classList.add("phone-code-picker-native");
    select.parentNode.insertBefore(picker, select);
    picker.appendChild(select);
    picker.appendChild(btn);
    picker.appendChild(panel);

    var label = fieldGroup.querySelector('label[for="' + select.id + '"]');
    if (label) {
      label.setAttribute("for", btn.id);
      label.addEventListener("click", function (e) {
        e.preventDefault();
        btn.focus();
        if (panel.hidden) openPanel();
      });
    }

    function optionNodes() {
      return list.querySelectorAll(".phone-code-picker-option");
    }

    function visibleOptions() {
      return Array.prototype.filter.call(optionNodes(), function (li) {
        return !li.classList.contains("is-filtered-out");
      });
    }

    function applyFilter() {
      var query = String(search.value || "").trim().toLocaleLowerCase(lang);
      var shown = 0;
      optionNodes().forEach(function (li) {
        var hay = [
          li.getAttribute("data-label") || "",
          li.getAttribute("data-country-code") || "",
          li.getAttribute("data-country-en") || "",
          li.getAttribute("data-value") || "",
          li.getAttribute("data-dial") || "",
        ]
          .join(" ")
          .toLocaleLowerCase(lang);
        var match = !query || hay.indexOf(query) !== -1;
        li.classList.toggle("is-filtered-out", !match);
        if (match) shown += 1;
      });
      empty.hidden = shown > 0;
      list.hidden = shown === 0;
    }

    function syncFromSelect() {
      var opt = select.options[select.selectedIndex];
      btn.disabled = select.disabled;
      if (!opt || !opt.value) {
        flagImg.hidden = true;
        labelSpan.textContent = placeholderText;
        btn.classList.remove("has-value");
        optionNodes().forEach(function (li) {
          li.classList.remove("is-selected", "is-active");
          li.setAttribute("aria-selected", "false");
        });
        return;
      }
      btn.classList.add("has-value");
      var cc = opt.getAttribute("data-country-code");
      if (cc) {
        flagImg.src = phoneFlagSrc(cc);
        flagImg.hidden = false;
      } else {
        flagImg.hidden = true;
      }
      labelSpan.textContent = opt.textContent;
      optionNodes().forEach(function (li) {
        var selected =
          li.getAttribute("data-value") === opt.value &&
          li.getAttribute("data-country-code") === cc;
        li.classList.toggle("is-selected", selected);
        li.classList.toggle("is-active", selected);
        li.setAttribute("aria-selected", selected ? "true" : "false");
      });
    }

    function closePanel() {
      panel.hidden = true;
      picker.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      search.value = "";
      applyFilter();
    }

    function openPanel() {
      if (select.disabled) return;
      closeOpenPickersExcept(picker);
      search.value = "";
      applyFilter();
      panel.hidden = false;
      picker.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      var selected = list.querySelector(".phone-code-picker-option.is-selected");
      optionNodes().forEach(function (li) {
        li.classList.toggle("is-active", li === selected);
      });
      try {
        search.focus({ preventScroll: true });
      } catch (e) {
        search.focus();
      }
      if (selected) selected.scrollIntoView({ block: "nearest" });
    }

    function chooseOption(li) {
      if (!li || li.classList.contains("is-filtered-out")) return;
      var value = li.getAttribute("data-value");
      var cc = li.getAttribute("data-country-code");
      var i;
      for (i = 0; i < select.options.length; i++) {
        var option = select.options[i];
        if (option.value === value && option.getAttribute("data-country-code") === cc) {
          select.selectedIndex = i;
          break;
        }
      }
      select.dispatchEvent(new Event("change", { bubbles: true }));
      syncFromSelect();
      closePanel();
      btn.focus();
    }

    function moveActive(delta) {
      var items = visibleOptions();
      if (!items.length) return;
      var current = list.querySelector(".phone-code-picker-option.is-active:not(.is-filtered-out)");
      var index = current ? items.indexOf(current) : -1;
      var next = items[(index + delta + items.length) % items.length];
      items.forEach(function (li) {
        li.classList.toggle("is-active", li === next);
      });
      if (next) next.scrollIntoView({ block: "nearest" });
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      if (panel.hidden) openPanel();
      else closePanel();
    });

    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (panel.hidden) openPanel();
      }
    });

    search.addEventListener("input", applyFilter);
    search.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveActive(1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        moveActive(-1);
      } else if (e.key === "Enter") {
        e.preventDefault();
        var active = list.querySelector(".phone-code-picker-option.is-active:not(.is-filtered-out)");
        chooseOption(active || visibleOptions()[0]);
      } else if (e.key === "Escape") {
        e.preventDefault();
        closePanel();
        btn.focus();
      }
    });

    list.addEventListener("click", function (e) {
      var li = e.target.closest(".phone-code-picker-option");
      if (!li) return;
      chooseOption(li);
    });

    document.addEventListener("click", function (e) {
      if (picker.contains(e.target)) return;
      if (label && label.contains(e.target)) return;
      closePanel();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) {
        closePanel();
        btn.focus();
      }
    });

    select.addEventListener("change", syncFromSelect);
    syncFromSelect();
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

  function initSectionToggles() {
    var sections = Array.prototype.slice.call(
      document.querySelectorAll(".application-page .form-section")
    );
    if (!sections.length) return;

    sections.forEach(function (section) {
      var body = section.querySelector(".section-body");
      if (!body) return;

      if (!body.id && section.id) body.id = section.id + "-body";

      if (!body.querySelector(":scope > .section-body-inner")) {
        var inner = document.createElement("div");
        inner.className = "section-body-inner";
        while (body.firstChild) inner.appendChild(body.firstChild);
        body.appendChild(inner);
      }

      var toggle = section.querySelector(".app-section-toggle");
      if (!toggle) return;

      var sectionLabel =
        toggle.getAttribute("data-section-label") ||
        (section.querySelector(".section-title") &&
          section.querySelector(".section-title").childNodes[0] &&
          section.querySelector(".section-title").childNodes[0].textContent &&
          section.querySelector(".section-title").childNodes[0].textContent.trim()) ||
        section.id;

      if (body.id) toggle.setAttribute("aria-controls", body.id);

      function syncToggleState(expanded) {
        toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
        toggle.setAttribute(
          "aria-label",
          (expanded ? uiText("collapseSection") : uiText("expandSection")) +
            (sectionLabel ? ": " + sectionLabel : "")
        );
        section.classList.toggle("is-collapsed", !expanded);
        body.setAttribute("aria-hidden", expanded ? "false" : "true");
      }

      syncToggleState(true);

      toggle.addEventListener("click", function () {
        var expanded = toggle.getAttribute("aria-expanded") !== "true";
        syncToggleState(expanded);
      });
    });
  }

  window.daabApplicationGoTo = goTo;
  window.daabApplicationNext = next;
  window.daabApplicationPrev = prev;
  window.daabApplicationSubmit = submitForm;

  function initEndpointNotice() {
    if (getFormEndpoint()) {
      var box = byId("app-endpoint-notice");
      if (box) box.hidden = true;
      return;
    }
    var box = byId("app-endpoint-notice");
    if (box) {
      box.hidden = false;
      var email = "info@daab-waas.com";
      box.innerHTML =
        uiText("noEndpoint") +
        ' <a href="mailto:' +
        email +
        '">' +
        email +
        "</a>";
    }
    var submitBtn = byId("appSubmitBtn");
    if (submitBtn) submitBtn.disabled = true;
  }

  function initForumRegisterStickyStack() {
    var stack = document.querySelector(".forum-register-sticky-stack");
    var spacer = document.querySelector(".forum-register-sticky-spacer");
    if (!stack) return;

    function headerOffset() {
      var style = window.getComputedStyle(document.documentElement);
      var h = parseFloat(style.getPropertyValue("--daab-sticky-top-stack"));
      if (!isFinite(h) || h <= 0) {
        h = parseFloat(style.getPropertyValue("--daab-nav-height"));
      }
      return !isFinite(h) || h <= 0 ? 86 : h;
    }

    function slotBox() {
      return (spacer || stack).getBoundingClientRect();
    }

    function applyPinnedBox(box) {
      var root = document.documentElement;
      root.style.setProperty("--forum-register-sticky-left", box.left + "px");
      root.style.setProperty("--forum-register-sticky-width", box.width + "px");
      root.style.setProperty("--forum-register-sticky-transform", "none");
    }

    function clearPinnedBox() {
      var root = document.documentElement;
      root.style.removeProperty("--forum-register-sticky-left");
      root.style.removeProperty("--forum-register-sticky-width");
      root.style.removeProperty("--forum-register-sticky-transform");
    }

    function syncStack() {
      var box = slotBox();
      var h = Math.ceil(stack.getBoundingClientRect().height);
      document.documentElement.style.setProperty(
        "--daab-sticky-local-offset",
        Math.max(0, h) + "px"
      );
      var naturalTop = spacer
        ? spacer.getBoundingClientRect().top
        : stack.getBoundingClientRect().top;
      var pin = naturalTop <= headerOffset() + 0.5;
      if (pin) applyPinnedBox(box);
      else clearPinnedBox();
      stack.classList.toggle("is-pinned", pin);
      if (spacer) spacer.style.height = pin ? h + "px" : "0px";
    }

    syncStack();
    if (typeof ResizeObserver !== "undefined") {
      var ro = new ResizeObserver(syncStack);
      ro.observe(stack);
      if (spacer) ro.observe(spacer);
      var band = document.querySelector(".page-content-search-band");
      if (band) ro.observe(band);
    }
    window.addEventListener("resize", syncStack, { passive: true });
    window.addEventListener("scroll", syncStack, { passive: true });

    var bar = document.querySelector(".forum-register-stepbar");
    var menu = byId("appStepsMenu");
    function scrollActivePill() {
      if (!bar || !menu) return;
      var active = menu.querySelector("a.tl-active");
      if (!active) return;
      var br = bar.getBoundingClientRect();
      var ar = active.getBoundingClientRect();
      if (ar.left < br.left + 8 || ar.right > br.right - 8) {
        bar.scrollLeft += ar.left - br.left - (br.width - ar.width) / 2;
      }
    }
    if (menu && typeof MutationObserver !== "undefined") {
      var mo = new MutationObserver(scrollActivePill);
      mo.observe(menu, {
        attributes: true,
        subtree: true,
        attributeFilter: ["class"],
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.classList.contains("application-page")) return;
    totalSections = countFormSections();
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.hidden = false;
    });
    var form = mainFormEl();
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        submitForm();
      });
    }
    bindRadioHighlight();
    initEmailValidation();
    initForumIdentityValidation();
    initCountryDropdowns();
    initPhoneCodeDropdown();
    initSectionToggles();
    initEndpointNotice();
    initForumRegisterStickyStack();
    updateProgress(1);
    initFileUploads();
    initSciFieldLimit();
    var sciFieldset = byId("sci-fields");
    if (sciFieldset) {
      sciFieldset.addEventListener("change", function () {
        if (getSciValues().length > 0) {
          sciFieldset.removeAttribute("aria-invalid");
          var box = byId("app-submit-status");
          if (box && box.classList.contains("app-submit-status--error")) {
            clearSubmitStatus();
          }
        }
      });
    }
    var submitBtn = byId("appSubmitBtn");
    if (submitBtn && !submitBtn.textContent.trim()) {
      submitBtn.textContent = uiText("submit");
    }
  });
})();
