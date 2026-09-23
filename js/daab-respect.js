/**
 * Shared respectful-language check for every form that sends visitor text.
 * The word lists live in i18n/feedback-language.json so the browser and PHP stay aligned.
 */
(function (root) {
  "use strict";

  var LEET = { "@": "a", "0": "o", "1": "i", "3": "e", "$": "s", "5": "s", "4": "a", "7": "t", "!": "i" };
  var MESSAGE = {
    az: "Zəhmət olmasa, nəzakətli ifadələrdən istifadə edin. Göndərməzdən əvvəl işarələnmiş xanadakı təhqiramiz və ya nalayiq ifadələri düzəldin.",
    en: "Please use respectful language. Review the highlighted field and remove any offensive or abusive wording before submitting."
  };
  var FORMS = { mainForm: 1, forumRegisterForm: 1, feedbackForm: 1, ctApplyForm: 1 };
  var NAME_RE = /^(name|surname|fathername|father_name|first_name|last_name|given-name|given_name|full_name|member2-name|member2_name|member3-name|member3_name)$/i;
  var model = null;
  var state = "loading";

  function charsOf(value) {
    var out = [];
    for (var i = 0; i < value.length;) {
      var cp = value.codePointAt(i);
      var ch = String.fromCodePoint(cp);
      out.push(ch);
      i += ch.length;
    }
    return out;
  }

  function foldChar(ch) {
    if (ch === "İ") return "i";
    var lower = ch.toLowerCase();
    return lower.length === 1 ? lower : ch;
  }

  function foldString(value) {
    return charsOf(value).map(foldChar).join("");
  }

  function isWordChar(ch) {
    return /[\p{L}\p{N}_]/u.test(ch || "");
  }

  function uniqueFolded(list) {
    var seen = {};
    var out = [];
    (list || []).forEach(function (term) {
      var folded = foldString(String(term || "").trim());
      if (folded.length < 3 || seen[folded]) return;
      seen[folded] = 1;
      out.push(folded);
    });
    return out;
  }

  function createRespect(data) {
    var grouped = data && data.terms ? data.terms : {};
    var always = [];
    Object.keys(grouped).forEach(function (key) {
      always = always.concat(grouped[key] || []);
    });
    always = uniqueFolded(always);
    var contextual = uniqueFolded(data && data.contextual);
    var frames = uniqueFolded(data && data.frames);
    var mentions = uniqueFolded(data && data.mentions);
    var allow = {};
    uniqueFolded(data && data.allow).forEach(function (word) {
      allow[word] = 1;
    });
    var alwaysSet = {};
    always.forEach(function (term) {
      if (term.indexOf(" ") === -1) alwaysSet[term] = 1;
    });
    var compactPhrases = [];
    always.forEach(function (term) {
      if (term.indexOf(" ") === -1) return;
      var compact = term.replace(/\s+/g, "");
      if (compact.length >= 6) compactPhrases.push(compact);
    });

    function findTermHits(foldedChars, termChars) {
      var hits = [];
      var len = termChars.length;
      if (len < 3 || len > foldedChars.length) return hits;
      var from = 0;
      while (from <= foldedChars.length - len) {
        var same = true;
        for (var i = 0; i < len; i++) {
          if (foldedChars[from + i] !== termChars[i]) {
            same = false;
            break;
          }
        }
        if (same) {
          var before = from > 0 ? foldedChars[from - 1] : "";
          var after = from + len < foldedChars.length ? foldedChars[from + len] : "";
          if (!isWordChar(before) && !isWordChar(after)) hits.push({ start: from, end: from + len });
          from += len;
        } else {
          from += 1;
        }
      }
      return hits;
    }

    function collapseRuns(foldedChars, minRun) {
      var collapsed = [];
      var map = [];
      var i = 0;
      while (i < foldedChars.length) {
        var j = i + 1;
        while (j < foldedChars.length && foldedChars[j] === foldedChars[i]) j += 1;
        if (j - i >= minRun) {
          collapsed.push(foldedChars[i]);
          map.push([i, j]);
        } else {
          for (var k = i; k < j; k++) {
            collapsed.push(foldedChars[k]);
            map.push([k, k + 1]);
          }
        }
        i = j;
      }
      return { chars: collapsed, map: map };
    }

    function tokensOf(foldedChars) {
      var tokens = [];
      var i = 0;
      while (i < foldedChars.length) {
        if (!isWordChar(foldedChars[i])) {
          i += 1;
          continue;
        }
        var j = i + 1;
        while (j < foldedChars.length && isWordChar(foldedChars[j])) j += 1;
        tokens.push({ text: foldedChars.slice(i, j).join(""), start: i, end: j });
        i = j;
      }
      return tokens;
    }

    function leetToken(token) {
      var letters = "";
      var changed = false;
      charsOf(token.text).forEach(function (ch) {
        if (LEET[ch]) {
          letters += LEET[ch];
          changed = true;
          return;
        }
        if (isWordChar(ch)) letters += ch;
        else changed = true;
      });
      return changed ? letters : "";
    }

    function coveredByAllow(joined, inner) {
      if (allow[joined]) return true;
      var from = 0;
      while (from <= joined.length - inner.length) {
        if (joined.slice(from, from + inner.length) === inner) {
          var before = from > 0 ? joined.charAt(from - 1) : "";
          var after = from + inner.length < joined.length ? joined.charAt(from + inner.length) : "";
          if (!before && !after) return !!allow[inner];
        }
        from += 1;
      }
      for (var word in allow) {
        if (!Object.prototype.hasOwnProperty.call(allow, word)) continue;
        if (word.length >= inner.length && joined.indexOf(word) !== -1 && word.indexOf(inner) !== -1) return true;
      }
      return false;
    }

    function pushHit(hits, start, end) {
      if (end - start < 3) return;
      hits.push({ start: start, end: end });
    }

    function rawHits(text) {
      var foldedChars = charsOf(foldString(text));
      var hits = [];
      always.forEach(function (term) {
        findTermHits(foldedChars, charsOf(term)).forEach(function (hit) {
          hits.push(hit);
        });
      });
      [3, 2].forEach(function (minRun) {
        var collapsed = collapseRuns(foldedChars, minRun);
        always.forEach(function (term) {
          if (term.indexOf(" ") !== -1) return;
          findTermHits(collapsed.chars, charsOf(term)).forEach(function (hit) {
            pushHit(hits, collapsed.map[hit.start][0], collapsed.map[hit.end - 1][1]);
          });
        });
      });
      tokensOf(foldedChars).forEach(function (token) {
        var letters = leetToken(token);
        if (letters && (alwaysSet[letters] || compactPhrases.indexOf(letters) !== -1)) {
          pushHit(hits, token.start, token.end);
        }
        if (token.text.length >= 4 && token.text !== letters) {
          var squeezed = token.text.replace(/(.)\1+/g, "$1");
          if (alwaysSet[squeezed]) pushHit(hits, token.start, token.end);
        }
      });
      var tokens = tokensOf(foldedChars);
      var run = [];
      function flushRun() {
        if (run.length >= 3) {
          var joined = run.map(function (token) { return token.text; }).join("");
          if (alwaysSet[joined] || compactPhrases.indexOf(joined) !== -1) {
            pushHit(hits, run[0].start, run[run.length - 1].end);
          } else if (!allow[joined]) {
            Object.keys(alwaysSet).forEach(function (term) {
              if (term.length < 3 || term.length > joined.length) return;
              var from = 0;
              while (from <= joined.length - term.length) {
                if (joined.slice(from, from + term.length) === term) {
                  var before = from > 0 ? joined.charAt(from - 1) : "";
                  var after = from + term.length < joined.length ? joined.charAt(from + term.length) : "";
                  if (!before && !after && !coveredByAllow(joined, term)) {
                    pushHit(hits, run[0].start, run[run.length - 1].end);
                  }
                  from += term.length;
                } else {
                  from += 1;
                }
              }
            });
          }
        }
        run = [];
      }
      tokens.forEach(function (token) {
        if (token.text.length === 1) run.push(token);
        else {
          flushRun();
        }
      });
      flushRun();
      always.forEach(function (term) {
        if (term.indexOf(" ") !== -1 || term.length < 3) return;
        var parts = charsOf(term).map(function (ch) {
          return ch.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        });
        var re = new RegExp("(?<![\\p{L}\\p{N}_])" + parts.join("[^\\p{L}\\p{N}_]{0,2}") + "(?![\\p{L}\\p{N}_])", "gu");
        var haystack = foldedChars.join("");
        var match = re.exec(haystack);
        while (match) {
          pushHit(hits, match.index, match.index + match[0].length);
          if (re.lastIndex <= match.index) re.lastIndex = match.index + match[0].length;
          match = re.exec(haystack);
        }
      });
      var foldedText = foldedChars.join("");
      foldedText.split(/\s+/).forEach(function (chunk) {
        if (chunk.length < 3 || !/[*._-]/.test(chunk)) return;
        var at = foldedText.indexOf(chunk);
        always.forEach(function (term) {
          if (term.indexOf(" ") !== -1) return;
          if (!maskEquals(chunk, term)) return;
          if (at >= 0) pushHit(hits, at, at + chunk.length);
        });
      });
      return { chars: foldedChars, hits: hits, tokens: tokens };
    }

    function maskEquals(token, term) {
      var left = charsOf(token);
      var right = charsOf(term);
      var i = 0;
      var j = 0;
      while (i < left.length && j < right.length) {
        var ch = left[i];
        if (ch === "*" || ch === "." || ch === "_" || ch === "-" || ch === "+") {
          i += 1;
          j += 1;
          continue;
        }
        if (LEET[ch]) ch = LEET[ch];
        if (ch !== right[j]) return false;
        i += 1;
        j += 1;
      }
      return i === left.length && j === right.length;
    }

    function tokenText(chars, start, end) {
      return chars.slice(start, end).join("");
    }

    function nearWord(chars, start, end, words) {
      var windowStart = Math.max(0, start - 48);
      var windowEnd = Math.min(chars.length, end + 24);
      var slice = chars.slice(windowStart, windowEnd).join("");
      var found = false;
      words.forEach(function (word) {
        if (found) return;
        var from = 0;
        while (from <= slice.length - word.length) {
          if (slice.slice(from, from + word.length) === word) {
            var abs = windowStart + from;
            var before = abs > 0 ? chars[abs - 1] : "";
            var after = abs + word.length < chars.length ? chars[abs + word.length] : "";
            if (!isWordChar(before) && !isWordChar(after) && (abs + word.length <= start || abs >= end)) {
              found = true;
              return;
            }
          }
          from += 1;
        }
      });
      return found;
    }

    function insideQuotation(text, start, end) {
      var chars = charsOf(text);
      var open = -1;
      var pairs = { "\"": "\"", "«": "»", "“": "”", "„": "“" };
      for (var i = 0; i < start; i++) {
        var ch = chars[i];
        if (open === -1 && pairs[ch]) open = i;
        else if (open !== -1 && ch === pairs[chars[open]]) open = -1;
      }
      if (open === -1) return false;
      var close = pairs[chars[open]];
      var endQuote = -1;
      for (var j = end; j < chars.length; j++) {
        if (chars[j] === close) {
          endQuote = j;
          break;
        }
      }
      if (endQuote === -1) return false;
      var outside = chars.slice(0, open).concat(chars.slice(endQuote + 1)).join("").replace(/\s/g, "");
      return outside.length >= 12;
    }

    function keepHit(text, chars, hit, nameField) {
      var word = tokenText(chars, hit.start, hit.end).replace(/[^\p{L}\p{N}_]+/gu, "");
      if (!word || allow[word]) return false;
      if (insideQuotation(text, hit.start, hit.end)) return false;
      if (!nameField && nearWord(chars, hit.start, hit.end, mentions) && !nearWord(chars, hit.start, hit.end, frames)) {
        return false;
      }
      return true;
    }

    function contextualHit(text, chars, tokens, nameField) {
      if (nameField) return false;
      var only = tokens.filter(function (token) { return token.text.length > 1 || contextual.indexOf(token.text) !== -1; });
      for (var i = 0; i < tokens.length; i++) {
        var token = tokens[i];
        if (contextual.indexOf(token.text) === -1 && contextual.indexOf(leetToken(token)) === -1) continue;
        var word = leetToken(token) || token.text;
        if (allow[word] || allow[token.text]) continue;
        var standalone = tokens.length === 1 || (only.length === 1 && only[0] === token);
        var framed = nearWord(chars, token.start, token.end, frames);
        if (!standalone && !framed) continue;
        if (insideQuotation(text, token.start, token.end)) continue;
        if (nearWord(chars, token.start, token.end, mentions) && !framed) continue;
        return true;
      }
      return false;
    }

    function offensive(text, options) {
      var value = String(text || "");
      if (foldString(value).replace(/\s/g, "").length < 3) return false;
      var nameField = !!(options && options.nameField);
      var found = rawHits(value);
      for (var i = 0; i < found.hits.length; i++) {
        if (keepHit(value, found.chars, found.hits[i], nameField)) return true;
      }
      return contextualHit(value, found.chars, found.tokens, nameField);
    }

    return { offensive: offensive };
  }

  function message() {
    var lang = "";
    if (typeof document !== "undefined") {
      lang = document.documentElement.getAttribute("data-daab-lang") || document.documentElement.lang || "";
    }
    return lang === "az" ? MESSAGE.az : MESSAGE.en;
  }

  function isNameField(field) {
    var id = field.id || "";
    var name = field.name || "";
    return NAME_RE.test(id) || NAME_RE.test(name);
  }

  function offensive(text, options) {
    if (!model) return false;
    return model.offensive(text, options || {});
  }

  function highlight(field) {
    if (!field || typeof document === "undefined") return;
    var form = field.closest ? field.closest("form") : null;
    var rootNode = form || document;
    rootNode.querySelectorAll(".field-required-warning").forEach(function (node) {
      if (node.parentNode) node.parentNode.removeChild(node);
    });
    rootNode.querySelectorAll("[aria-invalid='true']").forEach(function (node) {
      node.removeAttribute("aria-invalid");
      node.classList.remove("is-required-invalid");
    });
    var noteText = message();
    var box = document.getElementById("app-submit-status");
    if (box) {
      box.hidden = false;
      box.className = "app-submit-status app-submit-status--error";
      box.setAttribute("role", "alert");
      box.textContent = noteText;
    }
    field.classList.add("is-required-invalid");
    field.setAttribute("aria-invalid", "true");
    var group = (field.closest && (field.closest(".field-group") || field.closest(".opt-item") || field.closest(".app-file-card"))) || field.parentNode;
    var note = document.createElement("p");
    note.className = "field-required-warning";
    note.setAttribute("role", "alert");
    note.textContent = noteText;
    if (group) group.appendChild(note);
    if (typeof field.focus === "function") {
      try { field.focus(); } catch (err) { /* ignore */ }
    }
    if (typeof field.scrollIntoView === "function") {
      field.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  function fieldOffensive(field) {
    if (!field || field.disabled || field.readOnly) return false;
    var type = (field.type || "").toLowerCase();
    if (type === "hidden" || type === "file" || type === "checkbox" || type === "radio" || type === "submit" || type === "button" || type === "search") return false;
    if (!field.name || field.name === "website" || field.id === "website") return false;
    var value = String(field.value || "");
    if (!value.trim()) return false;
    return offensive(value, { nameField: isNameField(field) });
  }

  function firstField(form) {
    if (!form) return null;
    var fields = form.querySelectorAll("input, textarea");
    for (var i = 0; i < fields.length; i++) {
      if (fieldOffensive(fields[i])) return fields[i];
    }
    return null;
  }

  root.daabRespectCreate = createRespect;
  root.daabRespectOffensive = offensive;
  root.daabRespectMessage = message;
  root.daabRespectHighlight = function (form) {
    var field = firstField(form);
    if (field) highlight(field);
    return field;
  };

  if (typeof document === "undefined") return;

  var script = document.currentScript;
  var lexiconUrl = script && script.src
    ? new URL("../i18n/feedback-language.json", script.src).href
    : "i18n/feedback-language.json";
  root.daabRespectReady = fetch(lexiconUrl)
    .then(function (res) {
      if (!res.ok) throw new Error("lexicon");
      return res.json();
    })
    .then(function (data) {
      model = createRespect(data);
      state = "ready";
    })
    .catch(function () {
      state = "failed";
    });

  document.addEventListener("submit", function (event) {
    var form = event.target;
    if (!form || !form.id || !FORMS[form.id]) return;
    if (state !== "loading") return;
    if (form.getAttribute("data-respect-wait") === "1") return;
    event.preventDefault();
    event.stopImmediatePropagation();
    form.setAttribute("data-respect-wait", "1");
    root.daabRespectReady.then(function () {
      form.removeAttribute("data-respect-wait");
      if (typeof form.requestSubmit === "function") form.requestSubmit();
    });
  }, true);
})(typeof globalThis !== "undefined" ? globalThis : this);
