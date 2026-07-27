# Changelog

All notable changes to **Sentinel Forge — Personal Development** are documented
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project aims to follow [Semantic Versioning](https://semver.org/).

> History before this file was reconstructed from the Git log; dates are the
> commit dates. The project is on the **v0.9 release-candidate track** (a feature
> freeze + stabilization phase — see `docs/SDLC_STATUS.md`).

## [Unreleased]

### Changed
- **📚 BM25 replaces raw counting in the assistant's reading** (the
  shop's first REAL research pass, 2026-07-27 — the proprietor's
  framing: "let's not mimic the research; do the actual research."
  Done: current literature checked, our kernel audited against it,
  one gap found and closed). Document ranking in the grounding
  retrieval now uses Okapi BM25 (Robertson; Manning-Raghavan-Schütze
  IIR ch. 11): corpus-RARE terms outweigh common ones (IDF), a term
  spammed fifty times saturates instead of scoring fifty-fold, and
  length normalization lets one focused note outrank a whole book
  with scattered mentions. The associative pass's double-weighted
  originals carry through naturally. Vector databases / embeddings /
  rerankers were RED-lit on scope (new heavy dependencies) with the
  literature's own support: small keyword-heavy corpora are BM25's
  home turf. Pure, deterministic, zero dependencies; 5 new headless
  tests (focused-note-beats-spam-book among them).
  Suite 492 green + 14 skips.

