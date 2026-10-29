/* Tile Merge — slide and merge numbered tiles (classic sliding-merge mechanics, original code) */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var N = 4, grid, score, over, won, keepGoing, prev = null;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row"><button class="btn sun sm" data-new>New game</button><button class="btn ghost sm" data-undo disabled>Undo</button></div>' +
    '<div class="stats"><div class="stat"><small>Score</small><b data-score>0</b></div><div class="stat"><small>Best</small><b data-best>0</b></div></div></div>' +
    '<div class="tm-board" tabindex="0" aria-label="Tile board. Use arrow keys or swipe."></div><p class="game-msg" aria-live="polite"></p>';
  var board = el.querySelector(".tm-board"), msg = el.querySelector(".game-msg"), undoBtn = el.querySelector("[data-undo]");
  function empty() { var e = []; for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) if (!grid[r][c]) e.push([r, c]); return e; }
  function add() { var e = empty(); if (!e.length) return; var p = e[Math.floor(Math.random() * e.length)]; grid[p[0]][p[1]] = Math.random() < 0.9 ? 2 : 4; return p; }
  function reset() {
    grid = []; for (var r = 0; r < N; r++) grid.push([0, 0, 0, 0]);
    score = 0; over = false; won = false; keepGoing = false; prev = null; undoBtn.disabled = true;
    add(); add(); draw(); msg.textContent = "Join matching numbers to reach 2048.";
  }
  function draw(newPos, merged) {
    board.innerHTML = "";
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) {
      var v = grid[r][c], d = document.createElement("div");
      d.className = "tm-cell" + (v ? " v" + Math.min(v, 4096) : "") + (newPos && newPos[0] === r && newPos[1] === c ? " fresh" : "") + (merged && merged[r + "," + c] ? " merged" : "");
      d.textContent = v || ""; board.appendChild(d);
    }
    el.querySelector("[data-score]").textContent = score;
    el.querySelector("[data-best]").textContent = Math.max(score, AF.best("tile-merge") || 0);
  }
  function slide(line) {
    var vals = line.filter(Boolean), out = [], gained = 0, mergedIdx = [];
    for (var i = 0; i < vals.length; i++) {
      if (vals[i] === vals[i + 1]) { out.push(vals[i] * 2); gained += vals[i] * 2; mergedIdx.push(out.length - 1); i++; }
      else out.push(vals[i]);
    }
    while (out.length < N) out.push(0);
    return { line: out, gained: gained, merged: mergedIdx };
  }
  function move(dir) {
    if (over) return;
    var before = JSON.stringify(grid), snapshot = { g: JSON.parse(before), s: score }, merged = {}, moved = false;
    for (var k = 0; k < N; k++) {
      var line = [], coords = [];
      for (var j = 0; j < N; j++) {
        var r = dir === "up" ? j : dir === "down" ? N - 1 - j : k;
        var c = dir === "left" ? j : dir === "right" ? N - 1 - j : k;
        line.push(grid[r][c]); coords.push([r, c]);
      }
      var res = slide(line); score += res.gained;
      res.line.forEach(function (v, i) { grid[coords[i][0]][coords[i][1]] = v; });
      res.merged.forEach(function (i) { merged[coords[i][0] + "," + coords[i][1]] = 1; });
    }
    if (JSON.stringify(grid) !== before) moved = true;
    if (!moved) return;
    prev = snapshot; undoBtn.disabled = false;
    var p = add(); AF.best("tile-merge", score); draw(p, merged);
    if (!won && !keepGoing && grid.some(function (row) { return row.indexOf(2048) > -1; })) { won = true; msg.textContent = "You made 2048! Keep going for a bigger tile."; keepGoing = true; }
    if (!canMove()) { over = true; msg.textContent = "No moves left. Final score " + score + "."; }
  }
  function canMove() {
    if (empty().length) return true;
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) { var v = grid[r][c]; if ((c < N - 1 && grid[r][c + 1] === v) || (r < N - 1 && grid[r + 1][c] === v)) return true; }
    return false;
  }
  document.addEventListener("keydown", function (e) {
    var map = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right", w: "up", s: "down", a: "left", d: "right" };
    if (e.target.closest && e.target.closest("input,textarea,select")) return;
    if (map[e.key]) { e.preventDefault(); move(map[e.key]); }
  });
  var sx, sy;
  board.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  board.addEventListener("touchmove", function (e) { e.preventDefault(); }, { passive: false });
  board.addEventListener("touchend", function (e) {
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 24) return;
    move(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
  });
  el.querySelector("[data-new]").addEventListener("click", reset);
  undoBtn.addEventListener("click", function () { if (!prev) return; grid = prev.g; score = prev.s; prev = null; over = false; undoBtn.disabled = true; draw(); msg.textContent = "Move undone."; });
  reset();
})();
