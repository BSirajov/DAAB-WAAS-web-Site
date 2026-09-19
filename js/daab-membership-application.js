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
  var membershipScriptEl = document.currentScript;
  // Capitals and local-name aliases to pin and keep searchable.
  var CITY_GUARANTEES = {
    AG: [{ name: "Saint John's", aliases: ["St. John's", "Saint Johns", "St Johns"] }],
    AT: [
      { name: "Vienna", aliases: ["Wien", "Wien Stadt", "Vienna", "Vyana", "Viyana", "Vena"] },
      { name: "Wien", aliases: ["Vienna", "Wien Stadt"] },
    ],
    BF: [{ name: "Ouagadougou", aliases: ["Vaqaduqu"] }],
    BJ: [{ name: "Porto-Novo", aliases: ["Porto Novo"] }],
    CD: [{ name: "Kinshasa", aliases: ["Kinşasa"] }],
    CG: [{ name: "Brazzaville", aliases: ["Brazavil"] }],
    CM: [
      { name: "Yaoundé", aliases: ["Yaounde", "Yaunde"] },
      { name: "Yaounde", aliases: ["Yaoundé", "Yaunde"] },
    ],
    CO: [
      { name: "Bogotá", aliases: ["Bogota", "Santa Fe de Bogota", "Boqota"] },
      { name: "Bogota", aliases: ["Bogotá"] },
    ],
    CZ: [
      { name: "Prague", aliases: ["Praha", "Praqa"] },
      { name: "Praha", aliases: ["Prague", "Praqa"] },
    ],
    DM: [{ name: "Roseau", aliases: ["Rozo"] }],
    EG: [
      { name: "Cairo", aliases: ["Qahirə", "Kairo", "Al Qahirah", "Al-Qahirah", "Al Qāhirah"] },
      { name: "Qahirə", aliases: ["Cairo", "Kairo"] },
    ],
    ER: [{ name: "Asmara", aliases: ["Asmera"] }],
    FM: [{ name: "Palikir", aliases: ["Palikir, Pohnpei"] }],
    GQ: [{ name: "Malabo", aliases: [] }],
    GY: [{ name: "Georgetown", aliases: ["George Town"] }],
    IR: [{ name: "Tehran", aliases: ["Teheran", "Tehran"] }],
    KI: [{ name: "Tarawa", aliases: ["South Tarawa", "Bairiki"] }],
    KM: [{ name: "Moroni", aliases: [] }],
    LA: [
      { name: "Vientiane", aliases: ["Viangchan", "Vyençyan"] },
      { name: "Viangchan", aliases: ["Vientiane"] },
    ],
    LR: [{ name: "Monrovia", aliases: ["Monroviya"] }],
    MC: [{ name: "Monaco", aliases: ["Monako", "Monaco-Ville"] }],
    MD: [
      { name: "Chișinău", aliases: ["Chisinau", "Kishinev", "Kişinyov"] },
      { name: "Chisinau", aliases: ["Chișinău", "Kishinev", "Kişinyov"] },
    ],
    MK: [{ name: "Skopje", aliases: ["Skopye", "Üsküb"] }],
    MV: [
      { name: "Malé", aliases: ["Male", "Maale"] },
      { name: "Male", aliases: ["Malé", "Maale"] },
    ],
    PS: [{ name: "Ramallah", aliases: ["Ramallah and Al-Bireh", "Ramalla"] }],
    PY: [
      { name: "Asunción", aliases: ["Asuncion"] },
      { name: "Asuncion", aliases: ["Asunción"] },
    ],
    QA: [
      { name: "Doha", aliases: ["Ad Dawhah", "Ad-Dawhah", "Doha"] },
      { name: "Ad Dawhah", aliases: ["Doha"] },
    ],
    SC: [{ name: "Victoria", aliases: ["Victoria, Seychelles"] }],
    SL: [{ name: "Freetown", aliases: [] }],
    SO: [{ name: "Mogadishu", aliases: ["Muqdisho", "Mogadiso"] }],
    SY: [
      { name: "Damascus", aliases: ["Dimashq", "Dəməşq", "Damashq", "Sham"] },
      { name: "Dimashq", aliases: ["Damascus", "Dəməşq"] },
    ],
    SS: [{ name: "Juba", aliases: [] }],
    SZ: [{ name: "Mbabane", aliases: ["Lobamba"] }],
    TD: [
      { name: "N'Djamena", aliases: ["Ndjamena", "NDjamena", "Ncamena"] },
      { name: "Ndjamena", aliases: ["N'Djamena"] },
    ],
    TG: [
      { name: "Lomé", aliases: ["Lome"] },
      { name: "Lome", aliases: ["Lomé"] },
    ],
    TJ: [{ name: "Dushanbe", aliases: ["Düşənbə", "Dyushambe"] }],
    TO: [{ name: "Nuku'alofa", aliases: ["Nukualofa", "Nukuʻalofa"] }],
    TV: [{ name: "Funafuti", aliases: [] }],
    UZ: [
      { name: "Tashkent", aliases: ["Toshkent", "Toshkent Shahri", "Daşkənd"] },
      { name: "Toshkent", aliases: ["Tashkent", "Toshkent Shahri", "Daşkənd"] },
    ],
    VA: [{ name: "Vatican City", aliases: ["Vatican", "Vatikan", "Holy See"] }],
    VU: [{ name: "Port Vila", aliases: ["Port-Vila"] }],
    WS: [{ name: "Apia", aliases: [] }],
    XK: [
      { name: "Pristina", aliases: ["Prishtina", "Priština", "Priştina", "Priştinə"] },
      { name: "Prishtina", aliases: ["Pristina", "Priština"] },
    ],
    YE: [
      { name: "Sanaa", aliases: ["Sana'a", "San'a'", "Səna"] },
      { name: "Sana'a", aliases: ["Sanaa", "San'a'"] },
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

  function foldSearch(text) {
    var AZ = {
      "\u0259": "e", "\u0131": "i", "\u00f6": "o", "\u00fc": "u",
      "\u011f": "g", "\u015f": "s", "\u00e7": "c",
      "\u018f": "e", "\u0130": "i", "\u00d6": "o", "\u00dc": "u",
      "\u011e": "g", "\u015e": "s", "\u00c7": "c"
    };
    return String(text || "")
      .replace(/[^\u0000-\u007f]/g, function (ch) { return AZ[ch] || ch; })
      .toLowerCase()
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ")
      .trim();
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
    var dob = byId("dob");
    if (dob && String(dob.value || "").trim()) {
      dob.value = normalizeDobTypedValue(dob.value);
    }
    applyForumIdentityValidity();
    var emailInput = byId("email");
    if (emailInput && String(emailInput.value || "").trim() && !isEmailValid(emailInput.value || "")) {
      warnRequiredField(emailInput, emailInput.validationMessage || uiText("requiredFields"));
      return false;
    }
    if (!form.checkValidity()) {
      var invalid = form.querySelector(":invalid");
      warnRequiredField(invalid, requiredFieldMessage(invalid));
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
        degreeOtherRequired: "Digər akademik dərəcəni yazın.",
        titleRequired: "Akademik titulunuzu seçin.",
        titleOtherRequired: "Digər akademik titulu yazın.",
        genderRequired: "Cinsinizi seçin.",
        fatherNameRequired: "Atanızın adını daxil edin.",
        dobRequired: "Doğum tarixinizi daxil edin.",
        dobInvalid: "Tarixi dd/mm/yyyy formatında daxil edin.",
        dobCalendar: "Təqvimi aç",
        birthCountryRequired: "Doğulduğunuz ölkəni seçin.",
        citizenshipRequired: "Vətəndaşlığınızı seçin.",
        residenceCountryRequired: "Yaşadığınız ölkəni seçin.",
        requiredFields: "Zəhmət olmasa bütün məcburi sahələri doldurun.",
        requiredFieldNamed: "«{field}» sahəsi məcburidir.",
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
        reviewTitle: "Müraciətinizi yoxlayın",
        reviewLead: "Göndərməzdən əvvəl xülasəni yoxlayın. PDF də hazırlanır; istəsəniz yükləyə və aça bilərsiniz. Hər şey düzgündürsə, müraciəti göndərin.",
        reviewPreparing: "PDF xülasə hazırlanır…",
        reviewReady: "PDF xülasə hazırdır. Yoxlayın, sonra göndərin.",
        reviewFailed: "PDF hazırlanmadı. Məlumatları aşağıda yoxlaya, sonra göndərə bilərsiniz.",
        reviewDownload: "PDF yüklə",
        reviewOpenPdf: "PDF-ə bax",
        reviewEdit: "Düzəliş et",
        reviewClose: "Bağla",
        reviewEmpty: "Göstərilməyib",
        reviewYes: "Bəli",
        reviewNo: "Xeyr",
        reviewPrivacy: "Məxfilik bildirişi",
        reviewCvConfirm: "Foto və CV göndərmə təsdiqi",
        reviewSci: "Elmi sahələr",
        reviewPdfTitleForum: "Forum 2026 iştirakçı qeydiyyatı — xülasə",
        reviewPdfTitleMember: "Üzvlük müraciəti — xülasə",
        reviewGenerated: "Hazırlanma tarixi",
        reviewOrg: "Dünya Azərbaycanlı Alimlər Birliyi",
      },
      en: {
        submitting: "Submitting…",
        submit: "✓ Submit Application",
        sciRequired: "Select at least one scientific field.",
        sciLimitExceeded: "You can select up to two scientific fields. Deselect one of your current choices before selecting another.",
        degreeRequired: "Please select your academic degree.",
        degreeOtherRequired: "Please enter the other academic degree.",
        titleRequired: "Please select your academic title.",
        titleOtherRequired: "Please enter the other academic title.",
        genderRequired: "Please select your gender.",
        fatherNameRequired: "Please enter your father’s name.",
        dobRequired: "Please enter your date of birth.",
        dobInvalid: "Enter the date as dd/mm/yyyy.",
        dobCalendar: "Open calendar",
        birthCountryRequired: "Please select your country of birth.",
        citizenshipRequired: "Please select your citizenship.",
        residenceCountryRequired: "Please select your country of residence.",
        requiredFields: "Please fill in all required fields.",
        requiredFieldNamed: "“{field}” is required.",
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
        reviewTitle: "Review your application",
        reviewLead: "Review the summary before sending. A PDF is also prepared so you can download or open it. If everything is correct, send the application.",
        reviewPreparing: "Preparing the PDF summary…",
        reviewReady: "The PDF summary is ready. Review it, then send.",
        reviewFailed: "The PDF could not be created. You can still review the details below, then send.",
        reviewDownload: "Download PDF",
        reviewOpenPdf: "Open PDF",
        reviewEdit: "Edit",
        reviewClose: "Close",
        reviewEmpty: "Not provided",
        reviewYes: "Yes",
        reviewNo: "No",
        reviewPrivacy: "Privacy notice",
        reviewCvConfirm: "Photo and CV email confirmation",
        reviewSci: "Scientific fields",
        reviewPdfTitleForum: "Forum 2026 participant registration — summary",
        reviewPdfTitleMember: "Membership application — summary",
        reviewGenerated: "Generated",
        reviewOrg: "World Association of Azerbaijani Scientists",
      },
    };
    return (strings[lang] || strings.en)[key] || key;
  }

  function playValidationBeep() {
    function tone(ctx, start, freq, duration) {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.type = "square";
      osc.frequency.setValueAtTime(freq, start);
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.exponentialRampToValueAtTime(0.22, start + 0.01);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(start);
      osc.stop(start + duration);
    }

    function playFromContext(ctx) {
      var t = ctx.currentTime;
      tone(ctx, t, 880, 0.14);
      tone(ctx, t + 0.16, 660, 0.18);
    }

    try {
      var Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      if (!playValidationBeep._ctx) playValidationBeep._ctx = new Ctx();
      var ctx = playValidationBeep._ctx;
      if (ctx.state === "suspended" && ctx.resume) {
        ctx.resume().then(function () {
          playFromContext(ctx);
        }).catch(function () {});
        return;
      }
      playFromContext(ctx);
    } catch (e) {}
  }

  function labelTextForControl(el) {
    if (!el) return "";
    var text = "";
    if (el.id) {
      var forLabel = document.querySelector('.application-page label[for="' + el.id + '"]');
      if (forLabel) text = forLabel.textContent;
    }
    if (!text && el.labels && el.labels[0]) text = el.labels[0].textContent;
    if (!text) {
      var group = el.closest(".field-group");
      var lab = group && (group.querySelector("label.field-label") || group.querySelector(".field-label"));
      if (lab) text = lab.textContent;
    }
    return String(text || "")
      .replace(/\s*\*\s*/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function requiredFieldMessage(el) {
    var label = labelTextForControl(el);
    if (label) return uiText("requiredFieldNamed").replace("{field}", label);
    return uiText("requiredFields");
  }

  function clearFieldRequiredWarnings() {
    document.querySelectorAll(".application-page .field-required-warning").forEach(function (note) {
      note.parentNode.removeChild(note);
    });
    document.querySelectorAll(".application-page .is-required-invalid").forEach(function (el) {
      el.classList.remove("is-required-invalid");
      if (el.getAttribute("aria-invalid") === "true") el.removeAttribute("aria-invalid");
    });
  }

  function visibleTargetForControl(el) {
    if (!el) return null;
    if (el.classList && el.classList.contains("phone-code-picker-native")) {
      var pickerBtn = el.closest(".phone-code-picker") && el.closest(".phone-code-picker").querySelector(".phone-code-picker-btn");
      if (pickerBtn) return pickerBtn;
    }
    if (el.nodeName === "FIELDSET") {
      return el.querySelector("input, select, textarea") || el;
    }
    return el;
  }

  function focusInvalidControl(el) {
    if (!el) return;
    var target = visibleTargetForControl(el) || el;
    try {
      target.focus({ preventScroll: true });
    } catch (e) {
      try {
        target.focus();
      } catch (e2) {}
    }
    if (typeof target.scrollIntoView === "function") {
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  function showValidationToast(message) {
    var toast = byId("app-validation-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "app-validation-toast";
      toast.className = "app-validation-toast";
      toast.setAttribute("role", "alert");
      document.body.appendChild(toast);
    }
    toast.textContent = message || "";
    toast.hidden = !message;
  }

  function showFieldRequiredWarning(el, message) {
    clearFieldRequiredWarnings();
    if (!el) return;
    el.classList.add("is-required-invalid");
    el.setAttribute("aria-invalid", "true");
    var group =
      el.closest(".field-group") ||
      el.closest(".sci-fields-fieldset") ||
      el.closest(".opt-item") ||
      el.parentNode;
    if (!group) return;
    var note = document.createElement("p");
    note.className = "field-required-warning";
    note.setAttribute("role", "alert");
    note.textContent = message;
    group.appendChild(note);
    focusInvalidControl(el);
  }

  function warnRequiredField(el, message) {
    var text = message || requiredFieldMessage(el);
    showSubmitError(text, { alert: true });
    showFieldRequiredWarning(el, text);
  }

  function showSubmitError(message, options) {
    var opts = options || {};
    var box = byId("app-submit-status");
    if (box) {
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
    if (opts.alert) {
      showValidationToast(message);
      playValidationBeep();
    }
  }

  function clearSubmitStatus() {
    var box = byId("app-submit-status");
    if (box) {
      box.hidden = true;
      box.textContent = "";
      box.className = "app-submit-status";
      box.setAttribute("role", "status");
      box.setAttribute("aria-live", "polite");
    }
    showValidationToast("");
    clearFieldRequiredWarnings();
    var sciFieldset = byId("sci-fields");
    if (sciFieldset) sciFieldset.removeAttribute("aria-invalid");
  }

  function setSubmitting(isSubmitting) {
    var btn = byId("appSubmitBtn");
    if (btn) {
      btn.disabled = isSubmitting;
      btn.classList.toggle("is-loading", isSubmitting);
      btn.textContent = isSubmitting ? uiText("submitting") : uiText("submit");
    }
    var send = byId("app-review-send");
    if (send) {
      send.disabled = isSubmitting;
      send.classList.toggle("is-loading", isSubmitting);
      send.textContent = isSubmitting ? uiText("submitting") : uiText("submit");
    }
    var edit = byId("app-review-edit");
    var download = byId("app-review-download");
    if (edit) edit.disabled = isSubmitting;
    if (download) download.disabled = isSubmitting || !reviewPdfBlob;
    var openPdf = byId("app-review-open");
    if (openPdf) openPdf.disabled = isSubmitting || !reviewPdfBlob;
  }

  function getOtherSpecifyInput(radioName) {
    return document.querySelector(
      '.application-page .other-specify-input[data-other-for="' + radioName + '"]'
    );
  }

  function getOtherSpecifyValue(radioName) {
    if (getRadioValue(radioName) !== "other") return "";
    var input = getOtherSpecifyInput(radioName);
    return (input && String(input.value || "").trim()) || "";
  }

  function radioValueForSubmit(radioName) {
    var value = getRadioValue(radioName);
    if (value !== "other") return value;
    var specified = getOtherSpecifyValue(radioName);
    return specified ? "other: " + specified : value;
  }

  function syncOtherSpecify(radioName) {
    var input = getOtherSpecifyInput(radioName);
    if (!input) return;
    var show = getRadioValue(radioName) === "other";
    input.hidden = !show;
    input.required = show;
    if (show) {
      input.removeAttribute("aria-hidden");
    } else {
      input.value = "";
      input.setAttribute("aria-hidden", "true");
    }
  }

  function initOtherSpecifyFields() {
    document.querySelectorAll(".application-page .other-specify-input[data-other-for]").forEach(function (input) {
      var radioName = input.getAttribute("data-other-for");
      if (!radioName) return;
      document.querySelectorAll('.application-page input[name="' + radioName + '"]').forEach(function (radio) {
        radio.addEventListener("change", function () {
          syncOtherSpecify(radioName);
          if (getRadioValue(radioName) === "other") {
            try {
              input.focus({ preventScroll: true });
            } catch (e) {
              input.focus();
            }
          }
        });
      });
      syncOtherSpecify(radioName);
    });
  }

  function validateOtherSpecify(radioName, messageKey) {
    if (getRadioValue(radioName) !== "other") return true;
    if (getOtherSpecifyValue(radioName)) return true;
    var input = getOtherSpecifyInput(radioName);
    warnRequiredField(input, uiText(messageKey));
    if (input) {
      try {
        input.focus({ preventScroll: true });
      } catch (e) {
        input.focus();
      }
      input.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    return false;
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
    var card = document.querySelector('.app-file-card[data-file-kind="' + firstKind + '"]');
    warnRequiredField(card || byId(uploadInputId(firstKind)), firstError);
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
    warnRequiredField(field, uiText("privacyRequired"));
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
    warnRequiredField(sciFieldset, uiText("sciRequired"));
    var sec = sciFieldset && sciFieldset.closest
      ? sciFieldset.closest(".form-section")
      : byId("sec-4") || byId("sec-3");
    if (sec) sec.scrollIntoView({ behavior: "smooth", block: "start" });
    return false;
  }

  function validateRadioGroup(name, messageKey, focusId) {
    if (getRadioValue(name)) return true;
    var focusEl = byId(focusId) || document.querySelector(
      '.application-page input[name="' + name + '"]'
    );
    warnRequiredField(focusEl, uiText(messageKey));
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
      degree: radioValueForSubmit("degree"),
      degree_other: getOtherSpecifyValue("degree"),
      degree_institution: (byId("deginst") && byId("deginst").value.trim()) || "",
      academic_title: radioValueForSubmit("title"),
      title_other: getOtherSpecifyValue("title"),
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

  var reviewPdfBlob = null;
  var reviewPdfUrl = "";
  var reviewDialogOpen = false;
  var reviewLastFocus = null;
  var reviewPdfLibsPromise = null;
  var reviewScrollY = 0;
  var PDF_CAPTURE_SCALE = 2;

  function lockReviewScroll() {
    reviewScrollY = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.style.top = "-" + reviewScrollY + "px";
    document.body.classList.add("app-review-open");
  }

  function unlockReviewScroll() {
    document.body.classList.remove("app-review-open");
    document.body.style.top = "";
    if (typeof window.scrollTo === "function") {
      window.scrollTo(0, reviewScrollY);
    }
  }

  function applicationAssetRoot() {
    var fromAttr = document.documentElement.getAttribute("data-daab-asset-root");
    if (fromAttr) return fromAttr;
    var path = String(location.pathname || "").replace(/\\/g, "/");
    if (/\/(az|en)\/forum\//.test(path)) return "../../../";
    if (/\/(az|en)\//.test(path)) return "../";
    return "";
  }

  function loadScriptOnce(src) {
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[src="' + src + '"]');
      if (existing) {
        if (existing.getAttribute("data-daab-loaded") === "1") {
          resolve();
          return;
        }
        existing.addEventListener("load", function () { resolve(); }, { once: true });
        existing.addEventListener("error", function () { reject(new Error("Script failed: " + src)); }, { once: true });
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
        reject(new Error("Script failed: " + src));
      };
      document.head.appendChild(script);
    });
  }

  function getJsPDFConstructor() {
    if (window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
    if (typeof window.jsPDF === "function") return window.jsPDF;
    return null;
  }

  function ensurePdfLibs() {
    if (window.html2canvas && getJsPDFConstructor()) return Promise.resolve();
    if (reviewPdfLibsPromise) return reviewPdfLibsPromise;
    var root = applicationAssetRoot();
    reviewPdfLibsPromise = loadScriptOnce(root + "js/vendor/html2canvas.min.js?v=1").then(function () {
      return loadScriptOnce(root + "js/vendor/jspdf.umd.min.js?v=1");
    });
    return reviewPdfLibsPromise;
  }

  function cleanReviewLabel(text) {
    return String(text || "")
      .replace(/\s*\*\s*/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function radioDisplayLabel(el) {
    if (!el) return "";
    if (el.id) {
      var lab = document.querySelector('.application-page label[for="' + el.id + '"]');
      if (lab) return cleanReviewLabel(lab.textContent);
    }
    return el.value || "";
  }

  function sciDisplayLabels() {
    return Array.prototype.map.call(
      document.querySelectorAll('.application-page input[name="sci"]:checked'),
      function (el) {
        return radioDisplayLabel(el) || el.value;
      }
    );
  }

  function shouldSkipReviewControl(el) {
    if (!el) return true;
    if (el.id === "website" || el.id === "dob_picker") return true;
    if (el.classList.contains("dob-native-picker")) return true;
    if (el.classList.contains("other-specify-input")) return true;
    if (el.id === "city_manual") return true;
    if (el.type === "hidden" || el.type === "button" || el.type === "submit") return true;
    return false;
  }

  function collectReviewSections() {
    var sections = [];
    document.querySelectorAll(".application-page .form-section").forEach(function (sec) {
      var titleEl = sec.querySelector(".section-title");
      var title = "";
      if (titleEl) {
        var small = titleEl.querySelector("small");
        title = cleanReviewLabel(
          small
            ? String(titleEl.textContent || "").replace(small.textContent || "", "")
            : titleEl.textContent
        );
      }
      var rows = [];

      function addRow(label, value) {
        if (!label) return;
        rows.push({
          label: label,
          value: String(value || "").trim() || uiText("reviewEmpty"),
        });
      }

      sec.querySelectorAll(".field-group").forEach(function (group) {
        if (group.querySelector(".opt-item-privacy-confirm")) {
          addRow(uiText("reviewPrivacy"), getPrivacyConfirmValue() ? uiText("reviewYes") : uiText("reviewNo"));
          return;
        }
        if (group.querySelector(".opt-item-cv-confirm")) {
          addRow(uiText("reviewCvConfirm"), getCvConfirmValue() ? uiText("reviewYes") : uiText("reviewNo"));
          return;
        }
        var radios = group.querySelectorAll('input[type="radio"]');
        if (radios.length) {
          var name = radios[0].name;
          var checked = document.querySelector('.application-page input[name="' + name + '"]:checked');
          var lab = group.querySelector(".field-label");
          var value = "";
          if (checked) {
            value = radioDisplayLabel(checked);
            if (checked.value === "other") {
              var spec = getOtherSpecifyValue(name);
              if (spec) value = value + " — " + spec;
            }
          }
          addRow(cleanReviewLabel(lab && lab.textContent), value);
          return;
        }
        var control = null;
        Array.prototype.forEach.call(group.querySelectorAll("textarea, select, input"), function (el) {
          if (control) return;
          if (shouldSkipReviewControl(el)) return;
          if (el.type === "radio" || el.type === "checkbox" || el.type === "file") return;
          control = el;
        });
        if (!control) return;
        if (control.id === "phone_code") return;
        var val = "";
        if (control.id === "city") val = getCityValue();
        else if (control.id === "phone") {
          var code = (byId("phone_code") && byId("phone_code").value.trim()) || "";
          val = ((code ? code + " " : "") + String(control.value || "").trim()).trim();
        } else {
          val = String(control.value || "").trim();
        }
        addRow(
          labelTextForControl(control) || cleanReviewLabel((group.querySelector(".field-label") || {}).textContent),
          val
        );
      });

      var sci = sec.querySelector("#sci-fields");
      if (sci) {
        addRow(
          cleanReviewLabel((sci.querySelector("legend") || {}).textContent) || uiText("reviewSci"),
          sciDisplayLabels().join("; ")
        );
      }

      sec.querySelectorAll(".app-file-card").forEach(function (card) {
        var input = card.querySelector("input[type=file]");
        if (!input) return;
        var file = input.files && input.files[0];
        addRow(labelTextForControl(input), file ? file.name : "");
      });

      if (rows.length) sections.push({ title: title, rows: rows });
    });
    return sections;
  }

  function reviewDocumentTitle() {
    return isForumRegister() ? uiText("reviewPdfTitleForum") : uiText("reviewPdfTitleMember");
  }

  function reviewApplicantName() {
    var first = (byId("name") && byId("name").value.trim()) || "";
    var last = (byId("surname") && byId("surname").value.trim()) || "";
    return (first + " " + last).trim();
  }

  function formatReviewDate(date) {
    var lang = detectLang();
    try {
      return new Intl.DateTimeFormat(lang === "az" ? "az-AZ" : "en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(date);
    } catch (e) {
      return date.toISOString();
    }
  }

  function buildReviewSheetHtml(sections) {
    var rowsHtml = sections
      .map(function (section) {
        var body = section.rows
          .map(function (row) {
            return (
              '<div class="app-review-row">' +
              '<div class="app-review-k">' +
              escapeHtml(row.label) +
              "</div>" +
              '<div class="app-review-v">' +
              escapeHtml(row.value).replace(/\n/g, "<br>") +
              "</div>" +
              "</div>"
            );
          })
          .join("");
        return (
          '<section class="app-review-sec">' +
          (section.title ? "<h2>" + escapeHtml(section.title) + "</h2>" : "") +
          body +
          "</section>"
        );
      })
      .join("");
    return (
      '<div class="app-review-sheet">' +
      '<p class="app-review-org">' +
      escapeHtml(uiText("reviewOrg")) +
      "</p>" +
      "<h1>" +
      escapeHtml(reviewDocumentTitle()) +
      "</h1>" +
      (reviewApplicantName()
        ? '<p class="app-review-who">' + escapeHtml(reviewApplicantName()) + "</p>"
        : "") +
      '<p class="app-review-meta">' +
      escapeHtml(uiText("reviewGenerated")) +
      ": " +
      escapeHtml(formatReviewDate(new Date())) +
      "</p>" +
      rowsHtml +
      "</div>"
    );
  }

  function revokeReviewPdfUrl() {
    if (reviewPdfUrl) {
      var url = reviewPdfUrl;
      window.setTimeout(function () {
        URL.revokeObjectURL(url);
      }, 120000);
      reviewPdfUrl = "";
    }
    reviewPdfBlob = null;
  }

  function reviewPdfFileName() {
    var who = reviewApplicantName().replace(/\s+/g, "-") || "application";
    var safe = who.replace(/[\\/:*?"<>|]+/g, "");
    if (isForumRegister()) {
      return (detectLang() === "az" ? "Forum-2026-qeydiyyat-" : "Forum-2026-registration-") + safe + ".pdf";
    }
    return (detectLang() === "az" ? "DAAB-uzvluk-" : "WAAS-membership-") + safe + ".pdf";
  }

  function canvasToMultiPageA4Pdf(canvas) {
    var JsPDF = getJsPDFConstructor();
    if (!JsPDF) throw new Error("jsPDF library is not loaded.");
    var pdf = new JsPDF({
      unit: "mm",
      format: "a4",
      orientation: "portrait",
      compress: true,
    });
    var pageW = pdf.internal.pageSize.getWidth();
    var pageH = pdf.internal.pageSize.getHeight();
    var imgW = pageW;
    var imgH = (canvas.height * pageW) / canvas.width;
    var imgData;
    try {
      imgData = canvas.toDataURL("image/jpeg", 0.92);
    } catch (err) {
      imgData = canvas.toDataURL("image/png");
    }
    var format = imgData.indexOf("data:image/png") === 0 ? "PNG" : "JPEG";
    var y = 0;
    var remaining = imgH;
    pdf.addImage(imgData, format, 0, y, imgW, imgH, undefined, "FAST");
    remaining -= pageH;
    while (remaining > 2) {
      y -= pageH;
      pdf.addPage();
      pdf.addImage(imgData, format, 0, y, imgW, imgH, undefined, "FAST");
      remaining -= pageH;
    }
    return pdf.output("blob");
  }

  function generateReviewPdfBlob(sheet) {
    return ensurePdfLibs().then(function () {
      var waitFonts =
        document.fonts && document.fonts.ready
          ? Promise.race([
              document.fonts.ready,
              new Promise(function (resolve) {
                window.setTimeout(resolve, 4000);
              }),
            ])
          : Promise.resolve();
      return waitFonts.then(function () {
        return new Promise(function (resolve) {
          requestAnimationFrame(function () {
            requestAnimationFrame(resolve);
          });
        }).then(function () {
          var width = Math.max(sheet.scrollWidth, sheet.offsetWidth, 794);
          var height = Math.max(sheet.scrollHeight, sheet.offsetHeight, 1);
          return window.html2canvas(sheet, {
            scale: PDF_CAPTURE_SCALE,
            useCORS: true,
            logging: false,
            backgroundColor: "#ffffff",
            scrollX: 0,
            scrollY: 0,
            width: width,
            height: height,
            windowWidth: width,
            windowHeight: height + 24,
            x: 0,
            y: 0,
          });
        });
      });
    }).then(function (canvas) {
      if (!canvas || canvas.width < 10 || canvas.height < 10) {
        throw new Error("PDF capture returned an empty image.");
      }
      return canvasToMultiPageA4Pdf(canvas);
    });
  }

  function setReviewStatus(message, isError) {
    var status = byId("app-review-status");
    if (!status) return;
    status.textContent = message || "";
    status.classList.toggle("is-error", !!isError);
  }

  function renderReviewHtmlFallback(sections) {
    var box = byId("app-review-html");
    if (!box) return;
    box.innerHTML = buildReviewSheetHtml(sections);
    box.hidden = false;
  }

  function showReviewPdf(blob) {
    revokeReviewPdfUrl();
    reviewPdfBlob = blob;
    reviewPdfUrl = URL.createObjectURL(blob);
    var frame = byId("app-review-frame");
    var html = byId("app-review-html");
    if (frame) {
      frame.src = reviewPdfUrl;
      frame.hidden = false;
    }
    if (html) html.hidden = true;
    var download = byId("app-review-download");
    var openPdf = byId("app-review-open");
    if (download) download.disabled = false;
    if (openPdf) openPdf.disabled = false;
  }

  function downloadReviewPdf() {
    if (!reviewPdfBlob) return;
    var link = document.createElement("a");
    link.href = reviewPdfUrl || URL.createObjectURL(reviewPdfBlob);
    link.download = reviewPdfFileName();
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    link.remove();
  }

  function openReviewPdfTab() {
    if (!reviewPdfUrl && reviewPdfBlob) {
      reviewPdfUrl = URL.createObjectURL(reviewPdfBlob);
    }
    if (!reviewPdfUrl) return;
    window.open(reviewPdfUrl, "_blank", "noopener");
  }

  function onReviewKeydown(e) {
    if (!reviewDialogOpen) return;
    if (e.key === "Escape") {
      e.preventDefault();
      closeApplicationReview();
    }
  }

  function ensureReviewDialog() {
    var existing = byId("app-review-dialog");
    if (existing) return existing;
    var wrap = document.createElement("div");
    wrap.id = "app-review-dialog";
    wrap.className = "app-review-dialog";
    wrap.hidden = true;
    wrap.innerHTML =
      '<div class="app-review-panel" role="dialog" aria-modal="true" aria-labelledby="app-review-title">' +
      '<div class="app-review-head">' +
      '<div class="app-review-head-copy">' +
      '<h2 id="app-review-title"></h2>' +
      '<p id="app-review-lead"></p>' +
      '<p id="app-review-status" role="status" aria-live="polite"></p>' +
      "</div>" +
      '<button type="button" class="app-review-x" id="app-review-close"></button>' +
      "</div>" +
      '<div class="app-review-body">' +
      '<iframe id="app-review-frame" class="app-review-frame" title="" hidden></iframe>' +
      '<div id="app-review-html" class="app-review-html"></div>' +
      "</div>" +
      '<div class="app-review-actions">' +
      '<button type="button" class="app-btn app-btn-secondary" id="app-review-edit"></button>' +
      '<button type="button" class="app-btn app-btn-secondary" id="app-review-open" disabled></button>' +
      '<button type="button" class="app-btn app-btn-secondary" id="app-review-download" disabled></button>' +
      '<button type="button" class="app-btn app-btn-submit" id="app-review-send"></button>' +
      "</div>" +
      "</div>";
    document.body.appendChild(wrap);
    wrap.addEventListener("click", function (e) {
      if (e.target === wrap) closeApplicationReview();
    });
    byId("app-review-close").addEventListener("click", closeApplicationReview);
    byId("app-review-edit").addEventListener("click", closeApplicationReview);
    byId("app-review-download").addEventListener("click", downloadReviewPdf);
    byId("app-review-open").addEventListener("click", openReviewPdfTab);
    byId("app-review-send").addEventListener("click", sendApplication);
    return wrap;
  }

  function syncReviewDialogCopy() {
    var title = byId("app-review-title");
    var lead = byId("app-review-lead");
    var close = byId("app-review-close");
    var edit = byId("app-review-edit");
    var download = byId("app-review-download");
    var openPdf = byId("app-review-open");
    var send = byId("app-review-send");
    var frame = byId("app-review-frame");
    if (title) title.textContent = uiText("reviewTitle");
    if (lead) lead.textContent = uiText("reviewLead");
    if (close) {
      close.textContent = "×";
      close.setAttribute("aria-label", uiText("reviewClose"));
    }
    if (edit) edit.textContent = uiText("reviewEdit");
    if (download) download.textContent = uiText("reviewDownload");
    if (openPdf) openPdf.textContent = uiText("reviewOpenPdf");
    if (send) send.textContent = uiText("submit");
    if (frame) frame.setAttribute("title", reviewDocumentTitle());
  }

  function closeApplicationReview() {
    var dialog = byId("app-review-dialog");
    if (dialog) {
      dialog.hidden = true;
      dialog.style.display = "";
    }
    reviewDialogOpen = false;
    unlockReviewScroll();
    document.removeEventListener("keydown", onReviewKeydown);
    revokeReviewPdfUrl();
    var frame = byId("app-review-frame");
    if (frame) {
      frame.removeAttribute("src");
      frame.hidden = true;
    }
    var html = byId("app-review-html");
    if (html) {
      html.innerHTML = "";
      html.hidden = true;
    }
    var download = byId("app-review-download");
    var openPdfBtn = byId("app-review-open");
    if (download) download.disabled = true;
    if (openPdfBtn) openPdfBtn.disabled = true;
    if (reviewLastFocus && typeof reviewLastFocus.focus === "function") {
      try {
        reviewLastFocus.focus();
      } catch (e) {}
    }
    reviewLastFocus = null;
  }

  function openApplicationReview() {
    var sections = collectReviewSections();
    var dialog = ensureReviewDialog();
    syncReviewDialogCopy();
    reviewLastFocus = document.activeElement;
    reviewDialogOpen = true;
    lockReviewScroll();
    dialog.hidden = false;
    dialog.style.display = "flex";
    renderReviewHtmlFallback(sections);
    setReviewStatus(uiText("reviewPreparing"));
    var download = byId("app-review-download");
    if (download) download.disabled = true;
    document.addEventListener("keydown", onReviewKeydown);
    var send = byId("app-review-send");
    if (send) send.focus();

    var stage = document.createElement("div");
    stage.id = "daab-app-review-export-stage";
    stage.setAttribute("aria-hidden", "true");
    stage.innerHTML = buildReviewSheetHtml(sections);
    document.body.appendChild(stage);
    var sheet = stage.querySelector(".app-review-sheet");

    generateReviewPdfBlob(sheet)
      .then(function (blob) {
        if (!reviewDialogOpen) return;
        showReviewPdf(blob);
        setReviewStatus(uiText("reviewReady"));
      })
      .catch(function () {
        if (!reviewDialogOpen) return;
        setReviewStatus(uiText("reviewFailed"), true);
        var html = byId("app-review-html");
        if (html) html.hidden = false;
      })
      .finally(function () {
        if (stage.parentNode) stage.parentNode.removeChild(stage);
      });
  }

  function formIsReadyToSend() {
    clearSubmitStatus();
    var honeypot = byId("website");
    if (honeypot && String(honeypot.value || "").trim()) {
      showSuccessScreen();
      return false;
    }
    if (!validateForm()) return false;
    if (document.querySelector('.application-page input[name="degree"]')) {
      if (!validateRadioGroup("degree", "degreeRequired", "deg1")) return false;
      if (!validateOtherSpecify("degree", "degreeOtherRequired")) return false;
    }
    if (document.querySelector('.application-page input[name="title"]')) {
      if (!validateRadioGroup("title", "titleRequired", "tit1")) return false;
      if (!validateOtherSpecify("title", "titleOtherRequired")) return false;
    }
    if (document.querySelector('.application-page input[name="gender"]')) {
      if (!validateRadioGroup("gender", "genderRequired", "gender-male")) return false;
    }
    if (byId("sci-fields")) {
      if (!validateSciSelection()) return false;
    }
    if (!validateFileUploads()) return false;
    if (!validatePrivacyConfirm()) return false;
    return true;
  }

  function sendApplication() {
    if (!formIsReadyToSend()) {
      if (reviewDialogOpen) closeApplicationReview();
      return;
    }
    if (reviewDialogOpen) closeApplicationReview();
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

  function submitForm() {
    try {
      if (reviewDialogOpen) return;
      if (!formIsReadyToSend()) return;
      if (isForumRegister()) {
        openApplicationReview();
        return;
      }
      sendApplication();
    } catch (err) {
      showSubmitError(uiText("submitFailed"), { alert: true });
    }
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
      var query = foldSearch(search.value);
      var shown = 0;
      optionNodes().forEach(function (li) {
        var hay = foldSearch([
          li.getAttribute("data-label") || "",
          li.getAttribute("data-country-en") || "",
          li.getAttribute("data-code") || "",
        ].join(" "));
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
      citySelect._daabCityItems = [];
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
      citySelect._daabCityItems = [];
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
      citySelect._daabCityItems = [];

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
      citySelect._daabCityItems = cityList.map(function (cityName) {
        return {
          name: cityName,
          aliases: aliasesForCity(countryCode, cityName),
        };
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
      return items;
    }

    function citiesJsonUrl(countryCode) {
      var src = "";
      if (membershipScriptEl && membershipScriptEl.src) src = membershipScriptEl.src;
      else {
        var scripts = document.getElementsByTagName("script");
        var i;
        for (i = 0; i < scripts.length; i++) {
          if ((scripts[i].src || "").indexOf("daab-membership-application.js") !== -1) {
            src = scripts[i].src;
            break;
          }
        }
      }
      if (!src) return "../js/cities/" + encodeURIComponent(countryCode) + ".json";
      return src.replace(
        /daab-membership-application\.js(?:\?.*)?$/,
        "cities/" + encodeURIComponent(countryCode) + ".json"
      );
    }

    function fetchCitiesByCountryEnglishName(countryEnglishName, countryCode) {
      var cacheKey = countryCode || countryEnglishName;
      if (cityCache[cacheKey]) {
        return Promise.resolve(cityCache[cacheKey]);
      }
      return fetch(citiesJsonUrl(countryCode))
        .then(function (response) {
          if (!response.ok) throw new Error("city-fetch-failed");
          return response.json();
        })
        .then(function (raw) {
          var list = mergeGuaranteedCities(countryCode, Array.isArray(raw) ? raw : []);
          cityCache[cacheKey] = list;
          return list;
        })
        .catch(function () {
          var list = mergeGuaranteedCities(countryCode, []);
          cityCache[cacheKey] = list;
          return list;
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

    function cityItems() {
      return Array.isArray(select._daabCityItems) ? select._daabCityItems : [];
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

    function appendCityLi(item) {
      var li = document.createElement("li");
      li.className = "phone-code-picker-option country-picker-option";
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      li.setAttribute("data-value", item.name);
      li.setAttribute("data-label", item.name);
      li.setAttribute("data-aliases", item.aliases || "");
      var text = document.createElement("span");
      text.className = "phone-code-picker-option-text";
      text.textContent = item.name;
      li.appendChild(text);
      list.appendChild(li);
    }

    function renderCityList(query) {
      list.innerHTML = "";
      var q = foldSearch(query);
      var items = cityItems();
      var shown = 0;
      var i;
      var item;
      var hay;
      var limit = 400;
      for (i = 0; i < items.length; i++) {
        item = items[i];
        hay = foldSearch([item.name, item.aliases || ""].join(" "));
        if (q && hay.indexOf(q) === -1) continue;
        appendCityLi(item);
        shown += 1;
        if (shown >= limit) break;
      }
      empty.hidden = shown > 0;
      list.hidden = shown === 0;
    }

    function rebuildOptions() {
      search.value = "";
      renderCityList("");
      syncFromSelect();
    }

    function visibleOptions() {
      return Array.prototype.slice.call(optionNodes());
    }

    function applyFilter() {
      renderCityList(search.value);
      syncFromSelect();
    }

    function setNativeValue(value, label) {
      var ph = select.querySelector('option[value=""]');
      var phText = ph ? ph.textContent : placeholderText;
      select.innerHTML = "";
      var placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = phText;
      select.appendChild(placeholder);
      if (value) {
        var opt = document.createElement("option");
        opt.value = value;
        opt.textContent = label || value;
        select.appendChild(opt);
        select.value = value;
      } else {
        select.selectedIndex = 0;
      }
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
      setNativeValue(li.getAttribute("data-value"), li.getAttribute("data-label"));
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
      var query = foldSearch(search.value);
      var shown = 0;
      optionNodes().forEach(function (li) {
        var hay = foldSearch([
          li.getAttribute("data-label") || "",
          li.getAttribute("data-country-code") || "",
          li.getAttribute("data-country-en") || "",
          li.getAttribute("data-value") || "",
          li.getAttribute("data-dial") || "",
        ].join(" "));
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
        e.stopPropagation();
        submitForm();
      });
    }
    if (isForumRegister()) {
      var preload = function () {
        ensurePdfLibs().catch(function () {});
      };
      if (window.requestIdleCallback) window.requestIdleCallback(preload, { timeout: 2500 });
      else window.setTimeout(preload, 800);
    }
    bindRadioHighlight();
    initOtherSpecifyFields();
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
    if (submitBtn) {
      submitBtn.addEventListener("pointerdown", function () {
        try {
          var Ctx = window.AudioContext || window.webkitAudioContext;
          if (!Ctx) return;
          if (!playValidationBeep._ctx) playValidationBeep._ctx = new Ctx();
          if (playValidationBeep._ctx.state === "suspended") playValidationBeep._ctx.resume();
        } catch (e) {}
      });
    }
  });
})();
