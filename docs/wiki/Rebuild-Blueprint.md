# Rebuild Blueprint — the house plans for Sentinel Forge

> **Purpose:** disaster-recovery seed file. If every line of code were
> lost, this document + `Database-Schema.md` + the README is enough to
> reconstruct the product. Everything below is **pseudocode and
> blueprint** — not runnable, deliberately language-portable. It would
> all have to be recoded — but recoded in *days instead of months*,
> because the decisions are already made and written down.
> Maintained by the assistant; checked during README reviews.

_Blueprint drawn 2026-07-11 from the as-built structure (commit
`33f16f71`, 172 tests green)._

---

## 1. The lot and square footage (what you're building)

| Measure | As built |
| --- | --- |
| Shell | ONE Python/Tkinter file, ~24,000 lines (`sentinel_personal_development.py`) |
| Functional core | `lyceum/` package, ~20 modules, zero Tkinter imports |
| Foundation | One SQLite file, ~40 tables, additive-only migrations |
| Tests | 172, all headless (temp DBs, injectable clocks) |
| Data on disk | `Books/` folder of .md excerpts + `.meta.json` sidecars; `HANDOFF_STATE.json` |
| Utilities | Ollama (llama3.2:3b) via loopback; Piper TTS binaries in `tts/`; faster-whisper |
| Bill of materials | faster-whisper, sounddevice, numpy, noisereduce, python-docx, pypdf, beautifulsoup4, send2trash, tkinterdnd2, openpyxl, fsrs |

**The prime directive of the lot:** local-first. No cloud APIs, no
keys. Files never leave the laptop; "delete" always means "move to
archive."

## 2. The foundation (pour this first)

SQLite + one atomic primitive. Everything stands on it.

```pseudocode
module study_db:
    STUDY_DB = local_appdata / "study.db"       # live DB is LOCAL,
    snapshot_to_onedrive_on_init()              # backup is synced

    function connect():
        con = sqlite.connect(STUDY_DB)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    contextmanager transaction():
        con = connect()
        with con:            # commit on success, ROLLBACK on exception
            yield con
        con.close()

    function init_schema():
        executescript(SCHEMA)   # every statement CREATE ... IF NOT EXISTS
        # additive-only law: never ALTER existing columns; new features
        # get new tables. Old databases must upgrade in place, silently.
```

**Inspection rule:** any multi-statement write MUST go through
`transaction()`. The FSRS review loop is the reference example (§6).

## 3. The load-bearing wall (do not cut into it)

**Functional core / imperative shell.** One wall separates the house:

```pseudocode
lyceum/          # THE CORE: pure logic, no UI imports, no wall-clock
    every function that touches "now" takes now: datetime = None
    every module unit-testable headless
shell (one file) # THE SHELL: Tkinter windows, buttons, threads
    reads/writes ONLY through core functions
    owns all widgets, all event bindings, all after() scheduling
```

Everything hard that ever happened in this house happened when
something leaned on this wall wrong (UI-thread file I/O, swallowed
exceptions). Rebuild rule: **write the core module + its tests before
its window.**

## 4. The electrical system (threading — how power moves)

```pseudocode
MAIN THREAD: owns Tk. mainloop() runs always. NEVER blocks on I/O.

WORKER PATTERN (the only approved circuit):
    on user action:
        capture inputs from widgets            # main thread
        Thread(target=work, daemon=True).start()
    function work():                           # background
        result = slow_thing()                  # model call, file move, TTS
        root.after(0, deliver, result)         # ONLY way back to the UI
    function deliver(result):                  # main thread again
        update widgets, refresh lists, set status

FUSES (lessons paid for):
    - after() from a worker silently dies without a running mainloop
      → all headless tests must run a real mainloop
    - never call winfo_children() on a possibly-dead widget unguarded
    - bare `except: pass` around a feature = a fuse that hides fires;
      every failure must surface somewhere visible
```

## 5. The plumbing (how data flows through the house)

