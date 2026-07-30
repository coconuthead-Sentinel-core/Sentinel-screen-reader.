# Shop Punch List — the running ledger

Standing document, ordered by the proprietor 2026-07-25. Construction
vocabulary on purpose: a **punch list** is the trade's running record of
every item still open on a job, walked at each visit until every line is
struck. This one adds the classroom's discipline on top: every defect is
**classified**, classes are **tallied**, and a class that keeps recurring
gets a **🔴 red plum** — a standing order to stop patching instances and
trace the class to its origin. (The practice is textbook: defect
classification per IEEE 1044 plus trend analysis; the Former-Bugs page
is the *history*, this page is the *watch list*.)

**Foreman's duties on this page:** read it at every session start; add a
tally mark whenever a fix lands; strike lines when the owner's UAT
confirms; escalate any class reaching 3 marks to 🔴 and open a
trace-to-origin investigation as its own ticket.

---

## A. Defect-class tally (the red-plum board)

| Class | What it looks like | Marks | Status |
|---|---|---|---|
| Invisible state | control works but shows nothing (checkbox, meter, status — and now ART: drawn ≠ visible) | 10 (2026-07-27: the invisible skyline, values 1.17:1) | 🔴 red plum — standing design law: every action shows visible proof |
| Precondition quietly false | "button does nothing" because selection/focus/window silently invalid | 4 (2026-07-25: stolen selection, hidden confirm, ghost tab, empty curselection decline) | 🔴 red plum — decline paths must LOG (breadcrumb) and TELL (status line), never just return |
| Cross-cutting affordance missed | app-wide feature (clipboard menu, mic enrollment) skips one widget | 3 (glossary dialog, commentary dialog, earlier mic boxes) | 🔴 red plum — hand-applied sweeps always miss one; every sweep now ends with a static gate |
| Clipped/unreachable controls | last-packed rows starved off short windows; modal grabs freezing the toolbar | 3 (glossary row, commentary row, read-view row) | ⚠ watch — bottom-first law gated in tests |
| Heuristic where a contract belongs | search/guess dispatch missing in the field | 2 (find-a-save-button ×2 widenings) | ⚠ watch — rule: a second miss converts the heuristic to a registration |
| Stale lifetime (memory outlives owner) | `_study_active_tab` outliving its window | 1 (+ legacy handlers surviving by lucky TclError) | ⚠ watch — Blueprint §11 documents; sweep candidate below |

**Rule:** 3 marks = 🔴. A 🔴 class gets a named design law, a static gate
where possible, and its next occurrence is treated as a process failure,
not a code failure — the question becomes "why did the law not hold?"

## B. Open punch items (walk at every session)

