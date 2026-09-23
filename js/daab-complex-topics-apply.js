/**
 * Application form for Complex Topics, Clear Explanations.
 * Visual pattern follows the Forum 2026 registration form.
 */
(function () {
  "use strict";

  var MAX_FILES = 3;
  var MAX_BYTES = 8 * 1024 * 1024;
  var FILE_EXT = {
    pdf: 1, doc: 1, docx: 1, ppt: 1, pptx: 1, odt: 1, odp: 1, txt: 1,
    png: 1, jpg: 1, jpeg: 1, webp: 1, gif: 1, mp4: 1, zip: 1
  };
  var chosenFiles = [];
  var sending = false;
  var topics = [];
  var activeIndex = -1;
  var topicGuides = {};
  var topicNavLive = false;

  var COPY = {
    az: {
      nameRequired: "Ad mütləqdir.",
      surnameRequired: "Soyad mütləqdir.",
      nameInvalid: "Zəhmət olmasa adı hərflərlə yazın.",
      surnameInvalid: "Zəhmət olmasa soyadı hərflərlə yazın.",
      dobRequired: "Doğum tarixi mütləqdir.",
      dobInvalid: "Tarixi dd/mm/yyyy formatında daxil edin.",
      emailRequired: "E-poçt ünvanı mütləqdir.",
      emailInvalid: "Zəhmət olmasa etibarlı e-poçt ünvanı daxil edin.",
      countryRequired: "Ölkə mütləqdir.",
      cityRequired: "Şəhər mütləqdir.",
      categoryRequired: "İştirakçı qrupunu seçin.",
      categoryOtherRequired: "Qrupun adını yazın.",
      participationRequired: "Fərdi və ya komanda iştirakını seçin.",
      teamNameRequired: "Komandanın adı mütləqdir.",
      memberRequired: "Komandada ən azı bir üzvün də adını yazın.",
      topicRequired: "Zəhmət olmasa mövzu seçin və ya öz mövzunuzu təklif edin.",
      topicPlaceholder: "Mövzu seçin",
      otherTitleRequired: "Təklif olunan mövzunun adı mütləqdir.",
      otherWhyRequired: "Bu mövzunun niyə izaha ehtiyacı olduğunu qısaca yazın.",
      titleRequired: "İşin başlığı mütləqdir.",
      audienceRequired: "Materialınızın əsasən kimlər üçün nəzərdə tutulduğunu seçin.",
      audienceOtherRequired: "Kimlər üçün nəzərdə tutulduğunu qeyd edin.",
      descriptionRequired: "Qısa təsvir mütləqdir.",
      formatRequired: "Ən azı bir format seçin.",
      languageRequired: "İşin dilini seçin.",
      languageOtherRequired: "Materialın dilini yazın.",
      aiRequired: "Süni intellektin istifadə olunub-olunmadığını bildirin.",
      aiDetailRequired: "Aləti, məqsədi və istifadənin miqyasını yazın.",
      workRequired: "Hazır iş üçün fayl yükləyin və ya sabit keçid verin. İlkin maraq üçün həmin qeydi seçin.",
      linkInvalid: "Keçid http:// və ya https:// ilə başlamalıdır.",
      fileType: "Bu fayl növü qəbul edilmir. İcazə verilən növlər formada göstərilib.",
      fileSize: "Hər fayl ən çox 8 MB ola bilər. Daha böyük iş üçün sabit keçid verin.",
      fileCount: "Bu forma ən çox 3 fayl qəbul edir.",
      photoRequired: "Fotoşəkil seçin.",
      photoType: "Foto JPG və ya PNG formatında olmalıdır.",
      photoSize: "Fotoşəkil çox böyükdür (ən çox 5 MB).",
      photoInvalid: "Fotoşəkil oxuna bilmədi. Başqa fayl seçin.",
      conditionsRequired: "Müsabiqə şərtlərini oxuduğunuzu təsdiq edin.",
      originalityRequired: "İşin sizə və ya komandanıza məxsus olduğunu təsdiq edin.",
      attributionRequired: "Mənbə və hüquq bəyanatını təsdiq edin.",
      publicationRequired: "Yayım şərtini oxuduğunuzu təsdiq edin.",
      privacyRequired: "Məxfilik bildirişini təsdiq edin.",
      unsafe: "Zəhmət olmasa bunu adi dildə yazın. Kod və sayta zərər verə biləcək mətn göndərilə bilməz.",
      respect: "Zəhmət olmasa, nəzakətli ifadələrdən istifadə edin. Göndərməzdən əvvəl işarələnmiş xanadakı təhqiramiz və ya nalayiq ifadələri düzəldin.",
      sending: "Müraciət göndərilir…",
      submit: "Müraciətinizi göndərin",
      sent: "Müraciət göndərildi.",
      submitFailed: "Müraciət göndərilmədi. Yazdıqlarınız saxlanılıb. Bir az sonra yenidən cəhd edin.",
      phpUnavailable: "Bu önbaxışda poçt proqramı işləmir. Müraciət saxlanılıb, amma göndərilməyib.",
      fileReady: "Göndərməyə hazırdır",
      remove: "Sil",
      noTopic: "Uyğun mövzu tapılmadı. Aşağıdakı sahədə başqa mövzu təklif edə bilərsiniz."
    },
    en: {
      nameRequired: "A name is required.",
      surnameRequired: "A surname is required.",
      nameInvalid: "Please enter your name using letters.",
      surnameInvalid: "Please enter your surname using letters.",
      dobRequired: "A date of birth is required.",
      dobInvalid: "Enter the date as dd/mm/yyyy.",
      emailRequired: "An email address is required.",
      emailInvalid: "Please enter a valid email address.",
      countryRequired: "A country is required.",
      cityRequired: "A city is required.",
      categoryRequired: "Choose the participant group.",
      categoryOtherRequired: "Name the group.",
      participationRequired: "Choose individual or team participation.",
      teamNameRequired: "A team name is required.",
      memberRequired: "Name at least one other team member.",
      topicRequired: "Please select a topic or propose your own.",
      topicPlaceholder: "Select a topic",
      otherTitleRequired: "A title for the proposed topic is required.",
      otherWhyRequired: "Briefly explain why this topic needs a clear explanation.",
      titleRequired: "A submission title is required.",
      audienceRequired: "Choose who your material is mainly for.",
      audienceOtherRequired: "Say who the material is for.",
      descriptionRequired: "A brief description is required.",
      formatRequired: "Choose at least one format.",
      languageRequired: "Choose the submission language.",
      languageOtherRequired: "Name the language of the material.",
      aiRequired: "Say whether artificial intelligence was used.",
      aiDetailRequired: "Name the tool, the purpose and the scale of use.",
      workRequired: "Upload the work and/or give a stable link. For an expression of interest before the file is ready, tick that option.",
      linkInvalid: "The link must start with http:// or https://.",
      fileType: "This file type is not accepted. The permitted types are listed beside the upload.",
      fileSize: "Each file can be at most 8 MB. Give a stable link for a larger work.",
      fileCount: "This form accepts at most 3 files.",
      photoRequired: "Please select a photo.",
      photoType: "The photo must be a JPG or PNG image.",
      photoSize: "The photo is too large (maximum 5 MB).",
      photoInvalid: "The photo could not be read. Please choose another file.",
      conditionsRequired: "Confirm that you have read the competition conditions.",
      originalityRequired: "Confirm that the work is yours or your team’s.",
      attributionRequired: "Confirm the source and rights statement.",
      publicationRequired: "Confirm that you have read the publication note.",
      privacyRequired: "Confirm the privacy notice.",
      unsafe: "Please rewrite this in plain language. Code and other text that could harm the site cannot be sent.",
      respect: "Please use respectful language. Review the highlighted field and remove any offensive or abusive wording before submitting.",
      sending: "Sending your application…",
      submit: "Submit your application",
      sent: "Application sent.",
      submitFailed: "The application was not sent. What you entered is still here. Please try again in a moment.",
      phpUnavailable: "Mail is not available in this preview. Your application is still on the page, but it was not sent.",
      fileReady: "Ready to submit",
      remove: "Remove",
      noTopic: "No topic matches. You can propose another topic in the field below."
    }
  };

  function lang() {
    return document.documentElement.getAttribute("data-daab-lang") === "az" ? "az" : "en";
  }

  function t(key) {
    return (COPY[lang()] && COPY[lang()][key]) || COPY.en[key] || "";
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function val(id) {
    var el = byId(id);
    return el ? String(el.value || "").trim() : "";
  }

  function pickerOr(id) {
    return byId(id + "_picker") || byId(id);
  }

  function cityValue() {
    var manual = byId("city_manual");
    if (manual && !manual.hidden) return String(manual.value || "").trim();
    return val("city");
  }

  function cityControl() {
    var manual = byId("city_manual");
    if (manual && !manual.hidden) return manual;
    return pickerOr("city");
  }

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function parseDobDisplay(value) {
    var raw = String(value || "").trim();
    var match = raw.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (!match) return null;
    var day = parseInt(match[1], 10);
    var month = parseInt(match[2], 10);
    var year = parseInt(match[3], 10);
    if (year < 1900) return null;
    var date = new Date(year, month - 1, day);
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) return null;
    var today = new Date();
    today.setHours(23, 59, 59, 999);
    if (date > today) return null;
    return {
      iso: year + "-" + pad2(month) + "-" + pad2(day),
      display: pad2(day) + "/" + pad2(month) + "/" + year
    };
  }

  function formatDobDigits(raw) {
    var digits = String(raw || "").replace(/\D/g, "").slice(0, 8);
    if (digits.length <= 2) return digits;
    if (digits.length <= 4) return digits.slice(0, 2) + "/" + digits.slice(2);
    return digits.slice(0, 2) + "/" + digits.slice(2, 4) + "/" + digits.slice(4);
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

  function initDobField() {
    var dob = byId("dob");
    var picker = byId("dob_picker");
    var calendarBtn = byId("dob_calendar_btn");
    if (!dob) return;
    var today = new Date();
    if (picker) {
      picker.max = today.getFullYear() + "-" + pad2(today.getMonth() + 1) + "-" + pad2(today.getDate());
      picker.min = "1900-01-01";
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
          try {
            dob.setSelectionRange(Math.max(0, start + (next.length - before.length)), Math.max(0, start + (next.length - before.length)));
          } catch (err) {}
        }
      }
      syncPickerFromText();
    });
    dob.addEventListener("blur", function () {
      var normalized = normalizeDobTypedValue(dob.value);
      if (normalized) dob.value = normalized;
      syncPickerFromText();
    });
    dob.addEventListener("paste", function (event) {
      var pasted = event.clipboardData ? event.clipboardData.getData("text") : "";
      if (!pasted) return;
      event.preventDefault();
      dob.value = normalizeDobTypedValue(pasted);
      syncPickerFromText();
    });
    if (calendarBtn) {
      calendarBtn.addEventListener("click", function (event) {
        event.preventDefault();
        openDobPicker();
      });
    }
    if (picker) {
      picker.addEventListener("change", function () {
        var parts = String(picker.value || "").trim().match(/^(\d{4})-(\d{2})-(\d{2})$/);
        if (!parts) return;
        dob.value = parts[3] + "/" + parts[2] + "/" + parts[1];
      });
    }
  }

  function nameOk(value) {
    return /^[\p{L}\p{M}][\p{L}\p{M} .'’-]*$/u.test(String(value || "").trim());
  }

  function emailOk(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || "").trim());
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

  function checked(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : "";
  }

  function showStatus(message, isError) {
    var box = byId("app-submit-status");
    if (!box) return;
    box.hidden = false;
    box.className = "app-submit-status" + (isError ? " app-submit-status--error" : "");
    box.setAttribute("role", isError ? "alert" : "status");
    box.textContent = message;
  }

  function clearFieldWarnings() {
    document.querySelectorAll(".field-required-warning").forEach(function (node) {
      node.remove();
    });
    document.querySelectorAll("[aria-invalid='true']").forEach(function (node) {
      node.removeAttribute("aria-invalid");
    });
  }

  function warn(el, message) {
    if (!el) {
      showStatus(message, true);
      return;
    }
    el.setAttribute("aria-invalid", "true");
    var group = el.closest(".field-group") || el.closest(".opt-item") || el.parentNode;
    var note = document.createElement("p");
    note.className = "field-required-warning";
    note.setAttribute("role", "alert");
    note.textContent = message;
    if (group) group.appendChild(note);
    showStatus(message, true);
    if (typeof el.focus === "function") el.focus();
    el.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function fillCountries() {
    var sel = byId("country");
    if (!sel || !window.DAAB_COUNTRY_CODES) return;
    var codes = window.DAAB_COUNTRY_CODES;
    var azNames = window.DAAB_COUNTRY_NAMES_AZ || {};
    var display = null;
    if (lang() !== "az" && typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function") {
      display = new Intl.DisplayNames(["en"], { type: "region" });
    }
    var items = codes.map(function (code) {
      var name = lang() === "az" ? (azNames[code] || code) : (display ? display.of(code) : code);
      return { name: name || code };
    });
    items.sort(function (a, b) {
      return a.name.localeCompare(b.name, lang() === "az" ? "az" : "en");
    });
    items.forEach(function (item) {
      var opt = document.createElement("option");
      opt.value = item.name;
      opt.textContent = item.name;
      sel.appendChild(opt);
    });
  }

  var AZ_LETTERS = "abcçdeəfgğhxıijkqlmnoöprsştuüvyz";

  function foldAz(text) {
    return String(text || "")
      .replace(/\u0130/g, "i")
      .replace(/I/g, "\u0131")
      .toLocaleLowerCase("az");
  }

  function compareByAlphabet(a, b, alphabet, fold) {
    var left = fold(a);
    var right = fold(b);
    var i = 0;
    var j = 0;
    function rankAt(source, index) {
      while (index < source.length) {
        var ch = source.charAt(index);
        if (ch === " " || ch === "\u00a0" || ch === "-" || ch === "\u2013" || ch === "\u2014" || ch === "," || ch === "." || ch === "/" || ch === ":") {
          return { index: index, rank: -1 };
        }
        var letter = alphabet.indexOf(ch);
        if (letter !== -1) return { index: index, rank: letter };
        index += 1;
      }
      return { index: index, rank: null };
    }
    while (i < left.length && j < right.length) {
      var leftAt = rankAt(left, i);
      var rightAt = rankAt(right, j);
      if (leftAt.rank === null || rightAt.rank === null) {
        i = leftAt.index;
        j = rightAt.index;
        break;
      }
      if (leftAt.rank !== rightAt.rank) return leftAt.rank - rightAt.rank;
      i = leftAt.index + 1;
      j = rightAt.index + 1;
    }
    var leftRest = rankAt(left, i);
    var rightRest = rankAt(right, j);
    if (leftRest.rank !== null) return 1;
    if (rightRest.rank !== null) return -1;
    return 0;
  }

  function compareTopics(a, b) {
    var left = String(a.label || "");
    var right = String(b.label || "");
    var diff = lang() === "az"
      ? compareByAlphabet(left, right, AZ_LETTERS, foldAz)
      : compareByAlphabet(left, right, "abcdefghijklmnopqrstuvwxyz0123456789", function (text) {
          return String(text || "").toLocaleLowerCase("en");
        });
    return diff || left.localeCompare(right, lang() === "az" ? "az" : "en");
  }

  function loadTopics() {
    var node = byId("ct-topics");
    if (!node) return;
    try {
      topics = JSON.parse(node.textContent || "[]");
    } catch (err) {
      topics = [];
    }
    topics.sort(compareTopics);
  }

  function loadGuides() {
    var node = byId("ct-topic-guides");
    if (!node) return;
    try {
      topicGuides = JSON.parse(node.textContent || "{}");
    } catch (err) {
      topicGuides = {};
    }
  }

  function selectedTopic() {
    var id = val("topic-id");
    if (!id || id === "other") return null;
    for (var i = 0; i < topics.length; i++) {
      if (topics[i].id === id) return topics[i];
    }
    return null;
  }

  function showTopicGuide(topic) {
    var box = byId("topic-guide");
    if (!box) return;
    box.value = topic && topicGuides[String(topic.id)] ? topicGuides[String(topic.id)] : "";
  }

  function reflectTopic(topic) {
    var ui = combo();
    if (!ui.id || !ui.label || !topic) return;
    ui.id.value = topic.id;
    ui.label.textContent = topic.label;
    if (ui.button) ui.button.classList.add("has-value");
    var otherTitle = byId("other-title");
    var otherWhy = byId("other-explanation");
    if (otherTitle && otherTitle.value) {
      otherTitle.value = "";
      if (otherWhy) otherWhy.value = "";
      syncOtherTopic();
    }
    if (ui.list) {
      ui.list.querySelectorAll(".phone-code-picker-option").forEach(function (option) {
        var chosen = option.getAttribute("data-id") === String(topic.id);
        option.setAttribute("aria-selected", chosen ? "true" : "false");
        option.classList.toggle("is-selected", chosen);
      });
    }
    showTopicGuide(topic);
  }

  function combo() {
    return {
      picker: byId("topic-picker"),
      button: byId("topic_picker"),
      label: byId("topic-picker-text"),
      search: byId("topic-search"),
      list: byId("topic-list"),
      panel: byId("topic-panel"),
      empty: byId("topic-empty"),
      id: byId("topic-id")
    };
  }

  function filteredTopics(query) {
    var q = String(query || "").trim().toLocaleLowerCase();
    return topics.filter(function (topic) {
      if (!topic.id || topic.id === "other") return false;
      if (!q) return true;
      return String(topic.label || "").toLocaleLowerCase().indexOf(q) !== -1;
    });
  }

  function renderTopics() {
    var ui = combo();
    if (!ui.list || !ui.search) return;
    var items = filteredTopics(ui.search.value);
    ui.list.innerHTML = "";
    if (!items.length) {
      activeIndex = -1;
      ui.list.hidden = true;
      if (ui.empty) ui.empty.hidden = false;
      showTopicGuide(null);
      return;
    }
    ui.list.hidden = false;
    if (ui.empty) ui.empty.hidden = true;
    if (activeIndex >= items.length) activeIndex = items.length - 1;
    items.forEach(function (topic, index) {
      var li = document.createElement("li");
      li.className = "phone-code-picker-option country-picker-option";
      li.id = "topic-opt-" + topic.id;
      li.setAttribute("role", "option");
      li.setAttribute("data-id", topic.id);
      var selected = ui.id && ui.id.value === topic.id;
      li.setAttribute("aria-selected", selected ? "true" : "false");
      li.classList.toggle("is-selected", selected);
      li.classList.toggle("is-active", index === activeIndex);
      var text = document.createElement("span");
      text.className = "phone-code-picker-option-text";
      text.textContent = topic.label;
      li.appendChild(text);
      li.addEventListener("mousedown", function (event) {
        event.preventDefault();
        selectTopic(topic);
      });
      li.addEventListener("mouseenter", function () {
        activeIndex = index;
        ui.list.querySelectorAll(".phone-code-picker-option").forEach(function (option, optionIndex) {
          option.classList.toggle("is-active", optionIndex === index);
        });
        if (ui.search) ui.search.setAttribute("aria-activedescendant", li.id);
        reflectTopic(topic);
      });
      ui.list.appendChild(li);
    });
    var active = ui.list.querySelector(".is-active");
    if (active && ui.search) ui.search.setAttribute("aria-activedescendant", active.id);
    if (active) active.scrollIntoView({ block: "nearest" });
    if (items[activeIndex]) {
      if (topicNavLive) reflectTopic(items[activeIndex]);
      else showTopicGuide(items[activeIndex]);
    }
  }

  function openTopics() {
    var ui = combo();
    if (!ui.panel || !ui.button || !ui.search) return;
    document.querySelectorAll(".phone-code-picker.is-open").forEach(function (picker) {
      if (picker === ui.picker) return;
      picker.classList.remove("is-open");
      var panel = picker.querySelector(".phone-code-picker-panel");
      var button = picker.querySelector(".phone-code-picker-btn");
      if (panel) panel.hidden = true;
      if (button) button.setAttribute("aria-expanded", "false");
    });
    ui.search.value = "";
    var opened = filteredTopics("");
    var selectedId = val("topic-id");
    var found = -1;
    opened.forEach(function (topic, index) {
      if (topic.id === selectedId) found = index;
    });
    activeIndex = found >= 0 ? found : 0;
    ui.panel.hidden = false;
    ui.picker.classList.add("is-open");
    ui.button.setAttribute("aria-expanded", "true");
    topicNavLive = false;
    renderTopics();
    topicNavLive = true;
    try {
      ui.search.focus({ preventScroll: true });
    } catch (err) {
      ui.search.focus();
    }
  }

  function closeTopics() {
    var ui = combo();
    if (!ui.panel || !ui.button) return;
    ui.panel.hidden = true;
    if (ui.picker) ui.picker.classList.remove("is-open");
    ui.button.setAttribute("aria-expanded", "false");
    if (ui.search) {
      ui.search.value = "";
      ui.search.removeAttribute("aria-activedescendant");
    }
    showTopicGuide(selectedTopic());
  }

  function selectTopic(topic) {
    var ui = combo();
    if (!ui.id || !ui.label) return;
    ui.id.value = topic.id;
    ui.label.textContent = topic.label;
    if (ui.button) ui.button.classList.add("has-value");
    var otherTitle = byId("other-title");
    var otherWhy = byId("other-explanation");
    if (otherTitle) otherTitle.value = "";
    if (otherWhy) otherWhy.value = "";
    closeTopics();
    syncOtherTopic();
  }

  function useProposedTopic() {
    var ui = combo();
    var custom = val("other-title");
    if (custom) {
      if (ui.id) ui.id.value = "other";
      if (ui.label) ui.label.textContent = t("topicPlaceholder");
      if (ui.button) ui.button.classList.remove("has-value");
    } else if (ui.id && ui.id.value === "other") {
      ui.id.value = "";
    }
    syncOtherTopic();
    showTopicGuide(custom ? null : selectedTopic());
  }

  function syncOtherTopic() {
    var panel = byId("other-topic");
    if (!panel) return;
    panel.hidden = !val("other-title");
  }

  function syncAudience(changed) {
    if (changed && changed.checked) {
      document.querySelectorAll('input[name="audience"]').forEach(function (input) {
        if (input !== changed) input.checked = false;
      });
    }
    var panel = byId("audience-other-wrap");
    var input = byId("audience-other-text");
    if (!panel) return;
    var show = checked("audience") === "other";
    panel.hidden = !show;
    if (!show && input) input.value = "";
  }

  function syncLanguage() {
    var panel = byId("language-other-wrap");
    var input = byId("language-other-text");
    if (!panel) return;
    var show = checked("submission_language") === "other";
    panel.hidden = !show;
    if (!show && input) input.value = "";
  }

  function syncCategoryOther() {
    var panel = byId("category-other-wrap");
    var input = byId("category-other-text");
    if (!panel) return;
    var show = checked("category") === "other";
    panel.hidden = !show;
    if (!show && input) input.value = "";
  }

  function syncTeam() {
    var panel = byId("team-fields");
    if (!panel) return;
    panel.hidden = checked("participation") !== "team";
  }

  function syncAi() {
    var panel = byId("ai-detail-wrap");
    if (!panel) return;
    var use = val("ai-use");
    panel.hidden = use !== "limited" && use !== "substantial";
  }

  function fileExt(name) {
    var parts = String(name || "").toLowerCase().split(".");
    return parts.length > 1 ? parts.pop() : "";
  }

  function fileProblem(file) {
    var name = String(file.name || "");
    if (/\.(php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i.test(name)) {
      return t("fileType");
    }
    if (!FILE_EXT[fileExt(name)]) return t("fileType");
    if (file.size > MAX_BYTES) return t("fileSize");
    if (!file.size) return t("fileType");
    return "";
  }

  var PHOTO_MAX_BYTES = 5 * 1024 * 1024;
  var photoPreviewUrl = "";

  function photoInput() {
    return byId("photofile");
  }

  function selectedPhoto() {
    var input = photoInput();
    return input && input.files && input.files[0] ? input.files[0] : null;
  }

  function setPhotoError(message) {
    var box = byId("photofile-error");
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

  function showPhotoSelected(file) {
    var card = document.querySelector('.ct-org-photo .app-file-card[data-file-kind="photo"]');
    var status = byId("photofile-status");
    var nameEl = status ? status.querySelector(".app-file-name") : null;
    var thumb = byId("photofile-thumb");
    if (card) card.classList.toggle("is-selected", !!file);
    if (!status) return;
    if (!file) {
      status.hidden = true;
      if (nameEl) nameEl.textContent = "";
      revokePhotoPreview();
      return;
    }
    if (nameEl) nameEl.textContent = file.name;
    status.hidden = false;
    revokePhotoPreview();
    if (thumb) {
      photoPreviewUrl = URL.createObjectURL(file);
      thumb.src = photoPreviewUrl;
      thumb.alt = file.name || t("photoRequired");
      thumb.hidden = false;
    }
  }

  function photoProblem(file) {
    if (!file) return t("photoRequired");
    var name = String(file.name || "");
    if (/\.(php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i.test(name)) {
      return t("photoType");
    }
    var ext = fileExt(name);
    if (ext !== "jpg" && ext !== "jpeg" && ext !== "png") return t("photoType");
    if (file.size > PHOTO_MAX_BYTES) return t("photoSize");
    if (!file.size) return t("photoInvalid");
    return "";
  }

  function applyPhotoSelection() {
    var file = selectedPhoto();
    if (!file) {
      showPhotoSelected(null);
      setPhotoError("");
      return false;
    }
    var problem = photoProblem(file);
    if (problem && problem !== t("photoRequired")) {
      var input = photoInput();
      if (input) input.value = "";
      showPhotoSelected(null);
      setPhotoError(problem);
      return false;
    }
    setPhotoError("");
    showPhotoSelected(file);
    return true;
  }

  function clearPhotoSelection() {
    var input = photoInput();
    if (input) input.value = "";
    showPhotoSelected(null);
    setPhotoError("");
  }

  function rejectPhoto(message) {
    setPhotoError(message);
    showStatus(message, true);
    var card = document.querySelector('.ct-org-photo .app-file-card[data-file-kind="photo"]');
    var choose = card ? card.querySelector(".app-file-choose") : null;
    if (choose && typeof choose.focus === "function") choose.focus();
    if (card && card.scrollIntoView) card.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }

  function syncFileInput() {
    var input = byId("submission-files");
    if (!input || typeof DataTransfer === "undefined") return;
    var bag = new DataTransfer();
    chosenFiles.forEach(function (file) {
      bag.items.add(file);
    });
    input.files = bag.files;
  }

  function renderFiles() {
    var list = byId("file-list");
    var error = byId("file-error");
    if (!list) return;
    list.innerHTML = "";
    chosenFiles.forEach(function (file, index) {
      var item = document.createElement("li");
      var name = document.createElement("span");
      name.textContent = file.name + " — " + t("fileReady");
      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "app-file-remove";
      remove.textContent = t("remove");
      remove.addEventListener("click", function () {
        chosenFiles.splice(index, 1);
        syncFileInput();
        renderFiles();
      });
      item.appendChild(name);
      item.appendChild(remove);
      list.appendChild(item);
    });
    if (error && !error.textContent) error.hidden = true;
  }

  function addFiles(fileList) {
    var error = byId("file-error");
    var problem = "";
    Array.prototype.forEach.call(fileList || [], function (file) {
      if (problem) return;
      if (chosenFiles.length >= MAX_FILES) {
        problem = t("fileCount");
        return;
      }
      problem = fileProblem(file);
      if (!problem) chosenFiles.push(file);
    });
    syncFileInput();
    renderFiles();
    if (error) {
      error.hidden = !problem;
      error.textContent = problem || "";
    }
    return !problem;
  }

  function validate() {
    clearFieldWarnings();
    var name = byId("given-name");
    if (!val("given-name")) return warn(name, t("nameRequired")), false;
    if (!nameOk(val("given-name")) || textUnsafe(val("given-name"))) return warn(name, t("nameInvalid")), false;
    var surname = byId("surname");
    if (!val("surname")) return warn(surname, t("surnameRequired")), false;
    if (!nameOk(val("surname")) || textUnsafe(val("surname"))) return warn(surname, t("surnameInvalid")), false;
    var dob = byId("dob");
    if (!val("dob")) return warn(dob, t("dobRequired")), false;
    if (!parseDobDisplay(val("dob"))) return warn(dob, t("dobInvalid")), false;
    var email = byId("email");
    if (!val("email")) return warn(email, t("emailRequired")), false;
    if (!emailOk(val("email"))) return warn(email, t("emailInvalid")), false;
    if (!val("country")) return warn(pickerOr("country"), t("countryRequired")), false;
    if (textUnsafe(val("country"))) return warn(pickerOr("country"), t("unsafe")), false;
    if (!cityValue()) return warn(cityControl(), t("cityRequired")), false;
    if (textUnsafe(cityValue())) return warn(cityControl(), t("unsafe")), false;
    var org = byId("organisation");
    if (val("organisation") && textUnsafe(val("organisation"))) return warn(org, t("unsafe")), false;
    var photoErr = photoProblem(selectedPhoto());
    if (photoErr) return rejectPhoto(photoErr);
    setPhotoError("");
    if (!checked("category")) return warn(document.querySelector('input[name="category"]'), t("categoryRequired")), false;
    if (checked("category") === "other") {
      var categoryOther = byId("category-other-text");
      if (!val("category-other-text")) return warn(categoryOther, t("categoryOtherRequired")), false;
      if (textUnsafe(val("category-other-text"))) return warn(categoryOther, t("unsafe")), false;
    }
    var bio = byId("biography");
    if (val("biography") && textUnsafe(val("biography"))) return warn(bio, t("unsafe")), false;
    if (!checked("participation")) return warn(document.querySelector('input[name="participation"]'), t("participationRequired")), false;
    if (checked("participation") === "team") {
      var team = byId("team-name");
      if (!val("team-name")) return warn(team, t("teamNameRequired")), false;
      if (textUnsafe(val("team-name"))) return warn(team, t("unsafe")), false;
      var member = byId("member2-name");
      if (!val("member2-name")) return warn(member, t("memberRequired")), false;
      if (!nameOk(val("member2-name"))) return warn(member, t("nameInvalid")), false;
      var memberMail = byId("member2-email");
      if (val("member2-email") && !emailOk(val("member2-email"))) return warn(memberMail, t("emailInvalid")), false;
      var member3 = byId("member3-name");
      if (val("member3-name") && !nameOk(val("member3-name"))) return warn(member3, t("nameInvalid")), false;
      var member3Mail = byId("member3-email");
      if (val("member3-email") && !emailOk(val("member3-email"))) return warn(member3Mail, t("emailInvalid")), false;
    }
    var topicButton = byId("topic_picker");
    var otherTitle = byId("other-title");
    var hasCustom = !!val("other-title");
    var topicId = val("topic-id");
    var hasListed = !!topicId && topicId !== "other";
    if (hasListed === hasCustom) {
      return warn(topicButton, t("topicRequired")), false;
    }
    if (hasCustom) {
      if (textUnsafe(val("other-title"))) return warn(otherTitle, t("unsafe")), false;
      if (byId("topic-id")) byId("topic-id").value = "other";
      var otherWhy = byId("other-explanation");
      if (!val("other-explanation")) return warn(otherWhy, t("otherWhyRequired")), false;
      if (textUnsafe(val("other-explanation"))) return warn(otherWhy, t("unsafe")), false;
    }
    var title = byId("submission-title");
    if (!val("submission-title")) return warn(title, t("titleRequired")), false;
    if (textUnsafe(val("submission-title"))) return warn(title, t("unsafe")), false;
    var audience = checked("audience");
    var audienceBox = document.querySelector('input[name="audience"]:checked') || document.querySelector('input[name="audience"]');
    if (!audience) return warn(audienceBox, t("audienceRequired")), false;
    if (audience === "other") {
      var audienceOther = byId("audience-other-text");
      if (!val("audience-other-text")) return warn(audienceOther, t("audienceOtherRequired")), false;
      if (textUnsafe(val("audience-other-text"))) return warn(audienceOther, t("unsafe")), false;
    }
    var audienceNote = byId("audience-note");
    if (val("audience-note") && textUnsafe(val("audience-note"))) return warn(audienceNote, t("unsafe")), false;
    var description = byId("description");
    if (!val("description")) return warn(description, t("descriptionRequired")), false;
    if (textUnsafe(val("description"))) return warn(description, t("unsafe")), false;
    if (!document.querySelector('input[name="formats[]"]:checked')) {
      return warn(document.querySelector('input[name="formats[]"]'), t("formatRequired")), false;
    }
    if (!checked("submission_language")) return warn(document.querySelector('input[name="submission_language"]'), t("languageRequired")), false;
    if (checked("submission_language") === "other") {
      var languageOther = byId("language-other-text");
      if (!val("language-other-text")) return warn(languageOther, t("languageOtherRequired")), false;
      if (textUnsafe(val("language-other-text"))) return warn(languageOther, t("unsafe")), false;
    }
    var sources = byId("sources");
    if (val("sources") && textUnsafe(val("sources"))) return warn(sources, t("unsafe")), false;
    var ai = byId("ai-use");
    if (!val("ai-use")) return warn(ai, t("aiRequired")), false;
    var aiDetail = byId("ai-detail");
    if ((val("ai-use") === "limited" || val("ai-use") === "substantial")) {
      if (!val("ai-detail")) return warn(aiDetail, t("aiDetailRequired")), false;
      if (textUnsafe(val("ai-detail"))) return warn(aiDetail, t("unsafe")), false;
    }
    var link = byId("submission-link");
    var linkValue = val("submission-link");
    if (linkValue && !/^https?:\/\/\S+$/i.test(linkValue)) return warn(link, t("linkInvalid")), false;
    if (linkValue && textUnsafe(linkValue)) return warn(link, t("unsafe")), false;
    var interest = byId("interest-only");
    if (!(interest && interest.checked) && !chosenFiles.length && !linkValue) {
      return warn(byId("submission-files") || link, t("workRequired")), false;
    }
    var fileError = byId("file-error");
    if (fileError && !fileError.hidden && fileError.textContent) {
      warn(byId("submission-files"), fileError.textContent);
      return false;
    }
    var confirms = [
      ["conditions", "conditionsRequired"],
      ["originality", "originalityRequired"],
      ["attribution", "attributionRequired"],
      ["publication", "publicationRequired"],
      ["privacy", "privacyRequired"]
    ];
    var respectForm = byId("ctApplyForm");
    var respectFields = respectForm ? respectForm.querySelectorAll("input, textarea") : [];
    for (var r = 0; r < respectFields.length; r++) {
      var respectField = respectFields[r];
      if (!respectField || respectField.disabled || respectField.readOnly) continue;
      var respectType = (respectField.type || "").toLowerCase();
      if (respectType === "hidden" || respectType === "file" || respectType === "checkbox" || respectType === "radio" || respectType === "submit" || respectType === "button") continue;
      if (!respectField.name || respectField.name === "website") continue;
      var respectValue = String(respectField.value || "");
      if (!respectValue.trim()) continue;
      var respectName = /name/i.test(respectField.id || "") || /name/i.test(respectField.name || "");
      if (window.daabRespectOffensive && window.daabRespectOffensive(respectValue, { nameField: respectName })) {
        return warn(respectField, t("respect")), false;
      }
    }
    for (var i = 0; i < confirms.length; i++) {
      var box = byId(confirms[i][0]);
      if (!box || !box.checked) return warn(box, t(confirms[i][1])), false;
    }
    return true;
  }

  function serverMessage(status) {
    var map = {
      "error:name": t("nameInvalid"),
      "error:surname": t("surnameInvalid"),
      "error:dob": t("dobInvalid"),
      "error:email": t("emailInvalid"),
      "error:place": t("countryRequired"),
      "error:category": t("categoryRequired"),
      "error:category_other": t("categoryOtherRequired"),
      "error:participation": t("participationRequired"),
      "error:team": t("memberRequired"),
      "error:topic": t("topicRequired"),
      "error:topic_other": t("otherWhyRequired"),
      "error:title": t("titleRequired"),
      "error:audience": t("audienceRequired"),
      "error:audience_other": t("audienceOtherRequired"),
      "error:description": t("descriptionRequired"),
      "error:format": t("formatRequired"),
      "error:language": t("languageRequired"),
      "error:language_other": t("languageOtherRequired"),
      "error:ai": t("aiDetailRequired"),
      "error:work": t("workRequired"),
      "error:link": t("linkInvalid"),
      "error:file_type": t("fileType"),
      "error:file_size": t("fileSize"),
      "error:file_count": t("fileCount"),
      "error:file_invalid": t("fileType"),
      "error:photo_missing": t("photoRequired"),
      "error:photo_type": t("photoType"),
      "error:photo_size": t("photoSize"),
      "error:photo_invalid": t("photoInvalid"),
      "error:conditions": t("conditionsRequired"),
      "error:originality": t("originalityRequired"),
      "error:attribution": t("attributionRequired"),
      "error:publication": t("publicationRequired"),
      "error:privacy": t("privacyRequired"),
      "error:unsafe": t("unsafe"),
      "error:respect": t("respect")
    };
    return map[status] || "";
  }

  function setSending(on) {
    sending = on;
    var button = byId("appSubmitBtn");
    var form = byId("ctApplyForm");
    if (button) {
      button.disabled = on;
      button.classList.toggle("is-loading", on);
      button.setAttribute("aria-busy", on ? "true" : "false");
      var label = button.querySelector(".app-btn-label");
      if (label) label.textContent = on ? t("sending") : t("submit");
    }
    if (form) form.setAttribute("aria-busy", on ? "true" : "false");
    if (on) showStatus(t("sending"), false);
  }

  function showSuccess() {
    document.querySelectorAll(".form-section").forEach(function (section) {
      section.hidden = true;
    });
    var success = byId("success");
    if (success) {
      success.classList.add("active");
      success.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    showStatus(t("sent"), false);
  }

  function submit(event) {
    event.preventDefault();
    if (sending) return;
    if (!validate()) return;
    var form = byId("ctApplyForm");
    var pageUrl = byId("page-url");
    if (pageUrl) pageUrl.value = window.location.href;
    syncFileInput();
    var data = new FormData(form);
    setSending(true);
    fetch(form.getAttribute("action") || "mail-complex-topics.php", {
      method: "POST",
      body: data,
      headers: { Accept: "text/plain, */*" }
    }).then(function (response) {
      return response.text().then(function (text) {
        var status = String(text || "").trim().toLowerCase();
        if (status.indexOf("<?php") !== -1 || response.status === 404 || response.status === 405 || response.status === 501) {
          throw new Error(t("phpUnavailable"));
        }
        if (!response.ok || status !== "success") {
          throw new Error(serverMessage(status) || t("submitFailed"));
        }
        showSuccess();
      });
    }).catch(function (err) {
      var message = err && err.message ? err.message : t("submitFailed");
      if (/failed to fetch|networkerror|load failed/i.test(message)) message = t("phpUnavailable");
      showStatus(message, true);
    }).then(function () {
      setSending(false);
    });
  }

  function bindToggles() {
    document.querySelectorAll(".app-section-toggle").forEach(function (button) {
      button.addEventListener("click", function () {
        var body = byId(button.getAttribute("aria-controls"));
        if (!body) return;
        var open = button.getAttribute("aria-expanded") !== "false";
        button.setAttribute("aria-expanded", open ? "false" : "true");
        body.hidden = open;
      });
    });
  }

  function bindCombo() {
    var ui = combo();
    if (!ui.button || !ui.search) return;
    ui.button.addEventListener("click", function (event) {
      event.preventDefault();
      if (ui.panel.hidden) openTopics();
      else closeTopics();
    });
    ui.button.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown" || event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        if (ui.panel.hidden) openTopics();
      }
    });
    ui.search.addEventListener("input", function () {
      activeIndex = 0;
      renderTopics();
    });
    ui.search.addEventListener("keydown", function (event) {
      var items = filteredTopics(ui.search.value);
      if (event.key === "ArrowDown") {
        event.preventDefault();
        activeIndex = Math.min(items.length - 1, activeIndex + 1);
        renderTopics();
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        activeIndex = Math.max(0, activeIndex - 1);
        renderTopics();
      } else if (event.key === "Enter") {
        event.preventDefault();
        if (items[activeIndex]) selectTopic(items[activeIndex]);
      } else if (event.key === "Escape") {
        event.preventDefault();
        closeTopics();
        ui.button.focus();
      }
    });
    var fieldLabel = document.querySelector('label[for="topic_picker"]');
    if (fieldLabel) {
      fieldLabel.addEventListener("click", function (event) {
        event.preventDefault();
        if (ui.panel.hidden) openTopics();
        else ui.button.focus();
      });
    }
    document.addEventListener("click", function (event) {
      if (!ui.picker || ui.panel.hidden) return;
      if (ui.picker.contains(event.target)) return;
      if (fieldLabel && fieldLabel.contains(event.target)) return;
      closeTopics();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && ui.panel && !ui.panel.hidden) {
        closeTopics();
        ui.button.focus();
      }
    });
  }

  function init() {
    var form = byId("ctApplyForm");
    if (!form) return;
    loadTopics();
    loadGuides();
    initDobField();
    bindToggles();
    var otherTitle = byId("other-title");
    if (otherTitle) otherTitle.addEventListener("input", useProposedTopic);
    bindCombo();
    syncCategoryOther();
    syncAudience();
    syncLanguage();
    syncTeam();
    syncOtherTopic();
    document.querySelectorAll('input[name="category"]').forEach(function (input) {
      input.addEventListener("change", syncCategoryOther);
    });
    document.querySelectorAll('input[name="submission_language"]').forEach(function (input) {
      input.addEventListener("change", syncLanguage);
    });
    document.querySelectorAll('input[name="audience"]').forEach(function (input) {
      input.addEventListener("change", function () {
        syncAudience(input);
      });
    });
    syncAi();
    document.querySelectorAll('input[name="participation"]').forEach(function (input) {
      input.addEventListener("change", syncTeam);
    });
    var ai = byId("ai-use");
    if (ai) ai.addEventListener("change", syncAi);
    var files = byId("submission-files");
    if (files) {
      files.addEventListener("change", function () {
        addFiles(files.files);
        files.value = "";
        syncFileInput();
      });
    }
    var choose = byId("choose-files");
    if (choose && files) {
      choose.addEventListener("click", function () {
        files.click();
      });
    }
    var photoCard = document.querySelector('.ct-org-photo .app-file-card[data-file-kind="photo"]');
    var photoField = photoInput();
    if (photoCard) {
      photoCard.addEventListener("click", function (event) {
        var choosePhoto = event.target.closest(".app-file-choose, .app-file-replace");
        if (choosePhoto && photoCard.contains(choosePhoto)) {
          var target = byId(choosePhoto.getAttribute("data-file-target") || "photofile");
          if (target) target.click();
          return;
        }
        var removePhoto = event.target.closest(".app-file-remove");
        if (removePhoto && photoCard.contains(removePhoto)) clearPhotoSelection();
      });
    }
    if (photoField) photoField.addEventListener("change", applyPhotoSelection);
    form.addEventListener("submit", submit);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
