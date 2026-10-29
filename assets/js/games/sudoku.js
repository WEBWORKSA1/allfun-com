/* Sudoku — generated puzzles with a unique solution; daily puzzle seeded by date */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var CLUES = { easy: 40, medium: 32, hard: 27 };
  var level = "easy", daily = false, puzzle, solution, board, notes, given, sel = -1, noteMode = false, mistakes = 0, t0, timer, done = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<label class="vh" for="sd-l">Puzzle</label><select id="sd-l" class="mini-select"><option value="daily">Daily puzzle</option><option value="easy" selected>Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select>' +
    '<button class="btn sun sm" data-new>New puzzle</button></div>' +
    '<div class="stats"><div class="stat"><small>Time</small><b data-time>0:00</b></div><div class="stat"><small>Mistakes</small><b data-mis>0</b></div></div></div>' +
    '<div class="sd-grid" role="grid" aria-label="Sudoku grid"></div>' +
    '<div class="sd-pad"></div>' +
    '<div class="btn-row sd-tools"><button class="btn ghost sm" data-notes aria-pressed="false">✏️ Notes: off</button><button class="btn ghost sm" data-erase>Erase</button><button class="btn ghost sm" data-hint>Hint</button><button class="btn ghost sm" data-check>Check</button></div>' +
    '<p class="game-msg" aria-live="polite"></p>';
  var gridEl = el.querySelector(".sd-grid"), pad = el.querySelector(".sd-pad"), msg = el.querySelector(".game-msg");
  for (var d = 1; d <= 9; d++) { var b = document.createElement("button"); b.type = "button"; b.className = "sd-num"; b.textContent = d; b.dataset.n = d; pad.appendChild(b); }
  for (var i = 0; i < 81; i++) { var c = document.createElement("button"); c.type = "button"; c.className = "sd-cell"; c.dataset.i = i; c.setAttribute("role", "gridcell"); gridEl.appendChild(c); }
  var cellEls = gridEl.children;

  function rowOf(i) { return Math.floor(i / 9); } function colOf(i) { return i % 9; } function boxOf(i) { return Math.floor(rowOf(i) / 3) * 3 + Math.floor(colOf(i) / 3); }
  function solve(g, rnd, limit) {
    var rows = Array(9).fill(0), cols = Array(9).fill(0), boxes = Array(9).fill(0), count = 0, empties = [];
    for (var i = 0; i < 81; i++) { if (g[i]) { var m = 1 << g[i]; rows[rowOf(i)] |= m; cols[colOf(i)] |= m; boxes[boxOf(i)] |= m; } else empties.push(i); }
    function rec(k) {
      if (k === empties.length) { count++; return count >= limit; }
      var best = -1, bestMask = 0, bestCount = 10;
      for (var j = k; j < empties.length; j++) {
        var x = empties[j], used = rows[rowOf(x)] | cols[colOf(x)] | boxes[boxOf(x)], free = 0;
        for (var v = 1; v <= 9; v++) if (!(used & (1 << v))) free++;
        if (free < bestCount) { bestCount = free; best = j; bestMask = used; if (free <= 1) break; }
      }
      if (bestCount === 0) return false;
      var t = empties[k]; empties[k] = empties[best]; empties[best] = t;
      var cell = empties[k], vals = [1, 2, 3, 4, 5, 6, 7, 8, 9];
      if (rnd) vals = AF.shuffle(vals, rnd);
      for (var n = 0; n < 9; n++) {
        var val = vals[n], bit = 1 << val; if (bestMask & bit) continue;
        g[cell] = val; rows[rowOf(cell)] |= bit; cols[colOf(cell)] |= bit; boxes[boxOf(cell)] |= bit;
        if (rec(k + 1)) return true;
        g[cell] = 0; rows[rowOf(cell)] &= ~bit; cols[colOf(cell)] &= ~bit; boxes[boxOf(cell)] &= ~bit;
      }
      empties[best] = empties[k]; empties[k] = t;
      return false;
    }
    rec(0); return count;
  }
  function generate(lvl, rnd) {
    var full = Array(81).fill(0); solve(full, rnd, 1);
    var p = full.slice(), order = AF.shuffle(Array.from({ length: 81 }, function (_, k) { return k; }), rnd), clues = 81;
    for (var k = 0; k < order.length && clues > CLUES[lvl]; k++) {
      var idx = order[k], keep = p[idx]; p[idx] = 0;
      if (solve(p.slice(), null, 2) !== 1) p[idx] = keep; else clues--;
    }
    return { p: p, s: full };
  }
  function fmt(s) { return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }
  function key() { return "af-sd-daily-" + AF.today(); }
  function newGame() {
    clearInterval(timer); done = false; mistakes = 0; sel = -1;
    var g;
    if (daily) {
      var saved = AF.store.json(key(), null);
      g = generate("medium", AF.rng("sudoku-" + AF.today()));
      puzzle = g.p; solution = g.s;
      board = saved ? saved.b : puzzle.slice(); mistakes = saved ? saved.m : 0; done = saved ? saved.d : false;
    } else { g = generate(level, Math.random); puzzle = g.p; solution = g.s; board = puzzle.slice(); }
    given = puzzle.map(Boolean); notes = Array.from({ length: 81 }, function () { return new Set(); });
    t0 = Date.now(); el.querySelector("[data-mis]").textContent = mistakes;
    timer = setInterval(function () { if (!done) el.querySelector("[data-time]").textContent = fmt(Math.floor((Date.now() - t0) / 1000)); }, 500);
    msg.textContent = daily ? (done ? "You solved today's puzzle. A new one arrives tomorrow." : "Today's puzzle — same grid for everyone.") : "Fill every row, column and 3×3 box with 1–9.";
    draw();
  }
  function draw() {
    for (var i = 0; i < 81; i++) {
      var c = cellEls[i], v = board[i], cls = "sd-cell";
      if (given[i]) cls += " given"; if (i === sel) cls += " sel";
      if (sel > -1 && i !== sel && (rowOf(i) === rowOf(sel) || colOf(i) === colOf(sel) || boxOf(i) === boxOf(sel))) cls += " peer";
      if (sel > -1 && v && board[sel] === v) cls += " same";
      if (v && !given[i] && v !== solution[i]) cls += " bad";
      if (colOf(i) % 3 === 2 && colOf(i) < 8) cls += " br"; if (rowOf(i) % 3 === 2 && rowOf(i) < 8) cls += " bb";
      c.className = cls;
      if (v) c.textContent = v;
      else if (notes[i].size) c.innerHTML = '<span class="sd-notes">' + [1, 2, 3, 4, 5, 6, 7, 8, 9].map(function (n) { return '<i>' + (notes[i].has(n) ? n : "") + '</i>'; }).join("") + "</span>";
      else c.textContent = "";
      c.setAttribute("aria-label", "Row " + (rowOf(i) + 1) + ", column " + (colOf(i) + 1) + ": " + (v || "empty"));
    }
  }
  function input(n) {
    if (sel < 0 || given[sel] || done) return;
    if (noteMode && n) { notes[sel].has(n) ? notes[sel].delete(n) : notes[sel].add(n); board[sel] = 0; draw(); return; }
    board[sel] = n; notes[sel].clear();
    if (n && n !== solution[sel]) { mistakes++; el.querySelector("[data-mis]").textContent = mistakes; }
    if (n === solution[sel]) { var r = rowOf(sel), col = colOf(sel), bx = boxOf(sel); for (var i = 0; i < 81; i++) if (rowOf(i) === r || colOf(i) === col || boxOf(i) === bx) notes[i].delete(n); }
    if (daily) AF.store.put(key(), { b: board, m: mistakes, d: false });
    draw(); checkWin();
  }
  function checkWin() {
    for (var i = 0; i < 81; i++) if (board[i] !== solution[i]) return;
    done = true; clearInterval(timer);
    var secs = Math.floor((Date.now() - t0) / 1000);
    msg.textContent = "Solved in " + fmt(secs) + " with " + mistakes + " mistake" + (mistakes === 1 ? "" : "s") + "!";
    if (daily) { AF.store.put(key(), { b: board, m: mistakes, d: true }); AF.markDaily("sudoku"); }
    else if (AF.best("sd-" + level, secs, true)) msg.textContent += " New best time.";
  }
  gridEl.addEventListener("click", function (e) { var c = e.target.closest(".sd-cell"); if (!c) return; sel = +c.dataset.i; draw(); });
  pad.addEventListener("click", function (e) { var b = e.target.closest(".sd-num"); if (b) input(+b.dataset.n); });
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input,textarea,select")) return;
    if (/^[1-9]$/.test(e.key)) { input(+e.key); e.preventDefault(); }
    else if (e.key === "Backspace" || e.key === "Delete" || e.key === "0") { input(0); e.preventDefault(); }
    else if (e.key === "n" || e.key === "N") toggleNotes();
    else if (sel > -1 && e.key.indexOf("Arrow") === 0) {
      e.preventDefault(); var r = rowOf(sel), c = colOf(sel);
      if (e.key === "ArrowUp") r = (r + 8) % 9; if (e.key === "ArrowDown") r = (r + 1) % 9; if (e.key === "ArrowLeft") c = (c + 8) % 9; if (e.key === "ArrowRight") c = (c + 1) % 9;
      sel = r * 9 + c; draw(); cellEls[sel].focus();
    }
  });
  function toggleNotes() { noteMode = !noteMode; var b = el.querySelector("[data-notes]"); b.setAttribute("aria-pressed", noteMode); b.textContent = "✏️ Notes: " + (noteMode ? "on" : "off"); }
  el.querySelector("[data-notes]").addEventListener("click", toggleNotes);
  el.querySelector("[data-erase]").addEventListener("click", function () { if (sel > -1 && !given[sel]) { board[sel] = 0; notes[sel].clear(); draw(); } });
  el.querySelector("[data-hint]").addEventListener("click", function () {
    if (done) return;
    var target = sel > -1 && !given[sel] && board[sel] !== solution[sel] ? sel : board.findIndex(function (v, i) { return v !== solution[i]; });
    if (target < 0) return; sel = target; board[target] = solution[target]; notes[target].clear(); msg.textContent = "Hint placed."; draw(); checkWin();
  });
  el.querySelector("[data-check]").addEventListener("click", function () {
    var wrong = board.filter(function (v, i) { return v && v !== solution[i]; }).length;
    msg.textContent = wrong ? wrong + " square" + (wrong > 1 ? "s are" : " is") + " wrong — shown in pink." : "Everything so far is correct.";
  });
  el.querySelector("#sd-l").addEventListener("change", function (e) { daily = e.target.value === "daily"; if (!daily) level = e.target.value; newGame(); });
  el.querySelector("[data-new]").addEventListener("click", function () { if (daily) { msg.textContent = "There's one daily puzzle per day — switch to Easy, Medium or Hard for more."; return; } newGame(); });
  if (location.hash === "#daily") { daily = true; el.querySelector("#sd-l").value = "daily"; }
  newGame();
})();
