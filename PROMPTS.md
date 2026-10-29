# AllFun.com — Business case and phase-wise build prompt

Prepared 2026-10-29. Market figures are third-party estimates (Semrush, seodata.dev, vendor pricing pages, published RPM benchmarks) collected in `_build/research/market.md`; treat them as orders of magnitude. Competitive feature audit of 52 sites: `RESEARCH.md`.

---

## 1. The decision: what AllFun.com should be

**Model: an original "fun hub" with a habit loop, utility traffic, evergreen content, and a high-ticket lead-gen service bolted on.**

| Layer | What it is on the site | Job in the business |
|---|---|---|
| Habit | Daily FiveWord, Daily Sudoku, Daily 5 trivia, streaks, shareable result grids | Repeat visits, pages/session, word of mouth |
| Utility magnets | Spin wheel, coin flip, dice, team picker, random number, charades, would-you-rather, bored button | Raw search volume (head terms in the 0.2M–1.8M/month range) |
| Original games | 12 in-house HTML5 games with how-to, strategy and FAQ copy | Dwell time + AdSense-safe original content |
| Evergreen content | 14 idea guides + 7 fact collections | Long-tail SEO, topical authority, AdSense approval depth |
| Monetization | AdSense (auto ads), **Plan My Fun** lead gen, Game Night Kit email capture, sponsorships, contests, reader support, creator hiring | Revenue diversification |

### Why this model wins (the numbers)

- **Demand exists at scale.** US monthly searches: "flip a coin" 1.83M, "coin flip" 1.22–1.5M, "spin the wheel" 0.82–1.0M, "random number generator" 1.5M, "tic tac toe" 1.0M, "would you rather questions" 201K, "fun games" 201K, "fun facts" 135K, "party games" 60.5K, "team building activities" 368K–1.22M (tools disagree).
- **The ceiling is proven.** wheelofnames.com ≈22.7M visits/month on essentially one tool; neal.fun ≈12.7M on a handful of original toys; sporcle.com ≈15.5M with **7.9 pages/visit and 17-minute sessions** (the habit + quiz model); poki.com ≈178M (portal scale we will not chase).
- **The money is asymmetric.** Consumer fun keywords carry $0.05–$0.44 CPCs. "Virtual team building activities" carries **$12.56**, "corporate team building activities" **$11.56**. Vendors sell a 30-person virtual event from ~$1,000 and a 25-person in-person event for $2,800–$4,600. One planning lead is worth more than tens of thousands of coin-flip pageviews at display RPMs. That is why the lead-gen form sits in the global nav and inside every team/party guide.
- **Content beats portals for approval.** sessionlab.com (a content site, ~254K visits) ranks #1 in the US for "team building activities" — content wins that SERP, not vendors.

### Alternatives rejected

1. **Embedded game portal (Poki/CrazyGames clone).** Third-party iframed games = thin/duplicated content → high AdSense "low-value content" rejection risk; zero moat against 120–178M-visit incumbents; the embedded games run their own ads.
2. **Pure listicle / fun-facts site.** Low dwell, low RPM ($0.06 CPC on "fun facts"), saturated by AI content farms.
3. **"All Fun" venue directory (family entertainment centers).** Heavy data upkeep and the highest trademark-collision risk with real venues using similar names.

### Revenue model at month 12 (assumptions, not forecasts)

| Driver | Conservative | Base | Bold |
|---|---|---|---|
| Monthly pageviews | 100K | 400K | 1.5M |
| AdSense page RPM | $3 | $5 | $7 |
| **AdSense** | **$300** | **$2,000** | **$10,500** |
| Plan My Fun leads / month | 10 | 40 | 150 |
| Realized value per lead (referral fees, sold leads, own events) | $60 | $60 | $60 |
| **Lead gen** | **$600** | **$2,400** | **$9,000** |
| Sponsorships (daily, contests, newsletter) | $0 | $500 | $3,000 |
| Reader support | $50 | $200 | $800 |
| **Total / month** | **$950** | **$5,100** | **$23,300** |

The lead line is the lever: at base case it out-earns AdSense on 1/10th of the traffic. Prioritize team-building, virtual-team and icebreaker content and outreach to HR/people-ops audiences.

### Flaws to fix (do not skip)

1. **AdSense cannot approve a github.io subdomain.** Point `allfun.com` DNS at GitHub Pages, add the `CNAME` file, and confirm `https://allfun.com/ads.txt` resolves *before* applying. `ads.txt` only counts at the domain root.
2. **Utility tools bounce.** Wheel/coin tools show 1.2–2.4 pages/visit and 64–85% bounce. They buy volume, not depth — every tool page therefore cross-links to games, the Daily and Plan My Fun.
3. **FormSubmit is a free relay, not a CRM.** First submission triggers a one-time activation email; it has rate limits. Move leads to a real CRM (or Supabase + a serverless function) once volume passes ~50 leads/month.
4. **Referral fees are not yet contracted.** "Realized value per lead" is zero until 3–5 planner/vendor partners sign referral terms (target 10–20% or a flat per-lead fee). Close those before scaling traffic to team-building pages.
5. **The name is descriptive.** Other businesses may use similar names; the site carries an independence disclosure. Do not file a trademark without a clearance search.

