# Former Bugs & Regressions

*A documented history of notable defects that were found and fixed, each named
with the computer-science concept behind it and the guard now in place. This is
deliberately framed the way a professor would: a bug is only "fixed" when you can
**name the failure mode** and **show what prevents its return**.*

Commit hashes are clickable into the repo. Reviewed 2026-06-27 against `aea48c8`.

---

## 1. Thread-safety race: the vanishing highlights
**Commit [`99950c3`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/99950c3) — "Thread Safety Fix"**

- **Symptom:** when the AI assistant auto-read its reply aloud, the brand-new
  follow-along highlights were cleared *instantly*.
- **Concept — race condition / shared mutable state across threads.** Two
  asynchronous flows touched the same highlight tags: the new read-aloud worker
  painting highlights, and a *previous* worker's teardown still in flight,
  clearing them. Because GUI state was being mutated from more than one timeline,
  order of execution was non-deterministic — a classic data race.
- **Fix & guard:** serialize the hand-off so a stale clear cannot run after a
  fresh paint, and route all highlight mutation through the UI thread via
  `root.after(...)`. See the **threading model** in
  [Architecture §3](Architecture.md#3-the-concurrency--threading-model). Related:
  [`e7ba4ae`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/e7ba4ae)
  made the auto-reader reuse `_ftb_read_toggle` directly so there is **one**
  highlight engine, not two competing code paths.

## 2. Off-by-one / stale index: unhighlighted AI responses
**Commit [`bcdcfdf`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/bcdcfdf) — "Fix tk.END usage…"**

- **Symptom:** AI responses appeared but were never highlighted.
- **Concept — boundary error against a moving target.** In a Tk `Text` widget,
  `tk.END` resolves to the *current* end of the buffer **at evaluation time**.
  The code captured `tk.END` and then wrote more text, so the saved index now
  pointed *before* the newly inserted response — the highlight range covered
  empty space. This is the GUI cousin of an off-by-one / TOCTOU (the index was
  valid when read, stale when used).
- **Fix & guard:** compute the highlight bounds from the actual inserted span
  rather than a pre-captured `tk.END`. Anchor indices to the text you just wrote,
  not to a sentinel that drifts.

## 3. Unhandled exception in an iteration loop: TTS halts after one chunk
**Commit [`85906f5`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/85906f5) — "Fix continuous TTS reading halting after a single chunk…"**

- **Symptom:** continuous read-aloud spoke the first sentence, then stopped.
- **Concept — an exception escaping a loop body terminates the loop.** Computing
  the next chunk's text-widget indices could raise `tk.TclError` (out-of-bounds
  indexing) on certain inputs; the unhandled exception broke out of the
  read loop, so iteration died after chunk one.
- **Fix & guard:** bounds-check before indexing and handle `TclError` inside the
  loop so a single bad chunk is skipped, not fatal. **Robustness principle:** a
  long-running loop over user data must treat a single malformed item as
  recoverable.

## 4. Parser/encoding error: newlines break text-to-speech
**Commit [`d0917be`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/d0917be) — "Fix text-to-speech parser error with newlines"**

- **Symptom:** passages containing newlines failed to speak.
- **Concept — unescaped control characters crossing a process/quoting boundary.**
  Text handed to the speech subprocess was not safely quoted/escaped, so embedded
  newlines corrupted the command the TTS engine parsed.
- **Fix & guard:** sanitize and safely quote text before it crosses the
  subprocess boundary (`_ps_single_quote` and friends). This is the same class of
  problem as injection — **never build a command string by naive concatenation of
  untrusted text.** It also motivated fix #5.

## 5. Command-line length limit (ARG_MAX)
**Commit [`8dca41d`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/8dca41d) — "Bypass command-line length limits using a temp file…"**

- **Symptom:** reading a large selection aloud failed outright.
- **Concept — OS limit on total command-line length.** Every operating system
  caps the size of a process's argument vector (Windows `CreateProcess` ≈ 32 KB
  for the command line). Passing a whole chapter as a CLI argument blew past it.
- **Fix & guard:** write the text to a **temporary file** and pass the *path* to
  the TTS engine. **Lesson:** bulk data belongs in a file or stdin pipe, never in
  `argv`.

## 6. Non-atomic deletes (ACID violation)
**Commit [`d92afb3`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/d92afb3) — "DB: add transaction() primitive; make parent/child deletes atomic"**

