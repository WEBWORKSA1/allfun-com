# -*- coding: utf-8 -*-
"""AllFun: home, daily, lead generation, contests, support, careers, advertise, videos, about, contact, legal pages + tool widgets."""
import html, os, random
esc = lambda s: html.escape(str(s), quote=True)
EFFECTIVE = "October 29, 2026"

# Edit contests here. Rounds roll over monthly; winners are listed on the contests page.
CONTESTS = [
  dict(key="highscore", em="🏆", color="sky", title="Tile Merge High-Score Cup", prize="$50 digital gift card", entry="Post a screenshot of your best Tile Merge score (link to it) before the last day of the month.",
       judging="Highest verifiable score wins. Ties go to the earlier entry."),
  dict(key="riddle", em="🧩", color="pop", title="Riddle Writer Challenge", prize="$25 digital gift card + your riddle featured on AllFun", entry="Write one original, family-friendly riddle with its answer.",
       judging="Judged on originality (40%), cleverness (40%) and clarity (20%)."),
  dict(key="gamenight", em="📸", color="sun", title="Game Night Photo of the Month", prize="$25 digital gift card + feature in Friday Fun", entry="Share a link to a family-friendly photo of your game night and tell us what you played.",
       judging="Judged on creativity (50%), fun factor (30%) and story (20%)."),
]

def hp(): return '<div class="hp" aria-hidden="true"><label>Leave this empty<input name="_hp" tabindex="-1" autocomplete="off"></label></div>'

def opt_cards(name, opts, autonext=False, required=True):
    items = "".join(f'<label class="opt-card"><input type="radio" name="{name}" value="{esc(v)}"{" required" if required and i == 0 else ""}><span><i aria-hidden="true">{em}</i>{esc(v)}</span></label>' for i, (em, v) in enumerate(opts))
    return items

# ---------------------------------------------------------------- tool widgets
def tool_widget(slug):
    if slug == "spin-wheel":
        return '''<div id="tool" data-tool="wheel" class="wheel-tool">
<div><div class="wheel-box"><div class="wheel-pin" aria-hidden="true"></div><canvas aria-label="Spinning wheel with your entries"></canvas><button class="wheel-hub" type="button">Spin</button></div>
<div class="wheel-result" id="wh-out" aria-live="polite"></div><div class="history" id="wh-hist" aria-label="Recent results"></div></div>
<div class="tool-controls"><label for="wh-items">Entries (<span id="wh-count">0</span>) <span class="opt">— one per line</span></label><textarea id="wh-items" rows="10" spellcheck="false"></textarea>
<div><p class="small muted" style="margin:0 0 6px">Presets</p><div class="chips" id="wh-presets"></div></div>
<label class="check"><input type="checkbox" id="wh-remove"> Remove the winner after each spin</label>
<label class="check"><input type="checkbox" id="wh-sound"> Tick sound while spinning</label>
<div class="btn-row"><button class="btn" id="wh-spin" type="button">Spin the wheel</button><button class="btn ghost sm" id="wh-shuffle" type="button">Shuffle</button><button class="btn ghost sm" id="wh-share" type="button">Share this wheel</button></div></div></div>'''
    if slug == "team-picker":
        return '''<div id="tool" data-tool="teams"><div class="tool-controls" style="max-width:none;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start">
<div><label for="tp-names">Names (<span id="tp-count">0</span>) <span class="opt">— one per line</span></label><textarea id="tp-names" rows="11"></textarea></div>
<div class="form"><div><label for="tp-mode">Split by</label><select id="tp-mode"><option value="count">Number of teams</option><option value="size">People per team</option></select></div>
<div><label for="tp-n">Number</label><input id="tp-n" type="number" min="1" max="50" value="2"></div>
<label class="check"><input type="checkbox" id="tp-fun" checked> Give teams fun names</label>
<div class="btn-row"><button class="btn" id="tp-go" type="button">Make teams</button><button class="btn ghost sm" id="tp-copy" type="button" hidden>Copy teams</button></div></div></div>
<div id="tp-out" aria-live="polite"></div></div>'''
    if slug == "coin-flip":
        return '''<div id="tool" data-tool="coin" class="center"><div class="coin" role="img" aria-label="Coin"><div class="side heads">HEADS</div><div class="side tails">TAILS</div></div>
<p class="tool-out" id="cf-out" aria-live="polite">Ready</p>
<div class="btn-row" style="justify-content:center"><button class="btn lg" id="cf-flip" type="button">Flip the coin</button>
<label class="vh" for="cf-bo">Series</label><select id="cf-bo" class="mini-select"><option value="1">Single flip</option><option value="3">Best of 3</option><option value="5">Best of 5</option></select>
<button class="btn ghost sm" id="cf-reset" type="button">Reset tally</button></div>
<p id="cf-series" class="muted" aria-live="polite"></p>
<div class="stats" style="justify-content:center;margin-top:10px"><div class="stat"><small>Heads</small><b id="cf-h">0</b></div><div class="stat"><small>Tails</small><b id="cf-t">0</b></div></div>
<div class="history" id="cf-hist" aria-label="Recent flips"></div></div>'''
    if slug == "dice-roller":
        n = "".join(f'<option value="{i}"{" selected" if i == 2 else ""}>{i} {"die" if i == 1 else "dice"}</option>' for i in range(1, 7))
        s = "".join(f'<option value="{i}"{" selected" if i == 6 else ""}>d{i} ({i} sides)</option>' for i in (4, 6, 8, 10, 12, 20))
        return f'''<div id="tool" data-tool="dice" class="center"><div class="btn-row" style="justify-content:center"><label class="vh" for="dr-n">How many dice</label><select id="dr-n" class="mini-select">{n}</select>
<label class="vh" for="dr-s">Sides</label><select id="dr-s" class="mini-select">{s}</select><button class="btn" id="dr-roll" type="button">Roll</button></div>
<div class="dice" aria-live="polite"></div><p class="tool-out" id="dr-out" style="font-size:2rem"></p><div class="history" id="dr-hist" aria-label="Recent rolls"></div></div>'''
    if slug == "bored-button":
        cats = "".join(f'<option value="{c}">{c}</option>' for c in ("Creative", "Active", "Learn", "Social", "Chill", "Outdoors", "Kitchen", "Games"))
        return f'''<div id="tool" data-tool="bored"><div class="form" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));display:grid">
<div><label for="bb-cat">Mood</label><select id="bb-cat"><option value="">Anything</option>{cats}</select></div>
<div><label for="bb-who">Who's around</label><select id="bb-who"><option value="">Anyone</option><option value="solo">Just me</option><option value="friends">Friends</option><option value="family">Family</option></select></div>
<div><label for="bb-cost">Budget</label><select id="bb-cost"><option value="">Any</option><option value="free">Free</option><option value="low">Low cost</option><option value="some">Some cost</option></select></div>
<div><label for="bb-time">Time</label><select id="bb-time"><option value="0">Any</option><option value="15">15 min</option><option value="30">30 min</option><option value="60">1 hour</option><option value="120">2 hours</option></select></div></div>
<p class="center" style="margin:22px 0"><button class="btn lg" id="bb-go" type="button" disabled style="font-size:1.35rem;padding:20px 40px">I'm bored — give me an idea</button></p>
<div id="bb-out" aria-live="polite"></div></div>'''
    if slug == "would-you-rather":
        cats = "".join(f'<option value="{c}">{c}</option>' for c in ("Silly", "Superpowers", "Food", "Travel", "Life", "Kids", "Work & School", "Deep"))
        return f'''<div id="tool" data-tool="wyr"><div class="stage-bar"><div class="btn-row"><label class="vh" for="wy-cat">Category</label><select id="wy-cat" class="mini-select"><option value="">All categories</option>{cats}</select><span class="tag" id="wy-cat-l" style="--c:var(--sunk)">…</span></div>
<div class="stats"><div class="stat"><small>Answered</small><b id="wy-n">0</b></div></div></div>
<p class="quiz-q center">Would you rather…</p>
<div class="wyr"><button type="button" class="a" id="wy-a">Loading…</button><span class="or">or</span><button type="button" class="b" id="wy-b">…</button></div>
<div class="btn-row" style="justify-content:center;margin-top:18px"><button class="btn sun" id="wy-next" type="button" hidden>Next question</button><button class="btn ghost sm" id="wy-skip" type="button">Skip</button><button class="btn ghost sm" id="wy-share" type="button">Share this one</button></div></div>'''
    if slug == "charades-generator":
        return '''<div id="tool" data-tool="charades"><div class="stage-bar"><div class="btn-row">
<label class="vh" for="ch-cat">Category</label><select id="ch-cat" class="mini-select"><option value="">All categories</option></select>
<label class="vh" for="ch-lvl">Difficulty</label><select id="ch-lvl" class="mini-select"><option value="">All levels</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select>
<label class="vh" for="ch-time">Round length</label><select id="ch-time" class="mini-select"><option value="30">30 sec</option><option value="60" selected>60 sec</option><option value="90">90 sec</option><option value="120">2 min</option></select></div>
<div class="stats"><div class="stat"><small>Team A</small><b id="ch-a">0</b></div><div class="stat"><small>Team B</small><b id="ch-b">0</b></div></div></div>
<div class="big-card"><p class="muted" id="ch-team">Team A is up</p><p class="tool-out" id="ch-word" aria-live="polite">Ready?</p><p class="muted" id="ch-c">Press start and show the word only to the actor.</p>
<div id="ch-play" hidden><div class="timer-bar"><i id="ch-bar"></i></div><p><b id="ch-left">60s</b> left</p><div class="btn-row" style="justify-content:center"><button class="btn mint lg" id="ch-got" type="button">Got it! +1</button><button class="btn ghost" id="ch-skip" type="button">Skip word</button></div></div>
<div class="btn-row" style="justify-content:center;margin-top:12px"><button class="btn lg" id="ch-start" type="button">Start round</button><button class="btn ghost sm" id="ch-one" type="button">Just give me a word</button><button class="btn ghost sm" id="ch-reset" type="button">Reset scores</button></div></div></div>'''
    if slug == "random-number":
        return '''<div id="tool" data-tool="number"><div class="form" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr))">
<div><label for="rn-min">Minimum</label><input id="rn-min" type="number" value="1"></div><div><label for="rn-max">Maximum</label><input id="rn-max" type="number" value="100"></div>
<div><label for="rn-count">How many</label><input id="rn-count" type="number" value="1" min="1" max="500"></div></div>
<div class="btn-row" style="margin-top:12px"><label class="check"><input type="checkbox" id="rn-uniq" checked> No repeats</label><label class="check"><input type="checkbox" id="rn-sort"> Sort results</label><button class="btn" id="rn-go" type="button">Generate</button></div>
<p class="tool-out" id="rn-out" aria-live="polite" style="word-break:break-word"></p></div>'''
    return ""

