/**
 * Text-to-speech for forum story cards (Web Speech API).
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
      group: "Hekayə səsləndirməsi",
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
      group: "Story audio",
      playing: "Reading story aloud",
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
    story: null,
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

  function findAzVoice(voices) {
    for (var i = 0; i < voices.length; i++) {
      var name = (voices[i].name || "").toLowerCase();
      var code = (voices[i].lang || "").toLowerCase();
      if (name.indexOf("babek") >= 0 && code.indexOf("az") === 0) return voices[i];
    }
    for (var j = 0; j < voices.length; j++) {
      var n2 = (voices[j].name || "").toLowerCase();
      var c2 = (voices[j].lang || "").toLowerCase();
      if (c2.indexOf("az") === 0) return voices[j];
      if (n2.indexOf("banu") >= 0 && c2.indexOf("az") === 0) return voices[j];
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
        for (var k = 0; k < voices.length; k++) {
          if ((voices[k].lang || "").toLowerCase().indexOf(prefs[p]) === 0) {
            chosen = voices[k];
            break;
          }
        }
      }
    }
    voiceCache[cacheKey] = chosen;
    return chosen;
  }

  var CH_LOW = "\uE000";
  var CH_UP = "\uE001";
  var EN_C_WORDS =
    /^(Case|Canada|Clinical|Center|Centre|Computer|Conference|Cross|Culture|Current|Clarivate|Clinical)/i;

  function isLikelyEnglishToken(word) {
    if (!word || /[əğıöüşç]/.test(word)) return false;
    if (/^[Cc][aəeıioöuüAƏEİIOÖUÜ]/.test(word) && !EN_C_WORDS.test(word)) return false;
    if (/^[A-Z]{2,5}$/.test(word)) return true;
    if (/^(Ph\.?D|Dr\.?|Prof\.?)$/i.test(word)) return true;
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

  function normalizeBroadcastAz(text) {
    return (text || "")
      .split(/(\s+|[^\s\w\u00C0-\u024F\u0400-\u04FF]+)/)
      .map(function (part) {
        if (!part || /^\s+$/.test(part) || /^[^\w\u00C0-\u024F\u0400-\u04FF]+$/.test(part)) {
          return part;
        }
        return fixAzCInWord(part);
      })
      .join("")
      .replace(/\s+/g, " ")
      .replace(/\u2019/g, "'")
      .trim();
  }

  function normalizeSpeechText(text) {
    if (!text) return "";
    if (lang() === "az") return normalizeBroadcastAz(text);
    return text.replace(/\s+/g, " ").trim();
  }

  function storyTitle(story) {
    var el = story.querySelector(".card-header .card-title");
    return el ? el.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function storyTextBlocks(story) {
    var blocks = [];
    var title = storyTitle(story);
    if (title) blocks.push(title);
    var body = story.querySelector(".card-body");
    if (!body) return blocks;
    var nodes = body.querySelectorAll(
      "p.card-text, blockquote.card-quote p, blockquote.card-quote footer"
    );
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i].textContent.replace(/\s+/g, " ").trim();
      if (t) blocks.push(t);
    }
    return blocks;
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
      /\bABŞ\b/gi,
      /\bSSRİ\b/gi,
      /\bTNK-bp\b/gi,
      /\betc\.?\b/gi,
      /\b və s\.?\b/gi,
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

  function buildSpeechQueue(story) {
    var blocks = storyTextBlocks(story);
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
    var live = document.getElementById("story-tts-live");
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
    document.querySelectorAll(".forum-story-card .card-tts-btn").forEach(function (btn) {
      btn.classList.remove("is-playing", "is-paused");
      var story = btn.closest(".forum-story-card");
      if (story) story.classList.remove("is-tts-active");
      var L = labels();
      btn.innerHTML = ICONS.play + '<span class="card-tts-label">' + L.play + "</span>";
      btn.setAttribute("aria-label", L.play);
      btn.setAttribute("aria-pressed", "false");
    });
    document.querySelectorAll(".forum-story-card .card-tts-stop").forEach(function (btn) {
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
    if (session.story) session.story.classList.remove("is-tts-active");
    session.story = null;
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
    if (session.cancelled || !session.story) {
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

  function beginSpeech(story, playBtn, stopBtn, voices) {
    var queue = buildSpeechQueue(story);
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
    session.story = story;
    session.playBtn = playBtn;
    session.stopBtn = stopBtn;
    session.state = "playing";
    session.queue = queue;
    session.index = 0;
    story.classList.add("is-tts-active");
    updateButtonUi();
    setStatus(labels().playing + ": " + storyTitle(story), false);
    speakNext(voices);
  }

  function startStory(story, playBtn, stopBtn) {
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
      beginSpeech(story, playBtn, stopBtn, voices);
    });
  }

  function togglePlay(story, playBtn, stopBtn) {
    if (!supportsTts()) {
      setStatus(labels().unsupported, true);
      return;
    }
    if (session.story === story && session.state === "playing") {
      clearPauseTimer();
      global.speechSynthesis.pause();
      session.state = "paused";
      updateButtonUi();
      setStatus(labels().paused, false);
      return;
    }
    if (session.story === story && session.state === "paused") {
      primeSpeechEngine();
      global.speechSynthesis.resume();
      session.state = "playing";
      updateButtonUi();
      setStatus(labels().playing + ": " + storyTitle(story), false);
      return;
    }
    if (session.story && session.story !== story) stopAll();
    startStory(story, playBtn, stopBtn);
  }

  function buildControls(story) {
    var figure = story.querySelector(".forum-story-figure");
    if (!figure || figure.querySelector(".card-tts")) return;
    var img = figure.querySelector("img");
    if (!img) return;

    var caption = figure.querySelector(".forum-story-caption");
    if (caption) caption.remove();

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
      togglePlay(story, playBtn, stopBtn);
    });
    stopBtn.addEventListener("click", function () {
      if (session.story === story) stopAll();
    });

    wrap.appendChild(playBtn);
    wrap.appendChild(stopBtn);
    img.insertAdjacentElement("afterend", wrap);
  }

  function ensureLiveRegion() {
    if (document.getElementById("story-tts-live")) return;
    var live = document.createElement("div");
    live.id = "story-tts-live";
    live.className = "card-tts-status";
    live.setAttribute("aria-live", "polite");
    live.setAttribute("aria-atomic", "true");
    document.body.appendChild(live);
  }

  function init() {
    if (!document.querySelector("article.forum-story-card")) return;
    ensureLiveRegion();
    if (supportsTts()) {
      waitForVoices(100);
      global.speechSynthesis.addEventListener("voiceschanged", function () {
        voiceCache = {};
      });
    }
    var stories = document.querySelectorAll("article.forum-story-card");
    for (var i = 0; i < stories.length; i++) buildControls(stories[i]);
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

  global.DAAB_STORY_TTS = { stopAll: stopAll };
})(typeof window !== "undefined" ? window : this);
