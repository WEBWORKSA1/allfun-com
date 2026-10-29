/* Memory Match — flip cards, find pairs */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var DECKS = { animals: "🐶 🐱 🦊 🐼 🐸 🐵 🦁 🐯 🐨 🐷 🐙 🦉 🐢 🦄 🐝 🦋 🐬 🦒", food: "🍕 🍔 🌮 🍩 🍪 🍓 🍉 🍍 🥑 🥕 🍿 🧁 🍦 🥨 🍒 🥝 🌽 🍋", space: "🚀 🌙 ⭐ 🪐 🌈 🌍 🌟 🛸 👽 🔭 🌌 🌠 🌕 🌞 🌑 💫 🌎 🧑‍🚀" };
  var LEVELS = { easy: [4, 4], medium: [4, 5], hard: [6, 6] };
  var level = "easy", deck = "animals", cards = [], open = [], matched = 0, moves = 0, t0 = 0, timer = null, lock = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<label class="vh" for="mm-level">Difficulty</label><select id="mm-level" class="mini-select"><option value="easy">Easy · 8 pairs</option><option value="medium">Medium · 10 pairs</option><option value="hard">Hard · 18 pairs</option></select>' +
    '<label class="vh" for="mm-deck">Card theme</label><select id="mm-deck" class="mini-select"><option value="animals">Animals</option><option value="food">Food</option><option value="space">Space</option></select>' +
    '<button class="btn sun sm" data-new>New game</button></div>' +
    '<div class="stats"><div class="stat"><small>Moves</small><b data-moves>0</b></div><div class="stat"><small>Time</small><b data-time>0s</b></div><div class="stat"><small>Best</small><b data-best>–</b></div></div></div>' +
    '<div class="mm-grid"></div><p class="game-msg" aria-live="polite"></p>';
  var grid = el.querySelector(".mm-grid"), msg = el.querySelector(".game-msg");
  function key() { return "mm-" + level; }
  function showBest() { var b = AF.best(key()); el.querySelector("[data-best]").textContent = b === null ? "–" : b + " moves"; }
  function tick() { el.querySelector("[data-time]").textContent = Math.floor((Date.now() - t0) / 1000) + "s"; }
  function build() {
    clearInterval(timer); timer = null; t0 = 0; open = []; matched = 0; moves = 0; lock = false;
    var dims = LEVELS[level], pairs = dims[0] * dims[1] / 2, faces = DECKS[deck].split(" ");
    faces = AF.shuffle(faces).slice(0, pairs);
    cards = AF.shuffle(faces.concat(faces));
    grid.style.gridTemplateColumns = "repeat(" + dims[1] + ", minmax(0, 1fr))";
    grid.innerHTML = "";
    cards.forEach(function (f, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "mm-card"; b.dataset.i = i;
      b.setAttribute("aria-label", "Hidden card " + (i + 1));
      b.innerHTML = '<span class="mm-face">' + f + '</span>';
      grid.appendChild(b);
    });
    el.querySelector("[data-moves]").textContent = "0"; el.querySelector("[data-time]").textContent = "0s";
    msg.textContent = "Flip two cards. Find all " + pairs + " pairs."; showBest();
  }
  grid.addEventListener("click", function (e) {
    var b = e.target.closest(".mm-card"); if (!b || lock || b.classList.contains("up") || b.classList.contains("done")) return;
    if (!timer) { t0 = Date.now(); timer = setInterval(tick, 500); }
    b.classList.add("up"); b.setAttribute("aria-label", "Card " + cards[b.dataset.i]); open.push(b);
    if (open.length === 2) {
      moves++; el.querySelector("[data-moves]").textContent = moves; lock = true;
      var a = open[0], c = open[1];
      if (cards[a.dataset.i] === cards[c.dataset.i]) {
        a.classList.add("done"); c.classList.add("done"); open = []; lock = false; matched++;
        if (matched === cards.length / 2) {
          clearInterval(timer); tick();
          var secs = Math.floor((Date.now() - t0) / 1000), nb = AF.best(key(), moves, true);
          msg.textContent = "All pairs found in " + moves + " moves and " + secs + "s." + (nb ? " New best!" : "");
          showBest();
        }
      } else {
        setTimeout(function () { a.classList.remove("up"); c.classList.remove("up"); a.setAttribute("aria-label", "Hidden card"); c.setAttribute("aria-label", "Hidden card"); open = []; lock = false; }, 750);
      }
    }
  });
  el.querySelector("#mm-level").addEventListener("change", function (e) { level = e.target.value; build(); });
  el.querySelector("#mm-deck").addEventListener("change", function (e) { deck = e.target.value; build(); });
  el.querySelector("[data-new]").addEventListener("click", build);
  build();
})();
