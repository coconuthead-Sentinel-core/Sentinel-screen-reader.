# AGENTS.md — orientation for coding agents

Read this first; it is short on purpose.

1. **Start at the README** — the section "⚑ For the desktop coding
   assistant — start here" is the canonical orientation, and the
   "Cognitive architecture" section is the system's map.
2. **The laws are not optional.** Before writing code, read the skills
   in `.claude/skills/`: `classroom-code` (SDLC stages, pseudocode
   before code, tests before UI), `scope-first` (no code without a
   scope statement), `shop-defect-laws` (breadcrumbs first, full-path
   QA, silent declines are defects, the Tk trap checklist),
   `clinical-science-gate` and `learning-science` (no unverified or
   neuromyth claims — ever).
3. **The records:** `CHANGELOG.md` (what changed) ·
   `docs/wiki/Shop-Punch-List.md` (what's open; defect-class tallies) ·
   `docs/wiki/Former-Bugs-and-Regressions.md` (what broke, with
   lessons) · `docs/wiki/Rebuild-Blueprint.md` (rebuildable pseudocode
   — the fourth source of truth) · `docs/foreman/` (the working
   dashboard of the resident agent).
4. **Tests:** `python -m unittest discover -s tests` from the repo
   root. The suite must be green before any merge; headless tests
   isolate the database via `lyceum.db.study_db.temp_study_db()` —
   NEVER touch the live `study.db`.
5. **Mirrors:** GitHub `main` is the central truth; the live install
   (`Desktop\Sentinel-Forge`) and the OneDrive clone pull after every
   push. A change isn't done until all stations match.
6. **New features** go through the `/sentinel-sprint` pipeline: pure
   kernel → headless tests green → UI wiring with visible feedback →
   real-screen verification → paperwork → mirror.
