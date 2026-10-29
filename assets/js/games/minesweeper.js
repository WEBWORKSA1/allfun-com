/* Minesweeper — classic mine-finding logic puzzle (original code) */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var LV = { easy: [9, 9, 10], medium: [16, 16, 40], hard: [16, 30, 99] };
  var level = "easy", R, C, M, cells, first, over, revealed, flags, t0, timer, flagMode = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<label class="vh" for="ms-l">Difficulty</label><select id="ms-l" class="mini-select"><option value="easy">Easy 9×9</option><option value="medium">Medium 16×16</option><option value="hard">Expert 16×30</option></select>' +
    '<button class="btn sun sm" data-new>New game</button><button class="btn ghost sm" data-flag aria-pressed="false">🚩 Flag mode: off</button></div>' +
    '<div class="stats"><div class="stat"><small>Mines</small><b data-left>0</b></div><div class="stat"><small>Time</small><b data-time>0</b></div><div class="stat"><small>Best</small><b data-best>–</b></div></div></div>' +
    '<div class="ms-scroll"><div class="ms-grid" role="grid" aria-label="Minefield"></div></div><p class="game-msg" aria-live="polite"></p>';
  var gridEl = el.querySelector(".ms-grid"), msg = el.querySelector(".game-msg");
  function nb(r, c, fn) { for (var dr = -1; dr <= 1; dr++) for (var dc = -1; dc <= 1; dc++) { if (!dr && !dc) continue; var rr = r + dr, cc = c + dc; if (rr >= 0 && cc >= 0 && rr < R && cc < C) fn(rr, cc); } }
  function showBest() { var b = AF.best("ms-" + level); el.querySelector("[data-best]").textContent = b === null ? "–" : b + "s"; }
  function setup() {
    var l = LV[level]; R = l[0]; C = l[1]; M = l[2]; first = true; over = false; revealed = 0; flags = 0; clearInterval(timer); timer = null;
    cells = []; gridEl.innerHTML = ""; gridEl.style.gridTemplateColumns = "repeat(" + C + ", var(--ms))";
    gridEl.classList.toggle("wide", C > 16);
    for (var r = 0; r < R; r++) { cells.push([]); for (var c = 0; c < C; c++) {
      var b = document.createElement("button"); b.type = "button"; b.className = "ms-cell"; b.dataset.r = r; b.dataset.c = c; b.setAttribute("aria-label", "Hidden");
      gridEl.appendChild(b); cells[r].push({ mine: false, n: 0, open: false, flag: false, el: b });
    } }
    el.querySelector("[data-left]").textContent = M; el.querySelector("[data-time]").textContent = 0;
    msg.textContent = "Tap a square to start. Right-click or long-press to flag."; showBest();
  }
  function lay(sr, sc) {
    var spots = []; for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (Math.abs(r - sr) > 1 || Math.abs(c - sc) > 1) spots.push([r, c]);
    AF.shuffle(spots).slice(0, M).forEach(function (p) { cells[p[0]][p[1]].mine = true; });
    for (r = 0; r < R; r++) for (c = 0; c < C; c++) { var n = 0; nb(r, c, function (a, b) { if (cells[a][b].mine) n++; }); cells[r][c].n = n; }
    t0 = Date.now(); timer = setInterval(function () { el.querySelector("[data-time]").textContent = Math.floor((Date.now() - t0) / 1000); }, 500);
  }
  function open(r, c) {
    var stack = [[r, c]];
    while (stack.length) {
      var p = stack.pop(), x = cells[p[0]][p[1]];
      if (x.open || x.flag) continue;
      x.open = true; revealed++; x.el.classList.add("open");
      if (x.mine) { x.el.classList.add("boom"); x.el.textContent = "💥"; return lose(); }
      x.el.textContent = x.n || ""; if (x.n) x.el.classList.add("n" + x.n);
      x.el.setAttribute("aria-label", x.n ? x.n + " mines near" : "Empty");
      if (!x.n) nb(p[0], p[1], function (a, b) { if (!cells[a][b].open) stack.push([a, b]); });
    }
    if (revealed === R * C - M) win();
  }
  function chord(r, c) {
    var x = cells[r][c], f = 0; if (!x.open || !x.n) return;
    nb(r, c, function (a, b) { if (cells[a][b].flag) f++; });
    if (f === x.n) nb(r, c, function (a, b) { if (!over && !cells[a][b].flag && !cells[a][b].open) open(a, b); });
  }
  function flag(r, c) {
    var x = cells[r][c]; if (x.open || over) return;
    x.flag = !x.flag; flags += x.flag ? 1 : -1; x.el.textContent = x.flag ? "🚩" : ""; x.el.classList.toggle("flag", x.flag);
    x.el.setAttribute("aria-label", x.flag ? "Flagged" : "Hidden");
    el.querySelector("[data-left]").textContent = M - flags;
  }
  function lose() {
    over = true; clearInterval(timer);
    cells.forEach(function (row) { row.forEach(function (x) { if (x.mine && !x.flag) { x.el.textContent = "💣"; x.el.classList.add("open"); } if (!x.mine && x.flag) x.el.textContent = "❌"; }); });
    msg.textContent = "Boom! Press New game to try again.";
  }
  function win() {
    over = true; clearInterval(timer);
    var secs = Math.floor((Date.now() - t0) / 1000), nbst = AF.best("ms-" + level, secs, true);
    cells.forEach(function (row) { row.forEach(function (x) { if (x.mine) { x.el.textContent = "🚩"; } }); });
    msg.textContent = "Cleared in " + secs + "s!" + (nbst ? " New best." : ""); showBest();
  }
  function act(e, isFlag) {
    var b = e.target.closest(".ms-cell"); if (!b || over) return;
    var r = +b.dataset.r, c = +b.dataset.c;
    if (isFlag || flagMode) { if (!first) flag(r, c); return; }
    if (first) { first = false; lay(r, c); }
    if (cells[r][c].open) chord(r, c); else open(r, c);
  }
  gridEl.addEventListener("click", function (e) { if (pressTimer === -1) { pressTimer = null; return; } act(e, false); });
  gridEl.addEventListener("contextmenu", function (e) { e.preventDefault(); act(e, true); });
  var pressTimer = null;
  gridEl.addEventListener("touchstart", function (e) { var ev = e; pressTimer = setTimeout(function () { act(ev, true); pressTimer = -1; if (navigator.vibrate) navigator.vibrate(20); }, 420); }, { passive: true });
  gridEl.addEventListener("touchend", function () { if (pressTimer && pressTimer !== -1) { clearTimeout(pressTimer); pressTimer = null; } });
  gridEl.addEventListener("touchmove", function () { if (pressTimer && pressTimer !== -1) { clearTimeout(pressTimer); pressTimer = null; } }, { passive: true });
  el.querySelector("#ms-l").addEventListener("change", function (e) { level = e.target.value; setup(); });
  el.querySelector("[data-new]").addEventListener("click", setup);
  var fb = el.querySelector("[data-flag]");
  fb.addEventListener("click", function () { flagMode = !flagMode; fb.setAttribute("aria-pressed", flagMode); fb.textContent = "🚩 Flag mode: " + (flagMode ? "on" : "off"); });
  setup();
})();