```pseudocode
READING PIPE:  book file → parser (docx/pdf/md/txt/rtf/html, each
               try/except-optional) → text_area → highlight tags

EXCERPT PIPE:  selection → .md with YAML front-matter
               {doc_id, zone GREEN/YELLOW/RED, cognitive_load 1-10,
                source_book, timestamp, tags[]}
               + sidecar <file>.md.meta.json → Books/ (OneDrive-synced)

CONTEXT PIPE (feeds the small local model — the model never touches
network or disk itself):
    retrieval: score(text, query_terms) → rank docs → top passages
               capped ~6000 chars   # lyceum/local_context pattern
    sources:   library index (cached by path+mtime) | OneDrive index
               (same, repo-dirs pruned) | attachment | web search
               (DuckDuckGo lite, stdlib urllib)
    combined context string → ollama.chat(system + context, num_ctx=2048)
               # num_ctx pinned: default 128K tries to allocate ~15 GB

SESSION PIPE:  start goal/notes → HANDOFF_STATE.json → next-session
               roundup   # the cross-session memory loop

VOICE PIPES:   mic: sounddevice 16k mono → faster-whisper (Fast/
               Accurate/Best = base/small/medium.en) → target widget
               tts: text → normalize_for_speech() → piper.exe → wav →
               winsound.PlaySound (SYNC; stop = SND_PURGE)
               # NOT pyaudio — PortAudio dies on this hardware
```

## 6. The rooms (one per feature wing; rebuild in this order)

**Room 1 — the Reader (living room).** Big text area, sentence/word/
paragraph highlighting with 8 colors, font/size controls persisted.
Everything else attaches to this room.

**Room 2 — the Library (study).** Scan `Books/` recursively (skip
`Commentaries/`), Treeview list + in-window reading pane with
chapters/synthetic pages (~1800 chars). Row height FROM FONT METRICS.
Buttons: `+ Add files…` and the study-hub tab jumps. Remove = archive
move, background thread.

**Room 3 — the Study workspace.** Tabs: Study Notes, AI Chat, Topics,
Glossary, Commentary, Journal, Matrix (4 quadrants + checkbox lines),
Planner (week columns). All autosaving (debounced or on-switch).

**Room 4 — the Dashboard (front hall).** MDP marquee, Scoreboard
(3 lead-measure cards + marks-by-day + streaks), Idea Warehouse,
Focus Mode, Not-To-Do + hosts-file site blocker, Session Start panel.

**Room 5 — the Money wing.** ~15 calculators sharing two laws:
education-only (never execute trades) and **numbers need a picture**
(every figure gets a gauge/meter/translation). Tables: pay-first
balance, expenses, buckets, wishlist(+cooldown timestamps), holdings.

**Room 6 — the Memory room (FSRS).** The reference core module:

```pseudocode
class SRSService(db):
    scheduler = FSRS(enable_fuzzing=False)     # determinism law
    add_card(deck, front, back, source_ref):
        reject duplicate (source_kind, source_ref)   # unique index
        store fsrs_card_json (AUTHORITATIVE) + denormalized due/state
    review_card(card_id, rating 1..4, now):
        ONE transaction:
            card = from_json; card, log = scheduler.review(card, rating, now)
            UPDATE card json + due/state/reps/lapses
            INSERT append-only review_log row      # optimizer's food
    get_due_cards(now):  due <= now, unsuspended, oldest first, LIMIT small
    sync_from_glossary(rows): idempotent import, skip existing
    resync(): rebuild denormalized cols from json  # json always wins
window: front → "Show answer" → rate 1-4 → honest "comes back in N days"
```

**Room 7 — the AI room.** Chat with context sources (§5 pipe),
📎 attach, 📄 draft-document flow (model text → parse table → real
.xlsx with =SUM() / .docx paragraphs; refusal-guarded system prompts).

**Room 8 — the floating toolbar (hallway lighting).** Dockable bar:
quality picker, 🎤 voice, 🔊 read + scope/color/speed, ➕/➖ context-
routed add/remove, ❓ step-flash tour, dock menu of open windows;
host-destroy rescue re-docks to main.

## 7. The roof (UI laws that keep the weather out)

```pseudocode
size every window:  w = min(design_w, screen_w - margin)  # ~1097×617 usable
row heights:        from font.metrics("linespace") * 1.5+, never fixed px
one primary action per screen; <= 5 major choices
tuple pady ONLY in .pack()/.grid(), NEVER widget constructors
every save/action → visible confirmation (invisible success = bug)
reading surfaces honor user font (OpenDyslexic first)
palette: BG_DARK #0f172a, BG_PANEL #1e293b, BG_INPUT #0b1220,
         accents green/red/amber/cyan/purple/slate (see constants)
```

## 8. Construction schedule (the rebuild order, with acceptance gates)

