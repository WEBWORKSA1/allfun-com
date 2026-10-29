# -*- coding: utf-8 -*-
"""Original SVG illustrations for game tiles (320x200, transparent; tile supplies the color)."""
import math, os

INK = "#1F1A4D"; W = "#FFFFFF"; SUN = "#FFC93C"; POP = "#FF5C8A"; MINT = "#22C7A9"; SKY = "#5B95FF"; LIL = "#B9A6FF"; GRAY = "#9C98C9"

def burst(cx, cy, r1, r2, n):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append("%.1f %.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + " L".join(pts) + "Z"

def rect(x, y, w, h, fill, rx=10, sw=4): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
def txt(x, y, s, size=28, fill=INK, w=800): return f'<text x="{x}" y="{y}" font-family="Bricolage Grotesque,Arial Rounded MT Bold,Arial,sans-serif" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="middle" dominant-baseline="central">{s}</text>'
def circ(x, y, r, fill, sw=4): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'

def fiveword():
    cols = [MINT, SUN, GRAY, MINT, MINT]; out = ""
    for i, ch in enumerate("SMILE"):
        x = 40 + i * 50; out += rect(x, 40, 42, 42, cols[i], 8) + txt(x + 21, 62, ch, 24)
    for i in range(5): out += rect(40 + i * 50, 96, 42, 42, W, 8)
    out += rect(40, 152, 42, 30, W, 8, 3) + rect(90, 152, 42, 30, W, 8, 3)
    return out

def sudoku():
    out = rect(95, 25, 150, 150, W, 12)
    for i in (1, 2): out += f'<line x1="{95+50*i}" y1="25" x2="{95+50*i}" y2="175" stroke="{INK}" stroke-width="4"/><line x1="95" y1="{25+50*i}" x2="245" y2="{25+50*i}" stroke="{INK}" stroke-width="4"/>'
    nums = {(0, 0): "5", (1, 1): "3", (2, 0): "8", (0, 2): "1", (2, 2): "9", (1, 0): "", (0, 1): "7"}
    for (c, r), n in nums.items(): out += txt(120 + c * 50, 50 + r * 50, n, 30)
    out += rect(145, 75, 50, 50, SUN, 0, 4) + txt(170, 100, "4", 30)
    return out

def tile_merge():
    out = rect(85, 20, 160, 160, INK, 18, 0)
    vals = [("2", W), ("4", "#DCD3FF"), ("8", LIL), ("2048", POP)]
    for i, (v, c) in enumerate(vals):
        x = 97 + (i % 2) * 74; y = 32 + (i // 2) * 74
        out += f'<rect x="{x}" y="{y}" width="64" height="64" rx="10" fill="{c}"/>' + txt(x + 32, y + 32, v, 30 if len(v) < 3 else 19)
    return out

def minesweeper():
    out = ""; grid = ["1", "1", "F", "", "2", "M", "", "1", "1"]
    for i, v in enumerate(grid):
        x = 100 + (i % 3) * 42; y = 38 + (i // 3) * 42
        fill = SKY if v in ("F", "M") else "#E2E5FB"
        out += rect(x, y, 38, 38, fill, 7, 3)
        if v == "F": out += f'<path d="M{x+14} {y+30} V{y+8} L{x+30} {y+14} L{x+14} {y+20}" fill="{POP}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        elif v == "M": out += circ(x + 19, y + 19, 9, INK, 0) + f'<path d="M{x+19} {y+5} V{y+33} M{x+5} {y+19} H{x+33}" stroke="{INK}" stroke-width="4"/>'
        elif v: out += txt(x + 19, y + 20, v, 22, "#2D6BE0" if v == "1" else "#0F8A6C")
    return out

def memory_match():
    out = ""
    for i, (c, face) in enumerate([(W, "heart"), (SKY, None), (W, "heart"), (SKY, None)]):
        x = 50 + i * 58; rot = [-8, 4, -3, 7][i]
        out += f'<g transform="rotate({rot} {x+25} 100)">' + rect(x, 55, 50, 80, c, 9)
        if face: out += f'<path d="M{x+25} {y_(110)} C{x+5} {y_(92)} {x+12} {y_(76)} {x+25} {y_(88)} C{x+38} {y_(76)} {x+45} {y_(92)} {x+25} {y_(110)}Z" fill="{POP}" stroke="{INK}" stroke-width="3"/>'
        else: out += f'<path d="M{x+10} {y_(70)} L{x+40} {y_(120)} M{x+40} {y_(70)} L{x+10} {y_(120)}" stroke="#ffffff" stroke-opacity=".5" stroke-width="3"/>'
        out += "</g>"
    return out
def y_(v): return v

def snake():
    out = ""
    path = [(70, 140), (110, 140), (150, 140), (150, 100), (190, 100), (230, 100)]
    for i, (x, y) in enumerate(path): out += rect(x - 18, y - 18, 36, 36, MINT if i < len(path) - 1 else INK, 9, 3)
    out += circ(236, 94, 4, SUN, 0)
    out += f'<path d="{burst(262, 58, 18, 8, 5)}" fill="{SUN}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    return out

def mole_pop():
    out = ""
    for i, x in enumerate((80, 160, 240)):
        out += f'<ellipse cx="{x}" cy="150" rx="34" ry="13" fill="#3A2E1F" stroke="{INK}" stroke-width="4"/>'
    out += f'<path d="M136 150 V112 Q160 78 184 112 V150" fill="#C58B5A" stroke="{INK}" stroke-width="4"/>'
    out += circ(151, 112, 4, INK, 0) + circ(169, 112, 4, INK, 0) + f'<ellipse cx="160" cy="124" rx="8" ry="5" fill="{POP}" stroke="{INK}" stroke-width="2"/>'
    out += f'<path d="{burst(240, 70, 22, 10, 5)}" fill="{SUN}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    return out

def four_in_a_row():
    out = rect(70, 30, 180, 150, SKY, 14)
    board = ["......", "......", "...p..", "..ys..", ".yps..", "yppy.."]
    colors = {"y": SUN, "p": POP, "s": SUN}
    for r in range(4):
        for c in range(5):
            ch = board[r + 2][c] if c < 6 else "."
            out += circ(97 + c * 32, 60 + r * 32, 12, colors.get(ch, W), 3)
    return out

def tic_tac_toe():
    out = ""
    for i in (1, 2):
        out += f'<path d="M{95+43*i} 30 V170 M95 {30+46*i} H225" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    def X(cx, cy): return f'<path d="M{cx-13} {cy-13} L{cx+13} {cy+13} M{cx+13} {cy-13} L{cx-13} {cy+13}" stroke="{W}" stroke-width="7" stroke-linecap="round"/>'
    def O(cx, cy): return f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{SUN}" stroke-width="7"/>'
    return out + X(116, 53) + O(160, 100) + X(203, 147) + O(203, 53) + X(160, 53)

def reaction_time():
    out = circ(160, 108, 62, W, 5) + f'<rect x="150" y="30" width="20" height="16" rx="4" fill="{INK}"/>'
    out += f'<path d="M160 108 L160 66" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M160 108 L190 124" stroke="{POP}" stroke-width="6" stroke-linecap="round"/>' + circ(160, 108, 6, INK, 0)
    out += f'<path d="M248 40 L222 98 H244 L230 156 L274 84 H250 L264 40Z" fill="{SUN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    return out

def typing_test():
    out = rect(50, 60, 220, 110, W, 14)
    for r in range(3):
        for c in range(7 - r):
            x = 66 + c * 28 + r * 12; y = 74 + r * 30
            out += f'<rect x="{x}" y="{y}" width="22" height="22" rx="5" fill="{SUN if (r, c) in ((1, 2), (0, 4)) else "#E2E5FB"}" stroke="{INK}" stroke-width="2.5"/>'
    out += rect(110, 150, 100, 12, "#E2E5FB", 5, 2.5)
    out += rect(90, 20, 140, 30, INK, 8, 0) + txt(160, 35, "72 WPM", 17, W)
    return out

def pattern_echo():
    out = ""
    for i, c in enumerate((SUN, SKY, POP, MINT)):
        x = 108 + (i % 2) * 54; y = 26 + (i // 2) * 54
        out += rect(x, y, 50, 50, c, 14 if i != 2 else 14, 4)
    out += f'<rect x="104" y="22" width="58" height="58" rx="16" fill="none" stroke="{W}" stroke-width="4"/>'
    out += f'<path d="M230 70 q14 14 0 28 M244 60 q24 24 0 48" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    return out

ARTS = {"fiveword": fiveword, "sudoku": sudoku, "tile-merge": tile_merge, "minesweeper": minesweeper, "memory-match": memory_match, "snake": snake,
        "mole-pop": mole_pop, "four-in-a-row": four_in_a_row, "tic-tac-toe": tic_tac_toe, "reaction-time": reaction_time, "typing-test": typing_test, "pattern-echo": pattern_echo}

def write_game_art(base, slug):
    d = os.path.join(base, "assets", "img", "g"); os.makedirs(d, exist_ok=True)
    deco = f'<circle cx="28" cy="28" r="6" fill="{W}" fill-opacity=".55"/><circle cx="296" cy="176" r="9" fill="{W}" fill-opacity=".45"/><path d="{burst(292, 30, 9, 4, 4)}" fill="{W}" fill-opacity=".6"/>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200">{deco}{ARTS[slug]()}</svg>'
    open(os.path.join(d, slug + ".svg"), "w", encoding="utf-8").write(svg)

def _logo(x, y, s):
    k = s / 100.0
    return (f'<g transform="translate({x} {y}) scale({k})"><path d="{burst(50, 50, 47, 36, 11)}" fill="{SUN}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="39" cy="45" r="5" fill="{INK}"/><circle cx="61" cy="45" r="5" fill="{INK}"/><path d="M36 58 Q50 72 64 58" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>')

def og_svg():
    cx, cy, r = 1010, 190, 330
    cols = [SUN, SKY, POP, MINT, LIL, "#FF9F45", "#7FD8FF", "#FF8FB1"]
    segs = ""
    for i, c in enumerate(cols):
        a0 = math.radians(i * 45 - 90); a1 = math.radians((i + 1) * 45 - 90)
        segs += f'<path d="M{cx} {cy} L{cx + r*math.cos(a0):.1f} {cy + r*math.sin(a0):.1f} A{r} {r} 0 0 1 {cx + r*math.cos(a1):.1f} {cy + r*math.sin(a1):.1f} Z" fill="{c}" stroke="{INK}" stroke-width="4"/>'
    f = 'font-family="DejaVu Sans, Inter, Arial, sans-serif" font-weight="bold"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#EEF0FF"/>'
            f'<circle cx="{cx+14}" cy="{cy+14}" r="{r+4}" fill="{INK}"/>{segs}<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'{_logo(78, 78, 124)}<text x="222" y="172" {f} font-size="92" fill="{INK}" letter-spacing="-3">All<tspan fill="{POP}">Fun</tspan></text>'
            f'<text {f} font-size="62" fill="{INK}" letter-spacing="-2"><tspan x="80" y="330">All the fun.</tspan><tspan x="80" y="400">None of the</tspan><tspan x="80" y="470">downloads.</tspan></text>'
            f'<text x="80" y="560" font-family="DejaVu Sans, Inter, Arial, sans-serif" font-size="30" fill="#4F4A80">Free games · Daily puzzles · Quizzes · Party tools</text></svg>')

def icon_svg():
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="{SKY}"/>{_logo(56, 56, 400)}</svg>'
