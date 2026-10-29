/* Snake — classic grid snake */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var G = 20, snake, dir, queue, food, bonus, score, speed, loop, running = false, paused = false, walls = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row"><button class="btn sun sm" data-start>Start</button><button class="btn ghost sm" data-pause disabled>Pause</button>' +
    '<label class="check small"><input type="checkbox" data-walls> Solid walls</label></div>' +
    '<div class="stats"><div class="stat"><small>Score</small><b data-score>0</b></div><div class="stat"><small>Best</small><b data-best>0</b></div></div></div>' +
    '<div class="canvas-box"><canvas width="480" height="480" aria-label="Snake game board"></canvas>' +
    '<div class="overlay" data-ov><div><h2>Snake</h2><p>Arrow keys, WASD or swipe. Eat stars, don\'t bite yourself.</p><button class="btn lg" data-start>Play</button></div></div></div>' +
    '<div class="dpad" aria-label="Direction pad"><button class="up" data-d="up" aria-label="Up">▲</button><button class="left" data-d="left" aria-label="Left">◀</button><button class="down" data-d="down" aria-label="Down">▼</button><button class="right" data-d="right" aria-label="Right">▶</button></div>' +
    '<p class="game-msg" aria-live="polite"></p>';
  var cv = el.querySelector("canvas"), ctx = cv.getContext("2d"), ov = el.querySelector("[data-ov]"), msg = el.querySelector(".game-msg"), pauseBtn = el.querySelector("[data-pause]");
  var S = cv.width / G;
  function best() { el.querySelector("[data-best]").textContent = AF.best("snake") || 0; }
  function place() {
    var p; do { p = { x: Math.floor(Math.random() * G), y: Math.floor(Math.random() * G) }; } while (snake.some(function (s) { return s.x === p.x && s.y === p.y; }));
    return p;
  }
  function start() {
    snake = [{ x: 9, y: 10 }, { x: 8, y: 10 }, { x: 7, y: 10 }]; dir = "right"; queue = []; score = 0; speed = 130; bonus = null;
    food = place(); running = true; paused = false; ov.hidden = true; pauseBtn.disabled = false; pauseBtn.textContent = "Pause";
    el.querySelector("[data-score]").textContent = 0; msg.textContent = "";
    clearTimeout(loop); step();
    cv.focus && cv.focus();
  }
  function turn(d) {
    var last = queue.length ? queue[queue.length - 1] : dir, opp = { up: "down", down: "up", left: "right", right: "left" };
    if (d !== last && d !== opp[last] && queue.length < 3) queue.push(d);
  }
  function step() {
    if (!running) return;
    if (!paused) {
      if (queue.length) dir = queue.shift();
      var h = { x: snake[0].x, y: snake[0].y };
      if (dir === "up") h.y--; if (dir === "down") h.y++; if (dir === "left") h.x--; if (dir === "right") h.x++;
      if (walls && (h.x < 0 || h.y < 0 || h.x >= G || h.y >= G)) return end();
      h.x = (h.x + G) % G; h.y = (h.y + G) % G;
      if (snake.some(function (s, i) { return i < snake.length - 1 && s.x === h.x && s.y === h.y; })) return end();
      snake.unshift(h);
      if (h.x === food.x && h.y === food.y) {
        score += 10; food = place(); speed = Math.max(60, speed - 3);
        if (!bonus && Math.random() < 0.25) bonus = { p: place(), t: 40 };
      } else if (bonus && h.x === bonus.p.x && h.y === bonus.p.y) { score += 50; bonus = null; }
      else snake.pop();
      if (bonus && --bonus.t <= 0) bonus = null;
      el.querySelector("[data-score]").textContent = score;
      draw();
    }
    loop = setTimeout(step, speed);
  }
  function cell(x, y, color, r) { ctx.fillStyle = color; ctx.beginPath(); ctx.roundRect(x * S + 1, y * S + 1, S - 2, S - 2, r || 5); ctx.fill(); }
  function draw() {
    var dark = getComputedStyle(document.documentElement).getPropertyValue("--surface").trim();
    ctx.fillStyle = dark || "#fff"; ctx.fillRect(0, 0, cv.width, cv.height);
    ctx.fillStyle = "rgba(91,149,255,.08)";
    for (var y = 0; y < G; y++) for (var x = (y % 2); x < G; x += 2) ctx.fillRect(x * S, y * S, S, S);
    ctx.font = (S - 4) + "px system-ui"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("⭐", food.x * S + S / 2, food.y * S + S / 2 + 1);
    if (bonus) ctx.fillText("💎", bonus.p.x * S + S / 2, bonus.p.y * S + S / 2 + 1);
    snake.forEach(function (s, i) { cell(s.x, s.y, i === 0 ? "#1F1A4D" : (i % 2 ? "#22C7A9" : "#1DB598"), i === 0 ? 8 : 5); });
    var h = snake[0]; ctx.fillStyle = "#FFC93C"; ctx.beginPath(); ctx.arc(h.x * S + S / 2, h.y * S + S / 2, S / 7, 0, 7); ctx.fill();
  }
  function end() {
    running = false; clearTimeout(loop); pauseBtn.disabled = true;
    var nb = AF.best("snake", score); best();
    ov.hidden = false; ov.querySelector("h2").textContent = nb && score ? "New best: " + score + "!" : "Game over";
    ov.querySelector("p").textContent = "You scored " + score + ". Length " + snake.length + ".";
    ov.querySelector("button").textContent = "Play again";
  }
  function togglePause() { if (!running) return; paused = !paused; pauseBtn.textContent = paused ? "Resume" : "Pause"; msg.textContent = paused ? "Paused" : ""; }
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input,textarea,select")) return;
    var m = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right", w: "up", s: "down", a: "left", d: "right", W: "up", S: "down", A: "left", D: "right" };
    if (m[e.key] && running) { e.preventDefault(); turn(m[e.key]); }
    if (e.key === " ") { e.preventDefault(); running ? togglePause() : start(); }
  });
  el.querySelectorAll("[data-d]").forEach(function (b) { b.addEventListener("click", function () { turn(b.dataset.d); }); });
  var sx, sy; cv.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  cv.addEventListener("touchmove", function (e) { e.preventDefault(); }, { passive: false });
  cv.addEventListener("touchend", function (e) { var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; if (Math.max(Math.abs(dx), Math.abs(dy)) > 20) turn(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up")); });
  el.querySelectorAll("[data-start]").forEach(function (b) { b.addEventListener("click", start); });
  pauseBtn.addEventListener("click", togglePause);
  el.querySelector("[data-walls]").addEventListener("change", function (e) { walls = e.target.checked; });
  snake = [{ x: 9, y: 10 }, { x: 8, y: 10 }, { x: 7, y: 10 }]; food = { x: 14, y: 10 }; draw(); best();
})();