**Eisenhower triage 2026-07-25** (working order in
`docs/foreman/TOPICS.md`): DO → #3 (executed). SCHEDULE → cycles: #5,
then #4, then #9-implementation (blocked on delegate), then v1.0 cut
(proprietor's word). DELEGATE → #8, #9-scope-call (Falcon One).
DEFER → #6, #7 (scope-first before any code).

**Eisenhower triage 2026-07-30** (proprietor's order: DO-now queue
cleared, promote the deferred/scheduled items in order of date and
importance): **DO, foreman** → 'reader' ghost-tab defect (green-lit,
executed same session), then #5 silent-declines sweep (oldest open
engineering item, red-plum law, first motion next session). **DO,
Falcon One** → #11 signs UAT + 'reader'-fix UAT; Recycle Bin click
(C: at ~4 GB free); then #10 SUS scorecard (oldest open owner item,
2026-07-26). **SCHEDULE** → #4 legacy-handler sweep (rides behind #5,
same seam family); `.aitk` 20 GB relocation to E: (awaits owner OK);
hub-window signage extension (scope call). **DELEGATE** → Q3
warehouse freight to E: after the owner's pruning pass (foreman);
Imprint archive-ledger paperwork (concept, scoped when called).
**DEFER** → #6 Vault Catalog, #7 script-export, imaging node,
CleanroomIntake benchmark (owner's want, optional). **DELETE** →
nothing; the archive law stands.

| # | Item | Origin | State |
|---|---|---|---|
| 1 | Owner UAT: full CRUD cycle on Topics after 68fb199 (delete topic+7 entries, add fresh, delete again) | 2026-07-25 ticket 4 | ~~STRUCK~~ — owner UAT ✅ 2026-07-25 ("read, saved, deleted, copied and pasted into every section") |
| 2 | Owner UAT: paste → ➕ Add lands entries in all three sections (b73a7cf flow) | 2026-07-25 ticket 3 | ~~STRUCK~~ — owner UAT ✅ 2026-07-25; Matrix + all three planners also UAT-passed with toolbar add/remove/mark-off |
| 3 | Read-only glossary view has no copy-out clipboard menu | 2026-07-25 audit | ~~STRUCK~~ — Eisenhower DO, executed 2026-07-25 (Copy + Select-all menu; gated) |
| 4 | Legacy save/remove handlers survive ghost-tab only via lucky TclError — sweep to explicit window checks | Blueprint §11 trap | OPEN — sweep candidate, gate exists for Add route only |
| 5 | Decline paths in `_ftb_action_*` chains: several return silently with neither breadcrumb nor status | red-plum class 2 | OPEN — instrument-the-decline sweep |
| 6 | Vault Catalog (optical/external media index): archive-set export + media catalog table in study.db | owner's 2026-07-25 optical-media intake | BACKLOG — scope-first + blueprint before any code |
| 7 | Script-export pipeline for narrated educational segments (notes/glossary → script text for outside video tools) | same intake | BACKLOG — idea only, no scope yet |
| 8 | E: drive verification (E: = the 1TB external backup HDD); ~~7 unmerged branches~~ | journal 2026-07-20 | HALF-STRUCK — branch verdict ✅ 2026-07-26: proprietor ordered delete; both remaining Copilot branches verified 0-unique-commits and deleted; GitHub = main only. E: half still OPEN (drive not mounted; plug in → foreman verifies) |
| 10 | SUS baseline (Law 7, A-grade doctrine): proprietor takes the 10-question scorecard cold against v1.0+F-series (`docs/foreman/SUS-SCORECARD.md`), re-measures after ~2-3 weeks of daily use; target ≥85, shortfalls reported as-is | proprietor's order 2026-07-26 | OPEN — awaiting first administration |
| 9 | AI assistant grounding gaps | owner status report 2026-07-25 | ~~STRUCK~~ — scope call ✅ 2026-07-26 (proprietor: ALL FOUR sections) and implemented same session: commentaries, topic-entry bodies, Matrix, Planner added to the grounding feed (lyceum/local_context.py); headless test seeds one row per section and proves retrieval |
| 11 | Room signs: universal pictogram + word signage per panel/window (AAC picture-board principle, ISO 7001 pictograms, recognition-over-recall; extends the shipped traffic-light design language; one shared header seam) | owner's 2026-07-29 intake; board `Claude AI\Portfolio\boards\2026-07-29_RoomSigns.md` | SHIPPED (owner green light same night) — kernel `lyceum/room_signs.py` + `_draw_room_sign` seam in the study-tab loop; all 8 study rooms signed; 14 tests + static gate; smoke 8/8; suite 520 green. AWAITING OWNER UAT to strike. Hub windows (Library, Money Hub, …) NOT yet signed — their title bars already carry pictogram+word; extension is a follow-up scope call |

## C. How a line moves

OPEN → owner UAT / foreman evidence → STRUCK (moved to Former-Bugs or
CHANGELOG with its lesson) — or → BACKLOG (wanted, not scoped) — or
→ 🔴 investigation (recurrence traced to origin; outcome is a design
law + gate). Nothing is deleted from this page; struck lines move to
the history pages. The ledger is the memory; the red plums are the
alarm.
