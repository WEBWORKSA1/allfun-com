/* Reaction Time — wait for green, then tap as fast as you can (5 rounds) */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var ROUNDS = 5, state = "idle", times = [], t0 = 0, wait = null;
  el.innerHTML = '<div class="stage-bar"><div class="stats"><div class="stat"><small>Round</small><b data-round>0/5</b></div><div class="stat"><small>Average</small><b data-avg>–</b></div><div class="stat"><small>Best avg</small><b data-best>–</b></div></div></div>' +
    '<button type="button" class="rt-pad" data-state="idle"><span class="rt-big">Tap to start</span><span class="rt-small">When the box turns green, tap as fast as you can. Keyboard: Space.</span></button>' +
    '<ol class="rt-list" aria-label="Your times"></ol><p class="game-msg" aria-live="polite"></p>';
  var pad = el.querySelector(".rt-pad"), big = pad.querySelector(".rt-big"), small = pad.querySelector(".rt-small"), list = el.querySelector(".rt-list"), msg = el.querySelector(".game-msg");
  function showBest() { var b = AF.best("reaction"); el.querySelector("[data-best]").textContent = b === null ? "–" : b + " ms"; }
  function set(s, a, b2) { state = s; pad.dataset.state = s; big.textContent = a; small.textContent = b2 || ""; }
  function arm() { set("wait", "Wait for green…", "Don't tap yet."); wait = setTimeout(function () { set("go", "TAP!", ""); t0 = performance.now(); }, 1200 + Math.random() * 2600); }
  function hit() {
    if (state === "idle" || state === "done") { times = []; list.innerHTML = ""; msg.textContent = ""; el.querySelector("[data-avg]").textContent = "–"; arm(); }
    else if (state === "wait") { clearTimeout(wait); set("early", "Too soon!", "Tap to retry this round."); }
    else if (state === "early") arm();
    else if (state === "go") {
      var ms = Math.round(performance.now() - t0); times.push(ms);
      var li = document.createElement("li"); li.textContent = ms + " ms"; list.appendChild(li);
      el.querySelector("[data-round]").textContent = times.length + "/" + ROUNDS;
      if (times.length < ROUNDS) set("between", ms + " ms", "Tap for the next round.");
      else {
        var avg = Math.round(times.reduce(function (a, b) { return a + b; }, 0) / ROUNDS), nb = AF.best("reaction", avg, true);
        el.querySelector("[data-avg]").textContent = avg + " ms"; showBest();
        set("done", avg + " ms average", "Tap to play again.");
        msg.textContent = (avg < 220 ? "Lightning reflexes." : avg < 280 ? "Quick! Solidly above average." : avg < 350 ? "Nice and steady." : "Warm-up round? Try again.") + (nb ? " New personal best!" : "");
      }
    }
    else if (state === "between") arm();
  }
  pad.addEventListener("pointerdown", function (e) { e.preventDefault(); hit(); });
  pad.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); hit(); } });
  showBest();
})();
