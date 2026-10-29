/* Home hero wheel + daily widgets (home and daily pages) */
(function () {
  "use strict";
  var AF = window.AF;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var SEGS = [
    { label: "Word game", em: "🔤", picks: [["play/fiveword.html", "Today's FiveWord", "Six tries, one hidden word."], ["play/typing-test.html", "Typing Test", "How many words a minute?"]] },
    { label: "Brain puzzle", em: "🧩", picks: [["play/sudoku.html", "Sudoku", "Fresh grid, unique solution."], ["play/minesweeper.html", "Minesweeper", "Logic, flags and nerves."], ["play/tile-merge.html", "Tile Merge", "Slide, merge, reach 2048."]] },
    { label: "Arcade", em: "🕹️", picks: [["play/snake.html", "Snake", "Eat stars, grow long."], ["play/mole-pop.html", "Mole Pop", "30 seconds of chaos."]] },
    { label: "Trivia", em: "❓", picks: [["quizzes/general-knowledge.html", "General Knowledge Quiz", "15 questions, instant answers."], ["quizzes/space.html", "Space Quiz", "How cosmic is your brain?"], ["quizzes/animals.html", "Animal Quiz", "Wild facts, real answers."]] },
    { label: "Party tool", em: "🎭", picks: [["tools/charades-generator.html", "Charades Generator", "Words, timer and scores."], ["tools/team-picker.html", "Team Picker", "Fair teams in one click."]] },
    { label: "Fun facts", em: "💡", picks: [["facts/random-fun-facts.html", "75 Random Fun Facts", "Prepare to say 'wait, really?'"], ["facts/fun-facts-about-space.html", "Space Facts", "The universe is weird."]] },
    { label: "Beat boredom", em: "🎈", picks: [["tools/bored-button.html", "Bored Button", "One press, one idea."], ["ideas/fun-things-to-do-when-bored.html", "101 Things to Do When Bored", "A list for every mood."]] },
    { label: "Reflexes", em: "⚡", picks: [["play/reaction-time.html", "Reaction Time", "Wait for green… tap!"], ["play/pattern-echo.html", "Pattern Echo", "Watch, listen, repeat."]] },
    { label: "About you", em: "🎨", picks: [["quizzes/fun-style.html", "What's Your Fun Style?", "10 questions, 6 personalities."]] },
    { label: "Dilemmas", em: "🤔", picks: [["tools/would-you-rather.html", "Would You Rather", "220 tough-but-silly choices."]] }
  ];
  var cv = document.getElementById("hero-wheel");
  if (cv && window.AFWheel) {
    var out = document.getElementById("hero-pick"), hub = document.querySelector(".wheel-hub");
    var w = new window.AFWheel(cv, { items: SEGS.map(function (s) { return { label: s.em + " " + s.label, seg: s }; }), onResult: function (it) {
      var s = it.data.seg, p = s.picks[Math.floor(Math.random() * s.picks.length)];
      out.innerHTML = '<div class="pick pop-in"><span class="em" aria-hidden="true">' + s.em + '</span><div><b>' + esc(p[1]) + '</b><span class="muted small">' + esc(p[2]) + '</span></div><a class="btn sm" href="' + AF.root + p[0] + '">Play</a></div>';
      hub.disabled = false; hub.textContent = "Again";
    } });
    hub.addEventListener("click", function () { hub.disabled = true; out.innerHTML = ""; w.spin(); });
  }

  /* Daily status badges */
  document.querySelectorAll("[data-daily-status]").forEach(function (n) {
    var g = n.getAttribute("data-daily-status"); if (AF.doneToday(g)) { n.textContent = "✓ Done today"; n.style.setProperty("--c", "var(--mint)"); }
  });
  document.querySelectorAll("[data-dayno]").forEach(function (n) { n.textContent = AF.dayNumber(); });
  document.querySelectorAll("[data-date]").forEach(function (n) { n.textContent = new Date().toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" }); });

  /* Fact of the day */
  var fb = document.getElementById("fact-of-day");
  if (fb) fetch(AF.root + "assets/data/facts.json").then(function (r) { return r.json(); }).then(function (all) {
    var f = all[AF.hash("fact-" + AF.today()) % all.length];
    fb.innerHTML = '<p class="quiz-q" style="margin:0 0 8px">' + esc(f.h) + '</p><p class="muted">' + esc(f.t) + '</p><p class="small"><a href="' + AF.root + "facts/" + f.s + '.html">More like this</a></p>';
  }).catch(function () {});

  /* Would-you-rather of the day */
  var wb = document.getElementById("wyr-of-day");
  if (wb) fetch(AF.root + "assets/data/wyr.json").then(function (r) { return r.json(); }).then(function (all) {
    var q = all[AF.hash("wyr-" + AF.today()) % all.length], k = "af-wyrday-" + AF.today(), mine = AF.store.get(k, "");
    wb.innerHTML = '<div class="wyr"><button type="button" class="a" data-v="a">' + esc(q.a) + '</button><span class="or">or</span><button type="button" class="b" data-v="b">' + esc(q.b) + "</button></div>";
    function lock(v) { wb.querySelectorAll("button").forEach(function (b) { b.disabled = true; if (b.dataset.v === v) b.classList.add("picked"); }); }
    if (mine) lock(mine);
    wb.querySelectorAll("button").forEach(function (b) { b.addEventListener("click", function () { AF.store.set(k, b.dataset.v); lock(b.dataset.v); AF.toast("Locked in. Ask a friend which they'd pick!"); }); });
  }).catch(function () {});
})();
