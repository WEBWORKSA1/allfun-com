/* AllFun wheel — canvas spinner used by the home hero and the Spin the Wheel tool */
(function () {
  "use strict";
  var PALETTE = ["#FFC93C", "#5B95FF", "#FF5C8A", "#22C7A9", "#B9A6FF", "#FF9F45", "#7FD8FF", "#FF8FB1"];
  function Wheel(canvas, opts) {
    this.c = canvas; this.ctx = canvas.getContext("2d");
    this.items = []; this.angle = 0; this.spinning = false;
    this.onResult = opts.onResult || function () {};
    this.sound = !!opts.sound; this.audio = null; this.lastSeg = -1;
    this.resize(); this.set(opts.items || []);
    var self = this;
    window.addEventListener("resize", function () { self.resize(); self.draw(); });
  }
  Wheel.prototype.resize = function () {
    var dpr = Math.min(window.devicePixelRatio || 1, 2), w = this.c.clientWidth || 400;
    this.c.width = w * dpr; this.c.height = w * dpr; this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0); this.size = w;
  };
  Wheel.prototype.set = function (items) {
    this.items = items.map(function (it, i) {
      return typeof it === "string" ? { label: it, color: PALETTE[i % PALETTE.length] } : { label: it.label, color: it.color || PALETTE[i % PALETTE.length], data: it };
    });
    if (this.items.length % PALETTE.length === 1 && this.items.length > 1) this.items[this.items.length - 1].color = PALETTE[2];
    this.draw();
  };
  Wheel.prototype.draw = function () {
    var ctx = this.ctx, s = this.size, r = s / 2, n = this.items.length;
    ctx.clearRect(0, 0, s, s);
    if (!n) { ctx.fillStyle = "#E2E5FB"; ctx.beginPath(); ctx.arc(r, r, r, 0, Math.PI * 2); ctx.fill(); return; }
    var seg = Math.PI * 2 / n, fs = Math.max(10, Math.min(20, s / (n > 16 ? 34 : 24)));
    for (var i = 0; i < n; i++) {
      var a0 = this.angle + i * seg - Math.PI / 2;
      ctx.beginPath(); ctx.moveTo(r, r); ctx.arc(r, r, r, a0, a0 + seg); ctx.closePath();
      ctx.fillStyle = this.items[i].color; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = "#1F1A4D"; ctx.stroke();
      ctx.save(); ctx.translate(r, r); ctx.rotate(a0 + seg / 2);
      ctx.fillStyle = "#1F1A4D"; ctx.font = "700 " + fs + "px 'Atkinson Hyperlegible', system-ui, sans-serif";
      ctx.textAlign = "right"; ctx.textBaseline = "middle";
      var label = this.items[i].label, max = r * 0.62;
      while (ctx.measureText(label).width > max && label.length > 3) label = label.slice(0, -2) + "…";
      ctx.fillText(label, r - 16, 0); ctx.restore();
    }
  };
  Wheel.prototype.tick = function () {
    if (!this.sound) return;
    try {
      this.audio = this.audio || new (window.AudioContext || window.webkitAudioContext)();
      var o = this.audio.createOscillator(), g = this.audio.createGain();
      o.frequency.value = 880; g.gain.value = 0.05; o.connect(g); g.connect(this.audio.destination);
      o.start(); o.stop(this.audio.currentTime + 0.03);
    } catch (e) {}
  };
  Wheel.prototype.indexAt = function () {
    var n = this.items.length, seg = Math.PI * 2 / n;
    var a = ((-this.angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    return Math.floor(a / seg) % n;
  };
  Wheel.prototype.spin = function () {
    if (this.spinning || this.items.length < 2) return;
    var self = this, reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var start = this.angle, dur = reduce ? 600 : 4200 + Math.random() * 900;
    var target = start + (reduce ? 2 : 6 + Math.random() * 4) * Math.PI * 2 + Math.random() * Math.PI * 2;
    var t0 = performance.now(); this.spinning = true;
    function frame(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      self.angle = start + (target - start) * e; self.draw();
      var idx = self.indexAt(); if (idx !== self.lastSeg) { self.lastSeg = idx; self.tick(); }
      if (p < 1) requestAnimationFrame(frame);
      else { self.spinning = false; var i = self.indexAt(); self.onResult(self.items[i], i); }
    }
    requestAnimationFrame(frame);
  };
  window.AFWheel = Wheel;
})();
