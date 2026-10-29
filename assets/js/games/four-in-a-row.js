/* Four in a Row — drop discs, connect four; play the computer or a friend */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var W = 7, H = 6, b, turn, over, vsCpu = true, depth = 4, wins = AF.store.json("af-4r", { you: 0, cpu: 0, draw: 0 });
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<label class="vh" for="fr-m">Opponent</label><select id="fr-m" class="mini-select"><option value="2">Computer · Easy</option><option value="4" selected>Computer · Medium</option><option value="6">Computer · Hard</option><option value="pvp">Friend (same device)</option></select>' +
    '<button class="btn sun sm" data-new>New game</button></div>' +
    '<div class="stats"><div class="stat"><small>You</small><b data-w="you">0</b></div><div class="stat"><small>CPU</small><b data-w="cpu">0</b></div><div class="stat"><small>Draws</small><b data-w="draw">0</b></div></div></div>' +
    '<div class="fr-board" role="grid" aria-label="Four in a row board"></div><p class="game-msg" aria-live="polite"></p>';
  var boardEl = el.querySelector(".fr-board"), msg = el.querySelector(".game-msg");
  for (var c = 0; c < W; c++) {
    var col = document.createElement("button"); col.type = "button"; col.className = "fr-col"; col.dataset.c = c; col.setAttribute("aria-label", "Drop in column " + (c + 1));
    for (var r = 0; r < H; r++) { var s = document.createElement("span"); s.className = "fr-slot"; col.appendChild(s); }
    boardEl.appendChild(col);
  }
  function score() { ["you", "cpu", "draw"].forEach(function (k) { el.querySelector('[data-w="' + k + '"]').textContent = wins[k]; }); }
  function reset() { b = []; for (var c = 0; c < W; c++) b.push([]); turn = 1; over = false; draw(); msg.textContent = vsCpu ? "You're yellow. Connect four to win." : "Yellow goes first."; }
  function draw(winLine) {
    var cols = boardEl.children;
    for (var c = 0; c < W; c++) for (var r = 0; r < H; r++) {
      var v = b[c][H - 1 - r] || 0, s = cols[c].children[r];
      s.className = "fr-slot" + (v === 1 ? " p1" : v === 2 ? " p2" : "") + (winLine && winLine.some(function (p) { return p[0] === c && p[1] === H - 1 - r; }) ? " win" : "");
    }
  }
  function at(g, c, r) { return c >= 0 && c < W && r >= 0 && r < H ? (g[c][r] || 0) : -1; }
  function winner(g) {
    var dirs = [[1, 0], [0, 1], [1, 1], [1, -1]];
    for (var c = 0; c < W; c++) for (var r = 0; r < H; r++) {
      var p = at(g, c, r); if (p <= 0) continue;
      for (var d = 0; d < 4; d++) {
        var line = [[c, r]];
        for (var k = 1; k < 4; k++) { if (at(g, c + dirs[d][0] * k, r + dirs[d][1] * k) === p) line.push([c + dirs[d][0] * k, r + dirs[d][1] * k]); else break; }
        if (line.length === 4) return { p: p, line: line };
      }
    }
    return null;
  }
  function full(g) { return g.every(function (col) { return col.length >= H; }); }
  function evalWin(cells, p) {
    var mine = 0, theirs = 0; cells.forEach(function (v) { if (v === p) mine++; else if (v > 0) theirs++; });
    if (mine && theirs) return 0; if (mine === 4) return 1000; if (mine === 3) return 6; if (mine === 2) return 2;
    if (theirs === 3) return -8; if (theirs === 2) return -2; return 0;
  }
  function heur(g, p) {
    var s = 0, dirs = [[1, 0], [0, 1], [1, 1], [1, -1]];
    for (var r = 0; r < H; r++) if (at(g, 3, r) === p) s += 3;
    for (var c = 0; c < W; c++) for (r = 0; r < H; r++) for (var d = 0; d < 4; d++) {
      var ec = c + dirs[d][0] * 3, er = r + dirs[d][1] * 3; if (ec < 0 || ec >= W || er < 0 || er >= H) continue;
      var cells = []; for (var k = 0; k < 4; k++) { var v = at(g, c + dirs[d][0] * k, r + dirs[d][1] * k); cells.push(v < 0 ? 0 : v); }
      s += evalWin(cells, p);
    }
    return s;
  }
  var ORDER = [3, 2, 4, 1, 5, 0, 6];
  function minimax(g, d, a, beta, maxing) {
    var w = winner(g); if (w) return w.p === 2 ? 100000 + d : -100000 - d;
    if (full(g)) return 0; if (d === 0) return heur(g, 2);
    var best = maxing ? -Infinity : Infinity;
    for (var i = 0; i < W; i++) {
      var c = ORDER[i]; if (g[c].length >= H) continue;
      g[c].push(maxing ? 2 : 1); var v = minimax(g, d - 1, a, beta, !maxing); g[c].pop();
      if (maxing) { best = Math.max(best, v); a = Math.max(a, v); } else { best = Math.min(best, v); beta = Math.min(beta, v); }
      if (a >= beta) break;
    }
    return best;
  }
  function cpuMove() {
    var bestC = -1, bestV = -Infinity, opts = [];
    ORDER.forEach(function (c) {
      if (b[c].length >= H) return;
      b[c].push(2); var v = minimax(b, depth - 1, -Infinity, Infinity, false); b[c].pop();
      if (depth <= 2) v += Math.random() * 40 - 20;
      opts.push([c, v]); if (v > bestV) { bestV = v; bestC = c; }
    });
    return bestC;
  }
  function play(c) {
    if (over || b[c].length >= H) return false;
    b[c].push(turn); var w = winner(b); draw(w && w.line);
    if (w) {
      over = true;
      if (vsCpu) { wins[w.p === 1 ? "you" : "cpu"]++; AF.store.put("af-4r", wins); score(); msg.textContent = w.p === 1 ? "You win! 🎉" : "The computer wins this one."; }
      else msg.textContent = (w.p === 1 ? "Yellow" : "Pink") + " wins!";
      return true;
    }
    if (full(b)) { over = true; if (vsCpu) { wins.draw++; AF.store.put("af-4r", wins); score(); } msg.textContent = "It's a draw."; return true; }
    turn = 3 - turn;
    if (!vsCpu) msg.textContent = (turn === 1 ? "Yellow" : "Pink") + "'s turn.";
    return true;
  }
  boardEl.addEventListener("click", function (e) {
    var col = e.target.closest(".fr-col"); if (!col || over) return;
    if (vsCpu && turn !== 1) return;
    if (!play(+col.dataset.c)) return;
    if (vsCpu && !over) { msg.textContent = "Thinking…"; setTimeout(function () { play(cpuMove()); if (!over) msg.textContent = "Your move."; }, 280); }
  });
  el.querySelector("#fr-m").addEventListener("change", function (e) { vsCpu = e.target.value !== "pvp"; if (vsCpu) depth = +e.target.value; reset(); });
  el.querySelector("[data-new]").addEventListener("click", reset);
  score(); reset();
})();
