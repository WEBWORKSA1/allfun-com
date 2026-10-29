# AllFun.com — Competitive Feature Audit

Research date: 29 Oct 2026. 52 sites/pages reviewed: 46 from the brief plus 6 supplemental. I also read two Google references on AdSense placement.

**Method.** Every site was fetched with WebFetch or researched with WebSearch. Text extraction does not render visuals. Design notes marked `~` come from general familiarity with the live site and should be spot-checked in a browser. Unmarked notes come from page markup (theme colors, labels, structure).
Status: **F** = fetched · **P** = partial (JS-rendered or metadata only, supplemented by a secondary source) · **S** = substitute URL.

---

## 1. Summary table

| # | Site | Category | Key features | Forms | Monetization |
|---|---|---|---|---|---|
| 1 | neal.fun (F) | Viral web toys | ~33 original toys in a flat list | Contact link | Ads (per Wikipedia) |
| 2 | poki.com (F) | Game portal | Category pills, ratings, live trending, likes, fullscreen | Dev portal | Labelled ads below rails |
| 3 | crazygames.com (F) | Game portal | Mood hubs, recently played, weekly leaderboard seasons | Login | Ads, premium, apps |
| 4 | coolmathgames.com (F) | Brain games | Random button, Top 10, Daily, 9 languages, WCAG | Suggest game | Ads, Premium, merch |
| 5 | sporcle.com (F) | Quizzes | User quizzes, Daily Dose, badges, playlists, dark mode | Join, creator, trivia finder | Ads, ad-free sub, events |
| 6 | jetpunk.com (F) | Quizzes | Dated feed, timed typing, % of players stats | Account | Ads, tree-planting share |
| 7 | buzzfeed.com/quizzes (F) | Personality quizzes | 8 tabs, bookmarks, comments, quiz-maker | Newsletter link | Ads, partners, shopping |
| 8 | boredpanda.com (F) | Viral lists | Votes, comments, share per card, daily games | Login, newsletter | Ads, Premium ad-free |
| 9 | 9gag.com (P) | Memes | Feeds, votes, light/dark scheme | App sign-up | Ads |
| 10 | theuselessweb.com (F) | Random button | One button, dead-site archive | Google Form submit | None |
| 11 | boredbutton.com (F) | Random button | Red button, logo /random route | Add a site | None visible |
| 12 | wheelofnames.com (F) | Spin wheel | Weights, Sheets import, share links, OBS mode, randomness audit | Entries box | Few ads, close control |
| 13 | pickerwheel.com (F) | Picker tools | 3 modes, results dashboard, AI lists, PWA, embed | Inputs, account | Ads, Premium |
| 14 | random.org (F) | Random tools | 30+ generators, public draw records | Draw config | No ads; paid draws |
| 15 | miniclip.com (F) | Mobile publisher | Web games link only | Account | Mobile games |
| 16 | armorgames.com (F) | Game portal | Game of the Day, Quests, rankings, random | Account | Playwire ads, Steam |
| 17 | kongregate.com (F) | Game portal | Badge of the Day calendar, collectibles, install prompt | Sign in | Not visible |
| 18 | y8.com (F) | Mega portal | Category counts, achievements, highscores, 32 languages | Login, contact | Ads, dev revenue |
| 19 | addictinggames.com (F) | Game portal | 70 tags, mode/difficulty filters, rating counts | Submit game | Ads |
| 20 | arkadium.com (F) | Casual daily | "Surprise me", mood shortcuts, daily crossword | Sign in | Ads, Plus, gems, sweepstakes |
| 21 | aarp.org/games (F) | Casual 50+ | Dailies, rewards points, recently played | Membership join | Ads, sponsored game, membership |
| 22 | pogo.com (P) | Social casual | Rooms/chat, badges, seasons | Account | Video ads, club, gems |
| 23 | lichess.org (F) | Chess nonprofit | Puzzle of the Day, Storm/Streak/Racer | Patron | Donations, swag |
| 24 | chess.com/puzzles (P) | Puzzles | Rush, Battle, Daily, rated | Sign-up with return URL | Membership |
| 25 | NYT Games (S) | Daily puzzles | 8 dailies, streaks, archive, friends board | Subscribe | Subscription, ad-free |
| 26 | geoguessr.com (F) | Geo game | Party mode, badges, tournaments | Social sign-up | Subscription |
| 27 | jigsawexplorer.com (F) | Jigsaw | Daily puzzle, weekly mystery | 2 email sign-ups | Not visible |
| 28 | sudoku.com (F) | Sudoku | 6 tiers, daily calendar, awards, hints | Contact | AdSense, rewarded ad |
| 29 | puzzlebaron.com (F) | Puzzle network | 40 sites, daily printables, books | None | Books |
| 30 | kahoot.com (F) | Live quiz SaaS | PIN join, podium, audience menu | Sign-up, sales | SaaS tiers |
| 31 | funbrain.com (P) | Kids education | K–8 games and books | — | House ads |
| 32 | abcya.com (P) | Kids education | Grade picker PreK–6 | — | Ads, Premium |
| 33 | pbskids.org/games (F) | Kids public media | Character navigation, 3 top items | None | Underwriting |
| 34 | littlealchemy2.com (P) | Combo puzzle | Single play button | — | Paid apps |
| 35 | akinator.com (F) | Guessing AI | Mascot, recent-games ticker | Volunteer apply | Ads, app |
| 36 | quickdraw.withgoogle.com (F) | AI doodle | 20-second rounds, AI top-3 guesses | Optional survey | None |
| 37 | mentalfloss.com (F) | Trivia editorial | Lists, quizzes, fact generator | Newsletter, sweepstakes | Ads, gated sweepstakes |
| 38 | thefactsite.com (F) | Facts | Fact of the Day, generator, On This Day | Search | Ads~, shop |
| 39 | ripleys.com (F) | Oddities + attractions | Stories, cartoons | Tickets | Tickets |
| 40 | window-swap.com (P) | Ambient | One-click random window | Video submit | None |
| 41 | radio.garden (P) | Globe radio | Globe, favorites, share | — | App ad removal $2.99 |
| 42 | teambuilding.com (F) | Team events | 4-question matcher, advisor call | Quiz funnel, toolkit | Bookings |
| 43 | outbackteambuilding.com (S) | Team events | 60 activities, case studies | Quote modal and page | Quotes |
| 44 | withconfetti.com (S) | Virtual events | Browse by outcome, instant quote | Demo, sign-up | Bookings |
| 45 | ko-fi.com (F) | Creator tips | Tips, memberships, shop | Get started | 0–5% fee |
| 46 | Wikimedia giving (S) | Donations | Ways-to-give menu, monthly, matching | Regional forms | Donations |
| 47 | buymeacoffee.com (F) | Creator tips | 1/3/5 coffee presets, supporter wall | Tip widget | Platform fee |
| 48 | gleam.io (F) | Giveaways | Action-based bonus entries | Entry widget | SaaS |
| 49 | either.io (F) | Would-you-rather | Final votes, sorted comments | Submit question | Ad below vote |
| 50 | randomlists.com (F) | Generators | 100+ generators, rerun | Search | Ads~ |
| 51 | jackboxgames.com (F) | Party games | Phones join by room code | Newsletter ×2 | Pack sales |
| 52 | flipsimu.com (F) | Coin flip | Global/personal stats, URL state | Account | Ads~ |

