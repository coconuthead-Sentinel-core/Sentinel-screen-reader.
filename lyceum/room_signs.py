"""Room signs — the universal signage registry (punch item #11).

Every room in the house shows one sign: a pictogram AND a word,
always together (AAC picture-board principle; ISO 7001-style public
pictograms; the recognition-over-recall heuristic). One controlled
registry so a symbol never means two different things. Pure data plus
checks — no Tkinter, no I/O.
"""
from __future__ import annotations

from typing import NamedTuple


class Sign(NamedTuple):
    pictogram: str   # the picture half (may be a small symbol cluster)
    word: str        # the word half, uppercase like road signage


# room_id -> Sign. The registry is the single source of truth: the
# shell's _draw_room_sign() looks up here and nowhere else.
SIGNS: dict[str, Sign] = {
    "study_notes": Sign("📝", "STUDY NOTES"),
    "ai_chat":     Sign("🤖", "AI CHAT"),
    "topics":      Sign("📌", "TOPICS"),
    "glossary":    Sign("📒", "GLOSSARY"),
    "commentary":  Sign("📑", "COMMENTARY"),
    "journal":     Sign("📅", "JOURNAL"),
    # The proprietor's card: triangle DO, clock SCHEDULE, tools
    # DELEGATE, X DELETE — the four quadrants ride under the big word.
    "matrix":      Sign("△ ⏱ ⚒ ✕", "PRIORITY MATRIX"),
    "planner":     Sign("🗓", "PLANNER"),
}


def get_sign(room_id: str) -> Sign:
    """Return the sign for a room. KeyError means an unsigned room —
    the caller must breadcrumb it, never swallow it silently."""
    return SIGNS[room_id]


def validate(signs: dict[str, Sign] | None = None) -> list[str]:
    """Check the registry. Returns a list of defect strings; an empty
    list means every sign is fit to hang."""
    if signs is None:
        signs = SIGNS
    defects: list[str] = []
    seen_pictograms: dict[str, str] = {}
    seen_words: dict[str, str] = {}
    for room_id, sign in signs.items():
        if not room_id.strip():
            defects.append("empty room_id")
        if not sign.pictogram.strip():
            defects.append(f"{room_id}: sign has no pictogram")
        if not sign.word.strip():
            defects.append(f"{room_id}: sign has no word")
        elif sign.word != sign.word.upper():
            defects.append(f"{room_id}: word not uppercase signage")
        if sign.pictogram in seen_pictograms:
            defects.append(
                f"{room_id}: pictogram already means "
                f"{seen_pictograms[sign.pictogram]!r}")
        else:
            seen_pictograms[sign.pictogram] = room_id
        if sign.word in seen_words:
            defects.append(
                f"{room_id}: word already used by "
                f"{seen_words[sign.word]!r}")
        else:
            seen_words[sign.word] = room_id
    return defects