```pseudocode
PHASE 0  foundation: study_db + transaction + schema     GATE: atomicity tests
PHASE 1  Reader room + fonts + highlighting              GATE: open/read/highlight
PHASE 2  Library + excerpt pipe + archive workflow       GATE: save/scan/archive tests
PHASE 3  Study tabs + autosave                           GATE: notes survive restart
PHASE 4  Dashboard + Scoreboard + Focus                  GATE: streak math tests
PHASE 5  Voice (whisper in, piper/winsound out, speed)   GATE: on-hardware audio check
PHASE 6  Money wing                                      GATE: finance kernel tests
PHASE 7  AI room + context pipes + doc writer            GATE: end-to-end model answer
PHASE 8  FSRS room                                       GATE: the 10 spec tests (RELAY-SRS-001 §5)
PHASE 9  toolbar + tour + polish                         GATE: full suite green + wiki current
EVERY PHASE: core module + tests FIRST, window second; commit; mirror 3 ways.
```

## 9. Replacement-cost note (why this document exists)

From bare ground with only this blueprint + `Database-Schema.md` +
the README: estimated **8–12 focused sessions** to functional parity,
because every architectural decision, every trap, and every acceptance
gate is pre-answered here. Without it: months, and the traps get paid
for twice. This is the cheapest insurance in the repo — keep it
current when rooms are added.

---

## 10. The floating-toolbar control cluster (the "safe spot")

The floating toolbar is the ONE fixed command locus — same controls, same
colors, same place, docked or floating, in every panel. Intent:
zero-instruction recognition for a visual/tactile, ADHD/dyslexia learner by
borrowing universal real-world signal grammar.

```pseudocode
build_floating_toolbar(body):
    ... mic / read / voice / speed / format-preset pickers ...

    # ── A− / A+  as ROAD-MARKER signs = ONE black/white toggle ──
    make_font_marker(parent, text, dir):
        canvas 52x40, bg = panel
        plate  = rounded_rect(canvas, inset, r=9, fill=white, outline=black, w=2)
        letter = canvas_text(center, text, big bold, fill=black)
        on click: study_font_step(dir); set_font_toggle(dir<0 ? "dec" : "inc")
        return (canvas, plate, letter)
    dec = make_font_marker(body, "A-", -1);  inc = make_font_marker(body, "A+", +1)
    set_font_toggle(active):                 # ONE always white, ONE always black
        paint(active_marker, fill=white, ink=black)   # last-pressed = white
        paint(other_marker,  fill=black, ink=white)
        persist active                       # survives dock/undock rebuild

    # ── Traffic light: the WORD sits ABOVE a colored lamp ──
    signal(word, icon, lamp_color, cmd, ink=white):
        cell = frame
          label(word)              packed TOP     # names the action
          button(icon, lamp_color) packed below   # colored lamp == meaning
        return button
    signal("Add",    +,   GREEN)          -> ftb_action_add
    signal("Save",   disk, YELLOW, black) -> ftb_action_save
    signal("Delete", bin,  RED)           -> ftb_action_remove

    # ── Universal, context-dispatched actions (identical in every panel) ──
    ftb_action_add:    try each panel's add-from-toolbar; else click an
                       "add/new/create/upload" button in the active context
    ftb_action_save:   journal? save entry. notes? save. else click the active
                       panel/dialog's "Save" button; else fire Ctrl+S
    ftb_action_remove: try each panel's remove-from-toolbar; else click a
                       "delete/remove/clear" button; ALWAYS confirm first
```

**Design laws carried here:** color == meaning (green go / yellow hold /
red stop); the word sits ABOVE the color so it reads without training;
A−/A+ keep one marker white and one black at all times, so "which way did I
size it?" is answerable at a glance. Text-size + Format presets touch the
READING panes only, never the navigation lists (that scaling bug is fixed
and lint-gated). The three actions are one context-dispatch each, so the
cluster behaves the same everywhere it appears.

## 11. The paste-to-section workflow (traffic light × entry windows)

