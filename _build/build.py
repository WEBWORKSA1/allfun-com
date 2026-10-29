# -*- coding: utf-8 -*-
"""AllFun static site generator.  Run:  python3 _build/build.py
Builds every HTML page, sitemap.xml, facts.json and game art from _build/ sources."""
import os, re, json, html, random
import markdown
from catalog import GAMES, TOOLS
import art
import static_pages as SP

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "_build")
SITE_URL = "https://allfun.com"
UPDATED = "2026-10-29"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
OWNER_URL = "https://web.works/contact"
SITEMAP = []          # (path, priority)
ALLPAGES = []         # (path, title, section)

esc = lambda s: html.escape(str(s), quote=True)

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def rootof(path): return "../" * path.count("/")

def canon(path):
    if path == "index.html": return SITE_URL + "/"
    if path.endswith("/index.html"): return SITE_URL + "/" + path[:-10]
    return SITE_URL + "/" + path

NAV = [("play", "play/index.html", "Games"), ("quizzes", "quizzes/index.html", "Quizzes"), ("tools", "tools/index.html", "Tools"),
       ("ideas", "ideas/index.html", "Ideas"), ("facts", "facts/index.html", "Facts"), ("daily", "daily.html", "Daily")]

LOGO = ('<svg viewBox="0 0 100 100" aria-hidden="true"><path d="' + art.burst(50, 50, 47, 36, 11) + '" fill="#FFC93C" stroke="#1F1A4D" stroke-width="5" stroke-linejoin="round"/>'
        '<circle cx="39" cy="45" r="5" fill="#1F1A4D"/><circle cx="61" cy="45" r="5" fill="#1F1A4D"/>'
        '<path d="M36 58 Q50 72 64 58" fill="none" stroke="#1F1A4D" stroke-width="5" stroke-linecap="round"/></svg>')