### Bold path vs safe path (next 90 days)

- **Safe:** ship as-is, connect domain, Search Console + AdSense, publish 2 guides/week, wait for organic.
- **Bold:** same, plus (a) sign 5 team-building partners on per-lead terms, (b) launch a paid "AllFun Live" hosted virtual game hour at $25–40/person using our own games (you keep 100% instead of a referral cut), (c) run the monthly contests with a sponsored prize pool, (d) push the Daily share grid on social. The bold path turns AllFun from a display-ad site into an events business with a free top-of-funnel.

---

## 2. Phase-wise build prompt (reusable)

Copy each phase into a fresh session in order. Replace the bracketed values. **Never paste the owner's email in plain text into a prompt that writes files** — supply it once as two base64-encoded, reversed halves for `assets/js/config.js` (`_k`), so it never appears in markup or in the repo as plain text.

### Phase 0 — Inputs and guardrails
```
You are building ALLFUN.COM, a static, GitHub-Pages-compatible website (free plan; no server code).
Inputs: domain [allfun.com]; GitHub repo [WEBWORKSA1/allFun-com]; AdSense client [ca-pub-6620975821265271];
owner contact URL [https://web.works/contact]; owner email: provided ONLY as encoded parts for config.js.
Hard rules:
- Put the AdSense script tag in the <head> of every page; add ads.txt (google.com, pub-…, DIRECT, f08c47fec0942fa0).
- Every page shows a top bar: "Contact, if you are interested in this website / domain name / Sponsorship /
  Advertisement / Partnership" linking to the owner contact URL.
- The owner email must never appear in any page, attribute or file in plain text. Assemble it at runtime from
  encoded parts only for (a) the form relay endpoint and (b) "Email us" links that build a mailto on click.
- 100% original code and copy; no trademarked game/brand names (generic names only); family-friendly;
  no gambling, alcohol, violence; no invented statistics, testimonials or reviews.
- Include a trademark/copyright disclosure that the site is independent and not affiliated with any brand
  named "All Fun"/"Allfun" or similar.
```

### Phase 1 — Research
```
Visit at least 35 world-class sites across: browser game portals, daily puzzle sites, quiz/trivia sites,
random-picker tools, boredom/fun-fact sites, kids' learning games, team-building vendors and donation UIs.
For each record core offer, standout features, forms (fields, steps, CTA copy patterns), content types,
navigation, design, monetization, one thing to copy, one weakness to exploit. Write RESEARCH.md with a
summary table, per-site notes and a ranked must-have feature list. Separately collect market data with
sources (traffic estimates, search volume, CPCs, vendor pricing, RPM ranges) and 16 embeddable,
family-friendly YouTube videos (IDs taken only from real URLs) into _build/research/.
```

### Phase 2 — Architecture and design system
```
Information architecture: Home · Games (12) · Quizzes (9) · Tools (8) · Ideas (14 guides) · Facts (7) ·
Daily · Plan My Fun (lead gen) · Free Game Night Kit · Contests · Support · Careers · Advertise · Videos ·
About · Contact · Privacy · Terms · Disclaimer · Trademark · Sitemap · 404 · Thanks.
Design: "sticker-book arcade" — periwinkle paper (#EEF0FF), indigo ink (#1F1A4D) outlines with hard offset
shadows, category colors that encode content type (games sky #5B95FF, quizzes pink #FF5C8A, tools mint
#22C7A9, ideas sun #FFC93C, facts/daily lilac #B9A6FF). Type: Bricolage Grotesque (display) + Atkinson
Hyperlegible (body). Signature moment: a live spin wheel in the home hero that picks your next activity.
Dark mode, visible focus, reduced-motion support, 16px mobile gutters, no horizontal scroll.
```

### Phase 3 — Engine and layout
```
Write a Python generator (_build/build.py) that renders every page from shared head/header/footer
templates with relative links (works at a github.io subpath and at the custom domain). Head: title,
meta description, canonical (https://allfun.com/...), Open Graph, JSON-LD (WebSite, Organization,
BreadcrumbList, Article/VideoGame/WebApplication/Quiz, FAQPage), fonts, CSS, AdSense tag.
Core JS (assets/js/main.js): theme toggle, mobile menu, "Surprise me" random page, cookie notice
(essential-only requests non-personalized ads), multi-step forms, AJAX form relay to FormSubmit with
honeypot, redirect-on-success, lite YouTube embeds (no third-party load until click), localStorage
helpers, seeded RNG for daily content, streak tracking, share (Web Share API / clipboard).
Generate sitemap.xml, robots.txt, ads.txt, site.webmanifest, favicon, SVG share image and _config.yml (excludes sources and docs from the published site).
```