Intake (the owner's QA workflow, proven out 2026-07-25): copy in the
Library → paste into a little entry window → green ➕ (or yellow 💾) →
the entry lands in Topics / Glossary / Commentary. This pseudocode is
the FOURTH source of truth for that workflow — the other three are the
three synced copies of the code (GitHub, the live install, the OneDrive
clone). If they ever disagree, rebuild to this.

```text
ON green ➕ Add:
    IF an entry window is open (hook _ftb_inline_input registered):
        COMMIT it (run the hook); STOP.
    FOR each panel handler (prompt library, library, planner, matrix,
                            journal, review):
        IF that panel's WINDOW EXISTS and it claims the click: STOP.
    IF the Study workspace WINDOW EXISTS (not just a remembered tab):
        SWITCH on the visible tab:
            topics     -> open the new-topic box
            glossary   -> open the Glossary entry window
            commentary -> open the Commentary entry window
        STOP.
    ELSE fall through: breadcrumb to qa_debug.log + status-line hint.

ON yellow 💾 Save:
    IF an entry window is open: COMMIT it (same hook); STOP.
    ... existing panel chain unchanged ...

ENTRY-WINDOW LIFECYCLE (Glossary / Commentary / new-topic box):
    ON OPEN:  register save() as _ftb_inline_input — a CONTRACT the
              toolbar honors first; never a heuristic button search.
    ON CLOSE: clear the hook ONLY if it is still ours (identity check —
              a newer window may have taken the slot).
    LAYOUT:   button row packs BOTTOM-FIRST (Tk starves the last-packed
              widget, so bottom-first means Save can never clip);
              NO grab_set (a grab freezes the toolbar).

KNOWN TRAP (worked out here before code):
    _study_active_tab OUTLIVES the Study workspace window — it is a
    memory, not a state. On window close _study_win is nulled but the
    tab key persists. ANY dispatch keyed on the tab MUST also verify
    _study_win exists, or it acts on a ghost. (The legacy save/remove
    handlers survive only by accident — dead-widget TclError makes them
    decline. New routes must check the window explicitly.)
```

## 12. The Front Door — guided session flow (proprietor's design, 2026-07-26)

Universal-design guided flow: ONE entry, one job per screen, data walks
forward, no re-entry. Anchored in W3C COGA guidance (one purpose per
screen, minimal distraction, consistent cues, chunked steps, low memory
load), Hick–Hyman, and the curb-cut principle: built for neurodivergent
users, costs neurotypical users nothing.

```text
THE FLOW (the proprietor's spec, verbatim in structure):

  FRONT DOOR = ☸ Wheel of Life, wearing its OWN distinct color.
      No Start/Goals/Matrix tabs in view — the rooms remain,
      reached only by walking the flow (escape hatch: rooms stay
      programmatically reachable; guided path is the DEFAULT).

  THE KEY: before anything else, set today's 1-10 on the areas.
  THEN: push ONE colored area button →

  GOALS (one worksheet, area badge in the same color):
      write the goal (~3 sentences: what + why-now) → Save →
      AUTO-ADVANCE to →

  MATRIX (Eisenhower): sort THE GOAL's work:
      do-now / defer / delegate / schedule →

  PLAN (day planner): the do-now and scheduled items LAND here as
      tasks — carried, never re-typed → the goal's next step is
      the day's "idea" (this is what I'm working on: my mental
      stability / my finances / …) →

  START: click ▶ Start and begin the session with the plan loaded.

CARRY RULES (no re-entry):
  area color+icon+name ride the whole flow (redundant coding);
  goal title seeds the matrix entry; matrix do-now/schedule seed
  planner tasks (the Goals "Add to calendar" tie already exists —
  reuse, don't duplicate).

PHASES (each shippable alone, one commit each):
  A: wheel = default + only visible tab, distinct color band;
     Save goal auto-advances to Matrix           [small-functional]
  B: goal → matrix carry ................ EXECUTED 2026-07-27
     (lyceum/flow_carry.next_action: first plan line, else title →
      Do-Now bullet via add_text_to_matrix_quadrant, sourced 🎯)
  C: matrix → planner carry ............. EXECUTED 2026-07-27
     (the same next action lands on TODAY's planner via the house
      calendar idiom '🎯 goal: step', deduped case/space-insensitively
      so a re-save never doubles the day; kernel rules in
      lyceum/flow_carry.py)
  D: ▶ Start session + loaded-plan summary ... EXECUTED 2026-07-27
     (session_briefing + count_do_items kernels; the Start room
      rebuilds the briefing every time it is shown — today's tasks
      ✔/▫ capped at 6, Do-Now count, empty plan speaks)

KNOWN TRAP: hiding tabs must NOT orphan the rooms — every room
  reachable through the flow, verified per phase; a room you can't
  reach is a regression, not a simplification.
```

### §12 amendment (2026-07-26, F4): doors and the cost carry rule

The house has THREE doors, all on the Session tab bar: ☸ Wheel (front,
blue) · 📊 Track (garage, indigo) · 📓 Study (back, red). Planning and
Money are NOT doors: planning is the flow's destination, and money is
a CARRY — a cost attribute captured while walking the flow (a goal's
medication refill has a price and a pharmacy trip: the price belongs
to the budget, the trip to the schedule/do-now). Until the cost carry
is built (Phase B/C), the Planning hub and Money panel keep interior
doors at the Start room's foot — the trap rule holds: no orphan rooms.

### §12 amendment (2026-07-26, F6): the color law

Paint is code. (1) The traffic light's meanings are RESERVED — green
go/add, yellow save, RED stop/delete only (platform HIGs; ISO 3864
gives red the strongest reserved meaning): no room or door identity is
ever red-family. (2) Identities never duplicate the traffic light's own
shades. (3) No hue family repeats within one view — humans discriminate
only ~6-8 color categories in context (Ware). Applied: Study door
red→teal, Track door indigo→slate (ended the blue-family duplicate with
the front door), Career area red→brown. Gated: contrast, door
distinctness, and a computed red-family reserve check.

## 13. The Hero's Journey layer (proprietor's design intake, 2026-07-26)

Narrative theming over the EXISTING structure — never new mechanics.
The frame: no one is coming to save you; the dashboard is the
companion; the Sentinel challenges at the wall (§ F7); the Wheel's
seven colored buttons ARE the seven gates of the city; Reward-Draw is
the loot (variable-ratio, honesty-gated); streaks and trend graphs are
the character sheet.

```text
LAWS OF THE LAYER (ADHD-safe gamification):
  1. Theme = COPY + COLOR only. No new screens, popups, animations,
     or mechanics in the name of fun — for this audience the story
     must never become the distraction (W3C COGA: minimal
     distraction; the owner's own guardrail).
  2. Honesty survives the theme: reward payloads stay source-cited;
     no manufactured praise; numbers stay numbers (SUS, streaks).
  3. Attribution survives the theme: Hill/Tracy/Ziglar concepts keep
     their credits in code comments; the UI wears the game voice.
  4. Chore quests (money week: paycheck → rent → utilities) may be
     REFRAMED as quest steps in copy, but the figures are never
     softened — the game makes the truth pleasant, not vague.

PHASED (each = copy-level, one commit):
  G1: Wheel = the Seven Gates (header + focus line)      [ready]
  G2: Goals worksheet = the Quest (title copy)            [next]
  G3: Matrix = the War Room; Planner = the March          [later]
  G4: Money chore-flow quest copy (per Law 4)             [later]
```

### §13 amendment (2026-07-26, G5a): the wall is real, the law is realer

Logged decision (proprietor's enthusiastic order): the City Gates panel
carries STATIC vector art — a stone wall, crenellations, central arch
with portcullis, the Sentinel standing watch — drawn in ~30 lines of
canvas primitives, responsive to width, no images, no dependencies.
Two laws bound it: §13 Law 1 (static, muted — scenery never spectacle)
and the new ART-IS-NEVER-A-CONTROL law, earned from this shop's own
A−/A+ canvas-button defect: decoration and interaction never share a
widget; everything clickable stays a real tk.Button. Gated in tests.

### §13 amendment (2026-07-26, G5b + G4a): the fuller castle + the Treasury

Logged decisions. G5b: the wall doubled down — flanking towers with
arrow slits, wooden gate behind the portcullis, subtle top-light on
the stone; still static, muted, never a control. G4a: the Money panel
is **💰 The Treasury** (window, header, interior door). The G4 quest
vocabulary, per the proprietor: the empire being grown is YOUR OWN
financial security and five-year plan; the invaders are creditors and
grocery runs — "keeping the wolves at bay," not fighting armies; a
bank errand is a supply run to town. Candidate hero vocabulary: "What
are your labors today?" (the proprietor's Theseus framing — and the
black-sail story is the canonical CHECKLIST-FAILURE parable: one
forgotten step, catastrophic cost; the shop's gates exist so finances
never fly a black sail). Law 4 stands over all of it: figures are
never softened — the game makes the truth pleasant, not vague.
(Money Hub / Time-vs-Money renames wait for G4 proper.)

### §13 amendment (2026-07-26): the Idea Collision wheel + the gate's biggest catch

Logged decision from the proprietor's polymathy research intake. The
clinical-science-gate REJECTED the intake document's fabricated
evidence (an unverifiable 2026 journal, hyper-precise effect sizes,
an implausible fMRI-plus-cortisol school study) — the fabrications
are named in the whitepaper notes as a teaching specimen. What
SURVIVED and shipped: Llull's Ars Magna combinatorial wheel as a pure
kernel (lyceum/idea_collision.py) behind the ⚡ Collide button on the
Glossary tab — draws two of the user's OWN studied concepts (glossary
terms + topic titles) and prompts the connection. Honest evidence
label: retrieval practice (strong support) + elaboration (moderate,
Dunlosky et al. 2013); NO neuro-training claims, ever. Also
recognized: the document's "Phase 5" (spaced repetition) has been in
production here since the SRS sprint — FSRS, append-only review log.
Rejected as scope creep: graph-database re-platform, neurodivergent
diagnostic profiling, TEKS compliance mapping (wrong product).

