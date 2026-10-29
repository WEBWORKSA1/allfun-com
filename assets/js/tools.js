/* AllFun fun tools — one file, initialised by <div id="tool" data-tool="…"> */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("tool"); if (!el) return;
  var T = el.getAttribute("data-tool");
  function $(s) { return el.querySelector(s); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function rint(n) { if (window.crypto && crypto.getRandomValues) { var a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; } return Math.floor(Math.random() * n); }
  function load(name) { return fetch(AF.root + "assets/data/" + name + ".json").then(function (r) { return r.json(); }); }

  /* ---------- Spin the wheel ---------- */
  if (T === "wheel") {
    var PRESETS = {
      "Yes or no": "Yes\nNo",
      "What's for dinner?": "Pizza\nTacos\nPasta\nStir-fry\nBurgers\nSoup & sandwiches\nBreakfast for dinner\nSushi night\nCurry\nBig salad",
      "Weekend plan": "Hike\nMovie marathon\nBoard games\nBake something\nPicnic\nMuseum visit\nBike ride\nCraft project",
      "Chore picker": "Dishes\nVacuum\nLaundry\nTrash & recycling\nWipe counters\nWater plants",
      "Numbers 1–10": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10",
      "Game night": "Charades\nTrivia\nDrawing game\nWould you rather\nWord guess\nMemory match"
    };
    var ta = $("#wh-items"), out = $("#wh-out"), hist = [], wheel;
    var fromHash = decodeURIComponent((location.hash.match(/items=([^&]+)/) || [])[1] || "");
    ta.value = fromHash ? fromHash.split("|").join("\n") : AF.store.get("af-wheel", PRESETS["What's for dinner?"]);
    function items() { return ta.value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean).slice(0, 60); }
    wheel = new window.AFWheel($("canvas"), { items: items(), sound: AF.store.get("af-wheel-sound", "1") === "1", onResult: function (it) {
      out.innerHTML = '<div class="pick pop-in"><span class="em">🎉</span><div><span class="muted small">The wheel says</span><b>' + esc(it.label) + '</b></div></div>';
      hist.unshift(it.label); $("#wh-hist").innerHTML = hist.slice(0, 12).map(function (h) { return "<span>" + esc(h) + "</span>"; }).join("");
      if ($("#wh-remove").checked) { var arr = items(), i = arr.indexOf(it.label); if (i > -1) arr.splice(i, 1); ta.value = arr.join("\n"); wheel.set(arr); }
      $(".wheel-hub").disabled = false;
    } });
    function spin() { if (items().length < 2) { out.textContent = "Add at least two entries."; return; } $(".wheel-hub").disabled = true; out.innerHTML = '<p class="muted">Spinning…</p>'; wheel.spin(); }
    ta.addEventListener("input", function () { wheel.set(items()); AF.store.set("af-wheel", ta.value); $("#wh-count").textContent = items().length; });
    $(".wheel-hub").addEventListener("click", spin);
    $("#wh-spin").addEventListener("click", spin);
    $("#wh-shuffle").addEventListener("click", function () { var a = AF.shuffle(items()); ta.value = a.join("\n"); wheel.set(a); });
    $("#wh-share").addEventListener("click", function () { AF.share("Spin my wheel:", location.href.split("#")[0] + "#items=" + encodeURIComponent(items().join("|"))); });
    var snd = $("#wh-sound"); snd.checked = wheel.sound; snd.addEventListener("change", function () { wheel.sound = snd.checked; AF.store.set("af-wheel-sound", snd.checked ? "1" : "0"); });
    var pre = $("#wh-presets");
    Object.keys(PRESETS).forEach(function (k) { var b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = k; b.addEventListener("click", function () { ta.value = PRESETS[k]; wheel.set(items()); $("#wh-count").textContent = items().length; }); pre.appendChild(b); });
    $("#wh-count").textContent = items().length;
    document.addEventListener("keydown", function (e) { if (e.key === " " && e.target === document.body) { e.preventDefault(); spin(); } });
  }

  /* ---------- Team picker ---------- */
  if (T === "teams") {
    var COLORS = ["var(--sun)", "var(--sky)", "var(--pop)", "var(--mint)", "var(--lilac)", "#FF9F45", "#7FD8FF", "#FF8FB1"];
    var NAMES = ["Thunder Otters", "Pixel Pandas", "Rocket Llamas", "Comet Crew", "Taco Titans", "Neon Narwhals", "Brainy Badgers", "Turbo Turtles", "Cosmic Koalas", "Mighty Muffins"];
    var tn = $("#tp-names"); tn.value = AF.store.get("af-teams", "Ava\nBen\nChloe\nDev\nEmma\nFinn\nGrace\nHugo\nIvy\nJay");
    function make() {
      var people = tn.value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean);
      AF.store.set("af-teams", tn.value);
      var mode = $("#tp-mode").value, n = Math.max(1, parseInt($("#tp-n").value, 10) || 2);
      var teams = mode === "count" ? n : Math.ceil(people.length / n);
      if (people.length < 2 || teams < 1) { $("#tp-out").innerHTML = '<p class="muted">Add at least two names.</p>'; return; }
      teams = Math.min(teams, people.length);
      var sh = AF.shuffle(people), buckets = []; for (var i = 0; i < teams; i++) buckets.push([]);
      sh.forEach(function (p, i) { buckets[i % teams].push(p); });
      var names = AF.shuffle(NAMES);
      $("#tp-out").innerHTML = '<div class="teams">' + buckets.map(function (b, i) { return '<div class="team" style="background:' + COLORS[i % COLORS.length] + '"><h3>' + esc($("#tp-fun").checked ? names[i % names.length] : "Team " + (i + 1)) + ' <small>(' + b.length + ')</small></h3><ul>' + b.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + "</ul></div>"; }).join("") + "</div>";
      $("#tp-copy").hidden = false;
      $("#tp-copy").onclick = function () { var txt = Array.prototype.map.call(el.querySelectorAll(".team"), function (t) { return t.querySelector("h3").textContent + ": " + Array.prototype.map.call(t.querySelectorAll("li"), function (l) { return l.textContent; }).join(", "); }).join("\n"); if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { AF.toast("Teams copied"); }); };
    }
    $("#tp-go").addEventListener("click", make);
    tn.addEventListener("input", function () { $("#tp-count").textContent = tn.value.split("\n").filter(function (s) { return s.trim(); }).length; });
    $("#tp-count").textContent = tn.value.split("\n").filter(function (s) { return s.trim(); }).length;
  }

  /* ---------- Coin flip ---------- */
  if (T === "coin") {
    var coin = $(".coin"), rot = 0, counts = AF.store.json("af-coin", { h: 0, t: 0 }), seq = [];
    function show() { $("#cf-h").textContent = counts.h; $("#cf-t").textContent = counts.t; $("#cf-hist").innerHTML = seq.slice(-20).map(function (s) { return "<span>" + s + "</span>"; }).join(""); }
    function flip() {
      var heads = rint(2) === 0; rot += 1800 + (heads ? (rot % 360 === 0 ? 0 : 180) : (rot % 360 === 0 ? 180 : 0));
      coin.style.transform = "rotateY(" + rot + "deg)"; $("#cf-flip").disabled = true; $("#cf-out").textContent = "…";
      setTimeout(function () {
        heads ? counts.h++ : counts.t++; seq.push(heads ? "H" : "T"); AF.store.put("af-coin", counts);
        $("#cf-out").textContent = heads ? "Heads!" : "Tails!"; $("#cf-flip").disabled = false; show();
        var bo = +$("#cf-bo").value; if (bo > 1) { var last = seq.slice(-bo), h = last.filter(function (x) { return x === "H"; }).length; if (last.length === bo || h > bo / 2 || (last.length - h) > bo / 2) { /* status only */ } $("#cf-series").textContent = "Last " + Math.min(bo, last.length) + ": " + h + " heads, " + (last.length - h) + " tails"; }
      }, 1150);
    }
    $("#cf-flip").addEventListener("click", flip); coin.addEventListener("click", flip);
    $("#cf-reset").addEventListener("click", function () { counts = { h: 0, t: 0 }; seq = []; AF.store.put("af-coin", counts); show(); $("#cf-series").textContent = ""; });
    show();
  }

  /* ---------- Dice ---------- */
  if (T === "dice") {
    var PIPS = { 1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8] }, dh = [];
    function roll() {
      var n = +$("#dr-n").value, sides = +$("#dr-s").value, vals = [], box = $(".dice"); box.innerHTML = "";
      for (var i = 0; i < n; i++) {
        var v = rint(sides) + 1; vals.push(v); var d = document.createElement("div"); d.className = "die roll";
        if (sides === 6) { for (var k = 0; k < 9; k++) { var p = document.createElement("i"); if (PIPS[v].indexOf(k) > -1) p.style.visibility = "visible"; d.appendChild(p); } }
        else { d.classList.add("big"); d.textContent = v; }
        d.setAttribute("aria-label", "Die showing " + v); box.appendChild(d);
      }
      var tot = vals.reduce(function (a, b) { return a + b; }, 0);
      $("#dr-out").textContent = n > 1 ? "Total " + tot : "You rolled " + tot;
      dh.unshift(vals.join("+") + (n > 1 ? "=" + tot : "")); $("#dr-hist").innerHTML = dh.slice(0, 12).map(function (h) { return "<span>" + h + "</span>"; }).join("");
    }
    $("#dr-roll").addEventListener("click", roll);
    document.addEventListener("keydown", function (e) { if ((e.key === " " || e.key === "r") && e.target === document.body) { e.preventDefault(); roll(); } });
    roll();
  }

  /* ---------- Bored button ---------- */
  if (T === "bored") {
    var ACTS = [], seen = [];
    load("activities").then(function (d) { ACTS = d; $("#bb-go").disabled = false; });
    function pickAct() {
      var f = { cat: $("#bb-cat").value, who: $("#bb-who").value, cost: $("#bb-cost").value, mins: +$("#bb-time").value };
      var pool = ACTS.filter(function (a) { return (!f.cat || a.cat === f.cat) && (!f.who || a.who === f.who || a.who === "any") && (!f.cost || a.cost === f.cost) && (!f.mins || a.mins <= f.mins); });
      if (!pool.length) { $("#bb-out").innerHTML = '<p class="muted">Nothing matches those filters. Loosen one and press again.</p>'; return; }
      var fresh = pool.filter(function (a) { return seen.indexOf(a.t) === -1; }); if (!fresh.length) { seen = []; fresh = pool; }
      var a = fresh[rint(fresh.length)]; seen.push(a.t);
      var tags = [a.cat, a.cost === "free" ? "Free" : a.cost === "low" ? "Low cost" : "Some cost", a.who === "any" ? "Anyone" : a.who[0].toUpperCase() + a.who.slice(1), "~" + (a.mins >= 60 ? a.mins / 60 + " hr" : a.mins + " min")];
      $("#bb-out").innerHTML = '<div class="big-card pop-in"><p class="quiz-q">' + esc(a.t) + '</p><div class="chips" style="justify-content:center">' + tags.map(function (t) { return '<span class="tag" style="--c:var(--sunk)">' + esc(t) + "</span>"; }).join("") + "</div>" + (a.link ? '<p style="margin-top:16px"><a class="btn sky" href="' + AF.root + a.link + '">Do it on AllFun</a></p>' : "") + "</div>";
    }
    $("#bb-go").addEventListener("click", pickAct);
  }

  /* ---------- Would you rather ---------- */
  if (T === "wyr") {
    var Q = [], order = [], qi = 0, tally = AF.store.json("af-wyr", { n: 0 });
    load("wyr").then(function (d) { Q = d; shuffleQ(); next(); });
    function shuffleQ() { var cat = $("#wy-cat").value; order = AF.shuffle(Q.filter(function (q) { return !cat || q.cat === cat; })); qi = 0; }
    function next() {
      if (!order.length) return; if (qi >= order.length) shuffleQ();
      var q = order[qi++]; $("#wy-a").innerHTML = esc(q.a); $("#wy-b").innerHTML = esc(q.b); $("#wy-cat-l").textContent = q.cat;
      [$("#wy-a"), $("#wy-b")].forEach(function (b) { b.disabled = false; b.classList.remove("picked"); });
      $("#wy-next").hidden = true; $("#wy-n").textContent = tally.n;
    }
    function pick(btn) {
      [$("#wy-a"), $("#wy-b")].forEach(function (b) { b.disabled = true; }); btn.classList.add("picked");
      tally.n++; AF.store.put("af-wyr", tally); $("#wy-n").textContent = tally.n; $("#wy-next").hidden = false; $("#wy-next").focus();
    }
    $("#wy-a").addEventListener("click", function () { pick(this); });
    $("#wy-b").addEventListener("click", function () { pick(this); });
    $("#wy-next").addEventListener("click", next); $("#wy-skip").addEventListener("click", next);
    $("#wy-cat").addEventListener("change", function () { shuffleQ(); next(); });
    $("#wy-share").addEventListener("click", function () { AF.share("Would you rather " + $("#wy-a").textContent + " or " + $("#wy-b").textContent + "?"); });
  }

  /* ---------- Charades ---------- */
  if (T === "charades") {
    var DATA = null, deck = [], score = { a: 0, b: 0 }, team = "a", tmr = null, left = 0;
    load("charades").then(function (d) { DATA = d.categories; var sel = $("#ch-cat"); Object.keys(DATA).forEach(function (k) { var o = document.createElement("option"); o.value = k; o.textContent = k; sel.appendChild(o); }); build(); });
    function build() {
      var cat = $("#ch-cat").value, lvl = $("#ch-lvl").value, words = [];
      Object.keys(DATA).forEach(function (k) { if (cat && k !== cat) return; ["easy", "medium", "hard"].forEach(function (l) { if (lvl && l !== lvl) return; DATA[k][l].forEach(function (w) { words.push({ w: w, c: k }); }); }); });
      deck = AF.shuffle(words);
    }
    function draw() { if (!deck.length) build(); var x = deck.pop(); $("#ch-word").textContent = x.w; $("#ch-c").textContent = x.c; }
    function sc() { $("#ch-a").textContent = score.a; $("#ch-b").textContent = score.b; $("#ch-team").textContent = team === "a" ? "Team A is up" : "Team B is up"; }
    function startRound() {
      clearInterval(tmr); var total = +$("#ch-time").value; left = total; draw(); $("#ch-play").hidden = false; $("#ch-start").hidden = true;
      $("#ch-bar").style.width = "100%";
      tmr = setInterval(function () { left -= 0.2; $("#ch-bar").style.width = Math.max(0, left / total * 100) + "%"; $("#ch-left").textContent = Math.ceil(Math.max(0, left)) + "s"; if (left <= 0) stopRound(); }, 200);
    }
    function stopRound() { clearInterval(tmr); $("#ch-play").hidden = true; $("#ch-start").hidden = false; $("#ch-word").textContent = "Time!"; team = team === "a" ? "b" : "a"; sc(); }
    $("#ch-start").addEventListener("click", startRound);
    $("#ch-got").addEventListener("click", function () { score[team]++; sc(); draw(); });
    $("#ch-skip").addEventListener("click", draw);
    $("#ch-reset").addEventListener("click", function () { score = { a: 0, b: 0 }; team = "a"; sc(); });
    $("#ch-cat").addEventListener("change", build); $("#ch-lvl").addEventListener("change", build);
    $("#ch-one").addEventListener("click", function () { if (!DATA) return; draw(); });
    sc();
  }

  /* ---------- Random number ---------- */
  if (T === "number") {
    function gen() {
      var lo = parseInt($("#rn-min").value, 10), hi = parseInt($("#rn-max").value, 10), n = Math.min(500, Math.max(1, parseInt($("#rn-count").value, 10) || 1));
      if (isNaN(lo) || isNaN(hi) || hi < lo) { $("#rn-out").textContent = "Check min and max"; return; }
      var uniq = $("#rn-uniq").checked, span = hi - lo + 1, res = [];
      if (uniq && n > span) { $("#rn-out").textContent = "Only " + span + " unique numbers fit"; return; }
      if (uniq) { var set = new Set(); while (set.size < n) set.add(lo + rint(span)); res = Array.from(set); }
      else for (var i = 0; i < n; i++) res.push(lo + rint(span));
      if ($("#rn-sort").checked) res.sort(function (a, b) { return a - b; });
      $("#rn-out").textContent = res.join(", ");
    }
    $("#rn-go").addEventListener("click", gen); gen();
  }
})();
