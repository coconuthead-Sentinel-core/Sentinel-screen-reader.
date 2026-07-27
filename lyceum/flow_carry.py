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


def planner_task_title(carry: str, title: str, used_step: bool) -> str:
    """§12 Phase C: the line the flow carries onto TODAY's planner.

    Mirrors the Goals panel's calendar idiom (``🎯 goal: step``) so the
    two paths read identically in the day list. Returns "" when there
    is nothing to carry (caller says so — law 3).
    """
    c = (carry or "").strip()
    t = (title or "").strip()
    if not c:
        return ""
    if used_step and t:
        return f"🎯 {t}: {c}"
    return f"🎯 {c}"


def is_duplicate_task(existing_titles, candidate: str) -> bool:
    """Case- and whitespace-insensitive dedupe against a day's task
    list — the carry must never double a day by re-saving. An empty
    candidate counts as a duplicate (there is nothing to add)."""
    key = " ".join((candidate or "").lower().split())
    if not key:
        return True
    return any(" ".join((t or "").lower().split()) == key
               for t in existing_titles)