---

## 2. Per-site notes

Each entry gives the core offer, the look and the IA, then **Copy** (one thing AllFun should adopt) and **Exploit** (one weakness AllFun can use).

**neal.fun** — Original toys and visualisations. Look~: white canvas, rounded cards, a bespoke illustration per project. No search or categories. **Copy:** self-contained originals, each with a one-line premise and a shareable result. **Exploit:** no daily hook or email capture.

**Poki** — 1,500 games. Category pills, then curated rows, then a ~45-tile category grid. Mint #83ffe7 with mosaic thumbnails in 3 sizes. Game page order: title, likes and dislikes, fullscreen, related rail, *then* 3 labelled ad slots, then a long how-to and FAQ. **Copy:** the ad-below-rail structure and a FAQ under every game. **Exploit:** no dailies, tools or newsletter.

**CrazyGames** — Sort tabs plus **mood hubs** (brain training, with friends, 5-minute, relax). Leaderboards run in weekly seasons with Global/Country/Friends tabs and trophies; login is required. Dark navy #212233. **Copy:** mood hubs and weekly seasons. **Exploit:** teen-gamer tone; no non-game fun.

**Coolmath Games** — Mega-menu by thinking skill, a random button, category counts, a custom SVG icon set, a WCAG 2.2 claim and a no-violence pledge. Premium adds no ads, themes and playlists. Slate #2A445D. **Copy:** a family-safe promise stated outright, plus category icons. **Exploit:** no newsletter or party content.