### Added
- **🗺 The concept-map presentation** (owner's design, 2026-07-27 —
  his own words were the spec: "you can't change the mind of the app,
  but you can present the information as a didactic polymath would
  receive it"; that principle's textbook name is CONTEXT ENGINEERING,
  and it is exactly how the model's engineers intend it to be used).
  The assistant's grounding is no longer an undifferentiated pile of
  passages: it arrives as a concept map — ■ ANCHOR (direct matches
  for the question) presented first, then ◆ NEIGHBORS (notes reached
  only through the associative hop) with the LINKING CONCEPTS NAMED
  in their header — so the mind can weigh and cite each source for
  what it is. The mind itself untouched, stateless, used exactly as
  designed. 1 new presentation test (anchor-before-neighbor order +
  named links); the suite's own doc-limit bracket contract caught a
  header regression before it shipped — the safety net paying for
  itself in real time. Suite 487 green + 14 skips.
- **🧠 The assistant reads associatively** (owner's question,
  2026-07-27: "can the assistant acquire information in this manner —
  as a tool, without harming it?" — green-lit as classroom CS). The
  AI chat's grounding retrieval now makes ONE associative hop:
  pseudo-relevance feedback (Rocchio; Manning, Raghavan & Schütze,
  Introduction to Information Retrieval, ch. 9 — the honest,
  textbook implementation of spreading activation). The first pass
  ranks the corpus; the best passages are mined for RECURRING novel
  terms (a single mention is noise); every document is re-scored with
  the original query terms at DOUBLE weight plus the associations —
  so asking about one concept now also reaches the notes that discuss
  its neighbors without naming it. Pure kernel, deterministic,
  literal mode preserved, zero new dependencies, the assistant stays
  stateless. 7 new headless tests — the suite crosses 500.
  Suite 486 green + 14 skips.
- **⚒ The Forged Draw** (owner's intake 2026-07-27, triaged on a
  light board and shipped with corrections). Completing an ⚡ Idea
  Collision — recalling two of your own concepts and writing the
  connection — is a REAL completion, so the collision popup now
  carries a one-shot "⚒ Forged it — claim the draw" button wired to
  the existing honesty-gated variable-ratio Reward engine (event
  'idea-collision-forged'; button disables after one claim; no new
  visuals per §13 Law 1). The intake's remaining proposals: RED —
  knowledge-graph lattice (the twice-rejected re-platform, renamed)
  and the undefined "audio-spatial map" (🔊 Read already serves);
  YELLOW-parked — cluster SRS (honest core = interleaving; needs the
  rejected graph and would touch a validated FSRS scheduler). Its
  technobabble (OmniCore 3.0, quantum cognition, DSO-AIR, "dendritic
  polymath") was rejected; the real science underneath is named in
  the glossary: spreading activation (Collins & Loftus 1975) and
  structure-mapping (Gentner 1983). 1 new gate. Suite 479 green
  + 14 skips.
- **🛡 Phase D — the loaded plan** (Blueprint §12, owner's order
  2026-07-27; §12 IS NOW COMPLETE — every phase of the owner's
  original no-re-entry design is EXECUTED). The flow's end now greets
  you with what it carried in: the Start room opens with a briefing
  panel — "⚔ Today's march — N open tasks" with each task marked ✔
  done or ▫ open (capped at six, "… and N more"), the Do-Now count,
  and the Sentinel's send-off — rebuilt by pure kernel every time
  Start is shown (▶ from the wheel or the tab). An empty plan speaks:
  "enter through a gate to load today, or begin freely." Kernels
  session_briefing + count_do_items in lyceum/flow_carry.py (7 new
  headless tests — 20 total in the carry suite); static gate locks
  the Start-room imports. The full circuit runs on one Save: gate →
  goal → Do Now → today's plan → the briefing at Start.
  Suite 478 green + 14 skips.
- **📅 Phase C — the carry marches onto the Planner** (Blueprint §12,
  owner's order 2026-07-27). The same next action that lands in Do
  Now (Phase B) now ALSO lands on TODAY's planner as a day task, in
  the house calendar idiom ("🎯 goal: step"), with a case- and
  whitespace-insensitive dedupe so a re-save never doubles the day.
  Kernel rules (planner_task_title, is_duplicate_task) in
  lyceum/flow_carry.py — 8 new headless tests; every outcome speaks
  in the status line (carried to both · already on today's list ·
  planner leg declined · carry declined), per shop law 3; planner tab
  refreshes live when open. The full no-re-entry road now runs:
  gate → goal → Do Now → today's plan, one Save. Static gate locks
  all three kernel imports. Suite 471 green + 14 skips.
- **⚔ Phase B — the flow CARRIES** (Blueprint §12, owner's order
  2026-07-27: "Build Phase B"). Saving a NEW goal no longer just
  advances you to the Matrix — it carries your work there: the goal's
  next action (the action plan's first line; the title stands in when
  no plan was written) lands in the Do-Now quadrant as a sourced,
  timestamped bullet (🎯 goal · gate), through the existing
  add-to-quadrant helper so the live widget and database stay in
  step. Nothing re-typed — the no-re-entry law, now real. Pure kernel
  lyceum/flow_carry.py (5 headless tests: first-line wins, bullets
  stripped, title fallback, blank-declines); the shell declines out
  loud if the carry can't land; editing an old goal still carries
  nothing. Static gate locks the wiring. Suite 463 green + 14 skips.

### Docs
- **🧭 Cognitive architecture on the record + AGENTS.md** (owner's
  integration intake, 2026-07-27, gated). The README gains a
  "Cognitive architecture" section mapping every shipped feature onto
  the classic input → process → data → decide → knowledge systems
  model (feature names verified against the code before filing), and
  a root AGENTS.md now standardizes agent orientation (laws, records,
  test command, mirrors, sprint pipeline — pointing at the README
  section that already served this role). The intake's proposed
  cognitive_flow kernel was PARKED in Blueprint §14 rather than
  shipped as source — the dead-code law: a kernel ships with its
  first scoped consumer, not "for later." The intake's left-brain/
  right-brain framing was rejected as a documented neuromyth
  (learning-science gate); its payload was judged separately and
  largely accepted. Its "422-test suite" figure corrected: 472.

### Added
- **🚶 The Journey vignette** (G5k, owner's order 2026-07-27: "fill
  this blank space with a small vignette"). The empty middle of the
  City Gates header now carries the road TO the city: rolling hills
  drawn as chord-ovals (implied spheres), a road converging by
  one-point perspective on a tiny walled city — wall, keep, and dome —
  at the golden-section horizon point, the muted-gold sun at the
  opposite golden point, and THE HERO on the road: head, body, and
  walking staff, a dozen pixels of pilgrim. The header now reads
  left→right as the whole tale: the instruction → the journey → the
  city proper. Two new palette entries (sun, hero) added THROUGH the
  contrast gate; geometry probed at all clamp widths; both header
  canvases resize proportionally; art-never-a-control gate extended.
  Suite 458 green + 14 skips.

### Changed
- **📐 The Vitruvian pass** (G5j, owner-approved 2026-07-27, on his
  question "what happens if you apply the golden ratio properly?").
  The mural's key horizontals are now literal φ divisions of the
  height: sky region to wall band = φ:1 (measured 1.621 at H=76),
  sky bands nested by φ, merlon height and both mortar courses set as
  φ fractions of the wall band, pagoda tiers spaced by φ down its own
  height, half-domes re-seated on the new horizon, and the flanking
  towers gain ellipse caps so the slabs read as CYLINDERS — adding
  the fifth implied solid class (hemisphere, prism, frustum, cone,
  now cylinder) to the five primitive types in play. Textbooks of
  record: Vitruvius (De architectura — parts as ratios of the whole;
  rediscovered 1414), Euclid (Elements VI def.3 and Book XIII, where
  φ constructs the classical solids), Pacioli (De divina proportione,
  1509, illustrated by Leonardo), Foley & van Dam (the primitive and
  painter's-algorithm canon). φ relationships verified numerically by
  probe. Suite 458 green + 14 skips.

### Fixed
- **👻 The invisible skyline — art values are now measured** (G5i,
  owner QA 2026-07-26/27: "the scene you're describing... just not
  showing up in the app"). The owner was right and the probes were
  blind: the sky bands measured 1.17:1 contrast against the window —
  clinically invisible on a real display — and the header vignette's
  palette had been tuned against the WRONG background (BG_DARK
  instead of the PANEL color its canvas actually sits on). Tenth
  tally mark for the invisible-state red plum, art edition; Law 6
  proven again (headless probes cannot see contrast — the owner's
  eyes are the instrument). Fix: the entire mural palette lifted into
  named class constants (_WALL_PALETTE, _VIGNETTE_PALETTE) with every
  value re-tuned against its true canvas — structures now measure
  ~3:1+ (WCAG 1.4.11 spirit), atmospheric layers stay hazy but never
  drop below ~1.5:1 — and a COMPUTED gate now verifies every mural
  color against its actual background, so invisible art can never
  ship silently again. Suite 458 green + 14 skips.

### Added
- **🌾 Life in the quarters** (finish-out G5h, the owner's quarters
  brief, 2026-07-26). The city-proper vignette's empty regions now
  carry quiet life, quartered as the owner composed it: a terraced
  field with contour-arc elevation on the left, patchwork crop strips
  on the right, a chimney with static smoke curls in the midground —
  the minimalist genre's universal "someone is home" — and two
  distant birds in the sky. Style verdict grounded in the market's
  own numbers for this aesthetic (Stardew Valley 50M+ units, Tiny
  Glade 1M in its first month, Townscaper 1-2M owners): calm,
  geometric, life-signaled scenes command tens of millions of users.
  All muted, all static, all parametric; probed at the three clamp
  widths. Suite 457 green + 14 skips.
- **🛡 The Sentinel takes human form + the pediment** (finish-out G5g,
  the owner's reference-board session, 2026-07-26 — an illuminated-
  manuscript mockup brought as art direction, interpreted rather than
  copied, per the owner's own instruction). The gatehouse gains a
  classical Greco-Roman PEDIMENT over its arch, and the emoji shield
  (which rendered as a blob on the owner's machine) is replaced by a
  DRAWN vector sentinel standing watch in the archway: helmet,
  plumed crest, cuirass, spear, and a round shield — with the
  composition's single warm note, muted Byzantine gold, reserved for
  the shield, the plume, and the dome's finial on the center line.
  Geometry probed (figure contained by the arch, clear of the
  pediment); still static, still never a control. Suite 457 green
  + 14 skips.
- **⚡ Idea Collision — Llull's wheel over your own knowledge**
  (owner-approved from the polymathy research intake, 2026-07-26).
  New ⚡ Collide button on the Glossary tab: draws two of YOUR studied
  concepts (Glossary terms + Topic titles) and prompts you to recall
  both from memory and forge the connection in plain language, then
  save it as a Topic entry or Commentary. Pure kernel
  (lyceum/idea_collision.py, 4 headless tests, deterministic via
  injected rng); declines out loud when fewer than two concepts
  exist. Evidence label kept honest: retrieval practice (strong) +
  elaboration (moderate, Dunlosky et al. 2013) — no neural-rewiring
  claims. The same intake's fabricated studies (unverifiable journal,
  invented effect sizes) were REJECTED by the clinical-science-gate
  and documented as a teaching specimen; its knowledge-graph
  re-platform and diagnostic-profiling proposals were rejected as
  scope creep. Its "Phase 5" was found already shipped (FSRS spaced
  repetition). Suite 457 green + 14 skips.
- **🌏 The world-city skyline** (finish-out G5f, the owner's brief,
  2026-07-26: the highest art of Ming China, Japan, and India, fairly
  represented without clutter). The two golden-section turrets are now
  a tiered PAGODA (left) and a domed MUGHAL PAVILION (right), flanking
  the Byzantine Great Dome at center — three civilizations' geometric
  traditions in one hazed skyline, same quiet values, same §13 laws
  (static, muted, never a control). The narrative reading, per the
  proprietor: the hero approaches the city as toward Troy — "we're
  entering the city gates to go to the city" — and the city holds the
  world. Suite 453 green + 14 skips.
- **⛪ The Great Dome rises behind the gates** (finish-out G5e, the
  owner's Byzantine brief, 2026-07-26). The mural's background layer
  is now a full skyline: a structured sky in horizon-glow bands
  (lightest just above the rooftops — the future glows past the
  gate), two calm geometric clouds at golden positions, and at the
  focal center a great dome on its drum with flanking half-domes —
  the Hagia Sophia silhouette, chosen because Byzantium's highest art
  was built by engineer-geometers to catch light. All hazed per
  atmospheric perspective, all parametric (probed at three widths),
  all behind the midground wall — static, muted, never a control.
  Suite 453 green + 14 skips.
- **🏙 The city proper, glimpsed past the gate** (finish-out G5d, the
  owner's composition brief, 2026-07-26). The empty right side of the
  City Gates header now carries a one-point-perspective vignette:
  a walkway receding to a vanishing point placed at the canvas's
  golden sections, hazed rooftop gables flanking the way, a distant
  tower at the VP — the view a citizen gets just inside the walls.
  Deliberately low-contrast against the panel color: texture, not
  signal (the ADHD guardrail by VALUE, not absence); rooftops running
  off the canvas edge at minimum width read as "the city continues."
  Parametric throughout (canvas sizes to ~35% of the header, clamped
  120-280px; every shape a ratio); geometry probed at all three clamp
  widths; art-never-a-control gate extended to the vignette.
  Suite 453 green + 14 skips.
- **🏰 The wall becomes a painting** (finish-out G5c, the owner's
  composition brief, 2026-07-26: foreground/midground/background,
  vanishing light, golden ratio, "geometrically synced"). The scene
  is now a three-layer composition drawn in painter's-algorithm
  order: a hazed distant keep and golden-section turrets (atmospheric
  perspective — far = lighter), the curtain wall and flanking towers
  in the midground, the darkest-value gatehouse as the focal
  foreground. Every coordinate derives from canvas width as a RATIO
  (parametric layout, clamped for narrow windows), so the composition
  rescales in proportion and can never drift out of alignment —
  verified by a real-Tk geometry probe at three widths (golden
  sections in-canvas, towers always clear of the gate). Still static,
  muted, never a control. Suite 453 green + 14 skips.
- **🏰 The fuller castle + 💰 The Treasury** (finish-out G5b + G4a,
  Blueprint §13, owner's orders 2026-07-26). The city wall doubled
  down: flanking towers with arrow slits and crenellated teeth, a
  wooden gate with iron bands behind the portcullis, subtle top-light
  on the stone — still static, still muted, still never a control.
  And the Money panel takes its game name: **The Treasury** (window,
  header, and interior door) — the empire being grown is your own
  financial security; the wolves at the gate are creditors and
  grocery runs; figures are never softened (§13 Law 4). The
  proprietor's Theseus framing is on the blueprint: the black-sail
  story is the canonical checklist-failure parable — the shop's gates
  exist so finances never fly a black sail. Suite 453 green + 14
  skips.
- **🏰 The city wall is real** (finish-out G5a, Blueprint §13, the
  proprietor's logged and delighted decision, 2026-07-26). The City
  Gates panel now carries static vector art drawn in canvas
  primitives — stone wall, crenellations, a central arch with
  portcullis, the 🛡 Sentinel standing watch — responsive to window
  width, no images, no new dependencies, era-true to the 2D games
  the design honors. Bound by two laws: §13 Law 1 (static and muted —
  scenery, never spectacle) and ART IS NEVER A CONTROL, earned from
  this shop's own A−/A+ canvas-button defect: everything clickable
  remains a real button; the art canvas is gated against ever
  receiving a click binding. Real-Tk probe verified the drawing at
  full and narrow widths. Suite 453 green + 14 skips.

### Changed
- **🏰 The gates are named gates** (finish-out G1b, Blueprint §13,
  owner's design 2026-07-26). Header: "🏰 The City Gates" with the
  companion framing ("face ONE gate at a time — your Sentinel goes
  with you"); each area button now reads "… Gate" (🧠 Mental Gate,
  💰 Financial Gate, …) wearing a ridge border for the carved-plaque
  look; pushing a gate answers in the Sentinel's companion voice
  ("I know, friend — but we've got a plan…") while keeping the
  instruction crystal clear. Copy/color/border only per §13 Law 1;
  hardware note for the record: 1995-2005-class 2D game visuals are
  trivially within any 2026 budget laptop — the constraint is the
  distraction law, not the machine. Suite 452 green + 14 skips.
- **⚔ The Seven Gates** (finish-out G1, Hero's-Journey layer,
  Blueprint §13, owner's design 2026-07-26). The Wheel of Life front
  door now speaks the game's language: "☸ The Seven Gates — which
  gate do you enter today?", and the focus line reads "⚔ The quest is
  at the lowest gate." Theme is COPY + COLOR only, by §13 law — no
  new screens or mechanics, because for an ADHD audience the story
  must never become the distraction. The method underneath remains
  Ziglar's Wheel of Life, credited in the comments; the existing
  Reward-Draw engine, streaks, and trend graphs are recognized in the
  blueprint as the layer's loot and character sheet. Suite 452 green
  + 14 skips.
- **🛡 The Sentinel at the gate** (finish-out F7, owner's design
  2026-07-26). The dashboard's top banner now speaks in the product's
  own voice: "🛡 STATE YOUR PURPOSE — NAME YOUR GOAL", with the empty
  state "⚔ Halt! State your purpose. Name your goal — then enter."
  and the edit dialog recast as the Sentinel's challenge. Light
  gamified framing consistent with the app's name — the sentinel on
  the city wall challenges you before you enter, and answering it IS
  setting your aim. The underlying concept (Hill's Definite Chief
  Aim / Tracy's Major Definite Purpose) keeps its attribution in the
  code comments; no behavior change. Suite 452 green + 14 skips.

### Fixed
- **🎨 The color law — red means stop, nowhere else** (finish-out F6,
  owner QA 2026-07-26: "does the Study button need to be red? Red is
  stop… am I passionate about learning or am I stopping?"). Platform
  HIGs and ISO 3864 reserve red for errors/stop/destructive — and the
  red 📓 Study door sat in the same window as the red 🗑 Delete.
  Changes: Study door red→teal, Track door indigo→slate (ending the
  blue-family duplicate with the blue front door — humans discriminate
  only ~6-8 color categories per view), Career area red→brown
  (briefcase-neutral; red now means ONLY stop/delete anywhere in the
  house). The law is written into Blueprint §12 and enforced by a
  computed gate: contrast, door distinctness, and a red-family reserve
  check that correctly separates red from orange/brown. Suite 451
  green + 14 skips.
- **❓ Tour clipped to "❓ Tou" + shell-button uniformity** (finish-out
  F5, owner QA 2026-07-26). The toolbar's Dock/Undock and ❓ Tour were
  packed LAST, after the expanding content strip — so Tk starved them
  first and the Tour label clipped off the right edge (the Save-row
  law, horizontal edition; this corner had clipped before per the
  code's own history note). They now pack FIRST, beside the grip, and
  wear the bar's standard control spec (same font/padding as
  🎤 Voice / 🔊 Read) — consistency and standards, Nielsen #4.
  Gate locks the pack order. Suite 450 green + 14 skips.

### Added
- **🚪 One front door** (finish-out F4, owner's design 2026-07-26).
  The dashboard's four-button exterior row (Planning / Track / Money /
  Study) is gone. The house now has exactly three doors, on the
  Session panel's tab bar: ☸ Wheel of Life (front door, blue),
  📊 Track (garage, indigo), 📓 Study (back door, red). Planning is
  not a door anymore — it is where the FLOW goes (wheel → goal →
  matrix → plan); Money is not a door — cost rides the flow as an
  attribute of the goal (meds refill → cost → budget; pharmacy trip →
  schedule), blueprinted as a §12 carry rule. Per the §12 trap rule
  no room is orphaned: the Planning hub and Money panel keep quiet
  interior doors at the Start room's foot ("More rooms:"), and the
  morning/evening nudge-flash references were re-pointed there.
  1 new gate (exterior row stays gone + all four rooms reachable).
  Suite 449 green + 14 skips.
- **☸ The Front Door — guided session flow, Phase A** (finish-out F3,
  owner's design, Blueprint §12, 2026-07-26). The Session window now
  opens on the Wheel of Life as its ONE visible tab, wearing its own
  identity color (blue, distinct from all seven area colors, WCAG AA
  vs white — both computed in tests). The Start/Goals/Matrix tab
  buttons are gone; the rooms remain and are reached by WALKING the
  flow: rate today's 1-10 → push a colored area button → Goals
  (badge in the same color) → 💾 Save on a fresh goal AUTO-ADVANCES
  to the Matrix to sort do-now/defer/delegate/schedule (editing an
  old goal stays put) → ▶ Start session on the Wheel's footer ends
  the flow at Start. One purpose per screen, data walks forward —
  grounded in W3C COGA cognitive-accessibility guidance, Hick–Hyman,
  and the universal-design curb-cut principle (owner's spec:
  "not an exception to the rule — something that helps them").
  Phases B–D (goal→matrix→planner data carry) are blueprinted in
  §12. 1 new gate. Suite 448 green + 14 skips.
- **🎯 Goals: life area is a colored badge, not an open dropdown**
  (finish-out F2, owner accessibility QA 2026-07-26). Arriving from a
  wheel button, the worksheet now shows ONE colored chip — same color
  as the button you pushed, icon + word on it (three redundant
  signals) — instead of a dropdown holding seven alternatives while
  you work on one. Grounding: Hick–Hyman law (decision time grows
  with visible choices), extraneous-load reduction (cognitive load
  theory), and redundant coding per accessibility practice. Function
  kept via progressive disclosure: click the badge and the area menu
  opens on request; the badge repaints to the new area's color.
  1 new gate. Suite 447 green + 14 skips.
- **☸ Wheel of Life: colored area buttons → Goals** (finish-out F1,
  owner accessibility QA 2026-07-26 — first item of the post-1.0
  finish-out pass: ADHD/dyslexia/dyscalculia real-world lens, cosmetic
  and small-functional only, no restructure). Each life area's name is
  now a BUTTON in its own consistent color (color-coding aids scanning
  and cuts text-decoding load; color is never the only signal — icon
  and word remain; all seven shades hold ≥4.5:1 WCAG AA contrast
  against the white text, verified by a computed test). Set the 1-10
  slider, push the color: you land on a fresh Goals worksheet with
  that life area already selected and the cursor in the Goal line —
  the area rides along automatically, the first brick of the
  no-re-entry flow (wheel → goal → matrix → Start), which is on the
  board as a design item. 3 new gates. Suite 446 green + 14 skips.

## [1.0.0] — 2026-07-25

**First full release**, cut at the stakeholder's order. The v0.9
release-candidate scope passed both layers of V&V: **verification** —
457 automated tests (443 green, 14 platform-dependent skips) plus the
static design-law gates — and **validation** — the proprietor's
multi-week user-acceptance program, reported complete 2026-07-25:
books/articles load from the desktop into the Library and can be read,
saved, deleted, and copied into Topics, Study Notes, Journal, Glossary,
and Commentary; the Eisenhower Matrix and the daily/weekly/monthly
planners are fully operable from the floating toolbar (add, remove,
mark off, copy/paste). Known open items are tracked on the Shop Punch
List (`docs/wiki/Shop-Punch-List.md`) — v1.0 means the promised scope
is delivered and validated, not that the backlog is empty.

### Fixed
- **📒 Read-only glossary view: right-click copy-out** (punch item 3,
  Eisenhower DO, 2026-07-25). The view allowed selecting a definition
  but offered no Copy. Now: right-click → Copy / Select all (plus
  Ctrl+A) — deliberately not the full clipboard menu, since Cut/Paste
  would be dead items on a disabled body and a dead control is a
  defect. Static gate added.

### Docs
- **Foreman's dashboard** (`docs/foreman/`) — the proprietor's five
  dashboard sections mirrored for the foreman as versioned markdown
  (Journal, Topics, Glossary, Commentary, Library); Eisenhower-triaged
  work queue lives in its TOPICS.md and mirrors to all stations by
  git rather than OneDrive.

### Fixed
- **📌 Topics could not be cleared — the last section blocking an
  empty dashboard** (owner QA, 2026-07-25: "basic 101 stuff — can we
  add things, can we delete everything?"). Root cause: Tk's default
  `exportselection=1` makes the app's selection a SINGLE token —
  clicking the entries list or the compose pane silently DESELECTED
  the chosen topic, so toolbar 🗑 found `curselection()` empty and
  declined with only a status-line hint. The Topics tab, with two
  listboxes and a paste pane side by side, was the section most
  exposed. Fix: `exportselection=False` on the four CRUD listboxes
  (topics, topic entries, glossary, commentary) so a selection
  survives until the user changes it; plus `parent=` on both topic
  delete confirms, which could previously open BEHIND the Study
  window and make Delete look dead. Proven both ways: real-Tk test
  shows the default stealing the selection and the flag preserving
  it; static gates lock the flag and the parenting. Suite 442 green
  + 14 pre-existing skips.
- **👻 Ghost-tab guard on the new toolbar-Add route** (foreman's
  self-audit of the same-day fix, 2026-07-25 — caught on the board
  before it bit). `_study_active_tab` outlives the Study workspace
  window (close nulls `_study_win` but never the tab key), so the new
  `_study_add_from_toolbar` would have popped a Glossary/Commentary
  dialog from anywhere in the app after the workspace closed. The
  legacy save/remove handlers only survive this by accident (dead-
  widget TclError makes them decline). Fix: the Add route verifies
  `_study_win` exists before acting. The whole workflow is now also
  written down as pseudocode — Rebuild-Blueprint §11, the fourth
  source of truth — with this trap documented. 1 new static gate.
  Suite 438 green + 14 pre-existing skips.

### Docs
- **Rebuild-Blueprint §11** — the paste-to-section workflow (traffic
  light × entry windows) in rebuildable pseudocode: dispatch law,
  entry-window lifecycle (hook contract, bottom-first rows, no grab),
  and the known ghost-tab trap.

### Fixed
- **➕ The floating toolbar's green Add never reached Topics /
  Glossary / Commentary** (owner UAT continued, 2026-07-25; the
  qa_debug.log breadcrumbs showed `ftb-add: fell through` three times
  across two days while the owner's paste sat stranded). The Add
  dispatch chain had handlers for the Prompt Library, Library, Planner,
  Matrix, Journal and Review — but none for the three study sections,
  and committing an open entry dialog relied on a heuristic
  find-a-save-button search that kept missing in the field. Fix, the
  deterministic pilot pattern: (a) both entry dialogs now register
  their save() as `_ftb_inline_input` while open (cleared on close) —
  the hook `_prompt_inline` already proved; (b) green ➕ honors that
  hook first, exactly like yellow 💾 always has, so EITHER button
  commits the open box; (c) new `_study_add_from_toolbar` in the Add
  chain: with no box open, ➕ on Topics opens the new-topic box and on
  Glossary/Commentary opens that section's entry window. The owner's
  QA workflow — copy in the Library, paste into the box, click ➕ —
  now lands the entry in the section. 2 new static gates. Suite 437
  green + 14 pre-existing skips.
- **📒📑 Pasted text stranded in the Glossary/Commentary Add dialogs —
  no way to save it** (owner UAT of the same-day clipboard fix,
  2026-07-25). Three compounding causes: (a) `grab_set()` made the
  dialogs modal, freezing the floating toolbar's yellow 💾 Save;
  (b) the dialogs' own Save row was packed AFTER the expanding body —
  Tk starves the last-packed widget first, so a short window clipped
  Save clean off-screen (reproduced in a real-Tk probe: at 150px the
  button sat 70px past the edge, unmapped); (c) the toolbar's
  find-a-save-button fallback skipped every Toplevel ancestor, and
  these dialogs keep 💾 Save in a frame BESIDE the text field, so the
  Toplevel is the only shared ancestor — the docstring promised the
  fallback reached these dialogs; it structurally could not. Fix:
  grab_set dropped (non-modal, matching the toolbar-driven pilot),
  button rows bottom-packed BEFORE the body in all three dialogs
  (the `_prompt_for_text` law), and the fallback now skips only the
  root Tk — the <80-widget guard already keeps big windows out.
  3 new static gates in `tests/test_clipboard_wiring.py`. Suite 435
  green + 14 pre-existing skips.
- **📒 Glossary entry dialog had no right-click paste** (owner QA find,
  2026-07-25, screenshot evidence — a title copied in the Library
  could not be pasted into a new entry's Term field). The dialog was
  the one input form that never got the app-wide clipboard menu; the
  Commentary entry dialog mirrors it and had mirrored the miss. Fix:
  four wiring lines — `_attach_clipboard_menu` (the existing, tested
  helper) on the Term/Title Entry and the scrolled body of both
  dialogs, with the standard 🧹 Clear. New static regression gate
  `tests/test_clipboard_wiring.py` (ast scan, headless) locks the
  wiring in place. Suite 432 green + 14 pre-existing skips.
- **⏱ Pomodoro blocks could run long against the wall clock** (owner
  QA session 2026-07-22; diagnosed from the pomo breadcrumbs — a
  "20-minute" work block on 07-21 ran 61 real minutes, another 27).
  Root cause: the countdown SUBTRACTED one second per Tk `after(1000)`
  tick, so laptop sleep and event-loop load stretched every counted
  second — the timer trusted its ticks instead of the clock. Fix: new
  pure kernel `lyceum/pomo_clock.py` — a wall-clock DEADLINE is the
  single source of truth; ticks only refresh the display
  (`remaining_seconds(deadline, now)`, clamped, drift-immune by
  construction). Cycle machinery (work→break auto-transitions, 4-cycle
  long break, chime) verified correct from the same breadcrumbs and
  untouched. 7 new headless tests (drift, sleep-jump, spam-call
  immunity); smoke 5/5 under a real `mainloop()` (simulated sleep past
  the deadline ends the block and auto-starts the break with a fresh
  deadline). Suite 430 green + 14 pre-existing skips.
- **🧠 Harvest-terms checkboxes looked dead** (owner QA field report,
  2026-07-22, mid-coursework — "can't even check the boxes"). Ninth
  invisible-state instance: the approval dialog painted its indicator
  `selectcolor=BG_INPUT` (#0b1220) with a default-black checkmark on
  the dark theme — the boxes WORKED and defaulted to checked, but
  checked and unchecked were visually identical, so the control read
  as broken. Fix: white indicator (black ✓ on white, unmissable),
  term labels are click targets too (bigger than the 13px box), and
  the green button is now a live counter — "➕ Add N checked terms" —
  so every toggle shows visible proof. Smoke 8/8 under a real
  `mainloop()` (box click and label click both move the counter; only
  checked terms reach the Glossary on temp DB). Suite 423 green + 14
  pre-existing skips.
- **🗒 Prompt Library clipped its own bottom at large fonts** (owner QA
  field report + screenshot, 2026-07-21 — "top to bottom you can't see
  the whole screen"; at 26pt+ the Response box and the button row fell
  off the window edge, unreachable). Reproduced under a real mainloop
  first: window geometry was INNOCENT (stays clamped on-screen); the
  root cause was layout — Text `height` is requested in lines-of-
  current-font, so A+ ballooned the requests and Tk's packer starved
  the last-packed widgets (Response measured 1px at 32pt). Fix, both
  halves textbook: button row now packs FIRST at side=BOTTOM (the
  `_prompt_for_text` never-clip law, finally applied here), and
  Prompt/Response share one gridded frame with EQUAL uniform row
  weights — a guaranteed 50/50 split at any font, scrollbars reaching
  the rest. Height requests capped at 4 lines. Smoke 7/7 on the real
  display (Response 65px alive at 32pt + docked toolbar; buttons
  visible; window inside screen; 14 entries all reachable — the list
  has no cap, it scrolls). Suite 423 green + 14 pre-existing skips.
- **🔊 Read didn't speak the Session Start "Last session" box** (owner
  QA field report, 2026-07-21 — TTS read the notes box but not the
  handoff box). Root cause: the bug-5 rebuild enrolled the new box in
  the clipboard registry but not the reader's aim registry (Read speaks
  the last-clicked pane) — SEVENTH enrollment-class instance, this one
  introduced by the previous night's own repair. Fix: one-line
  enrollment in the house read-pane pattern (`_study_set_read_target`
  on click; works on a disabled Text; cursor parks at word 1). Smoke
  11/11 under a real `mainloop()` (click aims the reader; cursor at
  top). Also hardened `tests/gui_base.py`: one shared Tk interpreter
  per test process — repeated create/destroy cycles had begun
  intermittently skipping 4 GUI tests via Tcl's `tcl_findLibrary`
  re-init fault, making the suite count wobble. Suite now stable at
  423 green + 14 py-fsrs skips, twice consecutively.
- **🖱 Right-click "Select all" was dead on every single-line field**
  (owner QA field report, 2026-07-21, with screenshot — on the Session
  Start "One primary task" field, Select all did nothing; the only way
  to copy was drag-highlighting to the end of the line). Root cause:
  the helper behind the menu spoke only the multi-line Text API
  (`tag_add`); on a `tk.Entry` it raised inside the callback and the
  menu just closed — an invisible failure, SIXTH instance of the class,
  live on the 20+ Entries that carry the house right-click menu.
  Fix: new pure kernel `lyceum/select_all.py` dispatches by widget
  capability (Text family → tag the full range; Entry family →
  `select_range(0, end)`); `_select_all_in` is now a thin shell holding
  only the Tk error guard. 7 new tests (fake-dispatch + real-Tk proofs,
  incl. select-then-copy equals full Entry content and select-all on a
  disabled Text); suite 423 green + 14 pre-existing skips, 0 failures;
  smoke 9/9 under a real `mainloop()` — the app's own menu handler
  selects the real prefilled primary-task Entry end-to-end.
- **📋 Session Start "Last session" box couldn't be copied** (owner QA
  field report, 2026-07-21 — "I should have been able to copy and paste
  this whole thing just using right click"; he had to screenshot his own
  handoff to brief the coding assistant, blocking the session-start
  workflow). Diagnosis: the box was a `tk.Label` — no selection, no
  clipboard, not enrollable in the house right-click menu; FIFTH
  instance of the enrollment defect class, as the whitepaper note
  predicted. Fix: the box is now a read-only `tk.Text` (disabled =
  copy yes, edit no) with a scrollbar for long handoffs, filled through
  a new pure kernel `lyceum/handoff_view.py` (`fill_readonly` — the
  enable→replace→disable contract, re-locks even on error) and enrolled
  in `_attach_clipboard_menu` (right-click → Select all / Copy).
  8 new headless tests (fake-widget contract + real-Tk selection/copy
  proofs); suite 430 total — 416 green, 14 pre-existing `py-fsrs`
  optional-dependency skips, 0 failures; smoke 6/6 under a real
  `mainloop()` on temp sidecars (Copy → clipboard equals box text).
- **🔡 A−/A+ didn't grow the Prompt Library letters** (owner QA field
  report, 2026-07-21, mid-session — "the letters aren't increasing";
  breadcrumbs read FIRST per the standing method: every click fired and
  stepped 12→28pt, but only the Study surfaces were enrolled — the
  invisible-success class again). Fix: Prompt/Response boxes join the
  legibility loop (font + line spacing), the Title entry scales font-only,
  the navigation list stays fixed per the index-stays-legible rule, the
  window now OPENS at the owner's persisted size, and the breadcrumb line
  gains a `prompt_lib=yes/no` field. Smoke 5/5 under a real `mainloop()`
  (grew 27→31pt and back at the owner's real saved size); suite 422 green.
- **🎤 Mic couldn't dictate into the Prompt Library or Time Check boxes**
  (owner QA field report, 2026-07-20 — session titles couldn't be
  recorded by voice). The toolbar mic enrolls widgets via a `<FocusIn>`
  → `_set_mic_target` binding used in 20+ places, but the Prompt
  Library's Title / Prompt / Response boxes and the Time Check note box
  were never enrolled. Four one-line enrollments in the house pattern
  (+ clipboard menu on the Title). Smoke 5/5 under a real `mainloop()`:
  focus lands in each box → the mic targets it. Suite 422 green.
- **⏱ Time Check popup couldn't be saved from the safe spot** (owner QA
  field report, 2026-07-20 — blocker filed before his own break: "if we
  can't save the A-1 work, we can't go to break"). The check-in popup sat
  entirely outside the floating-toolbar world: no dock slot, no Save
  handler, no mic for the note box, no Enter-to-commit — and its "Logged"
  confirmation printed on the dashboard status bar the popup itself
  covered, so successful saves LOOKED like failures. House-pattern fix:
  `"time_check"` added to the dock map + dock menu; yellow **Save** (and
  Enter in the note box) files the check-in under the last-used category
  (first use defaults to 🅰 A-1 Task); the note box gets the standard
  right-click clipboard menu; and the status line now says on its face
  when the note went in ("⏱ Logged: 🅰 A-1 Task (30 min) · ✏ note
  saved"). Wiring-only; runtime proof: smoke 9/9 under a real
  `mainloop()` on a temp DB; suite 422 green.
- **Prompt Library: Save didn't work, Delete destroyed, and the toolbar
  never came** (owner QA field report, 2026-07-20 — found on the real
  screen while filing a live job-search exchange). Three defects, one
  repair in the house pattern: (1) the yellow Save lamp had no Prompt
  Library handler in the dispatch chain — `_prompt_lib_save_from_toolbar`
  added with visible "saved" confirmation; (2) the red lamp hard-deleted
  ("This can't be undone") against the archive-never-delete law — it now
  ARCHIVES: the row stays in the DB (`archived_at` additive migration,
  NULL = active) and a Markdown copy with YAML front-matter is written
  to a **Prompt Archive** folder beside Books on the OneDrive-synced
  Desktop — file written FIRST, DB updated second, so a failed write
  never loses the only copy; (3) the floating toolbar now auto-docks to
  the window on open (AAR/Study precedent) and goes home to the
  dashboard on close. New pure kernel `lyceum/prompt_archive.py`
  (Markdown render + Windows-safe filenames), 12 headless tests on a
  temp DB; suite 410→422; smoke 5/5 under a real `mainloop()`; the ❓
  toolbar tour cards updated to tell the truth about archiving.

### Added
- **QA breadcrumb trail (`qa_debug.log`)** — the standing breadcrumb
  method (voice_debug.log, fontsize_debug.log) extended to everything
  the proprietor road-tests: floating-toolbar dispatch (which panel
  claimed Add/Save/Delete, or that a click fell through), every dock
  move (target → resolved window), every reward draw (event → tier +
  drought counter), and ambience start/stop/unavailable. One timestamped
  line per real event, append-only, git-ignored, never raises. Method
  documented in `docs/wiki/Testing-and-QA.md` — a field report now
  resolves to "never fired / wrong values / fired invisibly" in one log
  read.

### Fixed
- **Floating toolbar (and its mic) couldn't live in the After-Action
  Review window** (owner QA field report, found on the real screen).
  The AAR's traffic-light *dispatch* was wired, but the window was
  missing from the toolbar's dock map — so the bar itself had nowhere
  to dock there. Fix in the house pattern, three parts: `"review"`
  added to the dock `window_map`, "Dock to After-Action Review" added
  to the dock menu (shown while the window is open), and the Study
  window's re-dock-on-open precedent applied (the bar comes home to the
  AAR if it lived there last time). Closed AAR falls back to main
  safely. Runtime-proven: 3/3 smoke checkpoints under a real
  `mainloop()`.

### Added
- **🪞 After-Action Review joins the floating-toolbar dispatch chain**
  (owner QA find). The traffic light now works inside the AAR window:
  **green Add** jumps to today's reflection (one entry per day, so "add"
  means "today, ready to type"), **yellow Save** commits the day shown,
  and **red Delete** clears TODAY's draft only — a past day is refused
  with "past reviews are history — never deleted" (the archive law).
  Same context-test pattern as every other panel; handlers step aside
  when focus is elsewhere. Runtime-proven under a real `mainloop()`
  (6/6 smoke checkpoints, temp DB).
- **🌧 Ambience — a quiet comfort bed under the read-aloud voice**
  (`lyceum/ambience.py`, +10 tests). New Library button opens a chooser:
  wind, rain, ocean, or a binaural 10 Hz tone, at Quiet/Medium volume, on
  its own audio stream so it mixes WITH the voice (sounddevice — already a
  dictation dependency; zero new packages). All sound is synthesized
  locally as seamless loops (crossfaded noise beds; whole-cycle binaural
  seam). Honesty labels ship in the kernel and render verbatim in the UI:
  every bed is a **comfort/preference feature**, and the binaural option
  carries "**NOT proven to improve learning** — needs headphones" on its
  face (the science gate's verdict on the entrainment literature). The
  proposal's "hear the same material twice simultaneously" idea was
  rejected — competing speech streams interfere; sequential re-listening
  is the honest alternative. Degrades gracefully when audio deps are
  missing; the button always shows what's playing.
- **🎁 Reward-Draw — variable-ratio reward engine** (`lyceum/reward_engine.py`,
  +15 tests). Finishing a Focus Mode block now draws from a weighted reward
  pool (70/25/5 STANDARD/UNCOMMON/RARE): a quiet green status dot, a quote
  card from the owner's library, or a rare gold flash + chime. Engineering
  honesty built in: a **pity guarantee** (a RARE can never be more than 12
  draws away — pure slot-machine math allows cruel droughts; this engine
  doesn't), an **honesty gate** (every pool payload carries a named library
  source; unsourced payloads are refused at write time — no fabricated
  quotes), **no reward without work** (blank events refused), and an
  **append-only `reward_log`** that doubles as the pity counter's memory
  across restarts. Mechanism labeled honestly: variable-ratio reinforcement
  (Ferster & Skinner, 1957) — anticipation, not magic. Two additive tables
  (`reward_pool`, `reward_log`); kernel is Tk-free and fully headless-tested;
  smoke-tested under a real `mainloop()`. Distilled from the NotebookLM
  BrainTrust review (2026-07-16) — the one proposal of four that cleared all
  intake gates on the first pass.

### Fixed
- **Read-aloud garbled backtick code spans — now atomic.** The normalizer ran
  its English rules over inline code, so `` `1024` `` was read as the year
  "ten twenty-four" and abbreviation replacement could corrupt tokens inside
  paths. Code spans are now exempt from ALL linguistic expansion and use a
  minimal code-reading form instead (`_` → "underscore", `/` → "slash",
  everything else verbatim) — standard TTS text-analysis practice (Sproat
  et al. 2001; Jurafsky & Martin). Externally proposed; **verified against
  the real code first** — the report's specific mechanism (slash/underscore/
  extension expansion rules) did not exist here, but the underlying defect
  and fix direction were real. +6 tests.
- **A− / A+ looked like "nonfunctional plugs" — they were working invisibly.**
  The breadcrumb log proved every click fired (16→32pt), but only three
  surfaces scaled (Glossary / Commentary / Topics pane) — a user watching
  Study Notes or the Journal saw nothing move, and the size silently pinned
  at the 32pt ceiling. Fix: **Study Notes editor and Journal body now scale
  too** (all five prose surfaces move together; navigation lists stay
  fixed), tour text updated, and the stuck persisted size was reset.

### Added
- **`scope-first` skill — the fourth permanent guardrail** (owner's order,
  2026-07-13): no code until a four-part scope statement (in-scope,
  explicit OUT-of-scope, acceptance criteria, lifecycle target) and a
  blueprint exist at project onset; scope changes are explicit logged
  decisions, never drift ("churn code" is the named failure mode).
  Anchored to ISO/IEC/IEEE 12207, SWEBOK, IEEE 29148, and Boehm's
  cost-of-change (1981). Installed project-level and user-level. Per the
  skill's own retroactive clause, this project's baseline was written:
  **`docs/SCOPE.md`** — including the 5–10-year lifecycle target, the
  stdlib-first stack rationale, and the named structural risk (single-file
  Tk shell) with its documented decomposition seam.
- **🧾 Bill Sentinel (Sprint F — the owner's own ask)** — prospective-memory
  scaffolding for bills. Pure kernel `lyceum/bills.py` (`next_due` with
  month-end clamping, `classify`, `next_action`) + a Money-hub card and
  window: every bill shows 🟢 automated / quiet / 🟡 due soon / 🔴 overdue,
  and ONE next-action line leads the panel (first red, else first amber,
  else "set up autopay for …"). Actions: add, mark paid, autopay toggle,
  send an amber/red bill to today's planner, archive (never delete). The
  goal state is every bill green (autopay) so the app goes quiet —
  automation and defaults beat remembering (Thaler & Benartzi 2004);
  the panel says plainly that the app cannot pay bills. Additive `bills`
  table; 17 tests incl. February clamping and next-action priority.
  Design decision (reconciled from the blueprint): a bill with no payment
  history is never called "overdue" — no evidence a cycle was missed.
- **V2MOM if-then line (Sprint D)** — the goal intake gains one **optional**
  field under Obstacles: *"If <your obstacle> happens, then I will …"*
  (implementation intentions roughly double follow-through — Gollwitzer &
  Sheeran 2006, meta-analytic d≈0.65). Stored in an **additive**
  `v2mom_goals.if_then` column (old tables migrate in place, data intact);
  the required fields are unchanged — the flow is not stiffened. 3 tests.
- **WCAG contrast kernel (Sprint C)** — `lyceum/wcag.py`: the W3C
  relative-luminance and contrast-ratio formulas with the AA thresholds
  (4.5:1 normal / 3:1 large) and an `audit_pairs` findings helper; 9 tests
  anchored to published W3C values. First palette audit: **all reading
  pairs pass AA (5.7–17.1)**; four white-label button colors fall short of
  AA-normal and are logged as **findings with proposed same-hue
  replacements** in `Assistant-Notes.md` §5 — the owner decides; nothing
  was recolored.
- **Two-lapse streak protocol (Sprint B)** — `lyceum/streaks.py`, a pure
  kernel behind the 📅 Never Miss Twice banner. ONE missed day is now an
  **amber rest-day encouragement** ("a rest day, not a broken chain" —
  self-compassion speeds lapse recovery, Neff 2003); only a **second
  consecutive miss** escalates to the **red fresh-start prompt** that asks
  for an exact time (fresh-start effect, Dai/Milkman/Riis 2014;
  implementation intentions, Gollwitzer & Sheeran 2006). Previously the
  banner went red on ANY yesterday-miss. 9 tests incl. a shame-free-language
  gate on the amber message.
- **`learning-science` skill** (`.claude/skills/learning-science/`) — the
  third permanent guardrail, from the vetted middle ground of the external
  framework proposal: study/review features and teaching use only
  techniques with real empirical support — retrieval practice (Roediger &
  Karpicke 2006; Dunlosky et al. 2013), spacing via FSRS (Cepeda et al.
  2006), worked examples with fading (Atkinson et al. 2000), expertise
  reversal (Kalyuga et al. 2003), delayed judgment-of-learning (Nelson &
  Narens 1990) — and known neuromyths are blocked with their debunking
  citations (learning-styles matching, Pashler et al. 2008; the
  10,000-hour rule, Macnamara et al. 2014). Includes the
  access-vs-efficacy distinction: accommodations are legitimate as access
  and are never claimed as learning outcomes. Handoff §6 now mirrors all
  THREE skills and specifies the no-drift fallback (bootstrap prompts are
  generated verbatim from the SKILL.md files, never re-summarized).
- **Interview-ownership framing in Job Readiness** — the Story and
  Interview pillar next-steps now teach defensible ownership language
  ("I built…", "I implemented…", answers in situation → action → result
  form) so practice matches what a candidate must say in the room.
  Adopted from the same proposal's career guardrail; the rejected parts
  (paste-in charters, per-session bootstrap prompts as the primary
  mechanism) are on the record in the session notes.
- **Permanent guardrail skills** — `.claude/skills/clinical-science-gate/`
  (the Strict Clinical Science 2026 evidence admission rule: verify every
  citation, label by evidence tier, no clinical claims) and
  `.claude/skills/classroom-code/` (textbook-CS SDLC in order, pseudocode
  first, tests before UI, functional code only, honest reporting). Written
  project-agnostic — Shannon's standing rules for ALL projects. The desktop
  handoff (§6) instructs the desktop assistant to install them as
  user-level mirror skills so they load everywhere.
- **Handoff memo** (`docs/HANDOFF_MEMO_2026-07-13.md`) — the state-of-the-
  world accounting: what merged in PR #50, and the six open items that only
  the desktop machine can finish (branch delete, both mirrors, mirror
  skills, dead-button audit, sprint queue, vetting the ~202 research files).
- **Desktop-assistant handoff** (`docs/DESKTOP_ASSISTANT_HANDOFF.md`) — the
  third reference, distilled from the vetted improvement audit and the
  2026-07-13 neurodivergence-research check-in: the "Strict Clinical Science
  2026" admission rule, the sprint queue in pseudocode (two-lapse streak
  protocol, WCAG contrast gate, V2MOM if-then line, **Bill Sentinel** —
  prospective-memory scaffolding for bills), the per-sprint paperwork duty,
  and the real-hardware dead-button audit. README now opens with the
  guardrails and points the desktop assistant at it.

### Removed
- Dead code: `_round_rect` / `_ftb_make_font_marker` (the Canvas road-marker
  A−/A+ that never received clicks; reverted to Buttons on 2026-07-12 and
  left as dead code since). Pseudocode preserved in `Rebuild-Blueprint.md` §10.
- **💼 Job Readiness audit** — the real-world job self-examination. A pure
  kernel (`lyceum/job_readiness.py`) scores six pillars a hiring process
  actually checks (Story, Proof, Skills, People, Pipeline, Interview) 0–4
  against plain-language rubrics; readiness is the share of the 24 rubric
  points, and the **next move** is always the concrete step above the lowest
  pillar (foundational order breaks ties). Wired into the Planning hub as
  **💼 Job Ready**: live meter + band badge (🔴 COLD START → 🏆 OFFER READY),
  per-pillar rubric text that follows the slider, one saved check-in per day
  (same-day saves replace, history is never deleted), delta vs the previous
  check-in on save, and slider prefill from the last check. New
  `job_readiness_checks` table (additive). 15 new tests incl. a
  `temp_study_db()` round-trip; smoke-tested under a real `mainloop()`.
- **Continuous Integration** — a GitHub Actions workflow (`.github/workflows/ci.yml`)
  runs `py_compile` and the unit-test suite on every push and pull request to
  `main`, on Python 3.11 and 3.13 (Windows). Automated Verification & Validation
  gate (IEEE SWEBOK).
- **Engineering wiki** — architecture, the 37-table database schema, a
  feature→method map, the fixed-bug history, testing/QA, SDLC posture, the
  development workflow, a CS glossary, and running session notes.
- This `CHANGELOG.md`.
- **Live-DB pollution guard** — `lyceum.db.assert_not_live_db` / `is_live_db`
  plus a `study_db.temp_study_db()` isolation context that refuses the live
  `study.db`, closing the recurring "headless run wrote to real data" bug class
  (`tests/test_db_isolation_guard.py`).
- **Design-law linter** (`lyceum/lint_designlaws.py`) — an AST check for the
  codebase's known UI traps: tuple `pady/padx` in a widget constructor
  (**Rule A**, regression-gated at zero) and hardcoded `.geometry("WxH")`
  literals (**Rule B**). `tests/test_designlaws.py`. First run flagged **4**
  hardcoded window sizes (one exceeds the owner's effective screen height).
- **`/sentinel-sprint` skill** (`.claude/skills/sentinel-sprint/`) — the proven
  kernel → test → wire → smoke → log → mirror pipeline, formalized as a
  project-local Claude Code skill.
- **Floating-toolbar traffic light + universal Save.** The action group is now
  green **➕ Add** → yellow **💾 Save** → red **➖ Remove**, same spot and colors
  in every panel. New `_ftb_action_save` context-dispatches like Add/Remove — it
  saves the Journal entry or Study Notes directly, and elsewhere commits the
  active panel/dialog's own Save (e.g. the Topics/Glossary/Commentary Add-Edit
  boxes) or fires `Ctrl+S`. The **A− / A+** buttons became a single black/white
  toggle: the last-pressed is white, the other black — a glanceable memory of
  which way you last sized the text.
- **Toolbar refined to a labeled, real-world control cluster.** Each action is
  now a **word above a colored lamp** — **Add** over green, **Save** over
  yellow, **Delete** over red (red relabeled from "Remove"). **A− / A+** are
  redrawn as **road-marker signs** (rounded canvas plates, large
  dyslexia-legible letter) forming the black/white toggle. Zero-instruction
  recognition for a visual/tactile, ADHD/dyslexia learner; identical in every
  panel. Pseudocode captured in `docs/wiki/Rebuild-Blueprint.md` §10.
- **Toolbar-driven text inputs (non-modal).** The New-topic, Rename-topic,
  Rename-bookmark, and Glossary Look-up boxes lost their OK/Cancel buttons and
  became non-modal `_prompt_inline` inputs: a right-click clipboard menu
  (Cut/Copy/Paste/🧹 Clear/Select-all) plus **Enter or the floating toolbar's
  yellow Save** to commit, Esc/✕ to cancel. The toolbar is the command locus
  even for entering text.

### Changed
- **Evidence-honesty pass on the README** (from the vetted July 2026 external
  improvement audit — see the new wiki page
  `Review-ImprovementAudit.md` for the full fact-check, per-item verdicts,
  and the Sprint B/C/D pseudocode blueprint). Claims now name their real
  mechanisms and citations: Vision Board "RAS programming" → goal-priming
  (Oettingen 2014); 10-Goals "subconscious" → retrieval practice (Roediger &
  Karpicke 2006); Pay-Yourself-First "refuses" labeled a pre-commitment
  device (Thaler & Benartzi 2004); All Seasons relabeled the simplified
  public Robbins mix, a fixed target allocation — not risk parity, not
  "Dalio's exact"; 5-4-3-2-1 labeled trade-book origin with an
  implementation-intention mechanism (Gollwitzer 1999); V2MOM attributed to
  Benioff/Salesforce. `lyceum/legibility.py` docstring adds the real
  specialized-font null results (Wery & Diliberto 2017; Kuster et al. 2017).
  Two citations in the source audit were found fabricated and kept OUT.
- **A− / A+ are real Buttons again (they were dead "empty plugs").** The
  road-marker **Canvas** version did not receive real clicks in the flow-layout
  toolbar — while the traffic-light **Buttons** in the same bar always did. A−/A+
  are now `tk.Button`s (styled as white/black sign plates), so clicking them
  reliably resizes the Study reading panes; the black/white toggle is preserved.
  A one-line breadcrumb log (`%LOCALAPPDATA%\SentinelForge\fontsize_debug.log`)
  records each click for on-machine verification.
- **README** corrected: test count `24 → 34`; entry-point and launcher names
  updated from the historical `book_reader.py` / `run_book_reader.bat` to the
  current `sentinel_personal_development.py` / `run_sentinel.bat`.
- **Study panels unified (Topics · Glossary · Commentary → Journal layout).**
  All three now follow the clean Journal anatomy — header → `[list | content]`
  → a single primary `+ Add/New` button. The multi-button rows and the
  paste-and-save boxes were removed; **Add / Remove route through the floating
  toolbar** (context-dispatched, with new `_glossary_remove_from_toolbar` /
  `_commentary_remove_from_toolbar` handlers), and secondary actions
  (Edit / Rename / Delete / Read / Import) moved to a **right-click menu** on
  the list. Reduces on-screen button count for a neurodivergent-first workflow.
- **Reading sliders.** Each Study read surface (Topics entries list, Glossary
  definition, Commentary pane) gained a **horizontal scrollbar** along the
  bottom so long lines can be slid into view and reviewed instead of clipping.

### Fixed
- **Study navigation lists no longer blow up with A− / A+.** The text-size
  control (`_apply_study_legibility`) was scaling the Topics/Glossary/Commentary
  index *lists* together with the reading text, so sizing up enlarged and
  **clipped the lists off-screen**. Scaling now applies only to the reading
  panes; the lists stay fixed and legible (matching the Journal list, which was
  already exempt — the reason it never exhibited the bug).
- **Delete-topic confirmation can no longer balloon off-screen.** When a topic
  title was a large pasted block (e.g. a whole AI reply), the confirm dialog
  grew until its Yes/No buttons left the visible area. It now shows a
  60-character single-line preview of the title.
- **Topics entries were unaddable/unreadable after the uniformity pass — fixed.**
  The Topics tab now has a **read/write pane** below the entries list: click an
  entry to READ its full text (word-wrapped, honoring your A−/A+ size),
  right-click to **paste** new content, and the **yellow toolbar Save** keeps it
  (blank lines split a paste into several entries; editing a loaded entry
  updates it in place, no duplicates).
- **Topics read/write pane: horizontal slider + working A−/A+.** The pane is now
  the canonical scrollable-Text widget (Text + vertical **and** horizontal
  scrollbars, `wrap=NONE`), so the **bottom bar slides a long line into view**.
  And `_apply_study_legibility` now includes this pane, so **A− / A+ actually
  resize it** (it had been left out of the resize list — the reason it appeared
  to "do nothing"). Selecting a topic now **auto-loads its most-recent entry
  into the pane**, so readable text is present to resize/slide immediately
  (before, the pane was cleared on select — the slider/resize acted on an empty
  pane and looked dead while the clipped entry list drew the eye). The pane also
  gets the larger share of the split for comfortable reading.
- **4 hardcoded window sizes removed** (Explain, Session End, Prompt Library,
  Add-to-topic) — routed through the screen-relative `_fit_dialog` helper. The
  Session-End dialog's `620x680` exceeded the owner's ~617 px effective height
  and clipped its bottom. Design-law linter **Rule B (hardcoded geometry) is now
  a hard test gate** so it can never regress.

## [0.9.0-rc1] — 2026-06-27

The stabilization increment: begin paying down structural and process debt while
keeping the product feature-complete.

### Added
- **Accessibility — hands-free spoken dictation commands.** `lyceum/dictation_commands.py`
  converts spoken punctuation ("period", "question mark"), formatting ("new line",
  "new paragraph", "tab"), and capitalization ("cap", "caps on/off", "all caps")
  into the characters they name, on the Whisper input path. Lets a user who
  cannot type punctuate, format, and capitalize entirely by voice. +10 unit tests.
- **Atomic database transactions.** `lyceum/db/study_db.py: transaction()` — an
  ACID-Atomicity context manager (commit on success, `ROLLBACK` on any error).
- **Pure functional core (`lyceum/`).** Extracted `metrics.py` (progress math) and
  `text_norm.py` (read-aloud text normalization) out of the GUI class, each
  unit-tested in isolation.
- **Read-aloud text normalization** — numbers, currency, percents, ordinals, and
  common abbreviations are expanded to their spoken form before TTS, applied at a
  highlight-safe seam so follow-along stays in sync.
- **Wheel of Life** — honest baseline→target progress and a roundness-trend graph.
- **First automated test suite** — now **34 unit tests**, all passing (progress
  kernels, DB atomicity, speech normalizer, dictation commands).
- **SDLC status & methodology declaration** (`docs/SDLC_STATUS.md`).

### Changed
- Four parent/child deletes (`budget_items`+`paychecks`, `system_steps`+`systems`,
  `habit_marks`+`habits`, `pert_steps`+`pert_plans`) are now single atomic units.
- Goals progress now uses the shared, tested accountability kernel
  `progress_pct = (current − baseline) / (target − baseline)`.

### Fixed
- **Non-atomic deletes** could orphan child rows if interrupted mid-operation
  (`d92afb3`). Now wrapped in `transaction()` and covered by a rollback test.

## [0.8.x] — 2026-06 (pre-changelog, summarized from Git history)

### Added
- AI Chat Assistant integrated across panels; onboard local AI (`ai_brain.py`,
  Ollama); AI web-search context; "Explain selection" tutor.
- Dockable floating read-aloud toolbar with dynamic sentence highlighting
  (PR #49); explicit accessibility toolbar (text +/−, OpenDyslexic overlay).
- Major Definite Purpose marquee; flexible time-audit intervals.

### Changed
- **Windows 11 native integration**: Immersive Dark Mode; WASAPI-compliant audio;
  native output-driver compliance for TTS.

### Fixed
- Read-aloud reliability: thread-safety race that cleared fresh highlights
  (`99950c3`); stale `tk.END` indexing leaving AI replies unhighlighted
  (`bcdcfdf`); continuous TTS halting after one chunk on `tk.TclError`
  (`85906f5`); newline parsing error in TTS (`d0917be`); command-line length
  limit bypassed via a temp file (`8dca41d`); `for…else` syntax error (`d00ef47`).

[Unreleased]: https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/compare/main...HEAD
