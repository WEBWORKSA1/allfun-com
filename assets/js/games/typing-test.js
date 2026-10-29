/* Typing Test — words per minute and accuracy */
(function () {
  "use strict";
  var AF = window.AF, el = document.getElementById("game"); if (!el) return;
  var WORDS = (
    "the to and of in is for that you it on with this was be as are have at he not by but from my or we an your all " +
    "so his they me if one can will just like about up out what has when more do no were who had their there her " +
    "which time get been would she new people how some also them now other its our than good only after first him " +
    "into know see two make over think any then could back these us want because go well said way most much very " +
    "where even should may here need really did right work year years being day too going before off why made still " +
    "take got many never those life say world down great through last while best such love man home long look use " +
    "same used both every am come part state three around between always better find help high little old since " +
    "another does own things under during game thing give house place school again next each without against end " +
    "found must show big feel sure team ever family keep might please put money free second someone away left " +
    "number city days lot name night play until company doing few let real called having set thought done however " +
    "getting group looking public top women business care start system times week already anything case nothing " +
    "person today change enough full live making point read told yet bad four hard mean once support tell music " +
    "power seen states stop water based believe call head men national small took white came far job side though " +
    "try went yes actually later less line order party run says service country open season thank children everyone " +
    "general trying united using area black law makes together whole car face five kind maybe per story working " +
    "course games health hope least means news within able book early friends local post thanks video young ago " +
    "others social talk court fact given guys half hand level mind often single become body coming control food guy " +
    "hours office pay problem south true almost history known large lost research room several started taking win " +
    "wrong along anyone else girl matter pretty remember air bit friend hit needs nice playing probably saying yeah " +
    "class close comes idea looks past possible wanted cause due happy human members months move question series"
  ).split(" ");
  var dur = 60, words = [], idx = 0, typed = [], started = false, endAt = 0, timer = null, correctChars = 0, totalChars = 0, finished = false;
  el.innerHTML = '<div class="stage-bar"><div class="btn-row">' +
    '<div class="seg" role="tablist" aria-label="Test length"><button class="segbtn" data-d="30" aria-selected="false">30s</button><button class="segbtn" data-d="60" aria-selected="true">60s</button><button class="segbtn" data-d="120" aria-selected="false">2 min</button></div>' +
    '<button class="btn sun sm" data-new>Restart</button></div>' +
    '<div class="stats"><div class="stat"><small>Time</small><b data-time>60</b></div><div class="stat"><small>WPM</small><b data-wpm>0</b></div><div class="stat"><small>Accuracy</small><b data-acc>100%</b></div><div class="stat"><small>Best</small><b data-best>–</b></div></div></div>' +
    '<div class="ty-text" aria-hidden="true"></div>' +
    '<label class="vh" for="ty-in">Type the words shown</label><input id="ty-in" class="ty-input" type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="Start typing to begin…">' +
    '<p class="game-msg" aria-live="polite"></p>';
  var text = el.querySelector(".ty-text"), inp = el.querySelector("#ty-in"), msg = el.querySelector(".game-msg");
  function showBest() { var b = AF.best("typing-" + dur); el.querySelector("[data-best]").textContent = b === null ? "–" : b; }
  function reset() {
    clearInterval(timer); started = false; finished = false; idx = 0; typed = []; correctChars = 0; totalChars = 0;
    words = []; for (var i = 0; i < 260; i++) words.push(WORDS[Math.floor(Math.random() * WORDS.length)]);
    inp.value = ""; inp.disabled = false; el.querySelector("[data-time]").textContent = dur; el.querySelector("[data-wpm]").textContent = 0; el.querySelector("[data-acc]").textContent = "100%";
    msg.textContent = "The timer starts with your first key. Press space after each word."; render(); showBest();
  }
  function render() {
    var start = Math.max(0, idx - 8), html = "";
    for (var i = start; i < Math.min(words.length, idx + 40); i++) {
      var cls = i < idx ? (typed[i] === words[i] ? "ok" : "no") : i === idx ? "cur" : "";
      html += '<span class="' + cls + '">' + words[i] + "</span> ";
    }
    text.innerHTML = html;
  }
  function stats() {
    var mins = Math.max(1 / 60, (dur - Math.max(0, (endAt - Date.now()) / 1000)) / 60);
    var wpm = Math.round(correctChars / 5 / mins), acc = totalChars ? Math.round(100 * correctChars / totalChars) : 100;
    el.querySelector("[data-wpm]").textContent = wpm; el.querySelector("[data-acc]").textContent = acc + "%";
    return { wpm: wpm, acc: acc };
  }
  function finish() {
    clearInterval(timer); finished = true; inp.disabled = true;
    var s = stats(), nb = AF.best("typing-" + dur, s.wpm); showBest();
    msg.textContent = s.wpm + " WPM at " + s.acc + "% accuracy." + (nb ? " New personal best!" : "") + " Press Restart to go again.";
  }
  inp.addEventListener("input", function () {
    if (finished) return;
    if (!started) {
      started = true; endAt = Date.now() + dur * 1000;
      timer = setInterval(function () { var left = Math.max(0, Math.ceil((endAt - Date.now()) / 1000)); el.querySelector("[data-time]").textContent = left; stats(); if (left <= 0) finish(); }, 200);
    }
    var v = inp.value;
    if (v.slice(-1) === " ") {
      var w = v.trim(); if (!w) { inp.value = ""; return; }
      typed[idx] = w; totalChars += words[idx].length + 1;
      if (w === words[idx]) correctChars += words[idx].length + 1;
      idx++; inp.value = ""; render(); stats(); return;
    }
    var cur = text.querySelector(".cur");
    if (cur) cur.classList.toggle("err", words[idx].indexOf(v) !== 0);
  });
  el.querySelectorAll(".segbtn").forEach(function (b) { b.addEventListener("click", function () { dur = +b.dataset.d; el.querySelectorAll(".segbtn").forEach(function (x) { x.setAttribute("aria-selected", String(x === b)); }); reset(); inp.focus(); }); });
  el.querySelector("[data-new]").addEventListener("click", function () { reset(); inp.focus(); });
  reset();
})();
