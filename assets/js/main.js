/* AllFun — core interactions and shared helpers (window.AF) */
(function () {
  "use strict";
  var S = window.SITE || {};
  var AF = window.AF = window.AF || {};
  var body = document.body;
  AF.root = (body && body.getAttribute("data-root")) || "";

  /* Storage that never throws */
  var store = AF.store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    json: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    put: function (k, o) { try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) {} }
  };

  /* Toast */
  var toastTimer;
  AF.toast = function (msg) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.hidden = true; }, 2600);
  };

  /* Dates + seeded randomness for daily challenges */
  AF.today = function (d) {
    d = d || new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  };
  AF.hash = function (s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  AF.rng = function (seed) {
    var a = typeof seed === "number" ? seed : AF.hash(String(seed));
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  };
  AF.shuffle = function (arr, rnd) { rnd = rnd || Math.random; var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
  AF.dayNumber = function () { var start = new Date(2026, 0, 1); var now = new Date(); now.setHours(0, 0, 0, 0); return Math.round((now - start) / 864e5) + 1; };

  /* Best scores */
  AF.best = function (key, val, lowerIsBetter) {
    var k = "af-best-" + key, cur = parseFloat(store.get(k, ""));
    if (val === undefined) return isNaN(cur) ? null : cur;
    var better = isNaN(cur) || (lowerIsBetter ? val < cur : val > cur);
    if (better) store.set(k, String(val));
    return better;
  };

  /* Daily streak */
  AF.markDaily = function (game) {
    var log = store.json("af-daily", {}), t = AF.today();
    log[t] = log[t] || {}; log[t][game] = 1;
    var keys = Object.keys(log).sort().slice(-60), trimmed = {};
    keys.forEach(function (k) { trimmed[k] = log[k]; });
    store.put("af-daily", trimmed);
    AF.renderStreak();
  };
  AF.doneToday = function (game) { var log = store.json("af-daily", {}); return !!(log[AF.today()] && log[AF.today()][game]); };
  AF.streak = function () {
    var log = store.json("af-daily", {}), n = 0, d = new Date();
    if (!log[AF.today(d)]) d.setDate(d.getDate() - 1);
    while (log[AF.today(d)]) { n++; d.setDate(d.getDate() - 1); }
    return n;
  };
  AF.renderStreak = function () {
    var n = AF.streak();
    document.querySelectorAll("[data-streak]").forEach(function (el) { el.textContent = n + (n === 1 ? " day" : " days"); });
  };

  /* Share */
  AF.share = function (text, url) {
    url = url || location.href.split("#")[0];
    if (navigator.share) { navigator.share({ title: document.title, text: text, url: url }).catch(function () {}); return; }
    var full = text ? text + " " + url : url;
    if (navigator.clipboard) navigator.clipboard.writeText(full).then(function () { AF.toast("Copied — paste it anywhere"); }, function () { AF.toast("Copy failed — select the address bar instead"); });
  };
  document.querySelectorAll("[data-share]").forEach(function (b) {
    b.addEventListener("click", function () { AF.share(b.getAttribute("data-share") || ""); });
  });

  /* Theme */
  var root = document.documentElement, saved = store.get("af-theme");
  if (saved) root.setAttribute("data-theme", saved);
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark" ||
        (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next); store.set("af-theme", next);
    });
  });

  /* Mobile menu */
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (mb && nav) {
    mb.addEventListener("click", function () { var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); mb.setAttribute("aria-expanded", "false"); mb.focus(); } });
  }

  /* Surprise me */
  var PAGES = ["play/fiveword.html", "play/memory-match.html", "play/tile-merge.html", "play/snake.html", "play/minesweeper.html", "play/sudoku.html", "play/four-in-a-row.html", "play/tic-tac-toe.html", "play/reaction-time.html", "play/typing-test.html", "play/pattern-echo.html", "play/mole-pop.html", "tools/spin-wheel.html", "tools/bored-button.html", "tools/would-you-rather.html", "tools/charades-generator.html", "quizzes/general-knowledge.html", "quizzes/fun-style.html", "quizzes/animals.html", "quizzes/space.html", "facts/random-fun-facts.html", "daily.html"];
  AF.pages = PAGES;
  document.querySelectorAll("[data-random]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); location.href = AF.root + PAGES[Math.floor(Math.random() * PAGES.length)]; });
  });

  /* Year */
  document.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* Cookie notice (Google's own consent message can replace this in EEA/UK via AdSense Privacy & messaging) */
  var c = document.getElementById("consent");
  if (c && !store.get("af-consent")) {
    c.hidden = false;
    c.querySelectorAll("[data-consent]").forEach(function (b) {
      b.addEventListener("click", function () {
        store.set("af-consent", b.getAttribute("data-consent"));
        if (b.getAttribute("data-consent") === "essential") (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1;
        c.hidden = true;
      });
    });
  }
  if (store.get("af-consent") === "essential") (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1;

  /* Relay endpoint — address assembled at runtime, never present in markup */
  function addr() {
    var k = S._k || [], rev = function (b) { return atob(b).split("").reverse().join(""); };
    return rev(k[0]) + String.fromCharCode(64) + rev(k[1]);
  }
  function relay() { return "https://formsubmit.co/ajax/" + addr(); }
  AF.relay = relay;

  /* "Email us" links: the address only exists after a click */
  document.querySelectorAll("[data-mail]").forEach(function (a) {
    a.setAttribute("href", "#");
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var subj = a.getAttribute("data-mail") || "Hello AllFun";
      window.location.href = "mai" + "lto:" + addr() + "?subject=" + encodeURIComponent(subj);
    });
  });

  /* Prefill from query string (?type=birthday&size=10-25) */
  var qs = new URLSearchParams(location.search);
  qs.forEach(function (v, k) {
    document.querySelectorAll('form [name="' + k + '"]').forEach(function (el) {
      if (el.type === "radio" || el.type === "checkbox") { if (el.value === v) el.checked = true; }
      else if (!el.value) el.value = v;
    });
  });

  /* Multi-step forms */
  document.querySelectorAll("form[data-steps]").forEach(function (f) {
    var steps = f.querySelectorAll(".step"), bars = f.querySelectorAll(".steps-bar i"), lbl = f.querySelector(".step-label"), i = 0;
    function show(n) {
      steps.forEach(function (s, j) { s.hidden = j !== n; });
      bars.forEach(function (b, j) { b.classList.toggle("on", j <= n); });
      if (lbl) lbl.textContent = "Step " + (n + 1) + " of " + steps.length;
      f.querySelectorAll("[data-prev]").forEach(function (b) { b.style.visibility = n === 0 ? "hidden" : "visible"; });
      f.querySelectorAll("[data-next]").forEach(function (b) { b.hidden = n === steps.length - 1; });
      i = n;
      var first = steps[n].querySelector("input:not([type=hidden]),select,textarea");
      if (first && n > 0) first.focus({ preventScroll: true });
    }
    function valid() {
      var ok = true, st = f.querySelector(".form-status");
      steps[i].querySelectorAll("[required]").forEach(function (el) { if (ok && !el.checkValidity()) { el.reportValidity(); ok = false; } });
      var group = steps[i].querySelector("[data-need-one]");
      if (ok && group && !group.querySelector("input:checked")) { ok = false; if (st) { st.className = "form-status err"; st.textContent = "Pick one option to continue."; } }
      if (ok && st) st.textContent = "";
      return ok;
    }
    f.querySelectorAll("[data-next]").forEach(function (b) { b.addEventListener("click", function () { if (valid()) show(i + 1); }); });
    f.querySelectorAll("[data-prev]").forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    /* Auto-advance when an option card is picked on a one-question step */
    f.querySelectorAll(".step [data-autonext] input[type=radio]").forEach(function (r) {
      r.addEventListener("change", function () { setTimeout(function () { if (i < steps.length - 1) show(i + 1); }, 180); });
    });
    show(0);
  });

  /* All forms → relay */
  document.querySelectorAll("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = f.querySelector(".form-status"), btn = f.querySelector("[type=submit]");
      var hp = f.querySelector(".hp input"); if (hp && hp.value) return;
      var data = {};
      new FormData(f).forEach(function (v, k) { if (k === "_hp") return; data[k] = data[k] ? data[k] + ", " + v : v; });
      data._subject = "AllFun — " + f.getAttribute("data-form") + (data.name ? " from " + data.name : "");
      data._template = "table"; data._captcha = "false";
      data.page = location.href;
      if (data.email) data._replyto = data.email;
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      if (status) { status.className = "form-status"; status.textContent = ""; }
      fetch(relay(), { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          var go = f.getAttribute("data-redirect");
          if (go) { location.href = go; return; }
          if (status) { status.className = "form-status ok"; status.textContent = f.getAttribute("data-ok") || "Sent. We reply within one business day."; }
          f.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = "That didn't send. Check your connection and try again in a moment."; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
    });
  });

  /* Lite YouTube: nothing loads from YouTube until a click */
  document.querySelectorAll("[data-yt]").forEach(function (b) {
    var id = b.getAttribute("data-yt");
    b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    b.addEventListener("click", function () {
      var fr = document.createElement("iframe");
      fr.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      fr.title = b.getAttribute("aria-label") || "Video"; fr.className = "yt-frame";
      fr.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      fr.allowFullscreen = true;
      b.replaceWith(fr);
    });
  });

  /* Support page: tiers + payment links */
  var tiers = document.querySelectorAll(".tier");
  if (tiers.length) {
    var amt = document.getElementById("amount");
    tiers.forEach(function (t) {
      t.addEventListener("click", function () {
        tiers.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        t.setAttribute("aria-pressed", "true");
        if (amt) { amt.value = t.getAttribute("data-amount"); amt.dispatchEvent(new Event("input")); }
      });
    });
  }
  var box = document.getElementById("pay-links");
  if (box) {
    var p = S.payments || {}, any = false;
    [["paypal", "Give with PayPal"], ["stripe", "Give by card"], ["buymeacoffee", "Buy us a coffee"], ["kofi", "Support on Ko-fi"]].forEach(function (l) {
      if (p[l[0]]) { any = true; var a = document.createElement("a"); a.href = p[l[0]]; a.className = "btn mint"; a.target = "_blank"; a.rel = "noopener"; a.textContent = l[1]; box.appendChild(a); }
    });
    var n1 = document.getElementById("pay-live"), n2 = document.getElementById("pay-pledge");
    if (n1) n1.hidden = !any; if (n2) n2.hidden = any;
  }

  AF.renderStreak();
})();
