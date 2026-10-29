/* Pattern Echo — watch the sequence of lights and tones, then repeat it */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var PADS = [{ c: "sun", f: 329.6, k: "1" }, { c: "sky", f: 261.6, k: "2" }, { c: "pop", f: 220, k: "3" }, { c: "mint", f: 164.8, k: "4" }];
  var seq = [], pos = 0, accepting = false, audio = null, muted = AF.store.get("af-pe-mute") === "1", strict = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row"><button class="btn sun sm" data-start>Start</button><button class="btn ghost sm" data-mute aria-pressed="' + muted + '">' + (muted ? "🔇 Sound off" : "🔊 Sound on") + '</button>' +
    '<label class="check small"><input type="checkbox" data-strict> Strict (one mistake ends the game)</label></div>' +
    '<div class="stats"><div class="stat"><small>Level</small><b data-lv>0</b></div><div class="stat"><small>Best</small><b data-best>0</b></div></div></div>' +
    '<div class="pe-board" role="group" aria-label="Pattern pads">' + PADS.map(function (p, i) { return '<button type="button" class="pe-pad ' + p.c + '" data-i="' + i + '" aria-label="Pad ' + (i + 1) + '"><span>' + p.k + '</span></button>'; }).join("") + '</div>' +
    '<p class="game-msg" aria-live="polite">Press Start. Keys 1–4 work too.</p>';
  var pads = el.querySelectorAll(".pe-pad"), msg = el.querySelector(".game-msg");
  function best() { el.querySelector("[data-best]").textContent = AF.best("pattern-echo") || 0; }
  function tone(f, ms) {
    if (muted) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      var o = audio.createOscillator(), g = audio.createGain(); o.type = "triangle"; o.frequency.value = f;
      g.gain.setValueAtTime(0.0001, audio.currentTime); g.gain.exponentialRampToValueAtTime(0.18, audio.currentTime + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + ms / 1000);
      o.connect(g); g.connect(audio.destination); o.start(); o.stop(audio.currentTime + ms / 1000 + 0.02);
    } catch (e) {}
  }
  function flash(i, ms) { pads[i].classList.add("lit"); tone(PADS[i].f, ms); setTimeout(function () { pads[i].classList.remove("lit"); }, ms); }
  function playSeq() {
    accepting = false; msg.textContent = "Watch…"; var gap = Math.max(260, 620 - seq.length * 18), k = 0;
    (function next() {
      if (k >= seq.length) { accepting = true; pos = 0; msg.textContent = "Your turn — repeat " + seq.length + (seq.length === 1 ? " step." : " steps."); return; }
      flash(seq[k], gap * 0.7); k++; setTimeout(next, gap);
    })();
  }
  function grow() { seq.push(Math.floor(Math.random() * 4)); el.querySelector("[data-lv]").textContent = seq.length; setTimeout(playSeq, 520); }
  function start() { seq = []; grow(); }
  function press(i) {
    if (!accepting) return;
    flash(i, 220);
    if (i !== seq[pos]) {
      accepting = false; tone(110, 400);
      if (strict) {
        var lv = seq.length - 1, nb = AF.best("pattern-echo", lv); best();
        msg.textContent = "Missed it! You reached level " + lv + "." + (nb && lv ? " New best!" : "") + " Press Start to play again."; return;
      }
      msg.textContent = "Not quite — watch again."; setTimeout(playSeq, 900); return;
    }
    pos++;
    if (pos === seq.length) { accepting = false; AF.best("pattern-echo", seq.length); best(); msg.textContent = "Nice!"; grow(); }
  }
  pads.forEach(function (p) { p.addEventListener("pointerdown", function (e) { e.preventDefault(); press(+p.dataset.i); }); p.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); press(+p.dataset.i); } }); });
  document.addEventListener("keydown", function (e) { if (e.target.closest && e.target.closest("input,textarea,select,button")) return; if (/^[1-4]$/.test(e.key)) press(+e.key - 1); });
  el.querySelector("[data-start]").addEventListener("click", start);
  el.querySelector("[data-strict]").addEventListener("change", function (e) { strict = e.target.checked; });
  var mb = el.querySelector("[data-mute]");
  mb.addEventListener("click", function () { muted = !muted; AF.store.set("af-pe-mute", muted ? "1" : "0"); mb.setAttribute("aria-pressed", muted); mb.textContent = muted ? "🔇 Sound off" : "🔊 Sound on"; });
  best();
})();
