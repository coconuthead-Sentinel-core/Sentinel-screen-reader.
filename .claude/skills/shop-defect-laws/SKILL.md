---
name: shop-defect-laws
description: The ledger-earned defect-prevention laws for ALL Sentinel's Forge work — read the breadcrumbs before diagnosing, QA the user's full path not the reported step, silent declines are defects, a heuristic that misses twice becomes a contract, every cross-cutting sweep ends with a static gate, and the Tk platform-trap checklist runs before any UI change ships. Use when diagnosing ANY reported defect, before shipping ANY Tk/UI change, and whenever a fix that was "done" misses again in the field.
---

# Shop Defect Laws — earned on the ledger, kept as law

Permanent guardrail, authorized by the proprietor 2026-07-25 after a
six-defect QA day whose classes were already tallied red on the punch
list. Each law below exists because its absence was PAID FOR at least
twice — origins cited so the law can be challenged against its
evidence (Disputatio applies). Textbook anchors: defensive
programming, fail-fast/fail-loud, design-by-contract, regression
gates. The running tally lives in `docs/wiki/Shop-Punch-List.md`;
history in `docs/wiki/Former-Bugs-and-Regressions.md`.

## Law 1 — Breadcrumbs before diagnosis

Before theorizing about any reported defect, READ the instrumentation
(`qa_debug.log` and kin). The log has held the diagnosis before the
ticket was even filed (`ftb-add: fell through` ×3 across two days,
2026-07-25). A diagnosis formed before reading the breadcrumbs is a
guess wearing a coat.

## Law 2 — QA the full path, not the reported step

A defect report names the step where the user STOPPED, not the only
broken step. Defects queue along a workflow: fixing paste exposed a
dead save; fixing save exposed a dead add (three round-trips,
2026-07-25). Before declaring a fix done, walk the user's entire
journey — copy → paste → commit → verify it landed — and test the
destination, not the doorway.

## Law 3 — A silent decline is a defect

Any handler that declines to act must BREADCRUMB (log why) and TELL
(status line). "The button does nothing" has meant, every single time,
a precondition quietly false underneath a working button: stolen
listbox selection, confirm dialog opening behind the window, ghost
tab, empty curselection (red-plum class, 4 marks in one day). Declines
that speak turn a mystery into a one-line read.

## Law 4 — The second miss converts a heuristic into a contract

A search/guess dispatch (find-a-button, walk-the-tree) that misses
twice in the field is not widened a third time — it is REPLACED with
explicit registration (the `_ftb_inline_input` hook pattern: the open
window registers its own commit; the toolbar honors the hook).
A search is a guess; a hook is a contract. Design-by-contract beats
heuristics wherever the code can simply be told the truth.

## Law 5 — Every sweep ends with a gate

A cross-cutting, hand-applied change (a menu on every field, mic
enrollment, a style rule) ALWAYS leaves a straggler, and a copied
widget copies the omission (glossary dialog missed, commentary
mirrored the miss; mic boxes before that — 3 marks). Therefore no
sweep is complete until a static gate (ast scan over the live source,
`test_designlaws` style) asserts the pattern everywhere it must hold.
The gate, not the memory to be careful, is the deliverable.

## Law 6 — The Tk trap checklist (run before ANY UI change ships)

Platform defaults encode another era's assumptions. Check every one
that applies; each has already cost a ticket:

- **exportselection**: Tk's default makes ALL listbox selections one
  mutually-exclusive token — any CRUD listbox needs
  `exportselection=False` or neighboring clicks steal the selection.
- **Pack order**: Tk starves the LAST-packed widget first. Button rows
  pack BOTTOM-FIRST, before the expanding body — `side=tk.BOTTOM`
  alone does not save a row packed last (row clipped 70px off-screen).
- **grab_set**: a modal grab freezes every other window including the
  floating toolbar. No grab on windows the toolbar must serve.
- **Dialog parenting**: every messagebox/Toplevel gets `parent=` (the
  owning window, e.g. `self._study_win or self.root`) or it can open
  BEHIND the workspace and look like a dead button.
- **State lifetime**: state that outlives its owner window
  (`_study_active_tab` after close) is a memory, not a state — every
  consumer must verify the owner exists (`winfo_exists()`), and
  "survives via lucky TclError" counts as a bug with good luck.
- **bindtags on Destroy**: a `<Destroy>` binding on a Toplevel fires
  for every child too — handlers must be idempotent/identity-guarded.
- **Headless probes can lie**: a probe passing without a real display
  has coexisted with real clicks failing (the A−/A+ Canvas). UI paths
  are verified on the real screen — the owner's UAT is the lab result.
- **Entry vs Text API**: they differ (`select_all` died silently on
  Entries once); helpers touching "any input widget" must dispatch on
  widget class and be tested on both.

## Enforcement

These laws bind alongside `classroom-code` (which governs stages and
honesty) — on conflict the stricter rule wins. Fix reports cite which
laws were applied. A law that blocks legitimate work is challenged in
Disputatio and amended on the record — never silently skipped.
