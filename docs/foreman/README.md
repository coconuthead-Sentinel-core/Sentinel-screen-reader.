# The Foreman's Dashboard — a mirror in pseudocode

Stood up at the proprietor's order, 2026-07-25. The proprietor works in
the Sentinel Personal Development dashboard (Journal, Topics, Glossary,
Commentary, Library); the foreman works in THIS folder — the same five
sections, as plain markdown "pseudocode" files, versioned in git.

**Why files and not the app's study.db:** the live database is the
proprietor's personal data, and the shop's isolation law (twice paid
for — see Former-Bugs) forbids anything but the app writing it. The
foreman's mirror therefore lives as repo documents: same sections, same
discipline, different substrate. What the proprietor's dashboard does
with SQLite, this folder does with git.

**Mirroring:** because these are repo files, every commit → push →
pull cycle lands them on all four stations automatically (worktree,
GitHub, the laptop's live install, the OneDrive clone). The
proprietor's data syncs by OneDrive; the foreman's syncs by git.

| Section | File | The foreman uses it for |
|---|---|---|
| 📓 Journal | `JOURNAL.md` | dated work-cycle entries (triage, decisions, cycle results) |
| 📌 Topics | `TOPICS.md` | work streams — the Eisenhower-triaged queue lives here |
| 📒 Glossary | `GLOSSARY.md` | CS terms taught on the shop floor, with where they came up |
| 📑 Commentary | `COMMENTARY.md` | foreman's assessments and standing opinions, signed |
| 📚 Library | `LIBRARY.md` | catalog of the shop's own documents — where every record lives |
