/**
 * Forum 2024 Photos Gallery — thumbnails in grid, full resolution in lightbox.
 */
(function () {
  "use strict";

  var MANIFEST_URL = "photos-gallery-manifest.json";
  var THUMB_INDEX_URL = "photos-gallery-thumbs.json";
  var EAGER_COUNT = 8;
  var IO_ROOT_MARGIN = "280px 0px";

  var grid = document.getElementById("photosGalleryGrid");
  var catList = document.getElementById("photosGalleryCategories");
  var titleEl = document.getElementById("photosGalleryTitle");
  var countEl = document.getElementById("photosGalleryCount");
  var statusEl = document.getElementById("photosGalleryStatus");
  var lightbox = document.getElementById("photosGalleryLightbox");
  var lightboxImg = document.getElementById("photosGalleryLightboxImg");
  var lightboxCaption = document.getElementById("photosGalleryLightboxCaption");
  var lightboxClose = document.querySelector(".photos-gallery-lightbox-close");

  if (!grid || !catList) return;

  var assetRoot =
    (window.DAAB_I18N && typeof window.DAAB_I18N.assetRoot === "function" && window.DAAB_I18N.assetRoot()) ||
    document.documentElement.getAttribute("data-daab-asset-root") ||
    "../";
  if (assetRoot && !assetRoot.endsWith("/")) assetRoot += "/";

  var lang = document.documentElement.getAttribute("data-daab-lang") || "en";
  var imageBase = assetRoot + "images/photos-gallery/";
  var thumbBase = imageBase + "_thumbs/";
  var manifestPath = assetRoot + "js/" + MANIFEST_URL;
  var thumbIndexPath = assetRoot + "js/" + THUMB_INDEX_URL;

  var categories = [];
  var thumbMeta = { folders: {} };
  var lastFocus = null;
  var renderId = 0;
  var lazyObserver = null;

  var strings = {
    en: {
      photos: "photos",
      photo: "photo",
      loading: "Loading gallery…",
      error: "Could not load the photo gallery. Please refresh the page.",
      empty: "No photos in this category.",
      enlarge: "View larger image",
      close: "Close image"
    },
    az: {
      photos: "foto",
      photo: "foto",
      loading: "Qalereya yüklənir…",
      error: "Foto qalereya yüklənə bilmədi. Səhifəni yeniləyin.",
      empty: "Bu kateqoriyada foto yoxdur.",
      enlarge: "Böyük ölçüdə bax",
      close: "Şəkli bağla"
    }
  };

  function t(key) {
    var pack = strings[lang] || strings.en;
    return pack[key] || strings.en[key] || key;
  }

  function titleFor(cat) {
    if (!cat || !cat.title) return "";
    return cat.title[lang] || cat.title.en || cat.folder;
  }

  function fullUrl(folder, file) {
    return imageBase + encodeURIComponent(folder) + "/" + encodeURIComponent(file);
  }

  function thumbUrl(folder, file) {
    var stem = file.replace(/\.[^.]+$/, "");
    return thumbBase + encodeURIComponent(folder) + "/" + encodeURIComponent(stem + ".jpg");
  }

  function thumbDimensions(folder, file) {
    var folderMeta = thumbMeta.folders && thumbMeta.folders[folder];
    if (!folderMeta) return null;
    var entry = folderMeta[file];
    if (!entry || !entry.w || !entry.h) return null;
    return { w: entry.w, h: entry.h };
  }

  function hasThumbEntry(folder, file) {
    var folderMeta = thumbMeta.folders && thumbMeta.folders[folder];
    return !!(folderMeta && folderMeta[file]);
  }

  function imagesForCategory(cat) {
    var list = cat.images || [];
    if (!thumbMeta.folders || !thumbMeta.folders[cat.folder]) {
      return list;
    }
    return list.filter(function (file) {
      return hasThumbEntry(cat.folder, file);
    });
  }

  function syncCategoryCounts() {
    categories = categories.map(function (cat) {
      var images = imagesForCategory(cat);
      return Object.assign({}, cat, { images: images, count: images.length });
    });
  }

  function setStatus(msg, hidden) {
    if (!statusEl) return;
    statusEl.textContent = msg || "";
    statusEl.hidden = !!hidden;
  }

  function mobileQuery() {
    if (window.DAAB_DESIGN && typeof window.DAAB_DESIGN.sidebarStackMq === "function") {
      return window.DAAB_DESIGN.sidebarStackMq();
    }
    return window.matchMedia("(max-width: 1060px)");
  }

  function bindSidebarMobile() {
    var widget = document.querySelector(".sidebar-widget");
    var toggle = document.querySelector(".events-menu-toggle");
    if (!widget || !toggle) return;

    function closeMenu() {
      widget.classList.remove("events-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = widget.classList.toggle("events-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (!mobileQuery().matches || !widget.classList.contains("events-open")) return;
      if (widget.contains(e.target)) return;
      closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    return closeMenu;
  }

  var closeSidebarMenu = null;

  function sidebarLinks() {
    return Array.from(catList.querySelectorAll('a[href^="#gallery-"]'));
  }

  function activateLink(link) {
    sidebarLinks().forEach(function (a) {
      a.classList.remove("tl-active");
    });
    if (link) link.classList.add("tl-active");
  }

  function updateUrl(id) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set("category", id);
      url.hash = id;
      history.replaceState(null, "", url.toString());
    } catch (e) {
      /* ignore */
    }
  }

  function ensureLazyObserver() {
    if (lazyObserver || typeof IntersectionObserver === "undefined") return lazyObserver;
    lazyObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var img = entry.target;
          lazyObserver.unobserve(img);
          var src = img.getAttribute("data-thumb-src");
          if (!src || img.getAttribute("data-loaded") === "1") return;
          img.setAttribute("data-loaded", "1");
          img.src = src;
        });
      },
      { root: null, rootMargin: IO_ROOT_MARGIN, threshold: 0.01 }
    );
    return lazyObserver;
  }

  function scheduleThumbLoad(img, thumb, eager) {
    if (eager) {
      img.setAttribute("data-loaded", "1");
      img.src = thumb;
      return;
    }
    img.setAttribute("data-thumb-src", thumb);
    img.loading = "lazy";
    img.decoding = "async";
    var obs = ensureLazyObserver();
    if (obs) {
      obs.observe(img);
    } else {
      img.src = thumb;
    }
  }

  function openLightbox(fullSrc, alt) {
    if (!lightbox || !lightboxImg) return;
    lastFocus = document.activeElement;
    lightboxImg.removeAttribute("src");
    lightboxImg.alt = alt || "";
    lightboxImg.classList.add("is-loading");
    if (lightboxCaption) lightboxCaption.textContent = alt || "";
    lightbox.classList.add("open", "is-loading-view");
    lightbox.setAttribute("aria-hidden", "false");

    var loader = new Image();
    loader.onload = function () {
      lightboxImg.src = fullSrc;
      lightboxImg.classList.remove("is-loading");
      lightbox.classList.remove("is-loading-view");
    };
    loader.onerror = function () {
      lightboxImg.classList.remove("is-loading");
      lightbox.classList.remove("is-loading-view");
      if (lightboxCaption) {
        lightboxCaption.textContent = (alt || "") + " — " + t("error");
      }
    };
    loader.src = fullSrc;

    if (lightboxClose) lightboxClose.focus();
  }

  function closeLightbox() {
    if (!lightbox || !lightboxImg) return;
    lightbox.classList.remove("open", "is-loading-view");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImg.removeAttribute("src");
    lightboxImg.classList.remove("is-loading");
    lightboxImg.alt = "";
    if (lightboxCaption) lightboxCaption.textContent = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function disconnectLazyObserver() {
    if (lazyObserver) {
      lazyObserver.disconnect();
    }
  }

  function renderAllImages(cat, activeRenderId) {
    var label = titleFor(cat);
    var frag = document.createDocumentFragment();

    var images = imagesForCategory(cat);
    images.forEach(function (file, i) {
      var full = fullUrl(cat.folder, file);
      var thumb = thumbUrl(cat.folder, file);
      var alt = label + " — " + (i + 1);
      var dims = thumbDimensions(cat.folder, file);
      var eager = i < EAGER_COUNT;

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "photos-gallery-item";
      btn.setAttribute("aria-label", t("enlarge") + ": " + alt);

      var img = document.createElement("img");
      img.alt = alt;
      img.className = "photos-gallery-thumb";
      img.sizes = "(max-width: 600px) 42vw, 168px";
      if (dims) {
        img.width = dims.w;
        img.height = dims.h;
      }
      img.addEventListener("error", function onImgErr() {
        if (activeRenderId !== renderId) return;
        btn.classList.add("photos-gallery-item--failed");
        btn.disabled = true;
        btn.setAttribute("aria-disabled", "true");
      });

      scheduleThumbLoad(img, thumb, eager);

      btn.appendChild(img);
      btn.addEventListener("click", function () {
        openLightbox(full, alt);
      });
      frag.appendChild(btn);
    });

    grid.appendChild(frag);
  }

  function renderCategory(cat, link) {
    if (!cat) return;
    renderId += 1;
    var activeRenderId = renderId;
    disconnectLazyObserver();
    lazyObserver = null;
    activateLink(link);
    updateUrl(cat.id);

    if (titleEl) titleEl.textContent = titleFor(cat);
    var images = imagesForCategory(cat);
    var n = images.length;
    if (countEl) {
      countEl.textContent = n + " " + (n === 1 ? t("photo") : t("photos"));
    }

    grid.innerHTML = "";

    if (!n) {
      setStatus(t("empty"), false);
      return;
    }
    setStatus("", true);
    grid.setAttribute("data-gallery-id", cat.id);
    grid.setAttribute("data-gallery-folder", cat.folder);
    renderAllImages(Object.assign({}, cat, { images: images }), activeRenderId);

    if (closeSidebarMenu && mobileQuery().matches) {
      closeSidebarMenu();
    }

    var panel = document.getElementById("photos-gallery-panel");
    if (panel) {
      panel.scrollIntoView({ block: "start", behavior: "smooth" });
    }
  }

  function selectCategory(id) {
    var cat = categories.find(function (c) {
      return c.id === id;
    });
    var link = catList.querySelector('a[href="#' + id + '"]');
    if (cat) renderCategory(cat, link);
  }

  function buildSidebar() {
    catList.innerHTML = "";
    categories.forEach(function (cat) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + cat.id;
      a.textContent = titleFor(cat);

      a.addEventListener("click", function (e) {
        e.preventDefault();
        renderCategory(cat, a);
      });

      li.appendChild(a);
      catList.appendChild(li);
    });
  }

  function categoryIdFromHash() {
    var hash = (window.location.hash || "").replace(/^#/, "");
    if (!hash) return null;
    if (categories.some(function (c) {
      return c.id === hash;
    })) {
      return hash;
    }
    return null;
  }

  function initialCategoryId() {
    try {
      var fromHash = categoryIdFromHash();
      if (fromHash) return fromHash;

      var url = new URL(window.location.href);
      var fromUrl = url.searchParams.get("category");
      if (fromUrl) {
        if (categories.some(function (c) {
          return c.id === fromUrl;
        })) {
          return fromUrl;
        }
        var legacy = categories.find(function (c) {
          return c.folder === fromUrl;
        });
        if (legacy) return legacy.id;
      }
    } catch (e) {
      /* ignore */
    }
    return categories.length ? categories[0].id : null;
  }

  function initLightbox() {
    if (!lightbox) return;
    lightbox.setAttribute("aria-hidden", "true");
    if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && lightbox.classList.contains("open")) {
        e.preventDefault();
        closeLightbox();
      }
    });
  }

  function loadJson(url) {
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error(url + " " + res.status);
      return res.json();
    });
  }

  setStatus(t("loading"), false);

  Promise.all([
    loadJson(manifestPath + "?v=7"),
    loadJson(thumbIndexPath + "?v=4").catch(function () {
      return { folders: {} };
    })
  ])
    .then(function (results) {
      var data = results[0];
      thumbMeta = results[1] || { folders: {} };
      categories = (data.categories || []).slice().sort(function (a, b) {
        return (a.order || 0) - (b.order || 0);
      });
      syncCategoryCounts();
      if (!categories.length) {
        setStatus(t("empty"), false);
        return;
      }
      buildSidebar();
      initLightbox();
      closeSidebarMenu = bindSidebarMobile();
      var start = initialCategoryId();
      if (start) selectCategory(start);
      window.addEventListener("hashchange", function () {
        var id = categoryIdFromHash();
        if (id) selectCategory(id);
      });
      setStatus("", true);
    })
    .catch(function () {
      setStatus(t("error"), false);
    });
})();
