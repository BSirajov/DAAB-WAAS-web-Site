/**
 * Load scientist profile data from chunked JSON (manifest) with monolithic fallback.
 */
(function (window) {
  "use strict";

  function joinUrl(prefix, relPath) {
    var base = String(prefix || "");
    if (base && !base.endsWith("/")) base += "/";
    return base + String(relPath || "").replace(/^\//, "");
  }

  function parseProfilesPayload(data) {
    if (!data) return [];
    if (Array.isArray(data.profiles)) return data.profiles;
    return [];
  }

  function loadMonolithic(prefix) {
    return fetch(joinUrl(prefix, "i18n/scientists-profiles.json"), {
      credentials: "same-origin",
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    });
  }

  function loadChunked(prefix, manifest) {
    var chunks = (manifest && manifest.chunks) || [];
    if (!chunks.length) return loadMonolithic(prefix);
    return Promise.all(
      chunks.map(function (name) {
        return fetch(joinUrl(prefix, "i18n/scientists-profiles/" + name), {
          credentials: "same-origin",
        }).then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        });
      })
    ).then(function (parts) {
      var profiles = [];
      parts.forEach(function (part) {
        profiles = profiles.concat(parseProfilesPayload(part));
      });
      return { version: manifest.version, profiles: profiles };
    });
  }

  function load(prefix) {
    var manifestUrl = joinUrl(prefix, "i18n/scientists-profiles/manifest.json");
    return fetch(manifestUrl, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) return loadMonolithic(prefix);
        return res.json().then(function (manifest) {
          return loadChunked(prefix, manifest);
        });
      })
      .catch(function () {
        return loadMonolithic(prefix);
      });
  }

  window.DAAB_SCIENTISTS_PROFILES_LOADER = {
    load: load,
  };
})(window);
