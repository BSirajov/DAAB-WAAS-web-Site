/**
 * Multi-step membership application form (AZ).
 */
(function () {
  "use strict";

  var totalSections = 4;
  var currentSection = 1;
  var cityCache = Object.create(null);
  // Codes come from the shared js/daab-country-codes.js module.
  var COUNTRY_CODES = window.DAAB_COUNTRY_CODES || [];

  function byId(id) {
    return document.getElementById(id);
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

  function validateForm() {
    var form = byId("mainForm");
    if (!form) return true;
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

  function buildFormDataForPhp(payload) {
    var fd = new FormData();
    Object.keys(payload).forEach(function (key) {
      if (key.charAt(0) === "_") return;
      var val = payload[key];
      if (val == null || val === "") return;
      fd.append(key, String(val));
    });
    return fd;
  }

  function uiText(key) {
    var lang = detectLang();
    var strings = {
      az: {
        submitting: "Göndərilir…",
        submit: "✓ Göndər",
        sciRequired: "Ən azı bir elmi sahə seçin.",
        noEndpoint:
          "Müraciət serveri hələ konfiqurasiya edilməyib. Zəhmət olmasa birbaşa info@daab-waas.com ünvanına yazın.",
        submitFailed: "Müraciət göndərilmədi. Bir az sonra yenidən cəhd edin və ya info@daab-waas.com ünvanına yazın.",
        networkError: "Şəbəkə xətası. İnternet bağlantınızı yoxlayın və yenidən cəhd edin.",
        phpUnavailable:
          "Müraciət forması bu serverdə işləmir (PHP dəstəyi lazımdır). Zəhmət olmasa məlumatlarınızı info@daab-waas.com ünvanına e-məktubla göndərin.",
      },
      en: {
        submitting: "Submitting…",
        submit: "✓ Submit Application",
        sciRequired: "Select at least one scientific field.",
        noEndpoint:
          "The application backend is not configured yet. Please email info@daab-waas.com directly.",
        submitFailed: "Could not submit your application. Please try again or email info@daab-waas.com.",
        networkError: "Network error. Check your connection and try again.",
        phpUnavailable:
          "This server cannot process applications (PHP mail handler required). Please email your details to info@daab-waas.com.",
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

  function validateSciSelection() {
    if (getSciValues().length > 0) return true;
    var sciFieldset = byId("sci-fields");
    if (sciFieldset) sciFieldset.setAttribute("aria-invalid", "true");
    showSubmitError(uiText("sciRequired"), { alert: true });
    var sec = byId("sec-3");
    if (sec) sec.scrollIntoView({ behavior: "smooth", block: "start" });
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

    return {
      _subject: (lang === "az" ? "DAAB üzvlük — " : "WAAS Membership — ") + fullName,
      locale: lang,
      submitted_at: new Date().toISOString(),
      page_url: location.href,
      email: email,
      first_name: firstName,
      last_name: lastName,
      full_name: fullName,
      country: (byId("country") && byId("country").value.trim()) || "",
      city: getCityValue(),
      phone_code: phoneCode,
      phone_number: phoneNumber,
      phone_full: phoneCode && phoneNumber ? phoneCode + " " + phoneNumber : phoneNumber,
      university: (byId("university") && byId("university").value.trim()) || "",
      field_of_study: (byId("fieldofstudy") && byId("fieldofstudy").value.trim()) || "",
      degree: getRadioValue("degree"),
      degree_institution: (byId("deginst") && byId("deginst").value.trim()) || "",
      academic_title: getRadioValue("title"),
      title_institution: (byId("titinst") && byId("titinst").value.trim()) || "",
      current_job: (byId("currentjob") && byId("currentjob").value.trim()) || "",
      previous_jobs: (byId("prevjobs") && byId("prevjobs").value.trim()) || "",
      contributions: (byId("contributions") && byId("contributions").value.trim()) || "",
      sci_fields: getSciValues().join(", "),
      sci_fields_count: String(getSciValues().length),
      additional_info: (byId("addinfo") && byId("addinfo").value.trim()) || "",
      cv_confirm: getCvConfirmValue(),
    };
  }

  function showSuccessScreen() {
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
            if (response.status === 405) {
              throw new Error(uiText("phpUnavailable"));
            }
            throw new Error(status === "error" ? uiText("submitFailed") : text || response.statusText);
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
    if (!validateForm()) return;
    if (!validateSciSelection()) return;

    setSubmitting(true);
    var payload = buildSubmissionPayload();

    postApplication(payload)
      .then(function () {
        showSuccessScreen();
      })
      .catch(function (err) {
        var msg = uiText("submitFailed");
        if (err && err.message) {
          if (err.message.indexOf("Failed to fetch") >= 0) {
            msg = uiText("networkError");
          } else if (
            err.message === uiText("phpUnavailable") ||
            err.message.indexOf("405") >= 0
          ) {
            msg = uiText("phpUnavailable");
          }
        }
        showSubmitError(msg);
      })
      .finally(function () {
        setSubmitting(false);
      });
  }

  function initResidenceDropdowns() {
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

    var lang = detectLang();
    var texts = {
      en: {
        countryPlaceholder: "Select country",
        cityDisabledPlaceholder: "Select country first",
        cityPlaceholder: "Select city",
        cityLoadingPlaceholder: "Loading cities...",
        cityUnavailablePlaceholder: "No cities available — type your city below"
      },
      az: {
        countryPlaceholder: "Ölkə seçin",
        cityDisabledPlaceholder: "Əvvəlcə ölkə seçin",
        cityPlaceholder: "Şəhər seçin",
        cityLoadingPlaceholder: "Şəhərlər yüklənir...",
        cityUnavailablePlaceholder: "Şəhərlər tapılmadı — aşağıda şəhəri yazın"
      }
    };
    var t = texts[lang] || texts.en;

    countrySelect.innerHTML = "";
    var countryPlaceholder = document.createElement("option");
    countryPlaceholder.value = "";
    countryPlaceholder.textContent = t.countryPlaceholder;
    countrySelect.appendChild(countryPlaceholder);

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

    var countries = COUNTRY_CODES.map(function (code) {
      return {
        code: code,
        name: formatter ? (formatter.of(code) || code) : code,
        englishName: enFormatter ? (enFormatter.of(code) || code) : code
      };
    });
    countries.sort(function (a, b) {
      if (collator) return collator.compare(a.name, b.name);
      return String(a.name).localeCompare(String(b.name));
    });
    countries.forEach(function (entry) {
      var option = document.createElement("option");
      option.value = entry.name;
      option.setAttribute("data-code", entry.code);
      option.setAttribute("data-country-en", entry.englishName);
      option.textContent = entry.name;
      countrySelect.appendChild(option);
    });

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

    function populateCitySelect(cityList) {
      citySelect.innerHTML = "";

      if (!Array.isArray(cityList) || cityList.length === 0) {
        var unavailable = document.createElement("option");
        unavailable.value = "";
        unavailable.textContent = t.cityUnavailablePlaceholder;
        citySelect.appendChild(unavailable);
        citySelect.disabled = true;
        showCityManual();
        return;
      }

      hideCityManual();
      citySelect.disabled = false;
      citySelect.required = true;
      var placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = t.cityPlaceholder;
      citySelect.appendChild(placeholder);

      cityList.forEach(function (cityName) {
        var option = document.createElement("option");
        option.value = cityName;
        option.textContent = cityName;
        citySelect.appendChild(option);
      });
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
        return a.localeCompare(b);
      });
      return items;
    }

    function fetchCitiesByCountryEnglishName(countryEnglishName) {
      if (cityCache[countryEnglishName]) {
        return Promise.resolve(cityCache[countryEnglishName]);
      }
      return fetch("https://countriesnow.space/api/v0.1/countries/cities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ country: countryEnglishName })
      })
        .then(function (response) {
          if (!response.ok) throw new Error("city-fetch-failed");
          return response.json();
        })
        .then(function (payload) {
          var list = normalizeCityList(payload && payload.data);
          cityCache[countryEnglishName] = list;
          return list;
        })
        .catch(function () {
          return [];
        });
    }

    countrySelect.addEventListener("change", function () {
      cityRequestSeq += 1;
      var requestId = cityRequestSeq;
      var selected = countrySelect.options[countrySelect.selectedIndex];
      var countryEnglishName = selected ? selected.getAttribute("data-country-en") : null;
      if (!countryEnglishName) {
        resetCitySelect();
        return;
      }
      showCityLoading();
      fetchCitiesByCountryEnglishName(countryEnglishName).then(function (cityList) {
        if (requestId !== cityRequestSeq) return;
        populateCitySelect(cityList);
      });
    });

    resetCitySelect();
  }

  function initPhoneCodeDropdown() {
    var phoneCodeSelect = byId("phone_code");
    var localPhoneInput = byId("phone");
    if (!phoneCodeSelect || !localPhoneInput) return;

    var lang = detectLang();
    var texts = {
      en: {
        placeholder: "Select area code",
        error: "Enter local phone number only (without country code)."
      },
      az: {
        placeholder: "Kod seçin",
        error: "Yalnız yerli telefon nömrəsini daxil edin (ölkə kodu olmadan)."
      }
    };
    var t = texts[lang] || texts.en;
    var phoneCodes = window.DAAB_PHONE_CODES || [];
    var formatter =
      typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function"
        ? new Intl.DisplayNames([lang], { type: "region" })
        : null;
    var collator =
      typeof Intl !== "undefined" && typeof Intl.Collator === "function"
        ? new Intl.Collator(lang, { sensitivity: "base" })
        : null;

    function localizedCountryName(code) {
      if (code === "TR") return lang === "az" ? "Türkiyə" : "Türkiye";
      return formatter ? (formatter.of(code) || code) : code;
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
      option.textContent = entry.countryName + " (" + entry.dialCode + ")";
      phoneCodeSelect.appendChild(option);
    });
    phoneCodeSelect.disabled = false;
    enhancePhoneCodePicker(phoneCodeSelect, t.placeholder);
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

  function enhancePhoneCodePicker(select, placeholderText) {
    if (!select || select.getAttribute("data-phone-code-picker-ready") === "1") return;
    select.setAttribute("data-phone-code-picker-ready", "1");

    var fieldGroup = select.closest(".field-group");
    if (!fieldGroup) return;

    var picker = document.createElement("div");
    picker.className = "phone-code-picker";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "phone-code-picker-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");

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
    panel.setAttribute("role", "listbox");

    var list = document.createElement("ul");
    list.className = "phone-code-picker-list";

    Array.prototype.forEach.call(select.options, function (opt) {
      if (!opt.value) return;
      var countryCode = opt.getAttribute("data-country-code") || "";
      var li = document.createElement("li");
      li.className = "phone-code-picker-option";
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      li.setAttribute("data-value", opt.value);
      li.setAttribute("data-country-code", countryCode);

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

    panel.appendChild(list);

    select.classList.add("phone-code-picker-native");
    select.parentNode.insertBefore(picker, select);
    picker.appendChild(select);
    picker.appendChild(btn);
    picker.appendChild(panel);

    var label = fieldGroup.querySelector('label[for="' + select.id + '"]');
    if (label) {
      label.setAttribute("for", "");
      label.addEventListener("click", function (e) {
        e.preventDefault();
        btn.focus();
        if (panel.hidden) openPanel();
      });
    }

    function syncFromSelect() {
      var opt = select.options[select.selectedIndex];
      btn.disabled = select.disabled;
      if (!opt || !opt.value) {
        flagImg.hidden = true;
        labelSpan.textContent = placeholderText;
        btn.classList.remove("has-value");
        list.querySelectorAll(".phone-code-picker-option").forEach(function (li) {
          li.classList.remove("is-selected");
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
      list.querySelectorAll(".phone-code-picker-option").forEach(function (li) {
        var selected =
          li.getAttribute("data-value") === opt.value &&
          li.getAttribute("data-country-code") === cc;
        li.classList.toggle("is-selected", selected);
        li.setAttribute("aria-selected", selected ? "true" : "false");
      });
    }

    function closePanel() {
      panel.hidden = true;
      btn.setAttribute("aria-expanded", "false");
    }

    function openPanel() {
      if (select.disabled) return;
      panel.hidden = false;
      btn.setAttribute("aria-expanded", "true");
      var selected = list.querySelector(".phone-code-picker-option.is-selected");
      if (selected) selected.scrollIntoView({ block: "nearest" });
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      if (panel.hidden) openPanel();
      else closePanel();
    });

    list.addEventListener("click", function (e) {
      var li = e.target.closest(".phone-code-picker-option");
      if (!li) return;
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
    });

    document.addEventListener("click", function (e) {
      if (!picker.contains(e.target)) closePanel();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePanel();
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

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.classList.contains("application-page")) return;
    document.querySelectorAll(".application-page .form-section").forEach(function (s) {
      s.hidden = false;
    });
    var stepNav = document.querySelector(".application-page .app-steps-nav");
    if (stepNav) stepNav.hidden = false;
    bindRadioHighlight();
    initEmailValidation();
    initResidenceDropdowns();
    initPhoneCodeDropdown();
    initStepNavigation();
    initBackToStepsButtons();
    initEndpointNotice();
    updateProgress(1);
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
