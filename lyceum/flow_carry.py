"""Flow carry rules — Blueprint §12 Phase B, pure kernel.

The guided flow's law is NO RE-ENTRY: what the user wrote at one
station travels to the next. This module holds the pure carry rules;
the Tk shell only calls them. First rule shipped: goal → Matrix.
"""
from __future__ import annotations


def next_action(title: str, action_plan: str = "") -> tuple[str, bool]:
    """What a freshly saved goal carries into the Do-Now quadrant.

    The action plan's FIRST non-blank line wins (leading bullet
    characters stripped); the goal title stands in when no plan was
    written. Returns (text, used_step). ("", False) when both are
    blank — the caller must SAY so (silent declines are defects,
    shop law 3).
    """
    for line in (action_plan or "").splitlines():
        s = line.strip().strip("•-*·[] ").strip()
        if s:
            return s, True
    return (title or "").strip(), False