# ---------------------------------------------------------------- pages
def pages(C):
    G, T, Q, QO, GU, FA, V = C["GAMES"], C["TOOLS"], C["QUIZ"], C["QORDER"], C["GUIDES"], C["FACTS"], C["VIDEOS"]
    gt, tt, qt, rt, crumbs, faq_html, OWNER = C["game_tile"], C["tool_tile"], C["quiz_tile"], C["read_tile"], C["crumbs"], C["faq_html"], C["OWNER_URL"]
    gmap = {g["slug"]: g for g in G}
    out = []

    def yt_card(v, h="h3"):
        return (f'<article class="tile"><button type="button" class="yt" data-yt="{esc(v["id"])}" aria-label="Play video: {esc(v["title"])}"></button>'
                f'<div class="body"><{h}>{esc(v["title"])}</{h}><p>{esc(v.get("blurb", ""))}</p><div class="meta"><span>{esc(v["channel"])}</span><span>{esc(v["category"])}</span></div></div></article>')

    # ------------------------------------------------ HOME
    def home(r):
        feat = ["fiveword", "sudoku", "tile-merge", "snake", "minesweeper", "four-in-a-row", "memory-match", "typing-test"]
        guides = GU[:6]
        facts = FA[:4]
        quick = [("🧩", "Team building", "Team building (in person)"), ("💻", "Virtual team event", "Virtual team event"), ("🎂", "Birthday party", "Birthday party"),
                 ("🎲", "Game night", "Game night"), ("🏫", "School or club", "School or club event"), ("👪", "Family reunion", "Family reunion")]
        qchips = "".join(f'<a class="chip" href="{r}plan.html?event_type={esc(v).replace(" ", "+")}">{em} {esc(l)}</a>' for em, l, v in quick)
        vids = "".join(yt_card(v) for v in V[:3])
        return f'''<section class="hero"><div class="wrap hero-grid">
<div><h1>All the fun. None of the downloads.</h1>
<p class="lead">Free browser games, daily puzzles, trivia quizzes, party tools and ideas for every crowd. Open a tab, start playing — no sign-up, ever.</p>
<div class="btn-row"><a class="btn sun lg" href="{r}play/fiveword.html">Play today's FiveWord</a><a class="btn ghost lg" href="{r}play/index.html">Browse all games</a></div>
<p class="hero-meta">{len(G)} games · {len(QO)} quizzes · {len(T)} fun tools · {len(GU) + len(FA)} guides and fact collections — all free.</p></div>
<div><div class="wheel-box"><div class="wheel-pin" aria-hidden="true"></div><canvas id="hero-wheel" aria-label="Fun picker wheel"></canvas><button class="wheel-hub" type="button" aria-label="Spin the fun wheel">Spin</button></div>
<div class="wheel-result" id="hero-pick" aria-live="polite"><p class="center muted small" style="margin-top:6px">Can't decide? Spin for something fun.</p></div></div>
</div></section>

<section class="section tight"><div class="wrap"><div class="sec-head"><div><h2>Today on AllFun</h2><p><span data-date></span> · Your streak: <span class="streak">🔥 <span data-streak>0 days</span></span></p></div><a class="more" href="{r}daily.html">All daily challenges</a></div>
<div class="daily">
<a class="tile c-facts" href="{r}play/fiveword.html"><div class="body"><span class="tag" data-daily-status="fiveword">New today</span><h3 style="margin-top:8px">FiveWord #<span data-dayno></span></h3><p>Six tries to find today's word.</p></div></a>
<a class="tile c-facts" href="{r}play/sudoku.html#daily"><div class="body"><span class="tag" data-daily-status="sudoku">New today</span><h3 style="margin-top:8px">Daily Sudoku</h3><p>One grid, the same for everyone.</p></div></a>
<a class="tile c-facts" href="{r}daily.html#daily5"><div class="body"><span class="tag" data-daily-status="trivia">New today</span><h3 style="margin-top:8px">Daily 5 trivia</h3><p>Five questions. Two minutes.</p></div></a>
<div class="tile c-facts"><div class="body"><span class="tag">Fact of the day</span><div id="fact-of-day" style="margin-top:8px"><p class="muted">Loading…</p></div></div></div>
</div></div></section>

<section class="section tight"><div class="wrap"><div class="sec-head"><div><h2>Play a game</h2><p>Original games built for quick breaks. Keyboard, mouse or touch.</p></div><a class="more" href="{r}play/index.html">All {len(G)} games</a></div>
<div class="grid g4">{"".join(gt(r, gmap[s]) for s in feat)}</div></div></section>

<section class="section tight"><div class="wrap"><div class="sec-head"><div><h2>Quizzes</h2><p>Trivia with instant explanations — plus one quiz that's all about you.</p></div><a class="more" href="{r}quizzes/index.html">All quizzes</a></div>
<div class="grid g2">{"".join(qt(r, s, Q[s]) for s in QO[:6])}</div></div></section>

<section class="section tight"><div class="wrap"><div class="sec-head"><div><h2>Fun tools</h2><p>Settle debates, split teams and run the party.</p></div><a class="more" href="{r}tools/index.html">All tools</a></div>
<div class="grid g2">{"".join(tt(r, t) for t in T[:6])}</div></div></section>

<section class="section"><div class="wrap"><div class="cta-band mint"><div><h2>Planning a team event, party or game night?</h2>
<p>Tell us the occasion, group size and budget. Our free Plan My Fun service sends a tailored plan within one business day — with vetted planner quotes if you want them.</p>
<div class="chips" style="margin-top:14px">{qchips}</div></div>
<div><ul><li>Free, no obligation</li><li>Ideas for 2 to 500+ people</li><li>In person, virtual or hybrid</li></ul><p style="margin-top:16px"><a class="btn ghost lg" href="{r}plan.html">Plan my event free</a></p></div></div></div></section>

<section class="section tight"><div class="wrap"><div class="split">
<div><div class="sec-head"><h2>Fun ideas</h2><a class="more" href="{r}ideas/index.html">All ideas</a></div><div class="grid" style="gap:12px">{"".join(rt(r, "ideas", m, "c-ideas") for m in guides)}</div></div>
<div><div class="sec-head"><h2>Fun facts</h2><a class="more" href="{r}facts/index.html">All facts</a></div><div class="grid" style="gap:12px">{"".join(rt(r, "facts", m, "c-facts") for m in facts)}</div></div>
</div></div></section>

<section class="section"><div class="wrap"><div class="cta-band"><div><h2>Free Game Night Kit</h2><p>30 printable party games, a host checklist, score sheets, 25 tie-breaker trivia questions and a game-night bingo card. Enter your email and it opens instantly.</p></div>
<form class="form" data-form="Game Night Kit request" data-redirect="{r}kit.html"><input type="hidden" name="lead_type" value="Game Night Kit (home)">
<label for="hk-email">Email address</label><input id="hk-email" type="email" name="email" required autocomplete="email" placeholder="you@example.com">
<label class="check"><input type="checkbox" name="newsletter" value="yes" checked> Also send me Friday Fun (one email a week, unsubscribe anytime)</label>{hp()}
<button class="btn ghost" type="submit">Send me the kit</button><p class="form-status" role="status"></p></form></div></div></section>

<section class="section tight"><div class="wrap"><div class="grid g3">
<a class="tile" href="{r}contests.html" style="--c:var(--sky)"><div class="art"><span class="em" aria-hidden="true">🏆</span></div><div class="body"><h3>Monthly contests</h3><p>High scores, riddles and game-night photos. Free to enter, real prizes.</p></div></a>
<a class="tile" href="{r}support.html" style="--c:var(--pop)"><div class="art"><span class="em" aria-hidden="true">♥</span></div><div class="body"><h3>Keep AllFun free</h3><p>Supporters fund new games, prizes and creators. See exactly where it goes.</p></div></a>
<a class="tile" href="{r}careers.html" style="--c:var(--mint)"><div class="art"><span class="em" aria-hidden="true">🛠️</span></div><div class="body"><h3>Make games with us</h3><p>We hire game developers, puzzle writers, illustrators and creators.</p></div></a>
</div></div></section>

{f'<section class="section tight"><div class="wrap"><div class="sec-head"><div><h2>Watch something fun</h2><p>Hand-picked riddles, science and satisfying builds.</p></div><a class="more" href="{r}videos.html">All videos</a></div><div class="grid g3">{vids}</div></div></section>' if vids else ""}

<section class="section tight"><div class="wrap prose"><h2>What is AllFun?</h2>
<p>AllFun is a free, family-friendly playground for the internet. We build original browser games, write trivia and personality quizzes, make simple tools for parties and classrooms, and publish practical guides to having more fun — with friends, family, coworkers or on your own. Everything runs in your browser and saves progress on your device, so there's no account to create.</p>
<p>New here? Start with <a href="{r}play/fiveword.html">today's FiveWord</a>, find your <a href="{r}quizzes/fun-style.html">fun style</a>, or press the <a href="{r}tools/bored-button.html">Bored Button</a>.</p></div></section>'''
    out.append(dict(path="index.html", title="AllFun", full_title="AllFun — Free Online Games, Quizzes, Puzzles & Fun Ideas",
        desc="Free online games, daily puzzles, trivia quizzes, spin wheel and party tools, plus fun ideas for game night, parties and team building. No download, no sign-up.",
        body=home, scripts=["wheel.js", "home.js"], css=["play.css"], priority="1.0"))

    # ------------------------------------------------ DAILY
    def daily(r):
        return f'''<div class="wrap phero">{crumbs(r, [("Daily", None)])}<h1>Today's daily challenges</h1>
<p class="lead"><span data-date></span>. Three quick challenges, the same for everyone, refreshed at midnight your time. Finish any one to keep your streak alive.</p>
<p><span class="streak">🔥 Streak: <span data-streak>0 days</span></span></p></div>
<section class="wrap"><div class="daily">
<a class="tile c-facts" href="{r}play/fiveword.html"><div class="body"><span class="tag" data-daily-status="fiveword">New today</span><h2 style="font-size:1.4rem;margin-top:8px">FiveWord #<span data-dayno></span></h2><p>Guess the five-letter word in six tries.</p></div></a>
<a class="tile c-facts" href="{r}play/sudoku.html#daily"><div class="body"><span class="tag" data-daily-status="sudoku">New today</span><h2 style="font-size:1.4rem;margin-top:8px">Daily Sudoku</h2><p>A medium grid with one solution.</p></div></a>
<a class="tile c-facts" href="#daily5"><div class="body"><span class="tag" data-daily-status="trivia">New today</span><h2 style="font-size:1.4rem;margin-top:8px">Daily 5 trivia</h2><p>Five mixed questions, below.</p></div></a>
</div></section>
<section class="wrap section tight" id="daily5"><h2>Daily 5 trivia</h2><div class="panel" id="quiz" data-daily aria-live="polite"><p class="muted">Loading today's questions…</p></div></section>
<section class="wrap section tight"><div class="split">
<div class="panel"><h2>Fact of the day</h2><div id="fact-of-day"><p class="muted">Loading…</p></div></div>
<div class="panel"><h2>Would you rather of the day</h2><div id="wyr-of-day"><p class="muted">Loading…</p></div><p class="small muted" style="margin-top:12px">More dilemmas in the <a href="{r}tools/would-you-rather.html">Would You Rather</a> tool.</p></div>
</div></section>
<section class="wrap section tight prose"><h2>How streaks work</h2><p>Complete at least one daily challenge — FiveWord, the Daily Sudoku or the Daily 5 — on a given day and your streak grows by one. Miss a day and it starts again. Streaks are saved in your browser on this device, so there's nothing to sign up for (and clearing your browser data will reset them).</p>
<p>Want a nudge? Subscribe to Friday Fun at the bottom of the page for a weekly round-up of new games and quizzes.</p></section>'''
    out.append(dict(path="daily.html", title="Daily Challenges — Word, Sudoku & Trivia", desc="Today's free daily challenges: FiveWord, Daily Sudoku and the Daily 5 trivia quiz, plus a fact and a would-you-rather of the day. Build your streak.",
        body=daily, active="daily", scripts=["home.js", "quiz.js"], css=["play.css"], crumb=[("Daily", None)], priority="0.9"))

    # ------------------------------------------------ PLAN (lead gen)
    plan_faq = [("Is Plan My Fun really free?", "Yes. Planning ideas and introductions to partners are free for you. If you choose to book a partner, you deal with them directly and AllFun may receive a referral fee from that partner — it never changes your price."),
        ("How fast will I hear back?", "Within one business day, usually sooner. Urgent date? Mention it in your notes."),
        ("Do you run the events yourselves?", "For small groups we send a ready-to-run plan you can host yourself. For larger or professionally facilitated events, we match you with vetted planners, venues and hosts."),
        ("Who sees my details?", "AllFun reviews every request. With your consent, we share it with up to three relevant partners so they can send ideas or quotes. We never sell your details to marketers."),
        ("Can you help with virtual or international teams?", "Yes. Many of our ideas work over any video-call app and across time zones.")]
    def plan(r):
        ev = [("🧩", "Team building (in person)"), ("💻", "Virtual team event"), ("🎂", "Birthday party"), ("🎈", "Kids' party"), ("🎲", "Game night"), ("🏫", "School or club event"), ("👪", "Family reunion"), ("📣", "Brand or community event"), ("✨", "Something else")]
        goals = "".join(f'<label class="opt-card"><input type="checkbox" name="goals" value="{g}"><span><i aria-hidden="true">{e}</i>{g}</span></label>' for e, g in [("🤝", "Team bonding"), ("🎉", "Celebrate"), ("👋", "Welcome new people"), ("💡", "Learn something"), ("💛", "Raise funds"), ("😂", "Pure fun")])
        return f'''<section class="hero" style="padding-top:clamp(28px,4vw,48px)"><div class="wrap hero-grid" style="align-items:start">
<div>{crumbs(r, [("Plan My Fun", None)])}<h1 style="font-size:clamp(2.2rem,5vw,3.8rem)">Plan a fun group event — free.</h1>
<p class="lead">Team building, a birthday, a school fun day or a game night for 200. Answer four quick questions and get a tailored plan within one business day — plus quotes from vetted planners if you want them.</p>
<div class="trust" style="flex-direction:column;gap:8px;font-size:1.02rem"><span>Free and no obligation</span><span>Ideas for 2 to 500+ people</span><span>In person, virtual or hybrid</span><span>Reply within one business day</span></div></div>
<div class="panel"><form class="form" data-form="Plan My Fun lead" data-steps data-redirect="thanks.html?f=plan" novalidate>
<input type="hidden" name="lead_type" value="Plan My Fun">
<div class="steps-bar" aria-hidden="true"><i></i><i></i><i></i><i></i></div><p class="step-label" aria-live="polite">Step 1 of 4</p>
<div class="step"><fieldset class="opt-grid" data-need-one data-autonext><legend>What are you planning?</legend>{opt_cards("event_type", ev)}</fieldset></div>
<div class="step" hidden><h2 style="font-size:1.3rem">Tell us about the group</h2>
<div class="two"><div><label for="pl-size">Group size</label><select id="pl-size" name="group_size" required><option value="">Choose…</option><option>2–10</option><option>11–25</option><option>26–50</option><option>51–100</option><option>101–250</option><option>250+</option></select></div>
<div><label for="pl-when">When</label><select id="pl-when" name="timeframe" required><option value="">Choose…</option><option>Within 2 weeks</option><option>This month</option><option>1–3 months</option><option>3+ months</option><option>Not sure yet</option></select></div></div>
<div class="two"><div><label for="pl-date">Date <span class="opt">(if known)</span></label><input id="pl-date" type="date" name="event_date"></div>
<div><label for="pl-format">Format</label><select id="pl-format" name="format"><option>In person</option><option>Virtual</option><option>Hybrid</option><option>Not sure</option></select></div></div>
<div><label for="pl-city">City or region <span class="opt">(for in-person events)</span></label><input id="pl-city" type="text" name="location" autocomplete="address-level2"></div></div>
<div class="step" hidden><h2 style="font-size:1.3rem">Budget and goals</h2>
<div><label for="pl-budget">Total budget</label><select id="pl-budget" name="budget" required><option value="">Choose…</option><option>DIY — free ideas only</option><option>Under $250</option><option>$250–$1,000</option><option>$1,000–$5,000</option><option>$5,000–$20,000</option><option>$20,000+</option><option>Not sure yet</option></select></div>
<fieldset class="opt-grid" style="margin-top:6px"><legend style="font-size:1rem">Goals <span class="opt">(pick any)</span></legend>{goals}</fieldset>
<div><label for="pl-notes">Anything else? <span class="opt">(ages, accessibility, themes, must-haves)</span></label><textarea id="pl-notes" name="notes" rows="3"></textarea></div></div>
<div class="step" hidden><h2 style="font-size:1.3rem">Where should we send your plan?</h2>
<div class="two"><div><label for="pl-name">Your name</label><input id="pl-name" name="name" required autocomplete="name"></div><div><label for="pl-email">Email</label><input id="pl-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="two"><div><label for="pl-phone">Phone <span class="opt">(optional)</span></label><input id="pl-phone" type="tel" name="phone" autocomplete="tel"></div><div><label for="pl-org">Company or group <span class="opt">(optional)</span></label><input id="pl-org" name="organization" autocomplete="organization"></div></div>
<div><label for="pl-pref">Best way to reach you</label><select id="pl-pref" name="contact_pref"><option>Email</option><option>Phone</option><option>Either</option></select></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required> AllFun may contact me about this request and share it with up to three vetted partners so they can send ideas or quotes. <a href="{r}privacy.html">Privacy policy</a></label>{hp()}
<button class="btn lg" type="submit">Get my free fun plan</button></div>
<p class="form-status" role="status"></p>
<div class="step-nav"><button class="btn ghost sm" type="button" data-prev>Back</button><button class="btn sun sm" type="button" data-next>Continue</button></div>
</form><p class="fine" style="margin-top:10px">Takes about 60 seconds. We reply within one business day.</p></div>
</div></section>
<section class="section tight"><div class="wrap"><h2>What you get</h2><div class="grid g3" style="margin-top:16px">
<div class="panel"><h3>🗒️ A tailored idea list</h3><p class="muted">Activities matched to your group's size, ages, setting and goals — not a generic top-ten.</p></div>
<div class="panel"><h3>🧭 A ready-to-run plan</h3><p class="muted">Timing, materials, scoring and a host script so the event runs itself, even if you've never facilitated before.</p></div>
<div class="panel"><h3>🤝 Optional partner quotes</h3><p class="muted">Want it handled for you? We introduce up to three vetted planners, hosts or venues. You choose; no pressure.</p></div></div></div></section>
<section class="section tight"><div class="wrap"><h2>How it works</h2><ol class="steps" style="margin-top:16px">
<li><h3>Tell us the basics</h3><p>Four quick steps: occasion, group, budget, contact.</p></li>
<li><h3>We build your plan</h3><p>An AllFun editor reviews your request and drafts ideas that fit.</p></li>
<li><h3>Pick your path</h3><p>Run it yourself with our plan, or compare partner quotes.</p></li>
<li><h3>Have a great time</h3><p>Then tell us how it went — we love hearing about it.</p></li></ol></div></section>
<section class="section tight"><div class="wrap split"><div class="panel" style="background:var(--sunk)"><h2 style="font-size:1.4rem">Sample plan: 25-person virtual team hour</h2>
<ul><li><b>0:00–0:10</b> — Icebreaker: two truths and a tall tale in breakout rooms</li><li><b>0:10–0:30</b> — Team trivia, five rounds, shared scoreboard</li><li><b>0:30–0:45</b> — Drawing-guessing relay on a shared whiteboard</li><li><b>0:45–0:55</b> — Would-you-rather lightning round</li><li><b>0:55–1:00</b> — Shout-outs and winners</li></ul>
<p class="small muted">Every plan includes links to the free tools you'll need, like the <a href="{r}tools/team-picker.html">team picker</a> and <a href="{r}tools/spin-wheel.html">spin wheel</a>.</p></div>
<div>{faq_html(plan_faq)}</div></div></section>
<section class="section"><div class="wrap"><div class="cta-band"><div><h2>Hosting something small?</h2><p>Our free Game Night Kit has 30 printable games and everything you need to run a great night at home.</p></div><div class="btn-row"><a class="btn ghost lg" href="{r}free-kit.html">Get the free kit</a></div></div></div></section>'''
    out.append(dict(path="plan.html", title="Plan My Fun — Free Team Building & Party Planning", desc="Plan a team building event, party or game night free. Answer four quick questions and get a tailored fun plan in one business day, plus optional vetted planner quotes.",
        body=plan, active="", crumb=[("Plan My Fun", None)], faq=plan_faq, priority="0.9"))

    # ------------------------------------------------ FREE KIT + KIT
    def free_kit(r):
        return f'''<section class="hero"><div class="wrap hero-grid" style="align-items:start">
<div>{crumbs(r, [("Free Game Night Kit", None)])}<h1 style="font-size:clamp(2.2rem,5vw,3.8rem)">The free Game Night Kit</h1>
<p class="lead">Everything you need to host a brilliant game night with zero prep: printable, family-friendly and free.</p>
<div class="trust" style="flex-direction:column;gap:8px;font-size:1.02rem"><span>30 party games with rules, player counts and timing</span><span>12-point host checklist</span><span>Scoring systems and low-cost prize ideas</span><span>25 tie-breaker trivia questions with answers</span><span>Printable score sheet and game-night bingo card</span></div></div>
<div class="panel"><h2 style="font-size:1.5rem">Get instant access</h2><form class="form" data-form="Game Night Kit request" data-redirect="kit.html">
<input type="hidden" name="lead_type" value="Game Night Kit">
<div><label for="fk-name">First name <span class="opt">(optional)</span></label><input id="fk-name" name="name" autocomplete="given-name"></div>
<div><label for="fk-email">Email</label><input id="fk-email" type="email" name="email" required autocomplete="email"></div>
<div><label for="fk-for">Who's it for?</label><select id="fk-for" name="audience"><option>Family</option><option>Friends</option><option>Office or team</option><option>Classroom</option><option>Club or community group</option><option>Other</option></select></div>
<label class="check"><input type="checkbox" name="newsletter" value="yes" checked> Send me Friday Fun — one email a week with new games and ideas. Unsubscribe anytime.</label>{hp()}
<button class="btn lg" type="submit">Open my free kit</button><p class="form-status" role="status"></p>
<p class="fine">We use your email to send the kit link and, if you opt in, Friday Fun. See our <a href="{r}privacy.html">privacy policy</a>.</p></form></div></div></section>
<section class="section tight"><div class="wrap prose"><h2>Why a printed kit?</h2><p>Phones are great for timers and scoreboards, but paper keeps everyone in the room. The kit is designed to print on standard letter or A4 paper: one page of rules per few games, a reusable score sheet and a bingo card that turns the whole evening into a meta-game. Mix in our <a href="{r}tools/charades-generator.html">charades generator</a> and <a href="{r}tools/team-picker.html">team picker</a> for the digital bits.</p>
<p>Looking for more inspiration? Read <a href="{r}ideas/game-night-ideas.html">40 game night ideas</a> or <a href="{r}ideas/party-games-for-kids.html">party games for kids by age</a>.</p></div></section>'''
    out.append(dict(path="free-kit.html", title="Free Printable Game Night Kit", desc="Get the free AllFun Game Night Kit: 30 printable party games, host checklist, score sheets, tie-breaker trivia and a bingo card. Instant access.", body=free_kit, crumb=[("Free Game Night Kit", None)], priority="0.8"))

    kit_md = open(os.path.join(C["SRC"], "content", "kit.md"), encoding="utf-8").read() if os.path.exists(os.path.join(C["SRC"], "content", "kit.md")) else ""
    def kit(r):
        return f'''<div class="wrap phero"><h1>Your AllFun Game Night Kit</h1><p class="lead">Print it, bookmark it, share it with your co-host. Have a brilliant night.</p>
<div class="btn-row no-print"><button class="btn" type="button" onclick="window.print()">Print the kit</button><a class="btn ghost" href="{r}tools/charades-generator.html">Open the charades generator</a><a class="btn ghost" href="{r}tools/team-picker.html">Make teams</a></div></div>
<div class="wrap"><article class="prose" style="max-width:80ch">{C["md"](kit_md)}</article></div>'''
    out.append(dict(path="kit.html", title="Game Night Kit", desc="The AllFun printable Game Night Kit.", body=kit, noindex=True, sitemap=False))

    def thanks(r):
        js = '''<script>(function(){var f=new URLSearchParams(location.search).get("f")||"";var m={plan:["Request received!","An AllFun editor will review your event and reply within one business day. Keep an eye on your inbox (and spam folder, just in case)."],pledge:["Thank you for supporting AllFun!","We'll email a secure payment link within one business day. Your support funds new games, prizes and creators."],apply:["Application received!","Thanks for your interest in making fun with us. If your skills match an open project, we'll be in touch within two weeks."],pitch:["Game pitch received!","We review every pitch. If it's a fit, we'll reach out about featuring it."],contest:["Your entry is in!","Good luck! Winners are announced on the contests page and contacted by email."],ads:["Thanks — we'll be in touch.","We'll reply within two business days with options and our media kit."]};var x=m[f];if(x){document.getElementById("t-h").textContent=x[0];document.getElementById("t-p").textContent=x[1];}})();</script>'''
        return f'''<div class="wrap phero center"><p style="font-size:4rem;margin:0" aria-hidden="true">🎉</p><h1 id="t-h">Thanks — message sent!</h1><p class="lead" id="t-p" style="margin-left:auto;margin-right:auto">We received your message and will reply soon.</p>
<div class="btn-row" style="justify-content:center"><a class="btn sun" href="{r}play/index.html">Play a game while you wait</a><a class="btn ghost" href="{r}index.html">Back to home</a></div></div>
<section class="wrap section tight"><div class="grid g4">{"".join(gt(r, gmap[s]) for s in ("fiveword", "tile-merge", "snake", "memory-match"))}</div></section>{js}'''
    out.append(dict(path="thanks.html", title="Thank you", desc="Thanks for contacting AllFun.", body=thanks, noindex=True, sitemap=False))

    # ------------------------------------------------ CONTESTS
    contest_faq = [("Do I have to pay to enter?", "No. Every AllFun contest is free to enter. No purchase is necessary and buying anything does not improve your chances."),
        ("How are winners chosen?", "By skill or by a judging panel using the published criteria — never by random draw."),
        ("When are winners announced?", "Within 14 days after each monthly round closes, on this page and by email to the winners."),
        ("Can kids enter?", "Entrants under the age of majority where they live need a parent or guardian's permission, and the parent or guardian accepts the prize on their behalf."),
        ("Can my company sponsor a prize?", "Yes! Sponsors get logo placement on this page and in Friday Fun. See Advertise & sponsor.")]
    def contests(r):
        cards = "".join(f'''<article class="tile" style="--c:var(--{c["color"]})"><div class="art" style="aspect-ratio:16/7"><span class="em" aria-hidden="true">{c["em"]}</span></div><div class="body"><h3>{esc(c["title"])}</h3>
<p><b>Prize:</b> {esc(c["prize"])}</p><p><b>How to enter:</b> {esc(c["entry"])}</p><p><b>Judging:</b> {esc(c["judging"])}</p><div class="meta"><span>Monthly · free entry</span></div></div></article>''' for c in CONTESTS)
        opts = "".join(f'<option value="{esc(c["title"])}">{esc(c["title"])}</option>' for c in CONTESTS)
        return f'''<div class="wrap phero">{crumbs(r, [("Contests", None)])}<h1>Contests with real prizes</h1>
<p class="lead">Monthly skill contests for players, puzzle-makers and game-night hosts. Free to enter, judged fairly, and funded by AllFun supporters and sponsors.</p></div>
<section class="wrap"><div class="grid g3">{cards}</div></section>
<section class="wrap section tight split">
<div class="panel"><h2>Enter a contest</h2><form class="form" data-form="Contest entry" data-redirect="thanks.html?f=contest">
<div><label for="ct-c">Contest</label><select id="ct-c" name="contest" required>{opts}</select></div>
<div class="two"><div><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div><label for="ct-email">Email</label><input id="ct-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="two"><div><label for="ct-country">Country</label><input id="ct-country" name="country" required autocomplete="country-name"></div><div><label for="ct-handle">Display name for winners list <span class="opt">(optional)</span></label><input id="ct-handle" name="display_name"></div></div>
<div><label for="ct-link">Link to your entry <span class="opt">(screenshot or photo link)</span></label><input id="ct-link" type="url" name="entry_link" placeholder="https://"></div>
<div><label for="ct-text">Your entry or description <span class="opt">(riddle + answer, or what you played)</span></label><textarea id="ct-text" name="entry_text" rows="4" required></textarea></div>
<label class="check"><input type="checkbox" name="age_ok" value="yes" required> I'm of the age of majority where I live, or I have a parent or guardian's permission to enter.</label>
<label class="check"><input type="checkbox" name="rules_ok" value="yes" required> I agree to the official rules below and confirm my entry is my own original work.</label>{hp()}
<button class="btn lg" type="submit">Submit my entry</button><p class="form-status" role="status"></p></form></div>
<div><div class="panel" style="background:var(--sunk)"><h2>Winners' wall</h2><p>The first winners will be announced here after the current round closes. Be the first name on the wall.</p></div>
<div class="cta-band sky" style="margin-top:22px;grid-template-columns:1fr"><div><h2 style="font-size:1.5rem">Sponsor a prize</h2><p>Put your brand in front of thousands of happy players. Prize sponsors get logo placement here and in Friday Fun.</p><p><a class="btn ghost" href="{r}advertise.html#sponsor">Become a sponsor</a></p></div></div></div></section>
<section class="wrap section tight prose" id="rules"><h2>Official rules</h2>
<details open><summary><b>1. Sponsor and eligibility</b></summary><p>Contests are run by AllFun.com ("AllFun"). Open to individuals worldwide where not prohibited by law. Entrants under the age of majority in their place of residence must have permission from a parent or legal guardian, who must accept any prize on their behalf. Employees and contractors of AllFun and their immediate households may not win. Void where prohibited or restricted.</p></details>
<details><summary><b>2. No purchase necessary</b></summary><p>No purchase, payment or donation is necessary to enter or win. Supporting AllFun does not improve your chances of winning.</p></details>
<details><summary><b>3. How to enter</b></summary><p>Use the entry form on this page during the open round (the calendar month). Limit one entry per person per contest per round. Entries must be your own original, family-friendly work and must not infringe anyone's rights. Automated or bulk entries are disqualified.</p></details>
<details><summary><b>4. Judging</b></summary><p>Winners are selected on skill or merit using the criteria shown for each contest — not by chance. High-score entries must be verifiable; AllFun may request additional proof. Judges' decisions are final.</p></details>
<details><summary><b>5. Prizes</b></summary><p>Prizes are as described for each contest. Prizes are non-transferable; no cash alternative unless AllFun chooses to offer one. AllFun may substitute a prize of equal or greater value. Winners are responsible for any taxes. Where required by local law, a skill-testing question may need to be answered correctly before a prize is awarded.</p></details>
<details><summary><b>6. Winner notification</b></summary><p>Winners are notified by email within 14 days after the round closes and must reply within 14 days, or an alternate winner may be selected.</p></details>
<details><summary><b>7. License and publicity</b></summary><p>By entering, you give AllFun a non-exclusive, royalty-free license to display your entry and display name on AllFun and its channels in connection with the contest. You keep ownership of your entry.</p></details>
<details><summary><b>8. Privacy and general conditions</b></summary><p>Entry information is used to run the contest as described in our <a href="{r}privacy.html">privacy policy</a>. AllFun may cancel, modify or suspend a contest if it cannot run as planned, and may disqualify entries that break these rules. These rules are subject to applicable law.</p></details></section>
<section class="wrap section tight">{faq_html(contest_faq)}</section>'''
    out.append(dict(path="contests.html", title="Contests & Prizes", desc="Enter free monthly AllFun contests: Tile Merge high-score cup, riddle writer challenge and game night photo of the month. Real prizes, fair judging, official rules.",
        body=contests, crumb=[("Contests", None)], faq=contest_faq, priority="0.7"))

    # ------------------------------------------------ SUPPORT (donations)
    support_faq = [("Is my contribution tax-deductible?", "No. AllFun is an independent website, not a registered charity, so contributions are not tax-deductible."),
        ("Do supporters get extra games?", "No — every game stays free for everyone. Supporters get a thank-you on our Supporters wall (if they want it), a supporter badge in Friday Fun and a vote on which game we build next."),
        ("How do I pay?", "If instant checkout buttons appear above, use those. Otherwise send a pledge and we'll email a secure payment link within one business day."),
        ("Can I cancel a monthly contribution?", "Anytime. Reply to any receipt or use the contact page and we'll stop it immediately."),
        ("Can I direct my gift?", "Yes — choose where it goes in the form. We'll report how earmarked support was spent.")]
    def support(r):
        tiers = [(3, "Coffee for the dev"), (5, "Fuel a new puzzle"), (10, "Fund a game hour"), (25, "Prize patron"), (50, "Level boss"), (100, "Legend")]
        tb = "".join(f'<button type="button" class="tier" data-amount="{a}" aria-pressed="{"true" if a == 10 else "false"}"><b>${a}</b><small>{esc(l)}</small></button>' for a, l in tiers)
        alloc = [("var(--sky)", 35, "New games & hiring creators"), ("var(--mint)", 25, "Operations & hosting"), ("var(--sun)", 20, "Contests & prizes"), ("var(--pop)", 20, "Promotion & marketing")]
        bar = "".join(f'<i style="width:{p}%;background:{c}" title="{l} {p}%"></i>' for c, p, l in alloc)
        leg = "".join(f'<span style="--c:{c}"><b>{p}%</b> {esc(l)}</span>' for c, p, l in alloc)
        return f'''<div class="wrap phero">{crumbs(r, [("Support AllFun", None)])}<h1>Keep AllFun free for everyone</h1>
<p class="lead">No paywalls, no accounts, no pay-to-win. Reader support pays for new games, contest prizes, the creators we hire and getting the word out.</p></div>
<section class="wrap split">
<div class="panel"><h2>Choose your support</h2>
<form class="form" data-form="Support pledge" data-redirect="thanks.html?f=pledge">
<fieldset class="opt-grid" style="grid-template-columns:repeat(2,1fr)"><legend style="font-size:1rem">How often?</legend>
<label class="opt-card"><input type="radio" name="frequency" value="Monthly" checked><span><i aria-hidden="true">🔁</i>Monthly</span></label><label class="opt-card"><input type="radio" name="frequency" value="One-time"><span><i aria-hidden="true">⭐</i>One-time</span></label></fieldset>
<div class="tiers" role="group" aria-label="Amount">{tb}</div>
<div class="two"><div><label for="amount">Amount</label><input id="amount" type="number" name="amount" min="1" step="1" value="10" required></div>
<div><label for="cur">Currency</label><select id="cur" name="currency"><option>USD</option><option>CAD</option><option>EUR</option><option>GBP</option><option>INR</option><option>AUD</option></select></div></div>
<div><label for="earmark">Where should it go?</label><select id="earmark" name="earmark"><option>Wherever it's needed most</option><option>New games & creators</option><option>Contests & prizes</option><option>Promotion & marketing</option><option>Operations & hosting</option></select></div>
<div class="two"><div><label for="sp-name">Name</label><input id="sp-name" name="name" required autocomplete="name"></div><div><label for="sp-email">Email</label><input id="sp-email" type="email" name="email" required autocomplete="email"></div></div>
<label class="check"><input type="checkbox" name="public_thanks" value="yes"> Thank me publicly on the Supporters wall</label>
<div><label for="sp-display">Display name <span class="opt">(optional)</span></label><input id="sp-display" name="display_name"></div>
<div><label for="sp-msg">Message <span class="opt">(optional)</span></label><textarea id="sp-msg" name="message" rows="2"></textarea></div>{hp()}
<div id="pay-live" hidden><p class="small"><b>Pay instantly:</b> pick a secure checkout below, or send the pledge and we'll email a link.</p><div class="btn-row" id="pay-links"></div></div>
<p class="small muted" id="pay-pledge">We'll email you a secure payment link within one business day. Nothing is charged until you complete it.</p>
<button class="btn lg" type="submit">Send my pledge</button><p class="form-status" role="status"></p></form></div>
<div><div class="panel"><h2>Where your support goes</h2><div class="alloc" role="img" aria-label="Budget split: 35% new games and creators, 25% operations, 20% contests, 20% promotion">{bar}</div><div class="legend">{leg}</div>
<p class="small muted" style="margin-top:12px">We publish a short spending summary for supporters every quarter.</p></div>
<div class="panel" style="margin-top:22px"><h2>What supporters get</h2><ul><li>A thank-you on the Supporters wall (opt-in)</li><li>A supporter badge in Friday Fun</li><li>A vote on the next game we build</li><li>Early looks at new games before launch</li></ul><p class="small muted">Every game stays free for everyone, always.</p></div>
<div class="panel" style="margin-top:22px;background:var(--sunk)"><h2>Other ways to help</h2><ul><li>Share a game you love with a friend or class</li><li><a href="{r}careers.html">Make games or puzzles with us</a></li><li><a href="{r}advertise.html#sponsor">Sponsor a contest prize</a></li><li><a href="{r}contact.html">Report a bug or suggest an idea</a></li></ul></div></div></section>
<section class="wrap section tight">{faq_html(support_faq)}</section>'''
    out.append(dict(path="support.html", title="Support AllFun — Keep It Free", desc="Support AllFun with a monthly or one-time contribution. See exactly where it goes: new games, creators, contest prizes and promotion. Every game stays free.",
        body=support, crumb=[("Support AllFun", None)], faq=support_faq, priority="0.6"))

    # ------------------------------------------------ CAREERS
    roles = [("🕹️", "HTML5 Game Developer", "Contract · Remote", "Build small, polished browser games in vanilla JavaScript or a lightweight framework. You care about feel, performance on cheap phones and accessibility.", "A portfolio of playable web games; clean, dependency-light code."),
             ("🧩", "Puzzle & Quiz Writer", "Freelance · Remote", "Write trivia sets, riddles, word puzzles and personality quizzes that are accurate, fair and genuinely fun.", "Writing samples and a love of fact-checking."),
             ("🎨", "Illustrator / Motion Designer", "Freelance · Remote", "Create characters, game art and small animations in AllFun's bright, sticker-book style.", "A portfolio with playful character and UI work."),
             ("🛡️", "Community & Contest Moderator", "Part-time · Remote", "Review contest entries, verify high scores, answer players and keep everything friendly and fair.", "Good judgment, clear writing, a few hours a week."),
             ("🎬", "Video Creator / Editor", "Freelance · Remote", "Make short videos of game tips, puzzle walkthroughs and party ideas for social channels.", "Short-form editing samples."),
             ("🤝", "Partnerships & Sponsorship Lead", "Commission · Remote", "Bring brands, event partners and prize sponsors to AllFun.", "Experience selling sponsorships or media.")]
    def careers(r):
        cards = "".join(f'<article class="panel"><h3>{em} {esc(t)}</h3><p class="small muted">{esc(k)}</p><p>{esc(d)}</p><p class="small"><b>We look for:</b> {esc(w)}</p></article>' for em, t, k, d, w in roles)
        ropts = "".join(f"<option>{esc(t)}</option>" for _, t, _, _, _ in roles)
        return f'''<div class="wrap phero">{crumbs(r, [("Careers & creators", None)])}<h1>Make fun for a living (or a weekend)</h1>
<p class="lead">AllFun is a small, remote-first studio. We hire freelancers and contractors around the world to build games, write puzzles, draw, moderate and grow the community.</p></div>
<section class="wrap"><h2>Open roles</h2><div class="grid g2" style="margin-top:14px">{cards}</div></section>
<section class="wrap section tight split">
<div class="panel"><h2>Apply</h2><form class="form" data-form="Job application" data-redirect="thanks.html?f=apply">
<div><label for="ap-role">Role</label><select id="ap-role" name="role" required>{ropts}<option>Something else</option></select></div>
<div class="two"><div><label for="ap-name">Name</label><input id="ap-name" name="name" required autocomplete="name"></div><div><label for="ap-email">Email</label><input id="ap-email" type="email" name="email" required autocomplete="email"></div></div>
<div><label for="ap-port">Portfolio, GitHub or LinkedIn</label><input id="ap-port" type="url" name="portfolio" required placeholder="https://"></div>
<div class="two"><div><label for="ap-loc">Location / time zone</label><input id="ap-loc" name="location" required></div><div><label for="ap-av">Availability</label><select id="ap-av" name="availability"><option>A few hours a week</option><option>Part-time</option><option>Full-time contract</option><option>Project by project</option></select></div></div>
<div><label for="ap-rate">Rate expectations <span class="opt">(optional)</span></label><input id="ap-rate" name="rate"></div>
<div><label for="ap-msg">Tell us about something fun you made</label><textarea id="ap-msg" name="message" rows="4" required></textarea></div>{hp()}
<button class="btn lg" type="submit">Send application</button><p class="form-status" role="status"></p></form></div>
<div class="panel" style="background:var(--sunk)"><h2>Made a browser game? Pitch it.</h2><p>We feature great indie HTML5 games and puzzles. If you own the rights and it's family-friendly, tell us about it.</p>
<form class="form" data-form="Game pitch" data-redirect="thanks.html?f=pitch">
<div><label for="gp-title">Game title</label><input id="gp-title" name="game_title" required></div>
<div><label for="gp-url">Playable link</label><input id="gp-url" type="url" name="game_url" required placeholder="https://"></div>
<div class="two"><div><label for="gp-name">Your name</label><input id="gp-name" name="name" required></div><div><label for="gp-email">Email</label><input id="gp-email" type="email" name="email" required></div></div>
<div><label for="gp-desc">What makes it fun?</label><textarea id="gp-desc" name="description" rows="3" required></textarea></div>
<label class="check"><input type="checkbox" name="rights" value="yes" required> I own or control the rights to this game and it contains no third-party trademarks or copyrighted assets I can't license.</label>{hp()}
<button class="btn sun" type="submit">Send pitch</button><p class="form-status" role="status"></p></form></div></section>'''
    out.append(dict(path="careers.html", title="Careers & Creators — Work With AllFun", desc="Join AllFun as a freelance HTML5 game developer, puzzle and quiz writer, illustrator, moderator, video creator or partnerships lead. Remote, worldwide.",
        body=careers, crumb=[("Careers & creators", None)], priority="0.6"))

    # ------------------------------------------------ ADVERTISE
    fmts = [("☀️", "Sponsored Daily", "Your brand on a day's FiveWord, Sudoku and Daily 5 — the most-visited part of the site."), ("❓", "Branded quiz", "A custom trivia or personality quiz about your topic, written to our quality bar and clearly labeled."),
            ("🏆", "Contest sponsorship", "Fund a monthly prize and get logo placement on the contests page and in Friday Fun."), ("📬", "Newsletter sponsor", "A short, clearly marked message in Friday Fun."),
            ("🧰", "Tool sponsorship", "Sponsor a popular tool like the Spin Wheel or Team Picker for a month."), ("🎮", "Custom mini-game", "A branded browser game built by our studio for campaigns, events or trade shows.")]
    def advertise(r):
        cards = "".join(f'<div class="panel"><h3>{em} {esc(t)}</h3><p class="muted">{esc(d)}</p></div>' for em, t, d in fmts)
        ints = "".join(f'<label class="opt-card"><input type="checkbox" name="interest" value="{esc(t)}"><span><i aria-hidden="true">{em}</i>{esc(t)}</span></label>' for em, t, _ in fmts)
        return f'''<div class="wrap phero">{crumbs(r, [("Advertise & sponsor", None)])}<h1>Advertise and sponsor on AllFun</h1>
<p class="lead">Reach curious, playful people — families, students, office teams and casual players — in a brand-safe, family-friendly environment. Every sponsored placement is clearly labeled.</p>
<div class="btn-row"><a class="btn" href="#sponsor">Request the media kit</a><a class="btn ghost" href="{OWNER}" rel="noopener" target="_blank">Domain, acquisition or partnership inquiry</a></div></div>
<section class="wrap"><h2>Formats</h2><div class="grid g3" style="margin-top:14px">{cards}</div></section>
<section class="wrap section tight split" id="sponsor">
<div class="panel"><h2>Tell us about your campaign</h2><form class="form" data-form="Advertising inquiry" data-redirect="thanks.html?f=ads">
<div class="two"><div><label for="ad-name">Name</label><input id="ad-name" name="name" required autocomplete="name"></div><div><label for="ad-email">Work email</label><input id="ad-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="two"><div><label for="ad-co">Company</label><input id="ad-co" name="company" required autocomplete="organization"></div><div><label for="ad-web">Website</label><input id="ad-web" type="url" name="website" placeholder="https://"></div></div>
<fieldset class="opt-grid"><legend style="font-size:1rem">Interested in</legend>{ints}</fieldset>
<div class="two"><div><label for="ad-budget">Budget</label><select id="ad-budget" name="budget"><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>$10,000+</option><option>Not sure yet</option></select></div>
<div><label for="ad-time">Timing</label><select id="ad-time" name="timeline"><option>As soon as possible</option><option>Next month</option><option>Next quarter</option><option>Just exploring</option></select></div></div>
<div><label for="ad-msg">Goals and details</label><textarea id="ad-msg" name="message" rows="4"></textarea></div>{hp()}
<button class="btn lg" type="submit">Request media kit</button><p class="form-status" role="status"></p></form></div>
<div><div class="panel"><h2>Our standards</h2><ul><li>Family-friendly brands and messages only</li><li>Every sponsored item is labeled "Sponsored"</li><li>No sponsored content disguised as editorial</li><li>We don't sell visitor data</li><li>Display ads are served by Google AdSense under Google's policies</li></ul></div>
<div class="cta-band lilac" style="grid-template-columns:1fr;margin-top:22px"><div><h2 style="font-size:1.5rem">Interested in AllFun.com itself?</h2><p>For domain acquisition, partnership or joint-venture inquiries, contact the owner directly.</p><p><a class="btn ghost" href="{OWNER}" rel="noopener" target="_blank">Contact the owner</a></p></div></div></div></section>'''
    out.append(dict(path="advertise.html", title="Advertise & Sponsor", desc="Advertise on AllFun: sponsored daily challenges, branded quizzes, contest sponsorships, newsletter and tool sponsorships, and custom mini-games. Request our media kit.",
        body=advertise, crumb=[("Advertise & sponsor", None)], priority="0.6"))

    # ------------------------------------------------ VIDEOS
    def videos(r):
        cats = []
        for v in V:
            if v["category"] not in cats: cats.append(v["category"])
        blocks = "".join(f'<h2 style="margin-top:32px">{esc(c)}</h2><div class="grid g3">{"".join(yt_card(v) for v in V if v["category"] == c)}</div>' for c in cats)
        return f'''<div class="wrap phero">{crumbs(r, [("Videos", None)])}<h1>Fun videos worth your time</h1>
<p class="lead">Hand-picked riddles, science experiments, satisfying builds and game challenges from great creators. Videos load only when you press play.</p></div>
<section class="wrap">{blocks or "<p>Videos are coming soon.</p>"}
<p class="small muted" style="margin-top:22px">Videos are embedded with YouTube's privacy-enhanced player. All rights belong to their creators; AllFun is not affiliated with these channels.</p></section>
<section class="wrap section tight split"><div class="prose"><h2>Turn watching into playing</h2><p>Loved the riddles? Try <a href="{r}play/minesweeper.html">Minesweeper</a> or the <a href="{r}play/sudoku.html">daily Sudoku</a> — both are pure logic. Inspired by the chain-reaction machines? Our <a href="{r}ideas/rainy-day-activities-for-kids.html">rainy day activities</a> include build-it-yourself ideas.</p></div>
<div class="panel"><h2>Suggest a video</h2><form class="form" data-form="Video suggestion" data-ok="Thanks! We'll take a look.">
<div><label for="vs-url">YouTube link</label><input id="vs-url" type="url" name="video_url" required placeholder="https://"></div>
<div><label for="vs-why">Why is it fun?</label><textarea id="vs-why" name="why" rows="3"></textarea></div>
<div><label for="vs-email">Your email <span class="opt">(optional)</span></label><input id="vs-email" type="email" name="email"></div>{hp()}
<button class="btn sun" type="submit">Suggest it</button><p class="form-status" role="status"></p></form></div></section>'''
    out.append(dict(path="videos.html", title="Fun Videos — Riddles, Science & Satisfying Builds", desc="Hand-picked fun videos: brain-teasing riddles, backyard science, domino and marble machines, and trick-shot challenges from great YouTube creators.",
        body=videos, crumb=[("Videos", None)], priority="0.6"))

    # ------------------------------------------------ ABOUT / CONTACT
    def about(r):
        return f'''<div class="wrap phero">{crumbs(r, [("About", None)])}<h1>About AllFun</h1><p class="lead">A free, family-friendly playground for the internet — original games, quizzes, tools and ideas, with no downloads and no accounts.</p></div>
<div class="wrap prose section tight"><h2>What we make</h2><p>AllFun builds and publishes {len(G)} original browser games, {len(QO)} quizzes, {len(T)} fun tools and a growing library of practical guides and fact collections. Everything is designed for short, satisfying sessions on any device, and for groups as much as for solo play.</p>
<h2>Our standards</h2><ul><li><b>Original.</b> Our games are coded by us and our writing is our own. Where we embed someone else's work, like a YouTube video, we credit the creator.</li><li><b>Accurate.</b> Facts and quiz answers are checked against reliable references. We leave out popular myths — and sometimes explain why.</li><li><b>Family-friendly.</b> No violence, adult themes or gambling mechanics. Content is suitable for a general audience.</li><li><b>Light on data.</b> No accounts. Scores and streaks live in your browser. Forms send only what you type.</li><li><b>Accessible.</b> Keyboard support, readable type, respectful motion and dark mode.</li></ul>
<h2>How AllFun is funded</h2><p>We show display ads from Google AdSense, offer clearly labeled sponsorships, accept optional reader support, and run a free event-planning service that may earn referral fees from partner planners. None of these change what's free on the site.</p>
<h2>Say hello</h2><p>Questions, ideas, bug reports or partnership proposals: use the <a href="{r}contact.html">contact page</a>. Planning an event? Try <a href="{r}plan.html">Plan My Fun</a>.</p></div>'''
    out.append(dict(path="about.html", title="About AllFun", desc="AllFun is a free, family-friendly playground of original browser games, quizzes, fun tools and ideas. Learn about our standards and how we're funded.", body=about, crumb=[("About", None)], priority="0.5"))

    def contact(r):
        return f'''<div class="wrap phero">{crumbs(r, [("Contact", None)])}<h1>Contact AllFun</h1><p class="lead">We read every message and reply within one to two business days.</p></div>
<section class="wrap split"><div class="panel"><form class="form" data-form="Contact message" data-ok="Message sent. We'll reply within one to two business days.">
<div class="two"><div><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div><div><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div></div>
<div><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>General question</option><option>Bug report</option><option>Game or quiz idea</option><option>Event planning</option><option>Advertising or sponsorship</option><option>Partnership</option><option>Press</option><option>Support or donation</option><option>Careers</option><option>Copyright or trademark notice</option><option>Privacy request</option></select></div>
<div><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>{hp()}
<button class="btn lg" type="submit">Send message</button><p class="form-status" role="status"></p></form></div>
<div><div class="panel"><h2>Prefer email?</h2><p><a class="btn ghost" href="#" data-mail="Hello AllFun">Email us</a></p><p class="small muted">Opens your email app with our address filled in.</p></div>
<div class="panel" style="margin-top:22px"><h2>Quick links</h2><ul><li><a href="{r}plan.html">Plan an event (free)</a></li><li><a href="{r}advertise.html">Advertise or sponsor</a></li><li><a href="{r}careers.html">Work with us</a></li><li><a href="{r}support.html">Support AllFun</a></li></ul></div>
<div class="panel" style="margin-top:22px;background:var(--lilac);color:#1F1A4D"><h2>About this domain</h2><p>Interested in this website, the AllFun.com domain name, sponsorship, advertisement or partnership?</p><a class="btn ghost" href="{OWNER}" rel="noopener" target="_blank">Contact the owner</a></div></div></section>'''
    out.append(dict(path="contact.html", title="Contact", desc="Contact AllFun about games, bugs, event planning, advertising, sponsorship, partnerships, press or careers. We reply within one to two business days.", body=contact, crumb=[("Contact", None)], priority="0.5"))

    # ------------------------------------------------ LEGAL
    def legal(title, sections):
        def f(r):
            body = "".join(f"<h2>{esc(h)}</h2>{t}" for h, t in sections)
            return f'<div class="wrap phero">{crumbs(r, [(title, None)])}<h1>{esc(title)}</h1><p class="muted">Effective {EFFECTIVE}</p></div><div class="wrap prose">{body}</div>'
        return f
    privacy = [
        ("Overview", "<p>This policy explains what information AllFun.com (\"AllFun\", \"we\") collects, how we use it and the choices you have. AllFun is designed to work without accounts: games, quizzes and tools run in your browser.</p>"),
        ("Information you give us", "<p>When you submit a form (contact, Plan My Fun, Game Night Kit, newsletter, contest, support pledge, job application, game pitch or advertising inquiry) we receive the details you type, such as your name, email address and message. We use them only to respond, deliver what you asked for and run the related service.</p><p>Plan My Fun requests may be shared with up to three relevant partner planners, hosts or venues <b>only when you tick the consent box</b>, so they can send ideas or quotes. We never sell your personal information.</p>"),
        ("Information stored on your device", "<p>We use your browser's local storage to remember game progress, scores, streaks, theme and settings. This data stays on your device; we can't see it. Clearing your browser data removes it.</p>"),
        ("Advertising and cookies", "<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to AllFun and/or other sites on the internet.</p><p>You can opt out of personalized advertising by visiting <a href=\"https://www.google.com/settings/ads\" rel=\"noopener\" target=\"_blank\">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href=\"https://optout.aboutads.info/\" rel=\"noopener\" target=\"_blank\">aboutads.info</a> and <a href=\"https://www.youronlinechoices.eu/\" rel=\"noopener\" target=\"_blank\">youronlinechoices.eu</a>. Learn more in <a href=\"https://policies.google.com/technologies/partner-sites\" rel=\"noopener\" target=\"_blank\">How Google uses information from sites or apps that use its services</a>.</p><p>Our cookie notice lets you choose \"Essential only\", which requests non-personalized ads. Visitors in the EEA, UK and Switzerland may also see Google's consent message.</p>"),
        ("Service providers", "<p>Form submissions are delivered to our inbox by FormSubmit (formsubmit.co). Fonts are served by Google Fonts. Videos use YouTube's privacy-enhanced player, which loads only when you press play; YouTube's own policies then apply. The site is hosted on GitHub Pages, which may log basic technical data such as IP addresses for security.</p>"),
        ("Children", "<p>AllFun is a general-audience website. It is not directed to children under 13 and we do not knowingly collect personal information from them. Kids can play games without giving any information. If you believe a child has sent us personal information, contact us and we will delete it.</p>"),
        ("Retention and security", "<p>We keep form submissions only as long as needed for the purpose you submitted them for, and then delete them. We use reasonable measures to protect information, but no method of transmission is perfectly secure.</p>"),
        ("Your rights", "<p>Depending on where you live (for example under the GDPR, UK GDPR, Canada's PIPEDA or California law), you may have the right to access, correct, delete or object to the use of your personal information, and to withdraw consent. To make a request, use the <a href=\"contact.html\">contact page</a> and choose \"Privacy request\". Newsletter emails include an unsubscribe link.</p>"),
        ("Changes", "<p>We may update this policy and will change the effective date above when we do.</p>")]
    terms = [
        ("Using AllFun", "<p>By using AllFun.com you agree to these terms. AllFun is provided for personal, non-commercial entertainment and education. You may use our games and tools in classrooms, offices and events without asking.</p>"),
        ("Acceptable use", "<p>Don't misuse the site: no attempts to disrupt it, scrape it at scale, submit spam or harmful content, interfere with ads, or cheat contests.</p>"),
        ("Our content", "<p>The AllFun games, code, text, quizzes, illustrations and design are owned by AllFun or its licensors and protected by copyright. Classic game mechanics are not owned by anyone; our implementations of them are ours.</p>"),
        ("Your submissions", "<p>When you send us ideas, contest entries or feedback, you confirm you have the right to do so and grant AllFun a non-exclusive, royalty-free license to use, display and adapt them in connection with the site. You keep ownership.</p>"),
        ("Services and partners", "<p>Plan My Fun provides ideas and optional introductions to independent partners. Any booking is between you and the partner; AllFun is not responsible for third-party services but may receive referral fees.</p>"),
        ("Contests and support", "<p>Contests are governed by the <a href=\"contests.html#rules\">official rules</a>. Contributions on the Support page are voluntary, are not tax-deductible and do not buy goods or services.</p>"),
        ("Disclaimers", "<p>AllFun is provided \"as is\" without warranties of any kind. We work hard on accuracy but can't guarantee every fact or that the site will always be available. To the extent permitted by law, AllFun is not liable for indirect or consequential damages arising from use of the site.</p>"),
        ("Links", "<p>We link to other websites and embed third-party media. We don't control and aren't responsible for them.</p>"),
        ("Changes and contact", "<p>We may update these terms; continued use means you accept the changes. Questions: <a href=\"contact.html\">contact us</a>.</p>")]
    disclaimer = [
        ("Entertainment and information only", "<p>Everything on AllFun is for entertainment and general information. Nothing here is professional, medical, legal, financial or safety advice. Activities in our guides should be done with common sense, and with adult supervision for children.</p>"),
        ("Accuracy", "<p>We check facts and quiz answers against reliable sources, but mistakes can happen. If you spot one, tell us through the <a href=\"contact.html\">contact page</a> and we'll fix it.</p>"),
        ("Advertising disclosure", "<p>AllFun displays ads served by Google AdSense. We don't choose individual ads and an ad is not an endorsement. Sponsored content, when present, is labeled \"Sponsored\".</p>"),
        ("Referral disclosure", "<p>Plan My Fun may introduce you to partner planners, hosts or venues, and AllFun may receive a referral fee if you book with them. This never increases your price.</p>"),
        ("No gambling", "<p>AllFun games are for fun only. There is no real-money play, betting or purchasable advantage. Contest prizes are awarded on skill or merit, never by chance.</p>"),
        ("External content", "<p>Embedded videos and external links belong to their owners. Their views are their own.</p>")]
    trademark = [
        ("Independent website", "<p>AllFun.com is an independent website. The name \"AllFun\" is used descriptively for a website offering many kinds of fun. AllFun.com is <b>not affiliated with, endorsed by, sponsored by or connected to</b> any company, product, app, game, venue, entertainment center or brand named \"All Fun\", \"AllFun\", \"Allfun\", \"All-Fun\" or any similar name. Any such names belong to their respective owners.</p>"),
        ("Third-party marks", "<p>All trademarks, service marks, logos and brand names mentioned on this site (including in embedded video titles) are the property of their respective owners and are used only for identification. Their use does not imply endorsement.</p>"),
        ("Our games", "<p>Our games are original software written by AllFun. They use classic, generic game mechanics (such as grid logic puzzles, sliding-tile merging, snake and three- or four-in-a-row) and are given their own names. They are not affiliated with any commercial product that uses similar mechanics.</p>"),
        ("Copyright", "<p>© 2026 AllFun.com. Site text, code, quizzes and illustrations are protected by copyright. YouTube videos are embedded through YouTube's official player; rights remain with their creators.</p>"),
        ("Copyright or trademark concerns", "<p>If you believe content on AllFun infringes your copyright or trademark, send a notice through the <a href=\"contact.html\">contact page</a> (topic: \"Copyright or trademark notice\") with your contact details, a description of the work or mark, the URL of the material, and a statement that you have a good-faith belief the use is unauthorized. We respond promptly and remove material where appropriate.</p>")]
    out.append(dict(path="privacy.html", title="Privacy Policy", desc="How AllFun handles information: forms, on-device storage, Google AdSense cookies and how to opt out, service providers, children's privacy and your rights.", body=legal("Privacy Policy", privacy), crumb=[("Privacy Policy", None)], priority="0.3"))
    out.append(dict(path="terms.html", title="Terms of Use", desc="The terms for using AllFun.com: acceptable use, our content, your submissions, partners, contests, disclaimers and changes.", body=legal("Terms of Use", terms), crumb=[("Terms of Use", None)], priority="0.3"))
    out.append(dict(path="disclaimer.html", title="Disclaimer", desc="AllFun disclaimer: entertainment and information only, accuracy, advertising and referral disclosures, no gambling and external content.", body=legal("Disclaimer", disclaimer), crumb=[("Disclaimer", None)], priority="0.3"))
    out.append(dict(path="trademark.html", title="Trademark & Copyright Notice", desc="AllFun.com is an independent website not affiliated with any brand named All Fun or similar. Trademark, copyright and infringement notice process.", body=legal("Trademark & Copyright Notice", trademark), crumb=[("Trademark & Copyright Notice", None)], priority="0.3"))

    # ------------------------------------------------ 404
    def notfound(r):
        return f'''<div class="wrap phero center"><p style="font-size:5rem;margin:0" aria-hidden="true">🙃</p><h1>This page wandered off.</h1><p class="lead" style="margin:0 auto 22px">The link may be old or mistyped. Here's something fun instead.</p>
<div class="btn-row" style="justify-content:center"><button class="btn sun lg" data-random>Surprise me</button><a class="btn ghost lg" href="index.html">Go home</a></div></div>
<section class="wrap section tight"><div class="grid g4">{"".join(gt(r, gmap[s]) for s in ("fiveword", "sudoku", "snake", "tile-merge"))}</div></section>'''
    out.append(dict(path="404.html", title="Page not found", desc="This page doesn't exist — but there's plenty of fun on AllFun.", body=notfound, noindex=True, sitemap=False))
    return out