**Sporcle** — 15 categories and 10 quiz formats; Daily Dose; badges, playlists and tournaments; user-made quizzes; a dark-mode toggle. Cards carry play-time and difficulty chips. Its events arm uses first-person audience cards, states 10k+ events hosted, shows a logo row and has a four-step booking flow. **Copy:** card chips, and "I'm a…" audience cards. **Exploit:** cluttered navigation; adult skew.

**JetPunk** — The homepage is a dated blog-style feed. Timed typing quizzes; results show % with a perfect score, the average and your best. A share of revenue funds tree planting. **Copy:** "you beat X%" stats. **Exploit:** weak navigation; plain look.

**BuzzFeed Quizzes** — Personality, Trivia, Fandom, Poll and Checklist tabs; bookmarks; comment counts; a community quiz-maker with a leaderboard. Red #ee3322. **Copy:** the personality, poll and checklist formats. **Exploit:** adult and news content mixed in.

**Bored Panda** — Lists and galleries with net vote scores, a share control on every card, Trending/Latest/Community tabs, and a brain-teaser module between blocks. Premium is ad-free. **Copy:** one-tap share on every card. **Exploit:** sensational, ad-heavy.

**9GAG (P)** — Meme feeds; supports light and dark schemes; pushes its app. **Copy:** follow the system theme. **Exploit:** not family-safe.

**The Useless Web** — One giant button framed by arrows with a polite plea, plus a catalogue and an archive of dead sites. **Copy:** a single-action hero. **Exploit:** sends all traffic away.

**Bored Button** — One red button, also on the logo's /random route. **Copy:** randomness reachable from the logo everywhere. **Exploit:** no categories (solo, with kids, outdoors).

**Wheel of Names** — Wheel beside an entries box; weights, Sheets import, remove-winner, short-link share, cloud or local save, 150+ sounds, OBS streamer mode, and a public randomness audit. All features free; few ads with a close control. **Copy:** the randomness trust page and share links that keep state. **Exploit:** a single tool.

**Picker Wheel** — Normal, elimination and accumulation modes; image entries; results history with image export; an AI list generator with a daily quota; PWA; embed; a 16-section explainer below; sibling tools in the header. **Copy:** a tool family with a shared bar, plus long explainers. **Exploit:** dense settings and inconsistent copy.

**RANDOM.ORG** — True randomness; FREE/PAID labels; a paid draw service with 5 years of public records; no ads. **Copy:** a public contest-draw archive. **Exploit:** 1990s design.

**Miniclip** — Pivoted to mobile; web games are one link. **Exploit:** a legacy browser audience left without a home.

**Armor Games** — Game of the Day, Quests, a Hero Board, rankings and a random link; cards show score and plays. Charcoal. **Copy:** a Game of the Day slot. **Exploit:** hardcore tone.

