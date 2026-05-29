/**
 * Text-to-speech for scientist profile cards (Web Speech API).
 */
(function (global) {
  "use strict";

  var ICONS = {
    play:
      '<svg class="card-tts-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">' +
      '<path d="M11 5L6 9H3v6h3l5 4V5z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>' +
      '<path d="M15.5 8.5a5 5 0 010 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
      '<path d="M17.8 6.2a8.5 8.5 0 010 11.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
      "</svg>",
    pause:
      '<svg class="card-tts-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">' +
      '<rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/>' +
      '<rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/>' +
      "</svg>",
    stop:
      '<svg class="card-tts-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">' +
      '<rect x="6" y="6" width="12" height="12" rx="1.5" fill="currentColor"/>' +
      "</svg>"
  };

  var LABELS = {
    az: {
      play: "Dinlə",
      pause: "Pauza",
      resume: "Davam et",
      stop: "Dayandır",
      group: "Profil səsləndirməsi",
      playing: "Oxunur",
      paused: "Pauza edilib",
      stopped: "Oxunuş dayandırıldı",
      loading: "Səs yüklənir…",
      unsupported:
        "Brauzeriniz səsləndirməni dəstəkləmir. Microsoft Edge tövsiyə olunur.",
      noAzVoice:
        "Azərbaycan səsi tapılmadı. Microsoft Edge ilə açın və ya az-AZ səs paketi quraşdırın.",
      empty: "Oxunacaq mətn tapılmadı."
    },
    en: {
      play: "Listen",
      pause: "Pause",
      resume: "Resume",
      stop: "Stop",
      group: "Profile audio",
      playing: "Reading profile aloud",
      paused: "Playback paused",
      stopped: "Playback stopped",
      loading: "Loading voice…",
      unsupported: "Text-to-speech is not supported in this browser",
      empty: "No text to read."
    }
  };

  var voiceCache = {};
  var PARAGRAPH_PAUSE_MS = 2000;
  var SENTENCE_PAUSE_MS = 850;
  var TITLE_BRIDGE_PAUSE_MS = 2500;
  var ABBR_TOKEN = "\uE010";
  var abbrMap = {};
  var session = {
    card: null,
    playBtn: null,
    stopBtn: null,
    state: "idle",
    queue: [],
    index: 0,
    cancelled: false,
    pauseTimer: null,
    voices: null
  };

  function lang() {
    var l = document.documentElement.lang || "az";
    return l.indexOf("en") === 0 ? "en" : "az";
  }

  function labels() {
    return LABELS[lang()] || LABELS.az;
  }

  function speechLang() {
    return lang() === "en" ? "en-US" : "az-AZ";
  }

  function supportsTts() {
    return !!(global.speechSynthesis && global.SpeechSynthesisUtterance);
  }

  function getVoicesList() {
    if (!supportsTts()) return [];
    return global.speechSynthesis.getVoices() || [];
  }

  function waitForVoices(timeoutMs) {
    timeoutMs = timeoutMs || 2500;
    return new Promise(function (resolve) {
      var voices = getVoicesList();
      if (voices.length) {
        resolve(voices);
        return;
      }
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        resolve(getVoicesList());
      }
      var timer = global.setTimeout(finish, timeoutMs);
      function onVoices() {
        global.clearTimeout(timer);
        global.speechSynthesis.removeEventListener("voiceschanged", onVoices);
        finish();
      }
      global.speechSynthesis.addEventListener("voiceschanged", onVoices);
      global.speechSynthesis.getVoices();
    });
  }

  function findBabekVoice(voices) {
    for (var i = 0; i < voices.length; i++) {
      var name = (voices[i].name || "").toLowerCase();
      var code = (voices[i].lang || "").toLowerCase();
      if (name.indexOf("babek") >= 0 && code.indexOf("az") === 0) return voices[i];
    }
    return null;
  }

  function findAzVoice(voices) {
    var babek = findBabekVoice(voices);
    if (babek) return babek;
    for (var i = 0; i < voices.length; i++) {
      var name = (voices[i].name || "").toLowerCase();
      var code = (voices[i].lang || "").toLowerCase();
      if (code.indexOf("az") === 0) return voices[i];
      if (name.indexOf("banu") >= 0 && code.indexOf("az") === 0) return voices[i];
    }
    return null;
  }

  function pickVoice(code, voices) {
    voices = voices || getVoicesList();
    var cacheKey = code + "|" + voices.length;
    if (voiceCache[cacheKey]) return voiceCache[cacheKey];

    var chosen = null;
    if (code.indexOf("az") === 0) {
      chosen = findAzVoice(voices);
    } else {
      var prefs = ["en-us", "en-gb", "en"];
      for (var p = 0; p < prefs.length && !chosen; p++) {
        for (var j = 0; j < voices.length; j++) {
          if ((voices[j].lang || "").toLowerCase().indexOf(prefs[p]) === 0) {
            chosen = voices[j];
            break;
          }
        }
      }
    }
    voiceCache[cacheKey] = chosen;
    return chosen;
  }

  function isEmailMetaRow(row) {
    if (!row) return false;
    if (row.querySelector(".card-email, .card-email--empty")) return true;
    var label = row.querySelector(".card-meta-label");
    if (!label) return false;
    var t = label.textContent.replace(/\s+/g, " ").trim().toLowerCase();
    return t === "e-poçt:" || t === "e-poct:" || t === "email:";
  }

  var CH_LOW = "\uE000";
  var CH_UP = "\uE001";
  var EN_C_WORDS =
    /^(Case|Canada|Clinical|Center|Centre|Computer|Conference|Cross|Culture|Current|Clarivate|Clinical)/i;

  function isLikelyEnglishToken(word) {
    if (!word || /[əğıöüşç]/.test(word)) return false;
    if (/^[Cc][aəeıioöuüAƏEİIOÖUÜ]/.test(word) && !EN_C_WORDS.test(word)) return false;
    if (/^[A-Z]{2,5}$/.test(word)) return true;
    if (/^(Ph\.?D|Dr\.?|Prof\.?|Case|Western|Reserve|Staff|Google|Microsoft)$/i.test(word)) {
      return true;
    }
    return /^[A-Za-z][A-Za-z.\-']*$/.test(word);
  }

  function shouldFixAzC(word) {
    if (!word) return false;
    if (/[əğıöüşç]/.test(word)) return true;
    if (/^[Cc][aəeıioöuüAƏEİIOÖUÜ]/.test(word) && !EN_C_WORDS.test(word)) return true;
    if (isLikelyEnglishToken(word)) return false;
    return false;
  }

  function fixAzCInWord(word) {
    if (!shouldFixAzC(word)) return word;
    return word
      .replace(/ç/g, CH_LOW)
      .replace(/Ç/g, CH_UP)
      .replace(/c(?=[aəeıioöuüAƏEİIOÖUÜ])/g, "dj")
      .replace(/C(?=[aəeıioöuüAƏEİIOÖUÜ])/g, "Dj")
      .replace(new RegExp(CH_LOW, "g"), "ç")
      .replace(new RegExp(CH_UP, "g"), "Ç");
  }

  function fixStandardAzC(text) {
    return text
      .split(/(\s+|[^\s\w\u00C0-\u024F\u0400-\u04FF]+)/)
      .map(function (part) {
        if (!part || /^\s+$/.test(part) || /^[^\w\u00C0-\u024F\u0400-\u04FF]+$/.test(part)) {
          return part;
        }
        return fixAzCInWord(part);
      })
      .join("");
  }

  function normalizeBroadcastAz(text) {
    return fixStandardAzC(
      (text || "")
        .replace(/\s+/g, " ")
        .replace(/\u2019/g, "'")
        .trim()
    );
  }

  function cardName(card) {
    var el = card.querySelector(".card-name");
    if (!el) return "";
    var clone = el.cloneNode(true);
    var creds = clone.querySelectorAll(".cred");
    for (var i = 0; i < creds.length; i++) creds[i].remove();
    return clone.textContent.replace(/\s+/g, " ").trim();
  }

  function cardHeaderBlocks(card) {
    var blocks = [];
    var name = cardName(card);
    if (name) blocks.push(name);

    var country = card.querySelector(".card-country");
    if (country) blocks.push(country.textContent.replace(/\s+/g, " ").trim());

    var title = card.querySelector(".card-title");
    if (title) blocks.push(title.textContent.replace(/\s+/g, " ").trim());

    var rows = card.querySelectorAll(".card-meta-row");
    for (var i = 0; i < rows.length; i++) {
      if (isEmailMetaRow(rows[i])) continue;
      blocks.push(rows[i].textContent.replace(/\s+/g, " ").trim());
    }
    return blocks.filter(Boolean);
  }

  function endsLikeSentence(text) {
    return /[.!?…]$/.test(String(text || "").trim());
  }

  function protectAbbreviations(text) {
    abbrMap = {};
    var tokenIdx = 0;
    var patterns = [
      /\bProf\.?\s*Dr\.?\b/gi,
      /\bPh\.?\s*D\.?\b/gi,
      /\bDr\.?\b/gi,
      /\bEd\.?\s*D\.?\b/gi,
      /\bMr\.?\b/gi,
      /\bMrs\.?\b/gi,
      /\bMs\.?\b/gi,
      /\bB\.?\s*A\.?\b/gi,
      /\bM\.?\s*A\.?\b/gi,
      /\bM\.?\s*Sc\.?\b/gi,
      /\bISBN\b/gi,
      /\bTRT\b/gi,
      /\bAAAS\b/gi,
      /\bABŞ\b/gi,
      /\bSSRİ\b/gi,
      /\bUNİCEF\b/gi,
      /\bScopus\b/gi,
      /\bWeb of Science\b/gi,
      /\betc\.?\b/gi,
      /\b və s\.?\b/gi,
      /\b e\.?\s*c\.?\b/gi,
      /\b i\.?\s*e\.?\b/gi,
      /\b\d+\.\d+\b/g
    ];
    var out = text;
    for (var p = 0; p < patterns.length; p++) {
      out = out.replace(patterns[p], function (match) {
        var token = ABBR_TOKEN + tokenIdx + ABBR_TOKEN;
        abbrMap[tokenIdx] = match;
        tokenIdx += 1;
        return token;
      });
    }
    return out;
  }

  function restoreAbbreviations(text) {
    return text.replace(
      new RegExp(ABBR_TOKEN + "(\\d+)" + ABBR_TOKEN, "g"),
      function (_, idx) {
        return abbrMap[idx] != null ? abbrMap[idx] : "";
      }
    );
  }

  function splitIntoSentences(text) {
    if (!text) return [];
    var protectedText = protectAbbreviations(text);
    var parts = protectedText.match(/[^.!?…]+[.!?…]+|[^.!?…]+$/g);
    if (!parts) {
      var single = text.trim();
      return single ? [single] : [];
    }
    var sentences = [];
    for (var i = 0; i < parts.length; i++) {
      var restored = restoreAbbreviations(parts[i]).replace(/\s+/g, " ").trim();
      if (restored) sentences.push(restored);
    }
    return sentences;
  }

  function cardBioParagraphs(card) {
    var bio = card.querySelector(".card-bio");
    if (!bio) return [];
    var nodes = bio.querySelectorAll(
      "p.bio, p.bio-lead, p.bio-section-title, p[class*='bio']"
    );
    var out = [];
    if (nodes.length) {
      for (var i = 0; i < nodes.length; i++) {
        var t = nodes[i].textContent.replace(/\s+/g, " ").trim();
        if (t) out.push(t);
      }
      return out;
    }
    var fallback = bio.textContent.replace(/\s+/g, " ").trim();
    return fallback ? [fallback] : [];
  }

  function normalizeSpeechText(text) {
    if (!text) return "";
    if (lang() === "az") return normalizeBroadcastAz(text);
    return text;
  }

  function buildSpeechQueue(card) {
    var blocks = cardHeaderBlocks(card).concat(cardBioParagraphs(card));
    var queue = [];
    var isFirst = true;
    var lastSpoken = "";

    for (var b = 0; b < blocks.length; b++) {
      var normalized = normalizeSpeechText(blocks[b]);
      var sentences = splitIntoSentences(normalized);
      if (!sentences.length) continue;

      if (!isFirst) {
        var blockPause =
          lastSpoken && !endsLikeSentence(lastSpoken)
            ? TITLE_BRIDGE_PAUSE_MS
            : PARAGRAPH_PAUSE_MS;
        queue.push({ type: "pause", ms: blockPause });
      }

      for (var s = 0; s < sentences.length; s++) {
        if (!isFirst && s > 0) {
          queue.push({ type: "pause", ms: SENTENCE_PAUSE_MS });
        }
        queue.push({ type: "speech", text: sentences[s] });
        lastSpoken = sentences[s];
        isFirst = false;
      }
    }
    return queue;
  }

  function setStatus(msg, isError) {
    var live = document.getElementById("profile-tts-live");
    if (!live) return;
    live.textContent = msg || "";
    live.classList.toggle("is-error", !!isError);
    live.classList.toggle("is-visible", !!msg);
  }

  function updateButtonUi() {
    if (!session.playBtn) return;
    var L = labels();
    if (session.state === "playing") {
      session.playBtn.classList.add("is-playing");
      session.playBtn.classList.remove("is-paused");
      session.playBtn.innerHTML = ICONS.pause + '<span class="card-tts-label">' + L.pause + "</span>";
      session.playBtn.setAttribute("aria-label", L.pause);
      session.playBtn.setAttribute("aria-pressed", "true");
    } else if (session.state === "paused") {
      session.playBtn.classList.remove("is-playing");
      session.playBtn.classList.add("is-paused");
      session.playBtn.innerHTML = ICONS.play + '<span class="card-tts-label">' + L.resume + "</span>";
      session.playBtn.setAttribute("aria-label", L.resume);
      session.playBtn.setAttribute("aria-pressed", "true");
    } else {
      session.playBtn.classList.remove("is-playing", "is-paused");
      session.playBtn.innerHTML = ICONS.play + '<span class="card-tts-label">' + L.play + "</span>";
      session.playBtn.setAttribute("aria-label", L.play);
      session.playBtn.setAttribute("aria-pressed", "false");
    }
    if (session.stopBtn) session.stopBtn.hidden = session.state === "idle";
  }

  function resetButtonUi() {
    document.querySelectorAll(".card-tts-btn").forEach(function (btn) {
      btn.classList.remove("is-playing", "is-paused");
      var card = btn.closest(".card");
      if (card) card.classList.remove("is-tts-active");
      var L = labels();
      btn.innerHTML = ICONS.play + '<span class="card-tts-label">' + L.play + "</span>";
      btn.setAttribute("aria-label", L.play);
      btn.setAttribute("aria-pressed", "false");
    });
    document.querySelectorAll(".card-tts-stop").forEach(function (btn) {
      btn.hidden = true;
    });
  }

  function clearPauseTimer() {
    if (session.pauseTimer) {
      global.clearTimeout(session.pauseTimer);
      session.pauseTimer = null;
    }
  }

  function cancelSpeechEngine() {
    if (!supportsTts()) return;
    session.cancelled = true;
    clearPauseTimer();
    try {
      global.speechSynthesis.cancel();
    } catch (e) { /* ignore */ }
  }

  function resetSession() {
    if (session.card) session.card.classList.remove("is-tts-active");
    session.card = null;
    session.playBtn = null;
    session.stopBtn = null;
    session.state = "idle";
    session.queue = [];
    session.index = 0;
    session.cancelled = false;
    session.voices = null;
    clearPauseTimer();
    resetButtonUi();
  }

  function stopAll() {
    cancelSpeechEngine();
    resetSession();
    setStatus(labels().stopped, false);
  }

  function primeSpeechEngine() {
    if (!supportsTts()) return;
    if (global.speechSynthesis.paused) {
      try {
        global.speechSynthesis.resume();
      } catch (e) { /* ignore */ }
    }
  }

  function speakNext(voices) {
    voices = voices || session.voices || getVoicesList();
    if (session.cancelled || !session.card) {
      resetSession();
      return;
    }
    if (session.index >= session.queue.length) {
      cancelSpeechEngine();
      resetSession();
      setStatus(labels().stopped, false);
      return;
    }

    var item = session.queue[session.index];
    if (item && item.type === "pause") {
      clearPauseTimer();
      session.pauseTimer = global.setTimeout(function () {
        session.pauseTimer = null;
        if (session.cancelled) return;
        session.index += 1;
        speakNext(voices);
      }, item.ms || PARAGRAPH_PAUSE_MS);
      return;
    }

    var chunk = item && item.text ? item.text : "";
    if (!chunk.trim()) {
      session.index += 1;
      speakNext(voices);
      return;
    }

    var utter = new global.SpeechSynthesisUtterance(chunk);
    var code = speechLang();
    utter.lang = code;
    var voice = pickVoice(code, voices);
    if (code.indexOf("az") === 0 && !voice) {
      setStatus(labels().noAzVoice, true);
      stopAll();
      return;
    }
    if (voice) utter.voice = voice;
    utter.rate = code.indexOf("az") === 0 ? 0.94 : 1;
    utter.pitch = 1;
    utter.volume = 1;

    utter.onstart = function () {
      if (session.playBtn) updateButtonUi();
    };
    utter.onend = function () {
      if (session.cancelled) return;
      session.index += 1;
      speakNext(voices);
    };
    utter.onerror = function (ev) {
      if (session.cancelled) return;
      if (ev && ev.error === "interrupted") return;
      setStatus(labels().noAzVoice, true);
      stopAll();
    };

    primeSpeechEngine();
    global.speechSynthesis.speak(utter);
  }

  function beginSpeech(card, playBtn, stopBtn, voices) {
    var queue = buildSpeechQueue(card);
    if (!queue.length) {
      setStatus(labels().empty, true);
      return;
    }

    var code = speechLang();
    if (code.indexOf("az") === 0 && !findAzVoice(voices)) {
      setStatus(labels().noAzVoice, true);
      return;
    }

    cancelSpeechEngine();
    session.cancelled = false;
    session.voices = voices;
    session.card = card;
    session.playBtn = playBtn;
    session.stopBtn = stopBtn;
    session.state = "playing";
    session.queue = queue;
    session.index = 0;
    card.classList.add("is-tts-active");
    updateButtonUi();
    setStatus(labels().playing + ": " + cardName(card), false);
    speakNext(voices);
  }

  function startCard(card, playBtn, stopBtn) {
    if (!supportsTts()) {
      setStatus(labels().unsupported, true);
      return;
    }
    setStatus(labels().loading, false);
    voiceCache = {};
    waitForVoices(3000).then(function (voices) {
      if (!voices.length && lang() === "az") {
        setStatus(labels().noAzVoice, true);
        return;
      }
      beginSpeech(card, playBtn, stopBtn, voices);
    });
  }

  function togglePlay(card, playBtn, stopBtn) {
    if (!supportsTts()) {
      setStatus(labels().unsupported, true);
      return;
    }
    if (session.card === card && session.state === "playing") {
      clearPauseTimer();
      global.speechSynthesis.pause();
      session.state = "paused";
      updateButtonUi();
      setStatus(labels().paused, false);
      return;
    }
    if (session.card === card && session.state === "paused") {
      primeSpeechEngine();
      global.speechSynthesis.resume();
      session.state = "playing";
      updateButtonUi();
      setStatus(labels().playing + ": " + cardName(card), false);
      return;
    }
    if (session.card && session.card !== card) stopAll();
    startCard(card, playBtn, stopBtn);
  }

  function buildControls(card) {
    if (card.querySelector(".card-tts")) return;
    var L = labels();
    var wrap = document.createElement("div");
    wrap.className = "card-tts";
    wrap.setAttribute("role", "group");
    wrap.setAttribute("aria-label", L.group);

    var playBtn = document.createElement("button");
    playBtn.type = "button";
    playBtn.className = "card-tts-btn";
    playBtn.innerHTML = ICONS.play + '<span class="card-tts-label">' + L.play + "</span>";
    playBtn.setAttribute("aria-label", L.play);
    playBtn.setAttribute("aria-pressed", "false");

    var stopBtn = document.createElement("button");
    stopBtn.type = "button";
    stopBtn.className = "card-tts-stop";
    stopBtn.innerHTML = ICONS.stop;
    stopBtn.setAttribute("aria-label", L.stop);
    stopBtn.hidden = true;

    playBtn.addEventListener("click", function () {
      togglePlay(card, playBtn, stopBtn);
    });
    stopBtn.addEventListener("click", function () {
      if (session.card === card) stopAll();
    });

    wrap.appendChild(playBtn);
    wrap.appendChild(stopBtn);

    var listenLead = (card.getAttribute("data-listen-lead") || "").trim();
    var listenLeadEl = null;
    if (listenLead) {
      listenLeadEl = document.createElement("p");
      listenLeadEl.className = "card-listen-lead";
      listenLeadEl.textContent = listenLead;
    }

    var bio = card.querySelector(".card-bio");
    var meta = card.querySelector(".card-meta");
    if (meta && meta.parentNode) {
      var parent = meta.parentNode;
      parent.insertBefore(wrap, bio || meta.nextSibling);
      if (listenLeadEl) parent.insertBefore(listenLeadEl, bio || wrap.nextSibling);
    } else {
      var body = card.querySelector(".card-body");
      if (body) {
        body.appendChild(wrap);
        if (listenLeadEl) body.appendChild(listenLeadEl);
      }
    }
  }

  function initCards() {
    var grid = document.querySelector("#scientists-catalog .cards-grid");
    if (!grid) return;
    var cards = grid.querySelectorAll(".card");
    for (var i = 0; i < cards.length; i++) buildControls(cards[i]);
  }

  function watchFilteredCards() {
    var grid = document.querySelector("#scientists-catalog .cards-grid");
    if (!grid || !global.MutationObserver) return;
    var observer = new MutationObserver(function () {
      if (!session.card) return;
      if (session.card.classList.contains("is-filtered-out")) stopAll();
    });
    observer.observe(grid, {
      attributes: true,
      attributeFilter: ["class"],
      subtree: true
    });
  }

  function ensureLiveRegion() {
    if (document.getElementById("profile-tts-live")) return;
    var live = document.createElement("div");
    live.id = "profile-tts-live";
    live.className = "card-tts-status";
    live.setAttribute("aria-live", "polite");
    live.setAttribute("aria-atomic", "true");
    document.body.appendChild(live);
  }

  function init() {
    if (!document.querySelector("#scientists-catalog .cards-grid")) return;
    ensureLiveRegion();
    if (supportsTts()) {
      waitForVoices(100);
      global.speechSynthesis.addEventListener("voiceschanged", function () {
        voiceCache = {};
      });
    }
    initCards();
    watchFilteredCards();
    document.addEventListener("visibilitychange", function () {
      if (document.hidden && session.state === "playing") {
        global.speechSynthesis.pause();
        session.state = "paused";
        updateButtonUi();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  global.DAAB_PROFILE_TTS = { stopAll: stopAll };
})(typeof window !== "undefined" ? window : this);