### Phase 4 — Original games
```
Build 12 dependency-free games, each its own JS file, keyboard + mouse + touch, best scores in
localStorage: FiveWord (daily 5-letter word guess, curated answers + large valid list, share grid),
Sudoku (generator with uniqueness check, daily seeded grid, notes, hints, check), Tile Merge (sliding
merge, undo), Minesweeper (safe first click, flags, chording, long-press), Memory Match, Snake (wrap or
walls, d-pad), Mole Pop, Four in a Row (minimax AI, 3 levels + local 2P), Tic-Tac-Toe (unbeatable AI),
Reaction Time, Typing Test (WPM/accuracy), Pattern Echo (Web Audio tones). Every game page: H1, lead,
stage, how-to (ordered), tips, about, FAQ, related games, share.
```

### Phase 5 — Tools and quizzes
```
Tools: spin wheel (editable entries, presets, remove-winner, share-by-link), team picker, coin flip,
dice roller (d4–d20), bored button (200 filtered activities), would-you-rather (220, 8 categories),
charades generator (336 words, timer, two-team score), random number generator (secure RNG).
Quizzes: 8 trivia × 15 questions with one-line explanations + 1 personality quiz (6 results with
next-step links) + Daily 5 drawn by date seed. Data lives in assets/data/*.json.
```

### Phase 6 — Content
```
Write 14 original idea guides (1,500–2,800 words: bored, at home, game night, party games adults/kids,
team building, virtual team building, icebreakers, dates, rainy day kids, friends, family night, free,
weekend) and 7 fact collections (animals, space, human body, ocean, food, history, random) with a
"myths we left out" section. Front matter: title, slug, description, category, emoji, minutes, cta
(play|kit|plan|quiz), related. Each article gets a TOC, a mid-article CTA matched to intent, FAQ,
rail with games + lead magnet, and 4–7 internal links.
```

### Phase 7 — Monetization pages
```
Plan My Fun (plan.html): above-the-fold 4-step form — occasion cards (auto-advance) → group size,
timeframe, date, format, city → budget, goals, notes → name, email, phone, organization, contact
preference, explicit consent to share with up to three vetted partners. Trust line beside submit, FAQ,
sample plan, "how it works". Redirect to thanks.html?f=plan. Prefill from ?event_type=.
Free Game Night Kit: email opt-in (newsletter checkbox) → redirects to printable kit.html (noindex).
Contests: 3 monthly skill contests with prizes, entry form, winners wall empty state, sponsor CTA,
full official rules (no purchase necessary, skill-based, eligibility, licence, privacy).
Support: monthly-first frequency, tiers, allocation bar (35% games/creators, 25% ops, 20% prizes,
20% promotion), earmark, public-thanks opt-in, pledge mode that switches to live checkout buttons when
PayPal/Stripe/Ko-fi/BMC links are pasted into config.js. Never ask users to click ads.
Careers: 6 remote roles + application form + "pitch your game" form.
Advertise: 6 sponsorship formats, standards, media-kit request form, owner contact for domain deals.
```

### Phase 8 — Legal and compliance
```
Privacy policy with Google AdSense cookie disclosures and opt-out links (Google Ads Settings,
aboutads.info, youronlinechoices), service providers (FormSubmit, Google Fonts, YouTube nocookie,
GitHub Pages), children (general audience, not directed to under-13s), rights (GDPR/UK/PIPEDA/CA),
retention. Terms, Disclaimer (ad + referral disclosures, no gambling), Trademark & Copyright notice
with takedown process. Cookie notice on first visit.
```

### Phase 9 — QA
```
Headless-browser pass on every page at 1280px and 390px: no JS errors; each game/tool/quiz reacts to
input; every form posts to the relay and redirects; the owner email string appears in no file and no
DOM; AdSense tag + owner bar present on every HTML page; all internal links resolve; sitemap lists every
indexable page; Lighthouse-style checks for contrast, focus and tap targets.
```

### Phase 10 — Deploy and launch
```
Run the generator, then push sources AND the generated site to WEBWORKSA1/allFun-com (main, repo root).
Enable Pages: Settings → Pages → Deploy from a branch → main / (root). Point DNS for allfun.com
to GitHub Pages (A records 185.199.108-111.153 + www CNAME
webworksa1.github.io), set Custom domain to allfun.com in Settings → Pages, enforce HTTPS. Verify https://allfun.com/ads.txt.
Submit sitemap in Google Search Console. Apply in AdSense with the site allfun.com; enable Auto ads and
the AdSense Privacy & messaging GDPR message. Send one test form to trigger FormSubmit activation.
```

### Phase 11 — Growth (post-launch)
```
Weekly: 2 new guides targeting team/party intent, 1 new quiz, refresh Daily. Monthly: new game or
tool, contest round, Friday Fun newsletter. Sign 5 planning partners with per-lead or referral terms.
Pitch the spin wheel and team picker to teachers; pitch virtual game hours to HR/people-ops.
Track: pageviews, RPM, leads/1,000 sessions on team pages, lead→booking rate, kit opt-ins.
```