def header(r, active):
    links = "".join('<a href="%s%s"%s>%s</a>' % (r, href, ' aria-current="page"' if key == active else "", label) for key, href, label in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="ownerbar"><a href="{OWNER_URL}" rel="noopener" target="_blank">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership</a></div>
<header class="site-header"><div class="wrap hbar">
<a class="logo" href="{r}index.html" aria-label="AllFun home">{LOGO}<span>All<b>Fun</b></span></a>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="btn sm" href="{r}plan.html">Plan an event</a></nav>
<div class="hicons"><button class="icon-btn" data-random title="Surprise me" aria-label="Surprise me: open a random game">🎲</button><a class="icon-btn" href="{r}support.html" title="Support AllFun" aria-label="Support AllFun">♥</a><button class="icon-btn" data-theme-toggle title="Light or dark" aria-label="Switch light or dark theme">◐</button><button class="icon-btn menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Menu">☰</button></div>
</div></header>'''

def footer(r):
    games = "".join(f'<li><a href="{r}play/{g["slug"]}.html">{esc(g["title"])}</a></li>' for g in GAMES[:6])
    tools = "".join(f'<li><a href="{r}tools/{t["slug"]}.html">{esc(t["title"])}</a></li>' for t in TOOLS[:6])
    return f'''<footer class="site-footer"><div class="wrap">
<div class="fgrid">
<div><a class="logo" href="{r}index.html" style="color:#fff">{LOGO}<span>All<b>Fun</b></span></a>
<p style="margin-top:12px;color:#BDB9E8">Free games, quizzes, puzzles and party ideas. No downloads, no accounts — just fun.</p>
<form class="form fnews" data-form="Newsletter signup" data-ok="You're in! Watch for Friday Fun.">
<label for="fn-email">Friday Fun email <span class="opt">— one new game, quiz and idea each week</span></label>
<input id="fn-email" type="email" name="email" required placeholder="you@example.com" autocomplete="email">
<div class="hp" aria-hidden="true"><input name="_hp" tabindex="-1" autocomplete="off"></div>
<button class="btn sun sm" type="submit">Subscribe free</button><p class="form-status" role="status"></p></form></div>
<div><h4>Play</h4><ul>{games}<li><a href="{r}play/index.html">All games</a></li></ul></div>
<div><h4>Tools</h4><ul>{tools}<li><a href="{r}tools/index.html">All tools</a></li></ul></div>
<div><h4>AllFun</h4><ul><li><a href="{r}about.html">About</a></li><li><a href="{r}plan.html">Plan an event</a></li><li><a href="{r}free-kit.html">Free Game Night Kit</a></li><li><a href="{r}contests.html">Contests</a></li><li><a href="{r}support.html">Support us</a></li><li><a href="{r}careers.html">Careers &amp; creators</a></li><li><a href="{r}advertise.html">Advertise &amp; sponsor</a></li><li><a href="{r}videos.html">Videos</a></li><li><a href="{r}contact.html">Contact</a></li></ul></div>
<div><h4>Legal</h4><ul><li><a href="{r}privacy.html">Privacy policy</a></li><li><a href="{r}terms.html">Terms of use</a></li><li><a href="{r}disclaimer.html">Disclaimer</a></li><li><a href="{r}trademark.html">Trademark &amp; copyright</a></li><li><a href="{r}sitemap.html">Sitemap</a></li><li><a href="{OWNER_URL}" rel="noopener" target="_blank">Buy or partner on this domain</a></li></ul></div>
</div>
<div class="fbase"><p>© <span data-year>2026</span> AllFun.com. All rights reserved. AllFun.com is an independent website and is not affiliated with, endorsed by or connected to any company, product, app or brand named “All Fun”, “Allfun” or similar. <a href="{r}trademark.html">Trademark &amp; copyright notice</a>.</p><p>Made for players of all ages.</p></div>
</div></footer>
<div class="consent" id="consent" hidden role="dialog" aria-label="Cookie notice"><p>We use cookies and similar storage to keep games working, remember your scores and show ads that keep AllFun free. <a href="{r}privacy.html">Privacy policy</a></p><div class="btn-row"><button class="btn sm" data-consent="all">Accept all</button><button class="btn ghost sm" data-consent="essential">Essential only</button></div></div>'''

def crumbs(r, items):
    out = [f'<a href="{r}index.html">Home</a>']
    for label, href in items:
        out.append(f'<a href="{r}{href}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(out) + "</nav>"

def crumb_ld(items, path):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
    for i, (label, href) in enumerate(items):
        lst.append({"@type": "ListItem", "position": i + 2, "name": label, "item": canon(href) if href else canon(path)})
    return {"@type": "BreadcrumbList", "itemListElement": lst}

def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}

def faq_html(faq, title="Frequently asked questions"):
    items = "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in faq)
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">{title}</h2>{items}</section>'

def render(path, title, desc, body, active="", scripts=(), css=(), noindex=False, ld=None, priority="0.6", og_type="website", sitemap=True, full_title=None):
    r = rootof(path)
    t = full_title or f"{title} | AllFun"
    graph = [{"@type": "WebSite", "@id": SITE_URL + "/#site", "name": "AllFun", "url": SITE_URL + "/"},
             {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "AllFun", "url": SITE_URL + "/", "logo": SITE_URL + "/assets/img/icon-512.png"}]
    if ld: graph += ld if isinstance(ld, list) else [ld]
    ldj = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    css_tags = "".join(f'<link rel="stylesheet" href="{r}assets/css/{c}">' for c in css)
    js_tags = "".join(f'<script src="{r}assets/js/{s}"></script>' for s in scripts)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon(path)}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="AllFun"><meta property="og:title" content="{esc(t)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon(path)}"><meta property="og:image" content="{SITE_URL}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F1A4D">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{r}assets/img/icon-180.png"><link rel="manifest" href="{r}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&amp;family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,600..800&amp;display=swap">
<link rel="stylesheet" href="{r}assets/css/site.css">{css_tags}
<script>(function(){{try{{var t=localStorage.getItem("af-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}}})();</script>
{ADS}
<script type="application/ld+json">{ldj}</script>
</head>
<body data-root="{r}">
{header(r, active)}
<main id="main">
{body}
</main>
{footer(r)}
<script src="{r}assets/js/config.js"></script><script src="{r}assets/js/main.js"></script>{js_tags}
</body>
</html>
'''
    write(path, page)
    ALLPAGES.append((path, title, active))
    if sitemap and not noindex: SITEMAP.append((path, priority))

# ---------------------------------------------------------------- content parsing
def parse_md(fp):
    raw = open(fp, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    meta, body = {}, raw
    if m:
        for line in m.group(1).splitlines():
            if ": " in line:
                k, v = line.split(": ", 1); meta[k.strip()] = v.strip()
            elif line.endswith(":"):
                meta[line[:-1].strip()] = ""
        body = m.group(2)
    meta["related"] = [s.strip() for s in meta.get("related", "").split(",") if s.strip()]
    return meta, body

def md(text):
    return markdown.markdown(text, extensions=["tables", "sane_lists", "attr_list"])

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

def split_sections(body):
    """Return (intro_md, [(h2, md)])"""
    parts = re.split(r"(?m)^## +(.+)$", body)
    intro = parts[0]; secs = []
    for i in range(1, len(parts), 2): secs.append((parts[i].strip(), parts[i + 1]))
    return intro, secs

def faq_from_md(text):
    out = []
    for blk in re.split(r"(?m)^### +", text)[1:]:
        lines = blk.strip().split("\n", 1)
        q = lines[0].strip(); a = md(lines[1].strip()) if len(lines) > 1 else ""
        a = re.sub(r"^<p>|</p>$", "", a.strip())
        out.append((q, a))
    return out

def fix_links(htm, depth_prefix):
    return htm  # content already uses correct relative paths

# ---------------------------------------------------------------- tiles
def game_tile(r, g, tag="h3"):
    return (f'<a class="tile c-games" href="{r}play/{g["slug"]}.html" data-cat="{g["cat"]}"><div class="art"><img src="{r}assets/img/g/{g["slug"]}.svg" alt="" width="320" height="200" loading="lazy"></div>'
            f'<div class="body"><{tag}>{esc(g["title"])}</{tag}><p>{esc(g["short"])}</p><div class="meta"><span>{g["cat"]}</span><span>{GMETA[g["slug"]]}</span></div></div></a>')

GMETA = {"fiveword": "Daily · 3 min", "sudoku": "Daily · 10 min", "tile-merge": "1 player · 5 min", "minesweeper": "1 player · 3 min", "memory-match": "Ages 4+ · 2 min",
         "snake": "1 player · 3 min", "mole-pop": "Ages 4+ · 30 sec", "four-in-a-row": "1–2 players · 5 min", "tic-tac-toe": "1–2 players · 1 min",
         "reaction-time": "1 player · 1 min", "typing-test": "1 player · 1 min", "pattern-echo": "Ages 5+ · 3 min"}

def tool_tile(r, t):
    return (f'<a class="tile c-tools row-tile" href="{r}tools/{t["slug"]}.html"><span class="dot" aria-hidden="true">{t["em"]}</span><div><h3>{esc(t["title"])}</h3><p>{esc(t["short"])}</p></div></a>')

def quiz_tile(r, slug, q):
    n = len(q["questions"])
    return (f'<a class="tile c-quiz row-tile" href="{r}quizzes/{slug}.html"><span class="dot" aria-hidden="true">{q["emoji"]}</span><div><h3>{esc(q["title"])}</h3><p>{n} questions · {"Personality" if q["type"] == "personality" else q.get("level", "Trivia")}</p></div></a>')

def read_tile(r, folder, m, cls):
    return (f'<a class="tile {cls} row-tile" href="{r}{folder}/{m["slug"]}.html"><span class="dot" aria-hidden="true">{m.get("emoji", "✨")}</span><div><h3>{esc(m["title"])}</h3><p>{esc(m.get("category", ""))} · {m.get("minutes", "5")} min read</p></div></a>')

# ---------------------------------------------------------------- load content
GUIDES, FACTS = [], []
for fn in sorted(os.listdir(os.path.join(SRC, "content", "guides"))):
    if fn.endswith(".md"):
        m, b = parse_md(os.path.join(SRC, "content", "guides", fn)); m.setdefault("slug", fn[:-3]); GUIDES.append((m, b))
fdir = os.path.join(SRC, "content", "facts")
for fn in sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []:
    if fn.endswith(".md"):
        m, b = parse_md(os.path.join(fdir, fn)); m.setdefault("slug", fn[:-3]); FACTS.append((m, b))
GUIDE_ORDER = ["fun-things-to-do-when-bored", "game-night-ideas", "team-building-activities", "party-games-for-adults", "party-games-for-kids", "virtual-team-building-games",
               "icebreaker-games", "fun-things-to-do-at-home", "fun-things-to-do-with-friends", "family-fun-night-ideas", "rainy-day-activities-for-kids", "fun-date-ideas", "free-fun-things-to-do", "fun-weekend-ideas"]
GUIDES.sort(key=lambda x: GUIDE_ORDER.index(x[0]["slug"]) if x[0]["slug"] in GUIDE_ORDER else 99)
GMAP = {m["slug"]: m for m, _ in GUIDES}
FMAP = {m["slug"]: m for m, _ in FACTS}
QUIZ = json.load(open(os.path.join(BASE, "assets", "data", "quizzes.json"), encoding="utf-8"))
QORDER = ["general-knowledge", "fun-style", "animals", "space", "world-geography", "science", "food", "history", "words"]
VIDEOS = []
vp = os.path.join(SRC, "research", "videos.json")
if os.path.exists(vp):
    try: VIDEOS = json.load(open(vp, encoding="utf-8"))
    except Exception: VIDEOS = []

def cta_box(r, kind):
    if kind == "plan":
        return f'<aside class="inline-cta mint"><h3>Planning this for a group?</h3><p>Tell us your group size, date and budget. Our free Plan My Fun service sends back a tailored plan — and planner quotes if you want them.</p><a class="btn ghost" href="{r}plan.html">Plan my event free</a></aside>'
    if kind == "kit":
        return f'<aside class="inline-cta"><h3>Grab the free Game Night Kit</h3><p>30 printable games, a host checklist, score sheets, tie-breaker trivia and a bingo card. Free, instant, yours to keep.</p><a class="btn ghost" href="{r}free-kit.html">Get the free kit</a></aside>'
    if kind == "quiz":
        return f'<aside class="inline-cta pop"><h3>Think you\'ll remember these?</h3><p>Test yourself with a 15-question trivia quiz — instant answers, no sign-up.</p><a class="btn ghost" href="{r}quizzes/index.html">Take a quiz</a></aside>'
    return f'<aside class="inline-cta sky"><h3>Need a 3-minute break?</h3><p>Play today\'s FiveWord, a quick Sudoku or a round of Snake — free, right in your browser.</p><a class="btn ghost" href="{r}play/index.html">Play a game</a></aside>'

def rail(r, kind, related_html=""):
    picks = random.Random(kind + related_html[:20]).sample(GAMES, 4)
    games = "".join(f'<li><a href="{r}play/{g["slug"]}.html">{esc(g["title"])}</a> <span class="muted small">— {esc(g["cat"])}</span></li>' for g in picks)
    side = f'<div class="box"><h3>Play something quick</h3><ul>{games}</ul></div>'
    if related_html: side += f'<div class="box"><h3>Read next</h3><ul>{related_html}</ul></div>'
    if kind == "plan":
        side += f'<div class="box" style="background:var(--mint);color:#1F1A4D"><h3>Free event planning</h3><p class="small">Team building, parties, game nights. Tell us what you need.</p><a class="btn ghost sm" href="{r}plan.html">Start planning</a></div>'
    else:
        side += f'<div class="box" style="background:var(--sun);color:#1F1A4D"><h3>Free Game Night Kit</h3><p class="small">30 printable games + score sheets.</p><a class="btn ghost sm" href="{r}free-kit.html">Get it free</a></div>'
    return f'<aside class="rail" aria-label="More from AllFun">{side}</aside>'

def share_row(text):
    return f'<div class="share"><b>Share:</b><button class="btn ghost sm" data-share="{esc(text)}">Share or copy link</button><button class="btn ghost sm" onclick="window.print()">Print</button></div>'

# ---------------------------------------------------------------- FiveWord word lists
def build_words():
    lines = [l for l in open(os.path.join(SRC, "data", "answers5.txt"), encoding="utf-8") if not l.startswith("#")]
    answers = [w for l in lines for w in l.split() if len(w) == 5 and w.isalpha()]
    valid = set(answers)
    try:
        from wordfreq import top_n_list
        valid |= {w for w in top_n_list("en", 80000) if len(w) == 5 and w.isalpha() and w.isascii() and w.islower()}
    except Exception as e:
        print("wordfreq unavailable, using answers as the guess list:", e)
    json.dump({"answers": "".join(answers), "valid": "".join(sorted(valid))}, open(os.path.join(BASE, "assets", "data", "words5.json"), "w"), separators=(",", ":"))
    return len(answers), len(valid)
print("words:", build_words())

# ---------------------------------------------------------------- articles (ideas + facts)
FACT_ITEMS = []
def build_article(meta, body, folder, section, cls):
    path = f"{folder}/{meta['slug']}.html"; r = rootof(path)
    intro, secs = split_sections(body)
    faq, main_secs, myths = [], [], None
    for h, s in secs:
        if h.lower().startswith("frequently asked"): faq = faq_from_md(s)
        elif h.lower().startswith("myths"): myths = (h, s)
        else: main_secs.append((h, s))
    is_facts = folder == "facts"
    toc = "".join(f'<li><a href="#{slugify(h)}">{esc(h)}</a></li>' for h, _ in main_secs)
    parts = []
    mid = max(1, len(main_secs) // 2)
    for i, (h, s) in enumerate(main_secs):
        if i == mid: parts.append(cta_box(r, meta.get("cta", "play")))
        inner = md(s)
        if is_facts:
            for fm in re.finditer(r"(?m)^- \*\*(.+?)\*\*\s*(.+)$", s):
                FACT_ITEMS.append({"h": fm.group(1).strip(), "t": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", fm.group(2).strip()), "s": meta["slug"]})
            parts.append(f'<section class="factsec"><h2 id="{slugify(h)}">{esc(h)}</h2>{inner}</section>')
        else:
            parts.append(f'<h2 id="{slugify(h)}">{esc(h)}</h2>{inner}')
    if myths: parts.append(f'<section class="myths"><h2 id="{slugify(myths[0])}">{esc(myths[0])}</h2>{md(myths[1])}</section>')
    if len(main_secs) < 2: parts.append(cta_box(r, meta.get("cta", "play")))
    mp = FMAP if is_facts else GMAP
    rel_items = [mp[s] for s in meta["related"] if s in mp]
    rel_html = "".join(f'<li><a href="{r}{folder}/{x["slug"]}.html">{esc(x["title"])}</a></li>' for x in rel_items)
    label = "Fun facts" if is_facts else "Ideas"
    hub = f"{folder}/index.html"
    body_html = f'''<div class="wrap phero">{crumbs(r, [(label, hub), (meta["title"], None)])}
<h1>{esc(meta["title"])}</h1>
<div class="byline"><span class="tag {cls}" style="--c:var(--{'lilac' if is_facts else 'sun'})">{esc(meta.get("category", label))}</span><span>{meta.get("minutes", "6")} min read</span><span>Updated {UPDATED}</span><span>By the AllFun editors</span></div></div>
<div class="wrap article-grid"><article class="prose{' facts-list' if is_facts else ''}">
{md(intro)}
<nav class="toc" aria-label="On this page"><b>On this page</b><ol>{toc}</ol></nav>
{"".join(parts)}
{faq_html(faq) if faq else ""}
{share_row(meta["title"])}
</article>{rail(r, meta.get("cta", "play"), rel_html)}</div>'''
    ld = [{"@type": "Article", "headline": meta["title"], "description": meta.get("description", ""), "datePublished": UPDATED, "dateModified": UPDATED,
           "author": {"@type": "Organization", "name": "AllFun editors"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": canon(path), "image": SITE_URL + "/assets/img/og.png"},
          crumb_ld([(label, hub), (meta["title"], None)], path)]
    if faq: ld.append(faq_ld(faq))
    render(path, meta["title"], meta.get("description", ""), body_html, active=section, ld=ld, priority="0.7", og_type="article")

for m, b in GUIDES: build_article(m, b, "ideas", "ideas", "c-ideas")
for m, b in FACTS: build_article(m, b, "facts", "facts", "c-facts")
if FACT_ITEMS:
    json.dump(FACT_ITEMS, open(os.path.join(BASE, "assets", "data", "facts.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------- games
for g in GAMES: art.write_game_art(BASE, g["slug"])
for g in GAMES:
    path = f"play/{g['slug']}.html"; r = rootof(path)
    others = [x for x in GAMES if x["slug"] != g["slug"]]
    rnd = random.Random(g["slug"]); more = rnd.sample(others, 6)
    more_list = "".join(f'<li><a href="{r}play/{x["slug"]}.html">{esc(x["title"])}</a></li>' for x in more[:5])
    how = "".join(f"<li>{esc(s)}</li>" for s in g["how"])
    tips = "".join(f"<li>{esc(s)}</li>" for s in g["tips"])
    extra = ""
    if g["slug"] in ("fiveword", "sudoku"):
        extra = f'<p class="small muted">Part of the <a href="{r}daily.html">AllFun Daily</a> — your streak: <b data-streak>0 days</b>.</p>'
    body = f'''<div class="wrap phero ghero" style="padding-bottom:18px">{crumbs(r, [("Games", "play/index.html"), (g["title"], None)])}
<h1>{esc(g["h1"])}</h1><p class="lead">{esc(g["short"])}</p>{extra}</div>
<div class="wrap stage-wrap"><div><section class="stage" id="game" aria-label="{esc(g["title"])} game"><noscript>This game needs JavaScript turned on.</noscript></section>
{share_row("Play " + g["title"] + " free on AllFun")}</div>
<aside class="rail" aria-label="More games"><div class="box"><h3>More games</h3><ul>{more_list}</ul><p><a class="btn ghost sm" href="{r}play/index.html">All games</a></p></div>
<div class="box" style="background:var(--sun);color:#1F1A4D"><h3>Hosting a game night?</h3><p class="small">Get 30 printable party games and score sheets free.</p><a class="btn ghost sm" href="{r}free-kit.html">Get the kit</a></div></aside></div>
<div class="wrap article-grid section tight"><div class="prose">
<p>{esc(g["intro"])}</p>
<h2 id="how">How to play {esc(g["title"])}</h2><ol>{how}</ol>
<h2 id="tips">Tips and strategy</h2><ul>{tips}</ul>
<h2 id="about">About the game</h2><p>{esc(g["about"])}</p>
{faq_html(g["faq"])}
</div><div></div></div>
<section class="wrap section tight"><div class="sec-head"><h2>Play next</h2><a class="more" href="{r}play/index.html">All games</a></div><div class="grid g3">{"".join(game_tile(r, x) for x in more[:3])}</div></section>'''
    ld = [{"@type": "VideoGame", "name": g["title"], "description": g["desc"], "url": canon(path), "genre": g["cat"], "gamePlatform": "Web browser", "applicationCategory": "Game",
           "operatingSystem": "Any", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": SITE_URL + "/#org"}},
          crumb_ld([("Games", "play/index.html"), (g["title"], None)], path), faq_ld(g["faq"])]
    render(path, g["title"] + " — Play Free Online", g["desc"], body, active="play", scripts=[f"games/{g['slug']}.js"], css=["play.css"], ld=ld, priority="0.8")

# games hub
cats = ["All", "Word", "Puzzle", "Arcade", "Strategy", "Skill", "Memory"]
r = "../"
chips = "".join(f'<button class="chip" type="button" data-f="{c}" aria-pressed="{str(c == "All").lower()}">{c}</button>' for c in cats)
hub_js = "<script>document.querySelectorAll('[data-f]').forEach(function(b){b.addEventListener('click',function(){var f=b.getAttribute('data-f');document.querySelectorAll('[data-f]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});document.querySelectorAll('#gamegrid .tile').forEach(function(t){t.hidden=!(f==='All'||t.getAttribute('data-cat')===f)})})});</script>"
body = f'''<div class="wrap phero">{crumbs(r, [("Games", None)])}<h1>Free online games</h1>
<p class="lead">Twelve original browser games — word, puzzle, arcade, strategy and skill. Nothing to download, no sign-up, and every game works on phones, tablets and computers.</p></div>
<section class="wrap"><div class="chips" role="group" aria-label="Filter games" style="margin-bottom:20px">{chips}</div>
<div class="grid g3" id="gamegrid">{"".join(game_tile(r, g, "h2") for g in GAMES)}</div></section>
<section class="wrap section"><div class="cta-band lilac"><div><h2>Play the Daily</h2><p>A new FiveWord, a fresh Sudoku and five trivia questions every day. Build a streak and share your results.</p></div><div class="btn-row"><a class="btn ghost lg" href="{r}daily.html">Today's challenges</a></div></div></section>
<section class="wrap prose section tight"><h2>Why play on AllFun?</h2><p>Every game here is built by AllFun from scratch, tuned for quick sessions and fair play. Scores and streaks are saved in your own browser — there's no account to create and nothing to install. Games load fast, work offline once open, and support keyboard, mouse and touch.</p>
<p>Looking for something to do with a group instead? Try the <a href="{r}tools/charades-generator.html">charades generator</a>, the <a href="{r}tools/team-picker.html">team picker</a> or our <a href="{r}ideas/game-night-ideas.html">game night ideas</a>.</p></section>{hub_js}'''
render("play/index.html", "Free Online Games — No Download", "Play 12 free original browser games: FiveWord, Sudoku, Tile Merge, Minesweeper, Snake, Four in a Row and more. No download, no sign-up, works on any device.",
       body, active="play", ld=[crumb_ld([("Games", None)], "play/index.html"), {"@type": "CollectionPage", "name": "Free online games", "url": canon("play/index.html")}], priority="0.9")

# ---------------------------------------------------------------- tools
for t in TOOLS:
    path = f"tools/{t['slug']}.html"; r = rootof(path)
    others = [x for x in TOOLS if x["slug"] != t["slug"]]
    how = "".join(f"<li>{esc(s)}</li>" for s in t["how"]); tips = "".join(f"<li>{esc(s)}</li>" for s in t["tips"])
    widget = SP.tool_widget(t["slug"])
    scripts = (["wheel.js"] if t["slug"] == "spin-wheel" else []) + ["tools.js"]
    body = f'''<div class="wrap phero ghero" style="padding-bottom:18px">{crumbs(r, [("Tools", "tools/index.html"), (t["title"], None)])}
<h1>{esc(t["h1"])}</h1><p class="lead">{esc(t["short"])}</p></div>
<section class="wrap"><div class="stage">{widget}</div>{share_row(t["title"] + " — free on AllFun")}</section>
<div class="wrap article-grid section tight"><div class="prose">
<p>{esc(t["intro"])}</p>
<h2 id="how">How to use the {esc(t["title"].lower())}</h2><ol>{how}</ol>
<h2 id="ideas">Ideas and tips</h2><ul>{tips}</ul>
{faq_html(t["faq"])}</div>
<aside class="rail"><div class="box"><h3>More fun tools</h3><ul>{"".join(f'<li><a href="{r}tools/{x["slug"]}.html">{x["em"]} {esc(x["title"])}</a></li>' for x in others[:6])}</ul></div>
<div class="box" style="background:var(--mint);color:#1F1A4D"><h3>Planning a group event?</h3><p class="small">Get a free custom plan for team building, parties or game night.</p><a class="btn ghost sm" href="{r}plan.html">Plan it free</a></div></aside></div>'''
    ld = [{"@type": "WebApplication", "name": t["title"], "description": t["desc"], "url": canon(path), "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
          crumb_ld([("Tools", "tools/index.html"), (t["title"], None)], path), faq_ld(t["faq"])]
    render(path, t["title"] + " — Free Online", t["desc"], body, active="tools", scripts=scripts, css=["play.css"], ld=ld, priority="0.8")

r = "../"
body = f'''<div class="wrap phero">{crumbs(r, [("Tools", None)])}<h1>Fun tools for decisions, parties and classrooms</h1>
<p class="lead">Spin a wheel, flip a coin, split teams, roll dice or find something to do. Every tool is free, fast and private — nothing you type leaves your device.</p></div>
<section class="wrap"><div class="grid g2">{"".join(tool_tile(r, t) for t in TOOLS)}</div></section>
<section class="wrap prose section"><h2>Made for real-life moments</h2><p>Teachers use the <a href="{r}tools/spin-wheel.html">spin wheel</a> and <a href="{r}tools/team-picker.html">team picker</a> to call on students fairly. Families settle "who goes first" with the <a href="{r}tools/coin-flip.html">coin flip</a> or <a href="{r}tools/dice-roller.html">dice roller</a>. Party hosts keep the energy up with the <a href="{r}tools/charades-generator.html">charades generator</a> and <a href="{r}tools/would-you-rather.html">would you rather questions</a>. And when nobody knows what to do, there's the <a href="{r}tools/bored-button.html">Bored Button</a>.</p></section>'''
render("tools/index.html", "Free Fun Tools — Spin Wheel, Coin Flip, Team Picker", "Free online fun tools: spin the wheel, coin flip, dice roller, random team generator, charades words, would you rather questions and the Bored Button.",
       body, active="tools", ld=[crumb_ld([("Tools", None)], "tools/index.html")], priority="0.9")

# ---------------------------------------------------------------- quizzes
for slug in QORDER:
    q = QUIZ[slug]; path = f"quizzes/{slug}.html"; r = rootof(path)
    others = [s for s in QORDER if s != slug]
    n = len(q["questions"])
    about = (f"<p>{n} multiple-choice questions, level {esc(q.get('level', 'Easy–Medium'))}. Each answer comes with a one-line explanation, so you learn something whether you're right or wrong. Questions stick to timeless, well-established facts.</p>"
             if q["type"] == "trivia" else "<p>Ten light-hearted questions match you to one of six fun styles — then point you to games, tools and ideas that suit you. There are no wrong answers.</p>")
    fact_link = {"animals": "fun-facts-about-animals", "space": "fun-facts-about-space", "food": "fun-facts-about-food", "history": "fun-facts-about-history", "science": "fun-facts-about-the-human-body", "world-geography": "fun-facts-about-the-ocean"}.get(slug, "random-fun-facts")
    fl = FMAP.get(fact_link)
    body = f'''<div class="wrap phero ghero" style="padding-bottom:18px">{crumbs(r, [("Quizzes", "quizzes/index.html"), (q["title"], None)])}
<h1>{esc(q["title"])} {q["emoji"]}</h1><p class="lead">{esc(q["intro"])}</p></div>
<section class="wrap"><div class="panel" id="quiz" data-quiz="{slug}" aria-live="polite"><p class="muted">Loading quiz…</p></div></section>
<div class="wrap article-grid section tight"><div class="prose"><h2>About this quiz</h2>{about}
{f'<p>Want to brush up first? Read <a href="{r}facts/{fl["slug"]}.html">{esc(fl["title"])}</a>.</p>' if fl else ""}
<p>Play the <a href="{r}daily.html">Daily 5</a> for five fresh questions every day, or challenge friends by sharing your score.</p></div><div></div></div>
<section class="wrap section tight"><div class="sec-head"><h2>More quizzes</h2><a class="more" href="{r}quizzes/index.html">All quizzes</a></div><div class="grid g2">{"".join(quiz_tile(r, s, QUIZ[s]) for s in others[:4])}</div></section>'''
    ld = [{"@type": "Quiz", "name": q["title"], "description": q["description"], "url": canon(path), "educationalLevel": q.get("level", "Beginner"), "isAccessibleForFree": True},
          crumb_ld([("Quizzes", "quizzes/index.html"), (q["title"], None)], path)]
    render(path, q["title"], q["description"], body, active="quizzes", scripts=["quiz.js"], css=["play.css"], ld=ld, priority="0.8")

r = "../"
body = f'''<div class="wrap phero">{crumbs(r, [("Quizzes", None)])}<h1>Free trivia and personality quizzes</h1>
<p class="lead">Fifteen-question trivia quizzes with instant explanations, plus a personality quiz that finds your fun style. No sign-up, no email gate — just questions.</p></div>
<section class="wrap"><div class="cta-band pop" style="margin-bottom:28px"><div><h2>The Daily 5</h2><p>Five mixed trivia questions, the same for everyone, refreshed every day.</p></div><div class="btn-row"><a class="btn ghost lg" href="{r}daily.html#daily5">Play today's 5</a></div></div>
<div class="grid g2">{"".join(quiz_tile(r, s, QUIZ[s]) for s in QORDER)}</div></section>
<section class="wrap prose section"><h2>How our quizzes are made</h2><p>Every question is written by AllFun and checked against reliable reference sources. We avoid trick questions, time-sensitive facts and popular myths, and each answer includes a short explanation so the quiz teaches as much as it tests.</p></section>'''
render("quizzes/index.html", "Free Online Quizzes — Trivia & Personality", "Free trivia quizzes on general knowledge, geography, science, animals, space, food, history and words, plus the What's Your Fun Style personality quiz.",
       body, active="quizzes", ld=[crumb_ld([("Quizzes", None)], "quizzes/index.html")], priority="0.9")

# ---------------------------------------------------------------- ideas & facts hubs
r = "../"
groups = {}
for m, _ in GUIDES: groups.setdefault(m.get("category", "Ideas"), []).append(m)
gh = "".join(f'<h2 style="margin-top:32px">{esc(c)}</h2><div class="grid g2">{"".join(read_tile(r, "ideas", m, "c-ideas") for m in ms)}</div>' for c, ms in groups.items())
body = f'''<div class="wrap phero">{crumbs(r, [("Ideas", None)])}<h1>Fun ideas for every day, crowd and budget</h1>
<p class="lead">Things to do when you're bored, game night plans, party games, team building and family fun — practical lists you can use today.</p></div>
<section class="wrap">{gh}</section>
<section class="wrap section"><div class="cta-band mint"><div><h2>Planning something bigger?</h2><p>Team building, a birthday, a school fun day or a game night for 50 — tell us about it and get a free tailored plan.</p></div><div class="btn-row"><a class="btn ghost lg" href="{r}plan.html">Plan my event</a></div></div></section>'''
render("ideas/index.html", "Fun Ideas — Things to Do, Party Games & Team Building", "Fun ideas for every occasion: things to do when bored, game night ideas, party games for kids and adults, team building activities, date and weekend ideas.",
       body, active="ideas", ld=[crumb_ld([("Ideas", None)], "ideas/index.html")], priority="0.9")

body = f'''<div class="wrap phero">{crumbs(r, [("Fun facts", None)])}<h1>Fun facts that make you say "wait, really?"</h1>
<p class="lead">Hand-checked facts about animals, space, the human body, the ocean, food and history — plus the myths we refused to include.</p></div>
<section class="wrap"><div class="grid g2">{"".join(read_tile(r, "facts", m, "c-facts") for m, _ in FACTS)}</div></section>
<section class="wrap section"><div class="cta-band lilac"><div><h2>Fact of the day</h2><p>One new fact every day on the Daily page, alongside FiveWord, Sudoku and the Daily 5 quiz.</p></div><div class="btn-row"><a class="btn ghost lg" href="{r}daily.html">See today's fact</a></div></div></section>'''
render("facts/index.html", "Fun Facts — Animals, Space, Ocean, Food & History", "Hundreds of fun facts about animals, space, the human body, the ocean, food and history — checked for accuracy, with common myths debunked.",
       body, active="facts", ld=[crumb_ld([("Fun facts", None)], "facts/index.html")], priority="0.9")

# ---------------------------------------------------------------- static / business pages
CTX = dict(GAMES=GAMES, TOOLS=TOOLS, QUIZ=QUIZ, QORDER=QORDER, GUIDES=[m for m, _ in GUIDES], FACTS=[m for m, _ in FACTS], VIDEOS=VIDEOS,
           game_tile=game_tile, tool_tile=tool_tile, quiz_tile=quiz_tile, read_tile=read_tile, crumbs=crumbs, faq_html=faq_html, esc=esc, md=md, SRC=SRC, OWNER_URL=OWNER_URL)
for spec in SP.pages(CTX):
    path = spec["path"]
    ld = spec.get("ld", [])
    if spec.get("crumb"): ld = ld + [crumb_ld(spec["crumb"], path)]
    if spec.get("faq"): ld = ld + [faq_ld(spec["faq"])]
    render(path, spec["title"], spec["desc"], spec["body"](rootof(path)), active=spec.get("active", ""), scripts=spec.get("scripts", []), css=spec.get("css", []),
           noindex=spec.get("noindex", False), ld=ld, priority=spec.get("priority", "0.6"), sitemap=spec.get("sitemap", True), full_title=spec.get("full_title"))

# ---------------------------------------------------------------- sitemap.html (built last so it lists everything)
r = ""
sections = [("Play", "play"), ("Quizzes", "quizzes"), ("Fun tools", "tools"), ("Ideas", "ideas"), ("Fun facts", "facts")]
blocks = ""
listed = set()
for label, key in sections:
    items = sorted([(p, t) for p, t, a in ALLPAGES if p.startswith(key + "/")])
    listed.update(p for p, _ in items)
    blocks += f'<div><h2>{label}</h2><ul>' + "".join(f'<li><a href="{p}">{esc(t)}</a></li>' for p, t in items) + "</ul></div>"
rest = sorted([(p, t) for p, t, a in ALLPAGES if p not in listed and p not in ("kit.html", "thanks.html")])
blocks += '<div><h2>AllFun</h2><ul>' + "".join(f'<li><a href="{p}">{esc(t)}</a></li>' for p, t in rest) + "</ul></div>"
body = f'<div class="wrap phero">{crumbs(r, [("Sitemap", None)])}<h1>Sitemap</h1><p class="lead">Every page on AllFun in one place.</p></div><section class="wrap prose" style="max-width:none"><div class="grid g3">{blocks}</div></section>'
render("sitemap.html", "Sitemap", "A complete list of every game, quiz, tool, idea guide and page on AllFun.", body, priority="0.3")

# ---------------------------------------------------------------- sitemap.xml, robots, ads.txt
urls = "".join(f"<url><loc>{canon(p)}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>\n" for p, pr in SITEMAP)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /kit.html\nDisallow: /thanks.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")
write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
# 404 works at any depth: set <base> to the site root before any relative URL resolves
p404 = os.path.join(BASE, "404.html"); s = open(p404, encoding="utf-8").read()
s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<script>document.write(\'<base href="\'+(location.hostname.slice(-10)===".github.io"?"/"+location.pathname.split("/")[1]+"/":"/")+\'">\');</script>', 1)
open(p404, "w", encoding="utf-8").write(s)

# share image + icon sources (PNGs are rendered in .github/workflows/deploy.yml)
write("assets/img/src/og.svg", art.og_svg()); write("assets/img/src/icon.svg", art.icon_svg())

# favicon + manifest
write("favicon.svg", LOGO.replace('<svg viewBox="0 0 100 100" aria-hidden="true">', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'))
write("site.webmanifest", json.dumps({"name": "AllFun", "short_name": "AllFun", "description": "Free games, quizzes, puzzles and fun ideas.", "start_url": "./index.html", "display": "standalone",
      "background_color": "#EEF0FF", "theme_color": "#1F1A4D", "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}, {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
      {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
print("pages:", len(ALLPAGES), "sitemap:", len(SITEMAP), "facts:", len(FACT_ITEMS))