**Kongregate** — Badge of the Day on a Mon–Sun calendar; earning the week's badges unlocks a collectible companion; rating plus plays; install prompt. **Copy:** a weekly collectible. **Exploit:** ageing catalogue.

**Y8** — Dense grids with counts in category headers; local and online multiplayer; achievements, highscores, bookmarks and recently played; 32 language subdomains. **Copy:** a recently-played rail. **Exploit:** clutter, and "no sign-up" claims that contradict its account push.

**AddictingGames** — 70 tags; filters for 2-player, controller and difficulty; rating counts; Indie Spotlight; dark theme. **Copy:** player and control filter chips. **Exploit:** repeated lists, zoom lock.

**Arkadium** — "Surprise me!" next to mood shortcuts (Coffee Break, Brain Boost); daily crossword; gems; Plus subscription; sweepstakes. **Copy:** mood plus surprise side by side. **Exploit:** says "no sign-up" while pushing sign-in; little sharing.

**AARP Games** — Daily category, rewards points, two labelled ad slots, a pharma-sponsored solitaire, a membership upsell, and an unrendered name placeholder. **Copy:** "presented by" sponsorship of a single game. **Exploit:** nagging and QA bugs.

**Pogo (P)** — Rooms and chat, badges, seasons, paid gems, up to 20-second in-game video ads; now shrunk. **Copy:** weekly challenge badges. **Exploit:** over-monetisation destroyed trust.

**Lichess** — Free, no ads. Puzzle of the Day on the homepage; Streak, Storm and Racer modes; a dashboard; blind and zen modes. The Patron page has a mission headline, a new-patrons ticker, a cost breakdown, a cosmetic wings badge, an FAQ and a registration link. **Copy:** "where the money goes" and cosmetic-only perks. **Exploit:** requires sign-in before donating.

**Chess.com Puzzles (P)** — Rush, Battle, Daily and rated modes; sign-up returns the player to the puzzle. **Copy:** return-URL sign-up. **Exploit:** free-tier limits.

**NYT Games (S)** — 8 dailies, per-game stats and streaks, an archive for subscribers, a friends board for the Mini (up to 25), ad-free. Look~: a color and icon per game, serif headings. Reviewers want badges. **Copy:** the daily-ritual hub with a spoiler-free share grid. **Exploit:** the paywall and thin rewards.

**GeoGuessr** — Party rooms, badges, tournaments, a free seasonal mode. **Copy:** private game-night rooms. **Exploit:** paywalled core.

**Jigsaw Explorer** — A daily puzzle, plus a weekly Mystery Puzzle that reveals its image as you assemble it; two separate email sign-ups by intent. **Copy:** newsletters split by intent. **Exploit:** no filters or social layer.

**Sudoku.com** — 6 difficulty tiers, a daily calendar and awards; 3 mistakes ends the game, with a second chance; hints teach the technique; printables and a solver; an opt-in rewarded ad framed as keeping the game free. **Copy:** a rewarded ad for a second chance. **Exploit:** one puzzle type.

**Puzzle Baron** — A hub for 40 sites, 17 printables and 16 books; a stat row; big offer cards. **Copy:** a Printables section. **Exploit:** no capture form.

**Kahoot!** — Audience mega-menu (school, work, home); "no card needed" sign-up; priced product cards; logo wall; education badges. **Copy:** audience-first entry to Plan My Fun. **Exploit:** a generic sales form.

**Funbrain (P)** — K–8 games and books; reviewers criticise constant house ads for a paid sister product. **Exploit:** promo overload.

**ABCya (P)** — Grade picker; Premium at $9.99/mo or $79.99/yr adds no ads, fullscreen, printables and offline. Locks zoom. **Copy:** printables as value. **Exploit:** accessibility.

**PBS Kids Games** — Three nav items, character tiles, a carousel, a local-station picker; bold blue. **Copy:** a minimal kids nav. **Exploit:** no age filters, and no visible pause control on the carousel.

