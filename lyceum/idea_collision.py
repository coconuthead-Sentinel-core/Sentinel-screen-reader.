"""Idea Collision — Llull's wheel as a pure kernel.

Ramon Llull's Ars Magna (13th c.) generated insight by mechanically
combining concepts from rotating discs; Leibniz formalized the idea in
De arte combinatoria (1666). The honest modern evidence label is
NOT "trains your neural wiring" — it is retrieval practice plus
elaboration: recalling two studied concepts and generating the
connection between them (Dunlosky et al. 2013 rate elaborative
interrogation moderate; retrieval practice and spacing high).

Pure logic, no UI, no DB: the shell passes in the concept list and an
optional rng for deterministic tests.
"""
from __future__ import annotations

import random


def draw_collision(items: list[str], rng: random.Random | None = None):
    """Pick two DISTINCT concepts and build the collision prompt.

    Returns (a, b, prompt) or None when fewer than two distinct
    concepts exist (the caller must SAY so — silent declines are
    defects, shop law 3).
    """
    distinct = sorted({(s or "").strip() for s in items if (s or "").strip()})
    if len(distinct) < 2:
        return None
    r = rng or random
    a, b = r.sample(distinct, 2)
    prompt = (
        f"⚡ IDEA COLLISION — Llull's wheel has turned.\n\n"
        f"Concept one: {a}\n"
        f"Concept two: {b}\n\n"
        "From memory first (no looking back): what does each one mean?\n"
        "Then forge the link — in 2-4 plain sentences, how could these "
        "two connect, combine, or collide into one idea?\n\n"
        "Write the result as a Topic entry, a Commentary, or explain it "
        "aloud to the AI chat (the Feynman check: if you need jargon, "
        "you found a gap — go re-read that concept)."
    )
    return a, b, prompt
