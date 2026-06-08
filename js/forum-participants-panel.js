/**
 * Forum 2024 hub — Participants panel (directory + profiles links).
 * Inner forum pages do not load this script; the hub uses static HTML in index.html.
 */
(function (window, document) {
  "use strict";

  var STRINGS = {
    az: {
      title: "İştirakçılar",
      lead: "Forumda iştirak etmiş alimlərin siyahısı və akademik profilləri.",
      listTitle: "Alimlərin siyahısı",
      profilesTitle: "Alimlərin profilləri",
    },
    en: {
      title: "Participants",
      lead: "Directory and academic profiles of scientists who took part in the Forum.",
      listTitle: "Directory of Scientists",
      profilesTitle: "Profiles of Scientists",
    },
  };

  function lang() {
    var l = document.documentElement.getAttribute("data-daab-lang") || document.documentElement.lang || "az";
    return l.slice(0, 2) === "en" ? "en" : "az";
  }

  function t() {
    return STRINGS[lang()];
  }

  function assetRoot() {
    return document.documentElement.getAttribute("data-daab-asset-root") || "../../../";
  }

  function scientistsHref(file) {
    var root = assetRoot();
    var path = location.pathname.replace(/\\/g, "/");
    if (/\/forum\/2024\//.test(path)) {
      return root + "../../scientists/" + file;
    }
    return root + "scientists/" + file;
  }

  function findInsertPoint() {
    var hero = document.querySelector(
      "header.page-hero, header.hero, header.forum-hero"
    );
    if (hero && hero.parentNode) {
      return { parent: hero.parentNode, before: hero.nextSibling };
    }
    var main = document.getElementById("content") || document.querySelector("main.main");
    if (main) {
      return { parent: main, before: main.firstElementChild };
    }
    return null;
  }

  function buildPanel() {
    var ui = t();
    var section = document.createElement("section");
    section.className = "forum-participants-panel";
    section.setAttribute("aria-labelledby", "forum-participants-title");

    var title = document.createElement("h2");
    title.id = "forum-participants-title";
    title.className = "forum-participants-panel__title";
    title.textContent = ui.title;
    section.appendChild(title);

    var lead = document.createElement("p");
    lead.className = "forum-participants-panel__lead";
    lead.textContent = ui.lead;
    section.appendChild(lead);

    var cards = document.createElement("div");
    cards.className = "forum-participants-panel__cards";

    [
      {
        href: scientistsHref("list.html"),
        icon: "📋",
        title: ui.listTitle,
        navId: "scientists-list",
      },
      {
        href: scientistsHref("profiles.html"),
        icon: "👤",
        title: ui.profilesTitle,
        navId: "scientists-profiles",
      },
    ].forEach(function (item) {
      var link = document.createElement("a");
      link.className = "forum-participants-card";
      link.href = item.href;
      link.setAttribute("data-nav-id", item.navId);

      var icon = document.createElement("span");
      icon.className = "forum-participants-card__icon";
      icon.setAttribute("aria-hidden", "true");
      icon.textContent = item.icon;

      var body = document.createElement("span");
      body.className = "forum-participants-card__body";

      var name = document.createElement("span");
      name.className = "forum-participants-card__title";
      name.textContent = item.title;

      body.appendChild(name);
      link.appendChild(icon);
      link.appendChild(body);
      cards.appendChild(link);
    });

    section.appendChild(cards);
    return section;
  }

  function mount() {
    if (document.querySelector(".forum-participants-panel")) return;
    var pageId = document.documentElement.getAttribute("data-daab-page-id") || "";
    if (pageId !== "forum-2024") return;

    var point = findInsertPoint();
    if (!point) return;

    var shell = document.createElement("div");
    shell.className = "forum-participants-shell";
    shell.appendChild(buildPanel());

    if (point.before) {
      point.parent.insertBefore(shell, point.before);
    } else {
      point.parent.appendChild(shell);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})(window, document);