**Little Alchemy 2 (P)** — One play button; amber #faa620; a combine-to-discover loop. **Copy:** a discovery counter mechanic. **Exploit:** zoom lock.

**Akinator** — Mascot; a last-10-games ticker; a call for volunteers. **Copy:** a live recent-activity ticker. **Exploit:** dated and ad-heavy.

**Quick, Draw!** — 20-second rounds; the AI's top 3 guesses; replay; an open dataset; 14 languages. **Copy:** short rounds with an AI reveal. **Exploit:** no progression.

**Mental Floss** — Lists, quizzes and a facts generator; a weekly newsletter pitched on tone; a terse uppercase button mid-page. Its sweepstakes entry form sits under a quiz and requires the newsletter; one entry per person; US 18+; random draw; 48-hour claim. **Copy:** contest entry under the activity. **Exploit:** forced opt-in; AllFun can make it optional.

**The Fact Site** — Fact of the Day; a "Next Random Fact" button with a source link, 6 share targets and reactions; On This Day pages; cards show a teaser fact and read time. **Copy:** a source on each fact. **Exploit:** no newsletter or quizzes.

**Ripley's** — Tickets-first; a Stories blog with cartoons; a hero with a pause control. **Copy:** a pause control on motion. **Exploit:** oddity content is buried.

**WindowSwap (P)** — One-click random window videos; curated submissions; black and calm. **Copy:** a "calm corner". **Exploit:** no revenue.

**Radio Garden (P)** — Dark globe, favorites, search, share; the app removes ads for $2.99. **Copy:** a one-time "remove ads" support option. **Exploit:** niche.

**TeamBuilding.com** — The hero is a 4-question matcher promising ranked picks in about 30 seconds; it remembers answers; an alternative free 15-minute advisor call; a 3-step booking explainer. Trust: 83k+ verified reviews averaging 4.96, a remake-or-refund guarantee, no markups. Blog guides carry a mid-list toolkit box and an end email form. **Copy:** the entire funnel. **Exploit:** corporate-only.

**Outback Team Building (S)** — "Request a Quote" in the header and after almost every section; the modal promises a tailored reply within one business day from a real person; association badges beside the form; case studies with numbers; a budget-tier table. **Copy:** a response-time promise beside the submit button. **Exploit:** hidden prices, inconsistent CTAs, unsourced stats.

**Confetti (S)** — Browse by Featured, Categories and Outcomes; instant quote by headcount; Capterra and Trustpilot badges; 25k+ teams; looping logo row; happiness guarantee; emoji section headers. **Copy:** browse by outcome. **Exploit:** virtual and corporate only.

**Ko-fi** — Tips, memberships, shop and commissions; transparent 0–5% fee; direct payouts; a warm voice; "$200M paid to creators" as social proof. **Copy:** honest fee language. **Exploit:** support happens off-site.

**Wikimedia giving (S)** — Online one-time and monthly gifts with local methods chosen by country, plus bank, cheque, matching gifts, payroll and legacy. Practice: an average gift of about $15, constant A/B tests, banner suppression after dismissal. The Australian chapter leads with monthly presets before one-off ones, allows guest checkout and states tax status plainly. **Copy:** monthly first, capped asks, a clear tax line. **Exploit:** guilt-heavy tone.

**Supplemental.** **Buy Me a Coffee:** 1/3/5 presets, a message box, the total in the button, a supporter wall with replies, $5/$15/$25 tiers. **Gleam:** bonus entries for actions. **Either.io:** votes are final; comments sort by agrees and newest; an ad sits after the vote. **RandomLists:** 100+ generators with rerun; no filters. **Jackbox:** room-code join; no family filter. **FlipSimu:** hold-to-charge flip, global vs personal stats, settings stored in the share URL.

---

## 3. Synthesis

### 3.1 Must-have features, ranked

