/**
 * Multi-step membership application form (AZ).
 */
(function () {
  "use strict";

  var totalSections = 4;
  var currentSection = 1;
  var cityCache = Object.create(null);
  var COUNTRY_CODES = [
    "AF","AL","DZ","AD","AO","AG","AR","AM","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BT","BO","BA","BW","BR","BN","BG","BF","BI","CV","KH","CM","CA","CF","TD","CL","CN","CO","KM","CG","CD","CR","CI","HR","CU","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","SZ","ET","FJ","FI","FR","GA","GM","GE","DE","GH","GR","GD","GT","GN","GW","GY","HT","HN","HU","IS","IN","ID","IR","IQ","IE","IL","IT","JM","JP","JO","KZ","KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MG","MW","MY","MV","ML","MT","MH","MR","MU","MX","FM","MD","MC","MN","ME","MA","MZ","MM","NA","NR","NP","NL","NZ","NI","NE","NG","MK","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PL","PT","QA","RO","RU","RW","KN","LC","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SK","SI","SB","SO","ZA","SS","ES","LK","SD","SR","SE","CH","SY","TJ","TZ","TH","TL","TG","TO","TT","TN","TR","TM","TV","UG","UA","AE","GB","US","UY","UZ","VU","VA","VE","VN","YE","ZM","ZW"
  ];

  function byId(id) {
    return document.getElementById(id);
  }

  function detectLang() {
    var explicit = document.documentElement.getAttribute("data-daab-lang");
    if (explicit === "en" || explicit === "az") return explicit;
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
        ? "Zəhmət olmasa etibarlı e-poçt ünvanı daxil edin."
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

  function submitForm() {
    if (!validateForm()) return;
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

  function initResidenceDropdowns() {
    var countrySelect = byId("country");
    var citySelect = byId("city");
    if (!countrySelect || !citySelect) return;
    var cityRequestSeq = 0;

    var lang = detectLang();
    var texts = {
      en: {
        countryPlaceholder: "Select country",
        cityDisabledPlaceholder: "Select country first",
        cityPlaceholder: "Select city",
        cityLoadingPlaceholder: "Loading cities...",
        cityUnavailablePlaceholder: "No cities available"
      },
      az: {
        countryPlaceholder: "Ölkə seçin",
        cityDisabledPlaceholder: "Əvvəlcə ölkə seçin",
        cityPlaceholder: "Şəhər seçin",
        cityLoadingPlaceholder: "Şəhərlər yüklənir...",
        cityUnavailablePlaceholder: "Şəhərlər tapılmadı"
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
      citySelect.disabled = true;
      citySelect.innerHTML = "";
      var option = document.createElement("option");
      option.value = "";
      option.textContent = t.cityDisabledPlaceholder;
      citySelect.appendChild(option);
    }

    function showCityLoading() {
      citySelect.disabled = true;
      citySelect.innerHTML = "";
      var option = document.createElement("option");
      option.value = "";
      option.textContent = t.cityLoadingPlaceholder;
      citySelect.appendChild(option);
    }

    function populateCitySelect(cityList) {
      citySelect.disabled = false;
      citySelect.innerHTML = "";

      var placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = t.cityPlaceholder;
      citySelect.appendChild(placeholder);

      if (!Array.isArray(cityList) || cityList.length === 0) {
        var unavailable = document.createElement("option");
        unavailable.value = "";
        unavailable.textContent = t.cityUnavailablePlaceholder;
        citySelect.appendChild(unavailable);
        citySelect.disabled = true;
        return;
      }

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
        loading: "Loading area codes...",
        placeholder: "Select area code",
        error: "Enter local phone number only (without country code)."
      },
      az: {
        loading: "Kodlar yüklənir...",
        placeholder: "Kod seçin",
        error: "Yalnız yerli telefon nömrəsini daxil edin (ölkə kodu olmadan)."
      }
    };
    var t = texts[lang] || texts.en;
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

    function normalizeDialCode(root, suffix) {
      var merged = String(root || "").trim() + String(suffix || "").trim();
      if (!merged) return "";
      if (merged.charAt(0) !== "+") merged = "+" + merged;
      return merged.replace(/\s+/g, "");
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

    phoneCodeSelect.disabled = true;
    phoneCodeSelect.innerHTML = "";
    var loadingOption = document.createElement("option");
    loadingOption.value = "";
    loadingOption.textContent = t.loading;
    phoneCodeSelect.appendChild(loadingOption);

    fetch("https://restcountries.com/v3.1/all?fields=cca2,idd")
      .then(function (response) {
        if (!response.ok) throw new Error("calling-code-fetch-failed");
        return response.json();
      })
      .then(function (rows) {
        var byCode = Object.create(null);
        (rows || []).forEach(function (row) {
          if (!row || !row.cca2) return;
          byCode[String(row.cca2).toUpperCase()] = row;
        });

        var entries = [];
        COUNTRY_CODES.forEach(function (code) {
          var row = byCode[code];
          if (!row || !row.idd || !row.idd.root) return;
          var root = row.idd.root;
          var suffixes = Array.isArray(row.idd.suffixes) && row.idd.suffixes.length ? row.idd.suffixes : [""];
          var countryName = localizedCountryName(code);
          suffixes.forEach(function (suffix) {
            var dialCode = normalizeDialCode(root, suffix);
            if (!dialCode) return;
            entries.push({
              countryCode: code,
              countryName: countryName,
              dialCode: dialCode
            });
          });
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
      })
      .catch(function () {
        phoneCodeSelect.innerHTML = "";
        var fallback = document.createElement("option");
        fallback.value = "";
        fallback.textContent = t.placeholder;
        phoneCodeSelect.appendChild(fallback);
        phoneCodeSelect.disabled = false;
      });
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
    initEmailValidation();
    initResidenceDropdowns();
    initPhoneCodeDropdown();
    initStepNavigation();
    initBackToStepsButtons();
    updateProgress(1);
  });
})();
