/* Maturité numérique — interactions hors DSFR (modale de suppression,
   questionnaire, impression). Le reste (accordéons, onglets, sidemenu,
   modales) est géré nativement par le JS du DSFR. */

(function () {
  "use strict";

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

  // ── Questionnaire (evaluation_fill) ──
  var fill = document.getElementById("fill-form");
  if (fill) {
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
          o.classList.toggle("is-selected", o === opt && !already);
        });
        card.querySelector("[data-na-btn]").setAttribute("aria-pressed", "false");
        updateProgress();
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
        card2.querySelectorAll(".level-option").forEach(function (o) { o.classList.remove("is-selected"); });
        updateProgress();
        return;
      }
      // justification
      var jbtn = e.target.closest("[data-justif-btn]");
      if (jbtn) {
        e.preventDefault();
        var area = jbtn.closest(".cap-card").querySelector("textarea");
        area.hidden = !area.hidden;
        jbtn.querySelector("span[data-label]").textContent =
          area.hidden ? "Ajouter une justification" : "Masquer la justification";
        if (!area.hidden) area.focus();
      }
    });

    updateProgress();
  }

  // ── Impression automatique (?print=1) ──
  if (new URLSearchParams(window.location.search).get("print") === "1") {
    window.addEventListener("load", function () {
      setTimeout(function () { window.print(); }, 800);
    });
  }
})();
