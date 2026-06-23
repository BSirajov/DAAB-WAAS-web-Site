/**
 * Excel-style multi-select checkbox filters for scientists catalogue toolbars.
 * Shared by scientists/list.html and scientists/profiles.html.
 */
(function (window) {
  "use strict";

  var instances = {};
  var openId = null;

  var STRINGS = {
    az: {
      selectAll: "Hamısını seç",
      search: "Axtar…",
      selectedCount: function (n) {
        return n + " seçilib";
      },
      moreSelected: function (n) {
        return "+" + n + " daha";
      },
      noneSelected: "Heç biri seçilməyib",
      noMatches: "Uyğun variant yoxdur",
    },
    en: {
      selectAll: "Select All",
      search: "Search…",
      selectedCount: function (n) {
        return n + " selected";
      },
      moreSelected: function (n) {
        return "+" + n + " more";
      },
      noneSelected: "None selected",
      noMatches: "No matching options",
    },
  };

  function lang() {
    var root = document.documentElement;
    return (root.getAttribute("data-daab-lang") || root.lang || "az").slice(0, 2);
  }

  function ui() {
    return STRINGS[lang()] || STRINGS.en;
  }

  function getPlaceholder(select) {
    var first = select.options && select.options[0];
    if (!first) return select.getAttribute("aria-label") || "";
    return (first.textContent || "")
      .replace(/^[^\p{L}\p{N}]+/u, "")
      .trim();
  }

  function readOptions(select) {
    var out = [];
    if (!select || !select.options) return out;
    for (var i = 0; i < select.options.length; i++) {
      var opt = select.options[i];
      if (!opt.value) continue;
      out.push({ value: opt.value, label: opt.textContent || opt.value });
    }
    return out;
  }

  function closePanel(id, focusTrigger) {
    var inst = instances[id];
    if (!inst || !inst.panel.classList.contains("is-open")) return;
    inst.panel.classList.remove("is-open");
    inst.panel.hidden = true;
    inst.trigger.setAttribute("aria-expanded", "false");
    if (openId === id) openId = null;
    if (focusTrigger) inst.trigger.focus();
  }

  function closeAll(exceptId) {
    Object.keys(instances).forEach(function (id) {
      if (id !== exceptId) closePanel(id, false);
    });
  }

  function positionPanel(id) {
    var inst = instances[id];
    if (!inst) return;
    var rect = inst.trigger.getBoundingClientRect();
    var gap = 4;
    var width = Math.max(rect.width, 240);
    var left = Math.min(rect.left, window.innerWidth - width - 8);
    var top = rect.bottom + gap;
    var maxH = Math.min(320, window.innerHeight - top - 12);
    if (maxH < 120 && rect.top > window.innerHeight * 0.45) {
      top = Math.max(8, rect.top - gap);
      inst.panel.style.transform = "translateY(-100%) translateY(" + (-gap) + "px)";
    } else {
      inst.panel.style.transform = "";
    }
    inst.panel.style.left = Math.max(8, left) + "px";
    inst.panel.style.top = top + "px";
    inst.panel.style.width = width + "px";
    inst.list.style.maxHeight = Math.max(100, maxH - (inst.searchWrap ? 52 : 0)) + "px";
  }

  function isChecked(inst, value) {
    if (inst.selected === null) return true;
    return inst.selected.has(value);
  }

  function syncSelectAll(inst) {
    if (!inst.selectAllInput) return;
    var total = inst.options.length;
    if (!total) {
      inst.selectAllInput.checked = false;
      inst.selectAllInput.indeterminate = false;
      return;
    }
    if (inst.selected === null) {
      inst.selectAllInput.checked = true;
      inst.selectAllInput.indeterminate = false;
      return;
    }
    var count = inst.selected.size;
    inst.selectAllInput.checked = count === total;
    inst.selectAllInput.indeterminate = count > 0 && count < total;
  }

  function updateTriggerLabel(id) {
    var inst = instances[id];
    if (!inst) return;
    var label = inst.trigger.querySelector(".ms-filter-trigger__label");
    if (!label) return;
    var placeholder = inst.placeholder;
    var options = inst.options;
    if (!options.length) {
      label.textContent = placeholder;
      return;
    }
    if (inst.selected === null) {
      label.textContent = placeholder;
      return;
    }
    if (inst.selected.size === 0) {
      label.textContent = ui().noneSelected;
      return;
    }
    var names = options
      .filter(function (o) {
        return inst.selected.has(o.value);
      })
      .map(function (o) {
        return o.label;
      });
    if (names.length <= 2) {
      label.textContent = names.join(", ");
      return;
    }
    label.textContent = names.slice(0, 2).join(", ") + " " + ui().moreSelected(names.length - 2);
  }

  function notifyChange(id) {
    var inst = instances[id];
    if (!inst) return;
    updateTriggerLabel(id);
    syncSelectAll(inst);
    if (inst.wrap) {
      inst.wrap.classList.toggle("active", inst.selected !== null);
    }
    if (typeof inst.onChange === "function") {
      inst.onChange();
    }
    inst.select.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function setSelectedFromCheckboxes(id) {
    var inst = instances[id];
    if (!inst) return;
    var total = inst.options.length;
    var checked = [];
    inst.optionInputs.forEach(function (pair) {
      if (pair.input.checked) checked.push(pair.value);
    });
    if (checked.length === total) {
      inst.selected = null;
    } else {
      inst.selected = new Set(checked);
    }
    notifyChange(id);
  }

  function setSelectAll(id, checked) {
    var inst = instances[id];
    if (!inst) return;
    inst.optionInputs.forEach(function (pair) {
      pair.input.checked = checked;
      var row = pair.input.closest(".ms-filter-option");
      if (row) row.classList.toggle("is-hidden", false);
    });
    inst.selected = checked ? null : new Set();
    if (inst.searchInput) inst.searchInput.value = "";
    filterOptions(id, "");
    notifyChange(id);
  }

  function filterOptions(id, query) {
    var inst = instances[id];
    if (!inst) return;
    var q = (query || "").toLowerCase().trim();
    var visible = 0;
    inst.optionInputs.forEach(function (pair) {
      var row = pair.input.closest(".ms-filter-option");
      if (!row || row.classList.contains("ms-filter-option--select-all")) return;
      var show = !q || pair.label.toLowerCase().indexOf(q) !== -1;
      row.classList.toggle("is-hidden", !show);
      if (show) visible += 1;
    });
    if (inst.emptyEl) {
      inst.emptyEl.classList.toggle("is-visible", !!q && visible === 0);
    }
  }

  function rebuildPanel(id) {
    var inst = instances[id];
    if (!inst) return;
    inst.options = readOptions(inst.select);
    inst.optionInputs = [];
    inst.list.innerHTML = "";
    var L = ui();

    if (inst.options.length > 10) {
      if (!inst.searchWrap) {
        inst.searchWrap = document.createElement("div");
        inst.searchWrap.className = "ms-filter-panel__search";
        inst.searchInput = document.createElement("input");
        inst.searchInput.type = "search";
        inst.searchInput.className = "ms-filter-panel__search-input";
        inst.searchInput.setAttribute("autocomplete", "off");
        inst.searchInput.addEventListener("input", function () {
          filterOptions(id, inst.searchInput.value);
        });
        inst.searchInput.addEventListener("keydown", function (e) {
          if (e.key === "Escape") {
            e.stopPropagation();
            closePanel(id, true);
          }
        });
        inst.searchWrap.appendChild(inst.searchInput);
        inst.panel.insertBefore(inst.searchWrap, inst.list);
      }
      inst.searchInput.placeholder = L.search;
      inst.searchInput.value = "";
    } else if (inst.searchWrap) {
      inst.searchWrap.remove();
      inst.searchWrap = null;
      inst.searchInput = null;
    }

    if (!inst.emptyEl) {
      inst.emptyEl = document.createElement("div");
      inst.emptyEl.className = "ms-filter-panel__empty";
      inst.emptyEl.textContent = L.noMatches;
      inst.panel.appendChild(inst.emptyEl);
    }
    inst.emptyEl.classList.remove("is-visible");

    var selectAllRow = document.createElement("label");
    selectAllRow.className = "ms-filter-option ms-filter-option--select-all";
    inst.selectAllInput = document.createElement("input");
    inst.selectAllInput.type = "checkbox";
    inst.selectAllInput.setAttribute("data-ms-select-all", "1");
    var selectAllText = document.createElement("span");
    selectAllText.className = "ms-filter-option__text";
    selectAllText.textContent = L.selectAll;
    selectAllRow.appendChild(inst.selectAllInput);
    selectAllRow.appendChild(selectAllText);
    selectAllRow.addEventListener("change", function () {
      setSelectAll(id, inst.selectAllInput.checked);
    });
    inst.list.appendChild(selectAllRow);

    inst.options.forEach(function (opt) {
      var row = document.createElement("label");
      row.className = "ms-filter-option";
      var input = document.createElement("input");
      input.type = "checkbox";
      input.value = opt.value;
      input.checked = isChecked(inst, opt.value);
      var text = document.createElement("span");
      text.className = "ms-filter-option__text";
      text.textContent = opt.label;
      row.appendChild(input);
      row.appendChild(text);
      row.addEventListener("change", function () {
        setSelectedFromCheckboxes(id);
      });
      inst.list.appendChild(row);
      inst.optionInputs.push({ value: opt.value, label: opt.label, input: input });
    });

    syncSelectAll(inst);
    updateTriggerLabel(id);
  }

  function openPanel(id) {
    var inst = instances[id];
    if (!inst) return;
    closeAll(id);
    rebuildPanel(id);
    positionPanel(id);
    inst.panel.hidden = false;
    inst.panel.classList.add("is-open");
    inst.trigger.setAttribute("aria-expanded", "true");
    openId = id;
    if (inst.searchInput) {
      inst.searchInput.focus();
    }
  }

  function mount(select, config) {
    if (!select || !select.id) return null;
    var id = select.id;
    if (instances[id]) {
      rebuildPanel(id);
      return instances[id];
    }

    var wrap = select.closest(".sel-wrap");
    if (!wrap) return null;

    config = config || {};
    wrap.classList.add("ms-filter-wrap");

    var trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "ms-filter-trigger";
    trigger.id = id + "MsTrigger";
    trigger.setAttribute("aria-haspopup", "listbox");
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-controls", id + "MsPanel");
    var aria = select.getAttribute("aria-label");
    if (aria) trigger.setAttribute("aria-label", aria);

    var labelSpan = document.createElement("span");
    labelSpan.className = "ms-filter-trigger__label";
    trigger.appendChild(labelSpan);

    var panel = document.createElement("div");
    panel.className = "ms-filter-panel";
    panel.id = id + "MsPanel";
    panel.setAttribute("role", "listbox");
    panel.setAttribute("aria-multiselectable", "true");
    panel.hidden = true;

    var list = document.createElement("div");
    list.className = "ms-filter-panel__list";
    panel.appendChild(list);

    select.classList.add("ms-filter-native");
    select.tabIndex = -1;
    select.setAttribute("aria-hidden", "true");

    wrap.insertBefore(trigger, select);
    document.body.appendChild(panel);

    instances[id] = {
      select: select,
      wrap: wrap,
      trigger: trigger,
      panel: panel,
      list: list,
      placeholder: getPlaceholder(select),
      options: [],
      optionInputs: [],
      selected: null,
      onChange: config.onChange || null,
      searchWrap: null,
      searchInput: null,
      emptyEl: null,
      selectAllInput: null,
    };

    trigger.addEventListener("click", function () {
      if (openId === id) {
        closePanel(id, true);
      } else {
        openPanel(id);
      }
    });

    trigger.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openPanel(id);
      }
    });

    select.dataset.msFilterReady = "1";
    rebuildPanel(id);
    return instances[id];
  }

  function getFilterValues(id) {
    var inst = instances[id];
    if (!inst) {
      var el = document.getElementById(id);
      if (!el) return null;
      return el.value ? [el.value] : null;
    }
    if (inst.selected === null) return null;
    return Array.from(inst.selected);
  }

  function isActive(id) {
    return getFilterValues(id) !== null;
  }

  function clear(id) {
    var inst = instances[id];
    if (!inst) {
      var el = document.getElementById(id);
      if (el) el.value = "";
      return;
    }
    inst.selected = null;
    if (inst.searchInput) inst.searchInput.value = "";
    rebuildPanel(id);
    notifyChange(id);
  }

  function remount(id) {
    if (!instances[id]) {
      var el = document.getElementById(id);
      if (el) mount(el, {});
      return;
    }
    rebuildPanel(id);
  }

  document.addEventListener("mousedown", function (e) {
    if (!openId) return;
    var inst = instances[openId];
    if (!inst) return;
    if (inst.panel.contains(e.target) || inst.trigger.contains(e.target)) return;
    closePanel(openId, false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && openId) {
      closePanel(openId, true);
    }
  });

  window.addEventListener("resize", function () {
    if (openId) positionPanel(openId);
  });

  window.addEventListener(
    "scroll",
    function () {
      if (openId) positionPanel(openId);
    },
    true
  );

  window.DAABScientistsMultiSelect = {
    mount: mount,
    remount: remount,
    getFilterValues: getFilterValues,
    isActive: isActive,
    clear: clear,
    clearAll: function (ids) {
      (ids || []).forEach(function (id) {
        clear(id);
      });
    },
    matches: function (filterValues, value) {
      if (filterValues === null) return true;
      if (!filterValues.length) return false;
      var v = (value == null ? "" : String(value)).trim();
      return filterValues.indexOf(v) !== -1;
    },
  };
})(typeof window !== "undefined" ? window : this);