1. **Instant play with no sign-up** for all core fun; accounts optional (Poki, Y8, Lichess).
2. **A daily hub:** 3–5 dailies (puzzle, trivia, fact, would-you-rather), local streaks, a spoiler-free share grid (NYT, Sporcle, Sudoku.com).
3. **A sitewide "Surprise me" / Bored Button** in the header and on the logo route.
4. **Mood and occasion hubs:** 5-minute, With friends, Family night, Brain boost, Chill, Party.
5. **A tool suite with state in the URL:** wheel, team picker, coin, dice, charades, would-you-rather; weights, elimination mode, TV/fullscreen mode, short-link share.
6. **Card chips:** play time, player count, age range, difficulty.
7. **Post-game comparison stats** ("you beat 72% of players").
8. **Local-first favorites and recently played.**
9. **Weekly leaderboard seasons** with Global/Country/Friends tabs and cosmetic trophies.
10. **Daily badges plus a weekly collectible.**
11. **Fact of the Day plus a generator** with source, reactions and share.
12. **An explainer and FAQ under every game and tool** for SEO depth and ad-safe inventory.
13. **Light theme first**, with dark mode via system preference and a toggle.
14. **Accessibility:** no zoom lock, motion pause, keyboard play, a WCAG statement.
15. **An installable PWA** with offline dailies.
16. **A family-safe pledge** stated on the homepage.
17. **Printables** feeding the Game Night Kit.
18. **Embed and streamer modes** for teachers and creators.
19. **A randomness and draw transparency page.**
20. **Later:** moderated user submissions, and more languages.

### 3.2 Lead-generation patterns (Plan My Fun, Game Night Kit)

- **Matcher before form** (TeamBuilding.com). The first screen is one tap on *What are you planning?* Show matched ideas, then offer "get a custom plan". Ask for contact details last.
- **Field order:** occasion, headcount band, date (or flexible), city or virtual, budget band, age mix, goals (chips), first name, email, optional phone, optional notes. Use 3–4 screens with a progress bar, chips over dropdowns, and no more than 2 typed fields per screen.
- **Remember partial answers** and greet returning visitors with their matches.
- **Two exits:** self-serve ideas, or book a 15-minute call.
- **Trust beside submit:** a response-time promise (Outback), a satisfaction guarantee (Confetti, TeamBuilding.com), verified review counts, sample plans, and a visible price-band table (beat Outback's hidden pricing).
- **Audience cards up front:** kid's party, team event, family night, school (Sporcle, Kahoot).
- **Guides as funnels:** a mid-article boxed offer (contents bullets, social proof, one field) plus a closing form.
- **Kit delivery:** one email field, an instant download on the thank-you page, email as a backup, and a separate, specific newsletter opt-in (Jigsaw Explorer's split lists; avoid Mental Floss's vague pitch).
- **One consistent CTA verb sitewide.**

### 3.3 Donation and support patterns

- **Mission headline plus a "where your money goes" cost list** (Lichess).
- **A unit metaphor:** "Fuel a new game" with 1/3/5 multiples, a custom amount, the total in the button and an optional message (Ko-fi, Buy Me a Coffee).
- **Monthly presets first**, defaulting to a mid preset anchored to a modest average gift (Wikimedia).
- **Cosmetic perks only:** a supporter badge on leaderboards, an ad-light mode, early access; never paywall fun (Lichess, Radio Garden).
- **A moderated supporter wall** with thank-you replies.
- **Guest checkout** with wallets; don't require sign-in (Lichess's weakness).
- **A plain tax statement** (Wikimedia AU).
- **Capped asks:** suppress after dismissal, and ask after a win or streak milestone, never mid-play.
- **A goal bar** tied to the next original game. An optional cause tie-in is another option (JetPunk).

### 3.4 Contest and leaderboard patterns

