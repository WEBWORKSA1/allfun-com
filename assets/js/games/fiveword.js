/* FiveWord — daily five-letter word guess (original implementation) */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game");
  if (!el) return;
  var ANS = [], VALID = null, mode = "daily", answer = "", guesses = [], cur = "", done = false, won = false, dayNo = AF.dayNumber();
  var ROWS = 6, LEN = 5;
  el.innerHTML =
    '<div class="stage-bar"><div class="seg" role="tablist" aria-label="Mode">' +
    '<button class="segbtn" role="tab" data-mode="daily" aria-selected="true">Daily #' + dayNo + '</button>' +
    '<button class="segbtn" role="tab" data-mode="practice" aria-selected="false">Practice</button></div>' +
    '<div class="stats"><div class="stat"><small>Played</small><b data-s="played">0</b></div><div class="stat"><small>Win %</small><b data-s="pct">0</b></div><div class="stat"><small>Streak</small><b data-s="streak">0</b></div></div></div>' +
    '<div class="fw-board" aria-label="Guess board" role="grid"></div>' +
    '<p class="game-msg" aria-live="polite"></p>' +
    '<div class="fw-actions btn-row" hidden><button class="btn sun sm" data-act="share">Share result</button><button class="btn ghost sm" data-act="again">Play a practice word</button></div>' +
    '<div class="fw-keys" aria-label="Keyboard"></div>';
  var board = el.querySelector(".fw-board"), msg = el.querySelector(".game-msg"), keys = el.querySelector(".fw-keys"), actions = el.querySelector(".fw-actions");
  for (var r = 0; r < ROWS; r++) {
    var row = document.createElement("div"); row.className = "fw-row"; row.setAttribute("role", "row");
    for (var c = 0; c < LEN; c++) { var t = document.createElement("div"); t.className = "fw-tile"; t.setAttribute("role", "gridcell"); row.appendChild(t); }
    board.appendChild(row);
  }
  ["qwertyuiop", "asdfghjkl", "+zxcvbnm-"].forEach(function (line) {
    var kr = document.createElement("div"); kr.className = "fw-krow";
    line.split("").forEach(function (ch) {
      var b = document.createElement("button"); b.type = "button"; b.className = "fw-key";
      if (ch === "+") { b.textContent = "Enter"; b.dataset.k = "Enter"; b.classList.add("wide"); }
      else if (ch === "-") { b.textContent = "⌫"; b.dataset.k = "Backspace"; b.setAttribute("aria-label", "Delete letter"); b.classList.add("wide"); }
      else { b.textContent = ch; b.dataset.k = ch; }
      kr.appendChild(b);
    });
    keys.appendChild(kr);
  });

  function say(t) { msg.textContent = t; }
  function stats() { return AF.store.json("af-fw-stats", { played: 0, wins: 0, streak: 0, max: 0, last: 0, dist: [0, 0, 0, 0, 0, 0] }); }
  function showStats() {
    var s = stats();
    el.querySelector('[data-s="played"]').textContent = s.played;
    el.querySelector('[data-s="pct"]').textContent = s.played ? Math.round(100 * s.wins / s.played) : 0;
    el.querySelector('[data-s="streak"]').textContent = s.streak;
  }
  function score(g, a) {
    var res = Array(LEN).fill("absent"), pool = {};
    for (var i = 0; i < LEN; i++) { if (g[i] === a[i]) res[i] = "correct"; else pool[a[i]] = (pool[a[i]] || 0) + 1; }
    for (i = 0; i < LEN; i++) { if (res[i] !== "correct" && pool[g[i]]) { res[i] = "present"; pool[g[i]]--; } }
    return res;
  }
  function paint() {
    var rows = board.children, keyState = {};
    for (var r = 0; r < ROWS; r++) {
      var word = r < guesses.length ? guesses[r] : (r === guesses.length ? cur : ""), sc = r < guesses.length ? score(guesses[r], answer) : null;
      for (var c = 0; c < LEN; c++) {
        var t = rows[r].children[c]; t.textContent = word[c] || ""; t.className = "fw-tile" + (word[c] ? " filled" : "") + (sc ? " " + sc[c] : "");
        t.setAttribute("aria-label", (word[c] || "blank") + (sc ? " " + sc[c] : ""));
        if (sc) { var k = word[c], rank = { correct: 3, present: 2, absent: 1 }; if (!keyState[k] || rank[sc[c]] > rank[keyState[k]]) keyState[k] = sc[c]; }
      }
    }
    keys.querySelectorAll(".fw-key").forEach(function (b) { b.classList.remove("correct", "present", "absent"); if (keyState[b.dataset.k]) b.classList.add(keyState[b.dataset.k]); });
    actions.hidden = !done;
  }
  function save() { if (mode === "daily") AF.store.put("af-fw-" + AF.today(), { g: guesses, done: done, won: won }); }
  function finish(w) {
    done = true; won = w;
    if (mode === "daily") {
      var s = stats();
      if (s.last !== dayNo) {
        s.played++; if (w) { s.wins++; s.dist[guesses.length - 1]++; s.streak = (s.last === dayNo - 1 ? s.streak : 0) + 1; s.max = Math.max(s.max, s.streak); } else s.streak = 0;
        s.last = dayNo; AF.store.put("af-fw-stats", s);
      }
      AF.markDaily("fiveword"); showStats();
    }
    say(w ? ["Genius!", "Brilliant!", "Impressive!", "Splendid!", "Great!", "Phew!"][guesses.length - 1] + " Solved in " + guesses.length + "." : "The word was " + answer.toUpperCase() + ". New word tomorrow.");
  }
  function submit() {
    if (done) return;
    if (cur.length < LEN) { say("Not enough letters"); shake(); return; }
    if (VALID && !VALID.has(cur)) { say("Not in the word list"); shake(); return; }
    guesses.push(cur); cur = ""; say("");
    if (guesses[guesses.length - 1] === answer) finish(true); else if (guesses.length === ROWS) finish(false);
    save(); paint();
  }
  function shake() { var row = board.children[guesses.length]; if (!row) return; row.classList.remove("shake"); void row.offsetWidth; row.classList.add("shake"); }
  function press(k) {
    if (done || !answer) return;
    if (k === "Enter") return submit();
    if (k === "Backspace") { cur = cur.slice(0, -1); return paint(); }
    if (/^[a-z]$/.test(k) && cur.length < LEN) { cur += k; paint(); }
  }
  keys.addEventListener("click", function (e) { var b = e.target.closest(".fw-key"); if (b) { press(b.dataset.k); b.blur(); } });
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest && e.target.closest("input,textarea,select")) return;
    var k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    if (k === "Enter" || k === "Backspace" || /^[a-z]$/.test(k)) { e.preventDefault(); press(k); }
  });
  function start(m) {
    mode = m; cur = ""; done = false; won = false;
    el.querySelectorAll(".segbtn").forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.mode === m)); });
    if (m === "daily") {
      answer = ANS[(dayNo - 1 + ANS.length * 10) % ANS.length];
      var st = AF.store.json("af-fw-" + AF.today(), null);
      guesses = st ? st.g : []; done = st ? st.done : false; won = st ? st.won : false;
      say(done ? (won ? "You solved today's word. Come back tomorrow!" : "Today's word was " + answer.toUpperCase() + ".") : "Guess the five-letter word in six tries.");
    } else {
      answer = ANS[Math.floor(Math.random() * ANS.length)]; guesses = []; say("Practice word — no streak at stake.");
    }
    paint();
  }
  el.querySelectorAll(".segbtn").forEach(function (b) { b.addEventListener("click", function () { start(b.dataset.mode); }); });
  actions.addEventListener("click", function (e) {
    var a = e.target.getAttribute("data-act");
    if (a === "again") start("practice");
    if (a === "share") {
      var grid = guesses.map(function (g) { return score(g, answer).map(function (s) { return s === "correct" ? "🟩" : s === "present" ? "🟨" : "⬜"; }).join(""); }).join("\n");
      AF.share((mode === "daily" ? "AllFun FiveWord #" + dayNo : "AllFun FiveWord practice") + " " + (won ? guesses.length : "X") + "/6\n" + grid + "\n");
    }
  });
  fetch(AF.root + "assets/data/words5.json").then(function (r) { return r.json(); }).then(function (d) {
    for (var i = 0; i < d.answers.length; i += 5) ANS.push(d.answers.substr(i, 5));
    VALID = new Set(); for (i = 0; i < d.valid.length; i += 5) VALID.add(d.valid.substr(i, 5));
    showStats(); start("daily");
  }).catch(function () { say("Couldn't load the word list. Refresh to try again."); });
})();
