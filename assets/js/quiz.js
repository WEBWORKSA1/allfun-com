/* AllFun quiz engine — trivia, personality, and the Daily 5 */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("quiz"); if (!el) return;
  var slug = el.getAttribute("data-quiz"), isDaily = el.hasAttribute("data-daily");
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  fetch(AF.root + "assets/data/quizzes.json").then(function (r) { return r.json(); }).then(function (all) {
    if (isDaily) return daily(all);
    var q = all[slug]; if (!q) { el.textContent = "Quiz not found."; return; }
    if (q.type === "personality") personality(q); else trivia(q.questions, q.title, "quiz-" + slug);
  }).catch(function () { el.innerHTML = '<p class="form-status err">The quiz didn\'t load. Refresh to try again.</p>'; });

  function trivia(questions, title, key, onDone) {
    var i = 0, right = 0, order = questions;
    function q() {
      var x = order[i];
      el.innerHTML = '<div class="progress" aria-hidden="true"><i style="width:' + (i / order.length * 100) + '%"></i></div>' +
        '<p class="muted small" style="margin-top:12px">Question ' + (i + 1) + ' of ' + order.length + ' · Score ' + right + '</p>' +
        '<p class="quiz-q" tabindex="-1">' + esc(x.q) + '</p><div class="answers">' +
        x.options.map(function (o, k) { return '<button type="button" class="answer" data-k="' + k + '">' + esc(o) + "</button>"; }).join("") + '</div><div class="quiz-after" aria-live="polite"></div>';
      el.querySelector(".quiz-q").focus({ preventScroll: true });
      el.querySelectorAll(".answer").forEach(function (b) {
        b.addEventListener("click", function () {
          var k = +b.dataset.k, ok = k === x.answer; if (ok) right++;
          el.querySelectorAll(".answer").forEach(function (a) { a.disabled = true; if (+a.dataset.k === x.answer) a.classList.add("right"); });
          if (!ok) b.classList.add("wrong");
          el.querySelector(".quiz-after").innerHTML = '<div class="why"><b>' + (ok ? "Correct! " : "Not quite. ") + "</b>" + esc(x.why || "") + '</div><p style="margin-top:14px"><button type="button" class="btn sun" data-next>' + (i + 1 < order.length ? "Next question" : "See my score") + "</button></p>";
          var nx = el.querySelector("[data-next]"); nx.focus({ preventScroll: true });
          nx.addEventListener("click", function () { i++; if (i < order.length) q(); else end(); });
        });
      });
    }
    function end() {
      var pct = Math.round(100 * right / order.length), nb = AF.best(key, right);
      var verdict = pct === 100 ? "Flawless. Take a bow." : pct >= 80 ? "Seriously sharp." : pct >= 60 ? "Solid score." : pct >= 40 ? "Not bad — rematch?" : "Every expert started here.";
      el.innerHTML = '<div class="result-card"><div class="big">' + right + "/" + order.length + '</div><p class="quiz-q">' + verdict + "</p>" +
        (nb && !isDaily ? '<p><span class="streak">New personal best</span></p>' : "") +
        '<div class="btn-row" style="justify-content:center;margin-top:16px">' + (isDaily ? "" : '<button type="button" class="btn sun" data-retry>Play again</button>') +
        '<button type="button" class="btn ghost" data-sh>Share score</button></div></div>';
      var r = el.querySelector("[data-retry]"); if (r) r.addEventListener("click", function () { i = 0; right = 0; order = AF.shuffle(questions); q(); });
      el.querySelector("[data-sh]").addEventListener("click", function () { AF.share("I scored " + right + "/" + order.length + " on the " + title + " at AllFun. Can you beat it?"); });
      if (onDone) onDone(right, order.length);
    }
    q();
  }

  function personality(Q) {
    var i = 0, tally = {};
    function q() {
      var x = Q.questions[i];
      el.innerHTML = '<div class="progress" aria-hidden="true"><i style="width:' + (i / Q.questions.length * 100) + '%"></i></div>' +
        '<p class="muted small" style="margin-top:12px">Question ' + (i + 1) + " of " + Q.questions.length + '</p><p class="quiz-q" tabindex="-1">' + esc(x.q) + '</p><div class="answers">' +
        AF.shuffle(x.options).map(function (o) { return '<button type="button" class="answer" data-r="' + o.r + '">' + esc(o.t) + "</button>"; }).join("") + "</div>";
      el.querySelector(".quiz-q").focus({ preventScroll: true });
      el.querySelectorAll(".answer").forEach(function (b) { b.addEventListener("click", function () { tally[b.dataset.r] = (tally[b.dataset.r] || 0) + 1; i++; i < Q.questions.length ? q() : end(); }); });
    }
    function end() {
      var top = Object.keys(tally).sort(function (a, b) { return tally[b] - tally[a]; })[0], r = Q.results[top];
      AF.store.set("af-funstyle", top);
      el.innerHTML = '<div class="result-card"><div class="big" aria-hidden="true">' + r.emoji + '</div><p class="muted">Your fun style is</p><h2>' + esc(r.name) + '</h2><p style="max-width:56ch;margin:0 auto 18px">' + esc(r.text) + '</p>' +
        '<h3>Try these next</h3><div class="chips" style="justify-content:center">' + r.picks.map(function (p) { return '<a class="chip" href="' + AF.root + p.href + '">' + esc(p.label) + "</a>"; }).join("") + '</div>' +
        '<div class="btn-row" style="justify-content:center;margin-top:20px"><button type="button" class="btn sun" data-retry>Retake quiz</button><button type="button" class="btn ghost" data-sh>Share my result</button></div></div>';
      el.querySelector("[data-retry]").addEventListener("click", function () { i = 0; tally = {}; q(); });
      el.querySelector("[data-sh]").addEventListener("click", function () { AF.share("My fun style is " + r.name + " " + r.emoji + " — what's yours?"); });
    }
    q();
  }

  function daily(all) {
    var pool = []; Object.keys(all).forEach(function (k) { if (all[k].type === "trivia") all[k].questions.forEach(function (x) { pool.push(x); }); });
    var rnd = AF.rng("daily5-" + AF.today()), picks = AF.shuffle(pool, rnd).slice(0, 5), key = "af-d5-" + AF.today(), prev = AF.store.json(key, null);
    if (prev) { el.innerHTML = '<div class="result-card"><div class="big">' + prev.r + "/5</div><p class=\"quiz-q\">You've played today's Daily 5.</p><p class=\"muted\">Five fresh questions arrive tomorrow. Want more now? Try a full quiz.</p><p><a class=\"btn sun\" href=\"" + AF.root + 'quizzes/index.html">Browse quizzes</a></p></div>'; return; }
    trivia(picks, "Daily 5", "daily5", function (r) { AF.store.put(key, { r: r }); AF.markDaily("trivia"); });
  }
})();