- **Weekly resetting seasons** so newcomers can win; cosmetic trophies on profiles (CrazyGames).
- **Short timed skill boards** (Lichess Storm, Chess.com Rush, the NYT Mini friends board).
- **A Mon–Sun badge calendar**, with a full week unlocking a collectible (Kongregate).
- **An entry form under the activity** (Mental Floss), with opt-in optional, explicit entry limits and plain-language rules.
- **Transparent draws** with a public archive and a winners list (RANDOM.ORG).
- **Rules checklist:** no purchase necessary, eligibility, entry period with time zone, prize value, selection method, claim window, alternate winner, privacy link. For Canadian entrants, add a skill-testing question and review Québec rules.
- **Bonus entries for sharing** (Gleam), always with a free alternate path to entry.
- **Live counters** ("X players today") as social proof.

### 3.5 AdSense-friendly layout

- **Policy guardrails** (AdSense help): keep ads clear of game frames and controls (Google cites a 150 px buffer for games); no pre-content wait gates; label ads only "Advertisement" or "Sponsored links"; no arrows or click incentives; nothing in pop-ups; no auto-refresh.
- **In-game breaks:** use Google's H5 Games Ads (Ad Placement API) for interstitials at natural breaks and opt-in rewarded ads, with frequency managed by Google (Sudoku.com's second-chance model).
- **Game and tool page order:** game above the fold with no ad above it on mobile, then the related rail, then one labelled responsive unit, then the how-to and FAQ with an in-article unit, then more games. On desktop add a sticky right-rail unit outside the buffer (Poki, Picker Wheel).
- **Lists and guides:** one unit every 4–6 items, never between a heading and its body.
- **Tools:** few ads, a dismiss option, and no ads in TV mode (Wheel of Names).
- **Would-you-rather:** the ad comes after the result reveal (Either).
- **Kids zone:** child-directed treatment, non-personalised ads, kept separate.
- **Sponsorship outside AdSense:** "Presented by" on one daily (AARP), or a sponsored contest prize.

### 3.6 Design patterns worth adopting

- A mosaic grid with oversized featured tiles (Poki).
- A color and illustrated icon per game (NYT) and bespoke art per original (neal.fun).
- A giant single-action Bored Button hero (Useless Web).
- Mood hubs with icon or emoji headers (CrazyGames, Confetti); a category SVG icon set with counts (Coolmath, Y8).
- A light, friendly family palette (Poki mint, PBS Kids blue) rather than dark gamer themes, with dark mode as an option.
- Celebration micro-motion (a confetti toggle, a results-card reveal) that respects reduced-motion settings.
- A calm corner with one-click shuffle (WindowSwap, Radio Garden).
- Big tap targets and character art in the kids zone (PBS Kids).
- **Avoid:** zoom locks (ABCya, Little Alchemy 2, Radio Garden, AddictingGames), unrendered placeholders (AARP, Sudoku.com), contradictory claims (Y8, Arkadium).

---

## 4. Sites not fetched, or only partially

| Target | Result | Used instead |
|---|---|---|
| nytimes.com/crosswords | Blocked | NYT Games App Store listing |
| donate.wikimedia.org (4 variants), payments.wikimedia.org | Not found | Wikimedia Ways to Give, Wikimedia AU donate page, Meta fundraising page |
| outbacktb.com | Disallowed by robots.txt | outbackteambuilding.com (home and quote page) |
| confetti.events | An unrelated ticketing SaaS | withconfetti.com |
| Ko-fi creator page and help centre | Client error | Ko-fi home and explore pages, buymeacoffee.com |
| teambuilding.com/quiz, pickerwheel.com/premium, crazygames.com/t/premium | Error or no pricing content | Main pages |
| letsroam.com, every.org, archive.org/donate, Wikipedia donation FAQ | Error, robots or JS-only | Not used |
| 9gag, pogo, funbrain, abcya, littlealchemy2, window-swap, radio.garden, chess.com/puzzles | Metadata only | Wikipedia, Common Sense Media, e-student review, AppleInsider |
| boredpanda.com, games.aarp.org | Redirected | Redirect targets audited |