## 14. The cognitive-flow attachment point (parked design, 2026-07-27)

Intake from the proprietor's agentic-patterns research, gated. The
payload that survived: the app's information-processing spine is now
DOCUMENTED in the README (input → process → data → decide → external
knowledge → knowledge/output — the classic systems model), and future
agentic loops attach HERE, not ad hoc.

```text
PARKED KERNEL (ships only WITH its first consumer, per the dead-code
law — a doorway to nowhere is a defect, not a placeholder):

  lyceum/cognitive_flow.py
      FlowState: inputs · process_results · data_snapshot · decision ·
                 external_knowledge · knowledge · output
      pure nodes: process(state, fn) → decide(state, router) →
                  knowledge(state, writer)
      runner:    run_minimal_cycle(...) — headless, deterministic,
                 tested with temp_study_db like every kernel

ADMISSION CRITERIA (all three, in order):
  1. a scoped consumer exists (scope-first: in/out/acceptance/lifecycle)
  2. kernel + tests land green BEFORE any UI wiring (classroom-code)
  3. any behavioral claims pass clinical-science-gate; framing stays
     free of neuromyths (the intake document's left-brain/right-brain
     costume is a documented myth and was rejected on arrival — the
     payload was judged separately, which is the whole method)

Candidate first consumers: the §12 Phase B-D data carries; a
"morning briefing" loop over the grounding feed; the Vault Catalog.

### §13 amendment (2026-07-27): the Forged Draw + the light-board triage

The 'dendritic polymath / OmniCore' intake was triaged on a light
board: RED — knowledge-graph lattice (the same re-platform rejected
twice, renamed) and the undefined "audio-spatial map" (🔊 Read already
serves); YELLOW-parked — cluster-based SRS (the honest core is
INTERLEAVING, which has real evidence, but it needs the rejected graph
and would modify a validated FSRS scheduler that isn't broken);
GREEN, corrected and SHIPPED — the Forged Draw: completing an ⚡ Idea
Collision is a REAL completion, so its popup carries a one-shot
"⚒ Forged it — claim the draw" button wired to the existing
honesty-gated Reward engine (event 'idea-collision-forged'). No new
visuals (§13 Law 1); one claim per collision. Real science under the
intake's costume, named honestly in the glossary: spreading
activation (Collins & Loftus 1975) and structure-mapping (Gentner
1983) — the invented vocabulary (dendritic polymath, OmniCore,
quantum cognition, DSO-AIR) rejected as technobabble.

### §14 amendment (2026-07-27): the assistant reads associatively

The proprietor asked the right version of the question: not "should
the HUMAN learn dendritically" but "can the app's resident mind
ACQUIRE information associatively — as a tool, without harm?" Answer:
yes, and it shipped — one associative hop in the grounding retrieval
(lyceum/local_context.py): pseudo-relevance feedback (Rocchio;
Manning-Raghavan-Schütze IIR ch.9), the retrieval analogue of
spreading activation. First pass ranks; the best passages are mined
for RECURRING novel terms; every document is re-scored with original
terms at double weight plus the associations — so a note that never
says "quokka" is still reached through "marsupial." Pure kernel,
deterministic, literal mode preserved (associative=False), zero new
dependencies, assistant stays stateless. The gated verdict: this was
the honest core of three rejected graph-lattice pitches, delivered in
~40 lines on the existing kernel.