- **Symptom (latent):** several deletions ran as **two independently
  auto-committed statements**. A crash *between* them could orphan child rows or
  half-delete a record.
- **Concept — Atomicity, the 'A' in ACID.** A logical operation made of multiple
  statements must be **all-or-nothing**. Two separate auto-commits are two
  separate transactions, so the in-between state is observable and corruptible.
- **Fix & guard:** the `transaction()` context manager (commit on success,
  `ROLLBACK` on any exception) now wraps four parent/child delete units. Locked
  in by **`tests/test_transactions.py`**, which proves both halves: a clean unit
  persists *all* statements, and a mid-unit exception rolls back to **zero** rows.
  See [Database Schema](Database-Schema.md#the-transaction-primitive--acid-atomicity).

## 7. Syntax error in a `for…else` construct
**Commit [`d00ef47`](https://github.com/coconuthead-Sentinel-core/sentinel-forge-personal-development/commit/d00ef47) — "Fix syntax error in for-else loop"**

- **Concept — Python's `for…else` is widely misread.** The `else` runs when the
  loop completes **without `break`**, not "if the loop was empty." A
  misunderstanding here produced a syntax/logic error.
- **Guard:** the project now runs **`py_compile`** as a pre-commit smoke check so
  a syntax error can't reach `main` (the build paperwork records "py_compile
  clean" on the DB-atomicity commit).

---

## Cross-cutting lessons baked into the codebase

These recurring fixes hardened into standing rules — apply them to all new code:

1. **UI mutation only on the UI thread** (`root.after`); workers compute, they
   don't paint. *(bugs 1, 2)*
2. **Index against the text you actually wrote**, never a sentinel that moves.
   *(bug 2)*
3. **Loops over user data swallow per-item failures** and continue. *(bug 3)*
4. **Escape/quote everything crossing a process boundary**; bulk data goes in a
   file, not `argv`. *(bugs 4, 5)*
5. **Multi-statement DB work is atomic or it doesn't ship** — wrap it in
   `transaction()`. *(bug 6)*
6. **`py_compile` is the floor**; tests are the ceiling. *(bug 7)*

## How to add to this page

When you fix a bug, append an entry with: **symptom → named CS concept →
fix & guard → commit link**. If the bug was a logic error in the functional
core, add a **failing-then-passing unit test** and cite it here — that is what
turns "fixed" into "can't regress." See [Testing & QA](Testing-and-QA.md).


## July 2026 — the "silent sweep" regression batch

Three regression families traced to the post-v0.9 refactor commits
(`2f08bfb`..`8e70f8e`), all sharing one root pattern: **failures hidden
inside bare `except: pass`.**

1. **Save-widget sweep orphans.** A cleanup removed Save/Delete buttons
   project-wide but left the save functions with nothing calling them —
   7 dialogs (Scoreboard editor, V2MOM, Daily 10 Goals, Session-End
   handoff, Glossary editor, Goals worksheet, block dialogs) accepted
   typing and silently kept nothing. Fix: buttons restored; Daily 10
   also gained an in-window ✓ confirmation + auto-close (a save the
   user can't SEE reads as broken).
2. **Read-aloud silence.** Piper playback was swapped from stdlib
   `winsound` to `pyaudio` inside `except: pass`; PortAudio raises
   OSError -9999 on this hardware, so every read highlighted in
   silence. Fix: winsound restored (the stop paths still expected its
   `SND_PURGE`); playback errors now surface as error events.
3. **Constructor-tuple pady crashes.** Seven `tk.Label(..., pady=(12, 2))`
   constructor tuples (glossary editor, folder + time-block dialogs)
   raised `bad screen distance` and aborted those windows half-built —
   the codebase's oldest recurring trap, now swept project-wide.

**Standing lesson:** when the user says "X doesn't work," grep for a
swallowed exception near X first, and check `voice_debug.log` for
anything voice-related. And after any large pulled refactor, verify the
audio/UI paths **on the real hardware** before trusting them.

---

### 2026-07-12 — Study-panel UI sweep (two display bugs)

4. **A−/A+ scaled the navigation lists, not just the reading text.**
   `_apply_study_legibility` pushed the reading font size onto the
   Topics/Glossary/Commentary index **listboxes** as well as the read
   panes, so sizing text up enlarged the lists until their rows clipped
   off-screen and became unreadable — while the **Journal list never
   showed the bug because it was already exempt** from that loop. Fix:
   scale only the reading panes (`_glossary_definition_widget`,
   `commentary_area`); leave the four nav lists at a fixed, compact size.
5. **Delete-topic confirm dialog ballooned off-screen.** A topic whose
   *title* was a whole pasted AI reply was interpolated verbatim into
   `messagebox.askyesno("Delete topic?", …)`, so the modal grew tall
   enough to push its Yes/No buttons past the screen edge — leaving it
   "stuck open." Fix: collapse the title to a 60-char single-line preview
   before formatting the message.

**Standing lesson (added):** any user-supplied string interpolated into a
messagebox or a fixed-height widget must be length-capped — a title/name
field can hold an entire pasted document. And accessibility font-scaling
must target reading surfaces only, never navigation indexes.

### 2026-07-25 — Glossary entry dialog: no right-click paste

Owner QA (screenshot evidence): text copied in the Library could not be
pasted into a new Glossary entry — the dialog's Term and Definition
fields were the one input form that never received the app-wide
right-click clipboard menu. The Commentary entry dialog, written by
mirroring the glossary one, had mirrored the omission. Fix: attach the
existing `_attach_clipboard_menu` helper to all four widgets (standard
🧹 Clear included). Regression gate: `tests/test_clipboard_wiring.py`
statically asserts (ast scan, headless) that both dialog builders call
the helper at least twice — the wiring can no longer be dropped
silently. Lesson: a hand-applied cross-cutting affordance always leaves
a straggler, and copied dialogs copy omissions — gate the pattern, don't
trust the sweep.

### 2026-07-25 — Entry dialogs: pasted text had no way to be saved

Owner UAT of the same-day clipboard fix found the next link in the
chain broken: text pasted into the Glossary/Commentary Add dialogs
could not be committed. Three causes stacked: `grab_set()` froze the
floating toolbar (modal grab), the dialogs' own Save row was packed
after the expanding body so short windows clipped it off-screen
(probe: at 150px the button sat 70px past the edge), and the toolbar's
find-a-save-button fallback skipped all Toplevels while these dialogs
keep Save in a frame beside the field — the Toplevel being the only
shared ancestor. Fix: no grab, bottom-first button rows, fallback skips
only the root Tk (the <80-widget guard bounds the search). Lesson: a
workflow is only fixed when its LAST step works — QA the full path
(copy → paste → save), not the step that was reported; and pack button
rows bottom-first, always (the `_prompt_for_text` law, now gated in
`tests/test_clipboard_wiring.py`).

### 2026-07-25 — Green ➕ Add never reached the study sections

Third link in the same QA chain (paste → save → add): the toolbar's Add
dispatch had handlers for six panels but none for Topics, Glossary, or
Commentary — qa_debug.log had recorded `ftb-add: fell through` three
times across two days, a defect self-reporting in the breadcrumbs while
nobody read them. And the commit path for an open entry dialog relied
on a heuristic button search that missed in the field even after being
widened. Fix: the deterministic hook pattern — dialogs register their
save() as `_ftb_inline_input` while open; ➕ and 💾 both honor it; a
new `_study_add_from_toolbar` opens the right section's entry box when
nothing is open. Lessons: (1) read the breadcrumbs FIRST — the log had
the diagnosis before the ticket was filed; (2) when a heuristic misses
twice, stop widening it and replace it with explicit registration —
search is a guess, a hook is a contract.

### 2026-07-25 — Ghost tab: the workspace's memory outlived its window
(Caught in the foreman's self-audit, before the owner ever saw it.)
`_study_active_tab` persists after the Study workspace closes — the
window handle is nulled, the tab key is not — so any toolbar dispatch
keyed on the tab alone acts on a ghost. The day's new Add route would
have opened entry dialogs from anywhere in the app; the older save/
remove handlers survive only because touching a dead widget throws
TclError and they decline by accident. Fix: the Add route checks
`_study_win.winfo_exists()` first; the trap is written into
Rebuild-Blueprint §11 and gated in tests. Lesson: state that OUTLIVES
its owner is a memory, not a state — every consumer must check the
owner is alive, and "it works because it crashes quietly" is a bug
with good luck, not a design.

### 2026-07-25 — Topics undeletable: the selection was a single stolen token

The owner's clear-the-dashboard test stalled on Topics alone. Tk's
default `exportselection=1` exports a listbox's selection to the
app-wide selection token — one owner at a time — so clicking the
entries list or the compose pane silently deselected the chosen topic,
and the toolbar 🗑 declined on an empty `curselection()`. Topics, with
two listboxes plus a paste pane in one tab, was the most exposed
section. Companion defect: the delete confirms had no `parent=` and
could open behind the Study window, making Delete look dead. Fix:
`exportselection=False` on the four CRUD listboxes; parented confirms;
a real-Tk test demonstrating steal-vs-survive; static gates on both.
Lesson: a "nothing happened" bug is usually a PRECONDITION quietly
false (selection gone, dialog hidden) — instrument the decline path,
and never trust a 1980s default in a multi-pane UI.

### 2026-07-26/27 — The invisible skyline (invisible-state mark #10)

The owner restarted twice and reported the described mural absent; the
code was correct and the owner was correct — the VALUES were wrong.
Sky bands measured 1.17:1 against the window (invisible); the vignette
palette had been tuned against BG_DARK while its canvas sits on
BG_PANEL. Geometry probes counted shapes and passed; only the owner's
eyes could see contrast (shop Law 6, proven a second time). Fix:
palette lifted to named constants and re-tuned against the TRUE
canvas of each drawing; a computed contrast gate now measures every
mural color vs its actual background. Lesson: an artwork has a
precondition too — sufficient value separation — and "drawn" is not
"visible"; measure the light, not just the geometry.

## 2026-07-30 — the ghost tab default: `[init] study window build: 'reader'`

- **Symptom:** every app start printed `[init] study window build:
  'reader'` to stderr; the study window skipped its startup
  `withdraw()`; and `_show_study_tab` with the unknown key tore down
  every tab before crashing, leaving ZERO tabs packed. A second copy
  of the same defect hid in `_load_book`: it requested the removed
  Reader tab on every book open, swallowed by a bare `except` — a
  silent decline, on the books since the Reader was removed.
- **Concept — stale reference after refactor + validate-before-mutate
  (design-by-contract).** The Reader tab was removed from the tabs
  registry, but two call sites still requested the key. The dispatch
  mutated shared state (pack_forget on all tabs) BEFORE validating its
  precondition, so the failure landed mid-teardown — the worst place.
- **Fix & guard:** `_show_study_tab` validates the key FIRST; unknown
  keys breadcrumb to `qa_debug.log` and fall back to the first
  registered tab (Law 3: declines speak). Workspace build lands on
  `study_notes`; the dead Reader request in `_load_book` retired with
  a logged decline path. Guard: `tests/test_study_tab_contract.py` —
  four static gates (no call site may request "reader"; validation
  must precede teardown; the decline must breadcrumb; the default tab
  must exist in the registry). Smoke proves startup withdraw + bogus-
  key fallback under a real mainloop.

## 2026-07-30 (later) — the hidden workspace that owned every click

- **Symptom:** with the Study workspace closed (hidden), the floating
  toolbar's Save/Add/Remove could still be CLAIMED by study tabs —
  saving into invisible panes, popping dialogs from anywhere. And four
  claimed-context handlers swallowed real failures (`except: return
  False`), so a failed journal/notes/AAR action reported as "nothing
  to save here."
- **Concept — stale state as authority + exception swallowing.** The
  close handler WITHDRAWS the window (never destroys, by design), so
  `_study_active_tab` and its widgets outlive the visible window; a
  context test keyed on the tab alone treats a memory as a state
  (Blueprint §11). Swallowed exceptions convert "claimed and failed"
  into "unclaimed" — a category error that misroutes the chain.
- **Fix & guard:** one seam, `_study_workspace_visible()` (exists AND
  normal/zoomed; half-dead probes breadcrumb), fronting all five
  tab-based context tests and the add route. All claimed-context
  failures now `_qlog` + honest ⚠ status + stop the chain (Law 3).
  Gates: `tests/test_ftb_decline_gate.py` (line-based except-swallow
  scan), tab-claim scan in `test_study_tab_contract.py`, AST guard
  checks in `test_clipboard_wiring.py`. Lesson paid for en route: the
  first version of the decline gate used a backtracking-prone regex
  that spun for minutes on the 18k-line source — rewritten as a
  line-based scan; pattern-match complexity is part of a gate's
  design, too.
