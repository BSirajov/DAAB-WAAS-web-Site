/**
 * Client-side scientist profile cards — loads i18n/scientists-profiles.json
 * and renders the catalog grid (replaces server-embedded HTML).
 */
(function () {
  "use strict";

  var CRED_LABEL = {
    PhD: "Ph.D.",
    "Prof.Dr.": "Prof. Dr.",
    "Ed.D.": "Ed.D.",
    Dr: "Dr.",
  };

  var META_LABELS = {
    az: { field: "İxtisas:", email: "E-məktub:" },
    en: { field: "Field:", email: "Email:" },
  };

  var QR_LABELS = {
    az: {
      aria: "Profil linkinin QR kodu",
      title: "Bu alimin profil səhifəsinə keçid",
    },
    en: {
      aria: "QR code for profile link",
      title: "Link to this scientist's profile page",
    },
  };

  var LOAD_ERROR = {
    az: "Profillər yüklənə bilmədi. Səhifəni yeniləyin.",
    en: "Could not load profiles. Please refresh the page.",
  };

  function pageLang() {
    var el = document.documentElement;
    return (el.getAttribute("data-daab-lang") || el.lang || "az").slice(0, 2);
  }

  function assetRoot() {
    return document.documentElement.getAttribute("data-daab-asset-root") || "../../";
  }

  function escAttr(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function escHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function normSearch(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function azUpperName(name) {
    return String(name || "")
      .trim()
      .toUpperCase()
      .replace(/I/g, "İ");
  }

  function azUpperNameLatin(name) {
    return String(name || "").trim().toUpperCase();
  }

  function slugFromPhoto(photo) {
    var base = String(photo || "").trim();
    if (!base) return "";
    var slash = base.lastIndexOf("/");
    if (slash >= 0) base = base.slice(slash + 1);
    var dot = base.lastIndexOf(".");
    return dot >= 0 ? base.slice(0, dot) : base;
  }

  function profileName(profile, lang) {
    var base = profile.name || profile.name_az || "";
    if (lang === "en") {
      return profile.name_en || base;
    }
    return base;
  }

  function profileCountry(profile, lang) {
    if (lang === "en") {
      return profile.country_en || profile.country_az || profile.country || "";
    }
    return profile.country_az || profile.country || "";
  }

  function profileField(profile, lang) {
    if (lang === "en") {
      return profile.field_en || profile.field_az || profile.field || "";
    }
    return profile.field_az || profile.field || "";
  }

  function profileTitle(profile, lang) {
    if (lang === "en") {
      return profile.title_en || profile.title_az || profile.title || "";
    }
    return profile.title_az || profile.title || "";
  }

  function profileBio(profile, lang) {
    if (lang === "en") {
      return profile.bio_html_en || profile.bio_html_az || profile.bio_html || "";
    }
    return profile.bio_html_az || profile.bio_html || "";
  }

  function profileCountryCode(profile) {
    return String(profile.country_code || "").trim();
  }

  function buildSearchBlob(profile, lang) {
    var degree = String(profile.degree || "").trim();
    var cred = CRED_LABEL[degree] || degree;
    var name = profileName(profile, lang);
    if (cred) name = name + " " + cred;
    var country = profileCountry(profile, lang);
    var field = profileField(profile, lang);
    var email = String(profile.email || "").trim();
    var code = profileCountryCode(profile);
    var title = profileTitle(profile, lang);
    var parts = [name, degree, title, country, email, field, code, degree, email, field];
    return normSearch(parts.filter(Boolean).join(" "));
  }

  function renderCard(profile, lang, prefix) {
    var email = String(profile.email || "").trim();
    var degree = String(profile.degree || "").trim();
    var cred = CRED_LABEL[degree] || degree;
    var country = profileCountry(profile, lang);
    var field = profileField(profile, lang);
    var code = profileCountryCode(profile);
    var search = buildSearchBlob(profile, lang);
    var title = profileTitle(profile, lang);
    var bioHtml = profileBio(profile, lang);
    var labels = META_LABELS[lang] || META_LABELS.az;
    var photo = String(profile.photo || "img_001_p61.jpeg").trim();
    var slug = slugFromPhoto(photo);
    var nameDisplay = profileName(profile, lang);
    var nameHeading;
    if (lang === "az" && profile.name_heading_az) {
      nameHeading = profile.name_heading_az;
    } else if (lang === "en" && profile.name_heading_en) {
      nameHeading = profile.name_heading_en;
    } else {
      nameHeading = lang === "en" ? azUpperNameLatin(nameDisplay) : azUpperName(nameDisplay);
    }

    var emailRow;
    if (email) {
      emailRow =
        '      <div class="card-meta-row"><span class="card-meta-label">' +
        escHtml(labels.field) +
        '</span><span class="card-meta-ixtilas">' +
        escHtml(field) +
        '</span></div>\n' +
        '      <div class="card-meta-row"><span class="card-meta-label">' +
        escHtml(labels.email) +
        '</span><a class="card-email" href="mailto:' +
        escAttr(email) +
        '">' +
        escHtml(email) +
        "</a></div>";
    } else {
      emailRow =
        '      <div class="card-meta-row"><span class="card-meta-label">' +
        escHtml(labels.field) +
        '</span><span class="card-meta-ixtilas">' +
        escHtml(field) +
        '</span></div>\n' +
        '      <div class="card-meta-row"><span class="card-meta-label">' +
        escHtml(labels.email) +
        '</span><span class="card-email card-email--empty">—</span></div>';
    }

    var credHtml = cred ? ' <span class="cred">' + escHtml(cred) + "</span>" : "";
    var qrLabels = QR_LABELS[lang] || QR_LABELS.en;
    var profileHref = "#" + escAttr(slug);
    var qrSrc = prefix + "images/qr/" + lang + "/" + escAttr(slug) + ".png?v=1";
    var listenLead =
      lang === "az"
        ? String(profile.listen_lead_az || "").trim()
        : String(profile.listen_lead_en || "").trim();

    var titleHtml = title.trim()
      ? '      <p class="card-title">' + escHtml(title) + "</p>\n"
      : "";
    var roleHtml = listenLead.trim()
      ? '      <p class="card-role">' + escHtml(listenLead) + "</p>\n"
      : "";

    return (
      '<div class="card" id="' +
      escAttr(slug) +
      '" tabindex="-1" data-country-name="' +
      escAttr(country) +
      '" data-country="' +
      escAttr(code) +
      '" data-search="' +
      escAttr(search) +
      '" data-email="' +
      escAttr(email) +
      '" data-ixtilas="' +
      escAttr(field) +
      '" data-degree="' +
      escAttr(degree) +
      '">\n' +
      '  <div class="card-avatar card-photo"><img src="' +
      prefix +
      "images/scientists-photos/" +
      escAttr(photo) +
      '" alt="' +
      escHtml(nameDisplay) +
      '" loading="lazy"/></div>\n' +
      '  <div class="card-body">\n' +
      '    <div class="card-head">\n' +
      '      <div class="card-profile-header">\n' +
      '        <div class="card-header">\n' +
      '          <span class="card-name">' +
      escHtml(nameHeading) +
      credHtml +
      '</span>\n' +
      '          <p class="card-country">' +
      escHtml(country) +
      "</p>\n" +
      titleHtml +
      "        </div>\n" +
      roleHtml +
      '        <div class="card-meta">\n' +
      emailRow +
      "\n" +
      "        </div>\n" +
      "      </div>\n" +
      "    </div>\n" +
      '    <div class="card-bio">' +
      bioHtml +
      "</div>\n" +
      "  </div>\n" +
      '  <a class="card-qr-link" href="' +
      profileHref +
      '" title="' +
      escAttr(qrLabels.title) +
      '" aria-label="' +
      escAttr(qrLabels.aria) +
      '">\n' +
      '    <img class="card-qr" src="' +
      qrSrc +
      '" width="80" height="80" alt="" decoding="async" loading="lazy"/>\n' +
      "  </a>\n" +
      "</div>"
    );
  }

  function dispatchRendered(count) {
    document.dispatchEvent(
      new CustomEvent("daab-scientists-profiles-rendered", {
        detail: { count: count },
      })
    );
  }

  function dispatchError(err) {
    document.dispatchEvent(
      new CustomEvent("daab-scientists-profiles-render-error", {
        detail: { error: err },
      })
    );
  }

  function showLoadError(grid, lang) {
    var msg = LOAD_ERROR[lang] || LOAD_ERROR.en;
    grid.innerHTML =
      '<p class="profiles-catalog-error" role="alert">' + escHtml(msg) + "</p>";
    grid.removeAttribute("aria-busy");
  }

  function renderCatalog() {
    var catalog = document.getElementById("scientists-catalog");
    if (!catalog || catalog.getAttribute("data-daab-profiles-client") !== "1") {
      return;
    }

    var grid = catalog.querySelector(".cards-grid");
    if (!grid) return;

    var lang = pageLang();
    var prefix = assetRoot();
    var jsonUrl = prefix + "i18n/scientists-profiles.json";

    fetch(jsonUrl, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (data) {
        var profiles = (data && data.profiles) || [];
        profiles.sort(function (a, b) {
          return (a.say || 0) - (b.say || 0);
        });
        var html = profiles
          .map(function (p) {
            return renderCard(p, lang, prefix);
          })
          .join("\n\n");
        grid.innerHTML = html;
        grid.removeAttribute("aria-busy");
        dispatchRendered(profiles.length);
      })
      .catch(function (err) {
        showLoadError(grid, lang);
        dispatchError(err);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderCatalog);
  } else {
    renderCatalog();
  }
})();
