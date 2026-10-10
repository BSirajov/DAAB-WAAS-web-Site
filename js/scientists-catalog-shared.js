/**
 * Shared sort/compare/escape helpers for scientists list + profiles catalog scripts.
 */
(function () {
  "use strict";

  function pageLang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function localeCollator() {
    var lang = pageLang();
    if (typeof Intl !== "undefined" && typeof Intl.Collator === "function") {
      return new Intl.Collator(lang === "en" ? "en" : "az", { sensitivity: "base" });
    }
    return null;
  }

  function compare(a, b) {
    var coll = window.DAAB_COLLATION;
    if (coll && typeof coll.compare === "function") {
      return coll.compare(a, b);
    }
    var intl = localeCollator();
    if (intl) return intl.compare(String(a || ""), String(b || ""));
    return String(a || "").localeCompare(String(b || ""), undefined, {
      sensitivity: "base",
    });
  }

  function sortValues(arr) {
    var coll = window.DAAB_COLLATION;
    if (coll && typeof coll.sort === "function") {
      return coll.sort(arr);
    }
    var copy = arr.slice();
    copy.sort(compare);
    return copy;
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normQuery(q) {
    var AZ = {
      "\u0259": "e", "\u0131": "i", "\u00f6": "o", "\u00fc": "u",
      "\u011f": "g", "\u015f": "s", "\u00e7": "c",
      "\u018f": "e", "\u0130": "i", "\u00d6": "o", "\u00dc": "u",
      "\u011e": "g", "\u015e": "s", "\u00c7": "c"
    };
    return String(q || "")
      .replace(/[^\u0000-\u007f]/g, function (ch) { return AZ[ch] || ch; })
      .toLowerCase()
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  /** Display name (AZ or EN) → ISO 3166-1 alpha-2. */
  var COUNTRY_ISO = {
    "ABŞ": "US",
    "USA": "US",
    "United States": "US",
    "Almaniya": "DE",
    "Germany": "DE",
    "Avstriya": "AT",
    "Austria": "AT",
    "Birləşmiş Krallıq": "GB",
    "United Kingdom": "GB",
    "Estoniya": "EE",
    "Estonia": "EE",
    "Fransa": "FR",
    "France": "FR",
    "Gürcüstan": "GE",
    "Georgia": "GE",
    "Kanada": "CA",
    "Canada": "CA",
    "Koreya": "KR",
    "South Korea": "KR",
    "Meksika": "MX",
    "Mexico": "MX",
    "Misir": "EG",
    "Egypt": "EG",
    "Oman": "OM",
    "Polşa": "PL",
    "Poland": "PL",
    "Qazaxıstan": "KZ",
    "Kazakhstan": "KZ",
    "Qırğızıstan": "KG",
    "Kyrgyzstan": "KG",
    "Rusiya Federasiyası": "RU",
    "Russia": "RU",
    "Səudiyyə Ərəbistanı": "SA",
    "Saudi Arabia": "SA",
    "Türkiyə": "TR",
    "Türkiye": "TR",
    "Turkey": "TR",
    "Ukrayna": "UA",
    "Ukraine": "UA",
    "Yaponiya": "JP",
    "Japan": "JP",
    "İsrail": "IL",
    "Israel": "IL",
    "İsveç": "SE",
    "Sweden": "SE",
    "İtaliya": "IT",
    "Italy": "IT"
  };

  /** Profile JSON country_code values that are not ISO alpha-2. */
  var PROFILE_CODE_ISO = {
    abs: "US",
    uk: "GB"
  };

  var FIELD_CODE = {
    "Beynəlxalq hüquq": "international-law",
    "International law": "international-law",
    "Bioinformatika": "bioinformatics",
    "Bioinformatics": "bioinformatics",
    "Biologiya": "biology",
    "Biology": "biology",
    "Ermənişünaslıq": "armenian-studies",
    "Armenian studies": "armenian-studies",
    "Farmakologiya": "pharmacology",
    "Pharmacology": "pharmacology",
    "Filologiya": "philology",
    "Philology": "philology",
    "Fizika": "physics",
    "Physics": "physics",
    "Fəlsəfə, Hüquq": "philosophy-law",
    "Philosophy, law": "philosophy-law",
    "Geofizika": "geophysics",
    "Geophysics": "geophysics",
    "Hüquq": "law",
    "Law": "law",
    "Həkim": "medicine",
    "Medicine": "medicine",
    "Kimya": "chemistry",
    "Chemistry": "chemistry",
    "Kompüter Elmləri": "computer-science",
    "Computer science": "computer-science",
    "Musiqiçi": "music",
    "Music": "music",
    "Mühəndis": "engineering",
    "Engineering": "engineering",
    "Nanotexnologiya": "nanotechnology",
    "Nanotechnology": "nanotechnology",
    "Psixologiya": "psychology",
    "Psychology": "psychology",
    "Riyaziyyat": "mathematics",
    "Mathematics": "mathematics",
    "Rəssam": "art",
    "Art": "art",
    "Siyasi tarix": "political-history",
    "Political history": "political-history",
    "Sosial Siyasət": "social-policy",
    "Social policy": "social-policy",
    "Sosiologiya": "sociology",
    "Sociology": "sociology",
    "Tarix": "history",
    "History": "history",
    "Tarix, Şərqşünaslıq": "history-oriental-studies",
    "History, oriental studies": "history-oriental-studies",
    "Türk Dili və Ədəbiyyatı": "turkish-language-literature",
    "Turkish language and literature": "turkish-language-literature",
    "Türkologiya": "turkology",
    "Turkology": "turkology",
    "Təhsil": "education",
    "Education": "education",
    "İqtisadiyyat": "economics",
    "Economics": "economics",
    "Ərəb dili və ədəbiyyatı": "arabic-language-literature",
    "Arabic language and literature": "arabic-language-literature"
  };

  function countryIso(nameOrCode) {
    var raw = String(nameOrCode || "").trim();
    if (!raw) return "";
    if (COUNTRY_ISO[raw]) return COUNTRY_ISO[raw];
    var lower = raw.toLowerCase();
    if (PROFILE_CODE_ISO[lower]) return PROFILE_CODE_ISO[lower];
    if (/^[A-Za-z]{2}$/.test(raw)) return raw.toUpperCase();
    return "";
  }

  function fieldCode(label) {
    var raw = String(label || "").trim();
    if (!raw) return "";
    return FIELD_CODE[raw] || raw;
  }

  function genderCode(value) {
    var v = String(value || "").trim().toLowerCase();
    if (v === "m" || v === "male" || v === "kişi" || v === "kisi") return "m";
    if (v === "f" || v === "female" || v === "qadın" || v === "qadin") return "f";
    return "";
  }

  window.DAAB_SCIENTISTS_CATALOG = {
    pageLang: pageLang,
    compare: compare,
    sortValues: sortValues,
    esc: esc,
    normQuery: normQuery,
    countryIso: countryIso,
    fieldCode: fieldCode,
    genderCode: genderCode
  };
})();
