/* Tic-Tac-Toe — vs computer (easy / smart / unbeatable) or a friend */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  var b, turn, over, busy = false, mode = "hard", youFirst = true, tally = AF.store.json("af-ttt", { x: 0, o: 0, d: 0 });
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<label class="vh" for="tt-m">Opponent</label><select id="tt-m" class="mini-select"><option value="easy">Computer · Easy</option><option value="smart">Computer · Smart</option><option value="hard" selected>Computer · Unbeatable</option><option value="pvp">Friend (same device)</option></select>' +
    '<button class="btn sun sm" data-new>New round</button></div>' +
    '<div class="stats"><div class="stat"><small>X wins</small><b data-t="x">0</b></div><div class="stat"><small>O wins</small><b data-t="o">0</b></div><div class="stat"><small>Draws</small><b data-t="d">0</b></div></div></div>' +
    '<div class="ttt" role="grid" aria-label="Tic-tac-toe board"></div><p class="game-msg" aria-live="polite"></p>';
  var g = el.querySelector(".ttt"), msg = el.querySelector(".game-msg");
  for (var i = 0; i < 9; i++) { var c = document.createElement("button"); c.type = "button"; c.className = "ttt-cell"; c.dataset.i = i; c.setAttribute("aria-label", "Square " + (i + 1) + ", empty"); g.appendChild(c); }
  function win(s) { for (var k = 0; k < 8; k++) { var l = LINES[k]; if (s[l[0]] && s[l[0]] === s[l[1]] && s[l[1]] === s[l[2]]) return { p: s[l[0]], l: l }; } return null; }
  function mm(s, p) {
    var w = win(s); if (w) return w.p === "O" ? 10 : -10; if (s.every(Boolean)) return 0;
    var best = p === "O" ? -99 : 99;
    for (var k = 0; k < 9; k++) if (!s[k]) { s[k] = p; var v = mm(s, p === "O" ? "X" : "O"); s[k] = ""; v += v > 0 ? -1 : v < 0 ? 1 : 0; best = p === "O" ? Math.max(best, v) : Math.min(best, v); }
    return best;
  }
  function cpu() {
    var free = b.map(function (v, k) { return v ? -1 : k; }).filter(function (k) { return k > -1; });
    if (mode === "easy" || (mode === "smart" && Math.random() < 0.3)) return free[Math.floor(Math.random() * free.length)];
    var best = -99, pick = free[0];
    AF.shuffle(free).forEach(function (k) { b[k] = "O"; var v = mm(b, "X"); b[k] = ""; if (v > best) { best = v; pick = k; } });
    return pick;
  }
  function draw(l) {
    for (var k = 0; k < 9; k++) { var c = g.children[k]; c.textContent = b[k]; c.className = "ttt-cell" + (b[k] ? " " + b[k].toLowerCase() : "") + (l && l.indexOf(k) > -1 ? " win" : ""); c.setAttribute("aria-label", "Square " + (k + 1) + ", " + (b[k] || "empty")); }
    ["x", "o", "d"].forEach(function (k) { el.querySelector('[data-t="' + k + '"]').textContent = tally[k]; });
  }
  function end() {
    var w = win(b);
    if (w) { over = true; tally[w.p.toLowerCase()]++; AF.store.put("af-ttt", tally); draw(w.l); msg.textContent = mode === "pvp" ? w.p + " wins!" : (w.p === "X" ? "You win! 🎉" : "Computer wins."); return true; }
    if (b.every(Boolean)) { over = true; tally.d++; AF.store.put("af-ttt", tally); draw(); msg.textContent = "Draw. Perfect play from both sides."; return true; }
    return false;
  }
  function reset() {
    b = Array(9).fill(""); over = false; turn = "X"; draw();
    if (mode !== "pvp" && !youFirst) { b[cpu()] = "O"; draw(); }
    msg.textContent = mode === "pvp" ? "X goes first." : "You're X. " + (youFirst ? "Your move." : "Computer opened — your move.");
    youFirst = !youFirst;
  }
  g.addEventListener("click", function (e) {
    var c = e.target.closest(".ttt-cell"); if (!c || over || busy || b[c.dataset.i]) return;
    if (mode === "pvp") { b[c.dataset.i] = turn; turn = turn === "X" ? "O" : "X"; draw(); if (!end()) msg.textContent = turn + "'s turn."; return; }
    b[c.dataset.i] = "X"; draw(); if (end()) return;
    busy = true;
    setTimeout(function () { b[cpu()] = "O"; draw(); end(); busy = false; }, 220);
  });
  el.querySelector("#tt-m").addEventListener("change", function (e) { mode = e.target.value; youFirst = true; reset(); });
  el.querySelector("[data-new]").addEventListener("click", reset);
  reset();
})();
