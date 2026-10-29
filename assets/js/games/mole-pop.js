/* Mole Pop — tap the moles before they duck, avoid the hedgehogs, catch golden stars */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var HOLES = 9, DUR = 30, score = 0, combo = 0, endAt = 0, running = false, timers = [], tick = null;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row"><button class="btn sun sm" data-start>Start 30-second round</button></div>' +
    '<div class="stats"><div class="stat"><small>Score</small><b data-score>0</b></div><div class="stat"><small>Time</small><b data-time>30</b></div><div class="stat"><small>Best</small><b data-best>0</b></div></div></div>' +
    '<div class="mp-field" role="group" aria-label="Mole holes">' + Array.from({ length: HOLES }, function (_, i) { return '<button type="button" class="mp-hole" data-i="' + i + '" aria-label="Hole ' + (i + 1) + '"><span class="mp-who"></span></button>'; }).join("") + '</div>' +
    '<p class="game-msg" aria-live="polite">Moles = +10 (combos add more). Golden star = +50. Hedgehog = −20.</p>';
  var holes = el.querySelectorAll(".mp-hole"), msg = el.querySelector(".game-msg");
  function best() { el.querySelector("[data-best]").textContent = AF.best("mole-pop") || 0; }
  function upd() { el.querySelector("[data-score]").textContent = score; }
  function pop() {
    if (!running) return;
    var free = Array.prototype.filter.call(holes, function (h) { return !h.dataset.who; });
    if (free.length) {
      var h = free[Math.floor(Math.random() * free.length)], r = Math.random();
      var who = r < 0.08 ? "star" : r < 0.24 ? "hog" : "mole";
      var left = (endAt - Date.now()) / 1000, stay = Math.max(520, 1100 - (DUR - left) * 18);
      h.dataset.who = who; h.classList.add("up"); h.querySelector(".mp-who").textContent = who === "star" ? "🌟" : who === "hog" ? "🦔" : "🐹";
      timers.push(setTimeout(function () { if (h.dataset.who === who) { if (who === "mole") combo = 0; hide(h); } }, stay));
    }
    var left2 = (endAt - Date.now()) / 1000;
    timers.push(setTimeout(pop, Math.max(280, 720 - (DUR - left2) * 14)));
  }
  function hide(h) { h.dataset.who = ""; h.classList.remove("up", "hit"); h.querySelector(".mp-who").textContent = ""; }
  function hit(h) {
    if (!running || !h.dataset.who) return;
    var who = h.dataset.who;
    if (who === "mole") { combo++; score += 10 + Math.min(combo - 1, 5) * 2; }
    else if (who === "star") score += 50;
    else { score = Math.max(0, score - 20); combo = 0; }
    h.classList.add("hit"); h.dataset.who = "";
    setTimeout(function () { hide(h); }, 160); upd();
  }
  function start() {
    timers.forEach(clearTimeout); timers = []; holes.forEach(hide);
    score = 0; combo = 0; upd(); running = true; endAt = Date.now() + DUR * 1000; msg.textContent = "Go!";
    clearInterval(tick); tick = setInterval(function () {
      var left = Math.max(0, Math.ceil((endAt - Date.now()) / 1000)); el.querySelector("[data-time]").textContent = left;
      if (left <= 0) end();
    }, 200);
    pop();
  }
  function end() {
    running = false; clearInterval(tick); timers.forEach(clearTimeout); timers = []; holes.forEach(hide);
    var nb = AF.best("mole-pop", score); best();
    msg.textContent = "Time! You scored " + score + "." + (nb && score ? " New best!" : "") + " Press Start for another round.";
  }
  holes.forEach(function (h) { h.addEventListener("pointerdown", function (e) { e.preventDefault(); hit(h); }); h.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hit(h); } }); });
  el.querySelector("[data-start]").addEventListener("click", start);
  best();
})();
