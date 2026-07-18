/* Maturité numérique — interactions hors DSFR (modale de suppression,
   questionnaire, impression). Le reste (accordéons, onglets, sidemenu,
   modales) est géré nativement par le JS du DSFR. */

(function () {
  "use strict";

  // ── Annonces pour lecteurs d'écran (#live-region, cf. base.html) ──
  function announce(msg) {
    var region = document.getElementById("live-region");
    if (!region) return;
    region.textContent = "";
    setTimeout(function () { region.textContent = msg; }, 50);
  }

  // ── Modale de suppression partagée ──
  // Tout bouton [data-delete-action] ouvre #delete-modal en pointant le
  // formulaire vers l'action donnée. data-delete-name alimente le texte.
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-delete-action]");
    if (!btn) return;
    e.preventDefault();
    var form = document.getElementById("delete-modal-form");
    var name = document.getElementById("delete-modal-name");
    form.setAttribute("action", btn.getAttribute("data-delete-action"));
    // champ next optionnel
    form.querySelectorAll("input[name=next]").forEach(function (i) { i.remove(); });
    if (btn.getAttribute("data-delete-next")) {
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = "next";
      input.value = btn.getAttribute("data-delete-next");
      form.appendChild(input);
    }
    name.textContent = btn.getAttribute("data-delete-name") || "cet élément";
    var modal = document.getElementById("delete-modal");
    if (window.dsfr && window.dsfr(modal) && window.dsfr(modal).modal) {
      window.dsfr(modal).modal.disclose();
    } else {
      modal.showModal ? modal.showModal() : modal.setAttribute("open", "");
    }
  });

  // ── Menu latéral repliable (desktop, état mémorisé) ──
  var layout = document.getElementById("app-layout");
  var sideBtn = document.getElementById("side-collapse-btn");
  if (layout && sideBtn) {
    var syncSideBtn = function () {
      var collapsed = layout.classList.contains("side-collapsed");
      sideBtn.setAttribute("aria-expanded", collapsed ? "false" : "true");
      sideBtn.title = collapsed ? "Déplier le menu" : "Replier le menu";
      var srLabel = sideBtn.querySelector(".fr-sr-only");
      if (srLabel) srLabel.textContent = collapsed ? "Déplier le menu latéral" : "Replier le menu latéral";
    };
    sideBtn.addEventListener("click", function () {
      layout.classList.toggle("side-collapsed");
      try { localStorage.setItem("side-collapsed", layout.classList.contains("side-collapsed") ? "1" : "0"); } catch (e) {}
      syncSideBtn();
      window.dispatchEvent(new Event("resize")); // les charts se réadaptent à la nouvelle largeur
    });
    syncSideBtn();
  }

  // ── Accordéon mobile du sidemenu ──
  var smToggle = document.querySelector(".sidemenu-toggle");
  if (smToggle) {
    smToggle.addEventListener("click", function () {
      var content = document.getElementById(smToggle.getAttribute("aria-controls"));
      var open = content.classList.toggle("is-open");
      smToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // ── Copie presse-papier générique (data-copy-text / data-copy-link) ──
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy-text], [data-copy-link]");
    if (!btn) return;
    e.preventDefault();
    var isLink = btn.hasAttribute("data-copy-link");
    var value = isLink ? btn.getAttribute("data-copy-link") : btn.getAttribute("data-copy-text");
    navigator.clipboard.writeText(value).then(function () {
      var initial = btn.textContent;
      btn.textContent = "Copié ✓";
      announce(isLink ? "Lien copié" : "Copié dans le presse-papier");
      setTimeout(function () { btn.textContent = initial; }, 2000);
    });
  });

  // ── Questionnaire (evaluation_fill) ──
  var fill = document.getElementById("fill-form");
  if (fill) {
    // ── Autosave : le brouillon est réellement conservé en continu ──
    // NB : fill.action est shadowé par les boutons name="action" (RadioNodeList),
    // on construit donc l'URL depuis le pathname.
    var autosaveUrl = window.location.pathname.replace(/\/fill\/?$/, "/autosave");
    var statusEl = document.getElementById("autosave-status");
    if (!statusEl) {
      var progressBar = document.querySelector("[data-progress-bar]");
      if (progressBar) {
        statusEl = document.createElement("p");
        statusEl.id = "autosave-status";
        statusEl.className = "fr-text--xs fr-mb-0";
        var barBox = progressBar.closest(".progress") || progressBar;
        barBox.parentNode.insertBefore(statusEl, barBox.nextSibling);
      }
    }
    var dirty = false;          // interaction non (encore) persistée côté serveur
    var inflight = 0;           // requêtes autosave en cours
    var debounceTimers = {};    // capId → timer (saisie de justification)
    var anchorInput = fill.querySelector('input[name="anchor"]');

    var setStatus = function (text) { if (statusEl) statusEl.textContent = text; };
    var maybeClean = function () {
      if (inflight === 0 && Object.keys(debounceTimers).length === 0) dirty = false;
    };

    var sendAutosave = function (card) {
      var input = card.querySelector("input[data-cap-input]");
      var capId = input.name.replace("cap_", "");
      delete debounceTimers[capId];
      var body = new URLSearchParams();
      body.set(input.name, input.value);
      var area = card.querySelector('textarea[name="just_' + capId + '"]');
      if (area) body.set(area.name, area.value);
      inflight++;
      setStatus("Enregistrement…");
      var failed = false;
      fetch(autosaveUrl, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(),
      }).then(function (r) {
        return r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status));
      }).then(function (data) {
        if (!data.ok) return Promise.reject(new Error(data.error || "réponse invalide"));
        var now = new Date();
        var hh = String(now.getHours()).padStart(2, "0");
        var mm = String(now.getMinutes()).padStart(2, "0");
        setStatus("✓ Enregistré à " + hh + ":" + mm);
        announce("Brouillon enregistré");
      }).catch(function () {
        failed = true;
        setStatus("⚠ Non enregistré — vérifiez votre connexion");
        announce("Échec de l'enregistrement automatique — vérifiez votre connexion");
      }).finally(function () {
        inflight--;
        if (!failed) maybeClean();
      });
    };

    // marque l'interaction : dirty, ancre de la dimension, autosave (debounce optionnel)
    var touch = function (card, immediate) {
      dirty = true;
      if (anchorInput) {
        var section = card.closest('section[id^="dim-"]');
        if (section) anchorInput.value = section.id;
      }
      var capId = card.querySelector("input[data-cap-input]").name.replace("cap_", "");
      if (debounceTimers[capId]) { clearTimeout(debounceTimers[capId]); delete debounceTimers[capId]; }
      if (immediate) sendAutosave(card);
      else debounceTimers[capId] = setTimeout(function () { sendAutosave(card); }, 1200);
    };

    window.addEventListener("beforeunload", function (e) {
      if (!dirty) return;   // rien en attente : ne pas gêner la navigation
      e.preventDefault();
      e.returnValue = "";
    });
    fill.addEventListener("submit", function () { dirty = false; });

    var updateProgress = function () {
      var cards = fill.querySelectorAll(".cap-card");
      var done = 0;
      cards.forEach(function (card) {
        var input = card.querySelector("input[data-cap-input]");
        var answered = input.value !== "";
        card.classList.toggle("is-answered", answered && input.value !== "na");
        card.classList.toggle("is-na", input.value === "na");
        if (answered) done++;
      });
      var total = cards.length;
      var pct = total ? Math.round(done / total * 100) : 0;
      document.querySelectorAll("[data-progress-done]").forEach(function (el) { el.textContent = done; });
      document.querySelectorAll("[data-progress-pct]").forEach(function (el) { el.textContent = pct + " %"; });
      var bar = document.querySelector("[data-progress-bar]");
      if (bar) bar.style.width = pct + "%";
      var validate = document.getElementById("btn-recap");
      var warn = document.getElementById("fill-incomplete-warn");
      if (validate) validate.disabled = done < total;
      if (warn) warn.hidden = done >= total;
      // compteurs par dimension
      document.querySelectorAll("[data-dim-count]").forEach(function (el) {
        var dimId = el.getAttribute("data-dim-count");
        var dimCards = fill.querySelectorAll('.cap-card[data-dim="' + dimId + '"]');
        var dimDone = 0;
        dimCards.forEach(function (c) {
          if (c.querySelector("input[data-cap-input]").value !== "") dimDone++;
        });
        el.textContent = dimDone + "/" + dimCards.length;
        el.classList.toggle("fr-badge--success", dimDone === dimCards.length);
      });
    };

    fill.addEventListener("click", function (e) {
      // choix d'un niveau
      var opt = e.target.closest(".level-option");
      if (opt) {
        e.preventDefault();
        var card = opt.closest(".cap-card");
        var input = card.querySelector("input[data-cap-input]");
        var already = input.value === opt.getAttribute("data-niveau");
        input.value = already ? "" : opt.getAttribute("data-niveau");
        card.querySelectorAll(".level-option").forEach(function (o) {
          var selected = o === opt && !already;
          o.classList.toggle("is-selected", selected);
          o.setAttribute("aria-pressed", selected ? "true" : "false");
        });
        card.querySelector("[data-na-btn]").setAttribute("aria-pressed", "false");
        updateProgress();
        touch(card, true);
        return;
      }
      // non applicable
      var na = e.target.closest("[data-na-btn]");
      if (na) {
        e.preventDefault();
        var card2 = na.closest(".cap-card");
        var input2 = card2.querySelector("input[data-cap-input]");
        var active = input2.value === "na";
        input2.value = active ? "" : "na";
        na.setAttribute("aria-pressed", active ? "false" : "true");
        card2.querySelectorAll(".level-option").forEach(function (o) {
          o.classList.remove("is-selected");
          o.setAttribute("aria-pressed", "false");
        });
        updateProgress();
        touch(card2, true);
        return;
      }
      // justification
      var jbtn = e.target.closest("[data-justif-btn]");
      if (jbtn) {
        e.preventDefault();
        var area = jbtn.closest(".cap-card").querySelector("textarea");
        area.hidden = !area.hidden;
        jbtn.setAttribute("aria-expanded", area.hidden ? "false" : "true");
        jbtn.querySelector("span[data-label]").textContent =
          area.hidden ? "Ajouter une justification" : "Masquer la justification";
        if (!area.hidden) area.focus();
      }
    });

    // saisie de justification : autosave débouncé (1,2 s)
    fill.addEventListener("input", function (e) {
      var area = e.target.closest('textarea[name^="just_"]');
      if (!area) return;
      touch(area.closest(".cap-card"), false);
    });

    updateProgress();

    // ── Mode « une dimension à la fois » (stepper, issue #8) ──
    var sections = Array.prototype.slice.call(fill.querySelectorAll('section[id^="dim-"]'));
    var stepper = document.getElementById("dim-stepper");
    var stepperNav = document.getElementById("stepper-nav");
    var toggleBox = document.getElementById("stepper-toggle-box");
    var toggle = document.getElementById("stepper-toggle");
    if (stepper && stepperNav && toggle && sections.length > 1) {
      toggleBox.hidden = false;
      var totalCaps = fill.querySelectorAll(".cap-card").length;
      var stored = null;
      try { stored = localStorage.getItem("fill-stepper"); } catch (e) {}
      // défaut : pas-à-pas pour les longs questionnaires (> 15 capacités)
      var stepperOn = stored !== null ? stored === "1" : totalCaps > 15;
      // démarrer sur la première dimension incomplète
      var current = 0;
      for (var i = 0; i < sections.length; i++) {
        var incomplete = Array.prototype.some.call(
          sections[i].querySelectorAll("input[data-cap-input]"),
          function (inp) { return inp.value === ""; });
        if (incomplete) { current = i; break; }
      }

      var renderStep = function (focusTitle) {
        sections.forEach(function (s, i) { s.hidden = stepperOn && i !== current; });
        stepper.hidden = !stepperOn;
        stepperNav.hidden = !stepperOn;
        toggle.checked = stepperOn;
        if (!stepperOn) return;
        var titleEl = sections[current].querySelector("h2");
        stepper.querySelector("[data-step-cur]").textContent = current + 1;
        stepper.querySelector("[data-step-title]").textContent = titleEl ? titleEl.textContent : "";
        stepper.querySelector(".fr-stepper__steps").setAttribute("data-fr-current-step", current + 1);
        var details = stepper.querySelector("[data-step-details]");
        if (current + 1 < sections.length) {
          var nextTitle = sections[current + 1].querySelector("h2");
          details.hidden = false;
          stepper.querySelector("[data-step-next]").textContent = nextTitle ? nextTitle.textContent : "";
        } else {
          details.hidden = true;
        }
        document.getElementById("step-prev").disabled = current === 0;
        var last = current === sections.length - 1;
        document.getElementById("step-next").hidden = last;
        document.getElementById("step-finish").hidden = !last;
        if (focusTitle && titleEl) {
          titleEl.setAttribute("tabindex", "-1");
          titleEl.focus({ preventScroll: false });
          window.scrollTo({ top: 0 });
        }
      };

      toggle.addEventListener("change", function () {
        stepperOn = toggle.checked;
        try { localStorage.setItem("fill-stepper", stepperOn ? "1" : "0"); } catch (e) {}
        renderStep(false);
      });
      document.getElementById("step-prev").addEventListener("click", function () {
        if (current > 0) { current--; renderStep(true); }
      });
      document.getElementById("step-next").addEventListener("click", function () {
        if (current < sections.length - 1) { current++; renderStep(true); }
      });
      // les liens « Dimensions » de l'aside pilotent l'étape en mode pas-à-pas
      document.querySelectorAll('a[href^="#dim-"]').forEach(function (a) {
        a.addEventListener("click", function (e) {
          if (!stepperOn) return;
          e.preventDefault();
          var idx = sections.findIndex(function (s) { return "#" + s.id === a.getAttribute("href"); });
          if (idx >= 0) { current = idx; renderStep(true); }
        });
      });

      renderStep(false);
    }
  }

  // ── Échelle fixe des charts (radar/line) ──
  // dsfr-chart laisse chart.js auto-échelonner : sur un radar, le minimum des
  // données se retrouve au centre, ce qui est trompeur pour une échelle 0–N.
  // Les templates posent data-scale-max="N" sur <dsfr-data-chart> ; on
  // retrouve l'instance chart.js interne du web component et on fige 0–N.
  function findChartInstance(component, canvas) {
    var found = null;
    var seen = new Set();
    (function scan(obj, depth) {
      if (!obj || typeof obj !== "object" || seen.has(obj) || depth > 6 || found) return;
      seen.add(obj);
      if (obj.canvas === canvas && obj.options && typeof obj.update === "function") { found = obj; return; }
      var keys = Object.keys(obj);
      for (var i = 0; i < keys.length && !found; i++) {
        try { scan(obj[keys[i]], depth + 1); } catch (e) { /* accès interdit : ignorer */ }
      }
    })(component._instance, 0);
    return found;
  }

  function fixChartScales() {
    var pending = false;
    document.querySelectorAll("[data-scale-max]").forEach(function (wrap) {
      var max = parseFloat(wrap.getAttribute("data-scale-max"));
      if (!max) return;
      wrap.querySelectorAll("radar-chart canvas, line-chart canvas").forEach(function (canvas) {
        var comp = canvas.closest("radar-chart, line-chart");
        var chart = comp && findChartInstance(comp, canvas);
        if (!chart) { pending = true; return; }
        // le composant peut recréer l'instance après l'arrivée des données :
        // on marque l'instance, pas le canvas, et on continue de surveiller
        if (chart.__scaleFixed) return;
        var sc = chart.options.scales || {};
        if (sc.r) { sc.r.min = 0; sc.r.max = max; sc.r.ticks = Object.assign(sc.r.ticks || {}, { stepSize: 1 }); }
        if (comp.tagName === "LINE-CHART" && sc.y) { sc.y.min = 0; sc.y.max = max; }
        // update() seul ne repeint pas toujours ce web component : resize() force le redraw
        chart.resize();
        chart.update();
        chart.__scaleFixed = true;
      });
      if (!wrap.querySelector("canvas")) pending = true;
    });
    return pending;
  }

  if (document.querySelector("[data-scale-max]")) {
    var tries = 0;
    var timer = setInterval(function () {
      fixChartScales();
      if (++tries > 24) clearInterval(timer);  // surveille ~12 s (recréations tardives)
    }, 500);
  }

  // ── Focus de série sur les radars comparatifs (lisibilité) ──
  // Les profils proches se superposent : le select [data-radar-focus] isole
  // une organisation (dataset) face à la moyenne, via l'instance chart.js.
  document.addEventListener("change", function (e) {
    var sel = e.target.closest("[data-radar-focus]");
    if (!sel) return;
    var wrap = sel.closest(".panel, .chart-card") || document;
    var canvas = wrap.querySelector("radar-chart canvas");
    var comp = canvas && canvas.closest("radar-chart");
    if (!comp) return;
    var chart = findChartInstance(comp, canvas);
    if (!chart) return;
    var keep = parseInt(sel.getAttribute("data-keep-index"), 10);
    var chosen = sel.value === "" ? null : parseInt(sel.value, 10);
    chart.data.datasets.forEach(function (_, i) {
      chart.setDatasetVisibility(i, chosen === null || i === chosen || i === keep);
    });
    chart.update();
  });

  // ── Impression automatique (?print=1) ──
  if (new URLSearchParams(window.location.search).get("print") === "1") {
    window.addEventListener("load", function () {
      setTimeout(function () { window.print(); }, 800);
    });
  }
})();
