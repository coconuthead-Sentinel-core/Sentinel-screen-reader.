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


def count_do_items(body: str) -> int:
    """§12 Phase D: open items in a Do-Now quadrant body — the bullet
    lines ('•' or unchecked '[ ]'), never source/timestamp lines and
    never checked-off '[x]' lines."""
    n = 0
    for ln in (body or "").splitlines():
        s = ln.strip()
        if s.startswith("•") or s.startswith("[ ]"):
            n += 1
    return n


def session_briefing(tasks, do_count: int = 0) -> str:
    """§12 Phase D: the loaded-plan summary at the flow's end.

    ``tasks``: iterable of (title, done) for today, in list order.
    Returns the briefing text; an empty plan SPEAKS (law 3) instead of
    rendering blank.
    """
    items = [((t or "").strip(), bool(d)) for t, d in tasks
             if (t or "").strip()]
    if not items and do_count <= 0:
        return ("🛡 The plan is empty — enter through a gate to load "
                "today, or begin freely.")
    open_n = sum(1 for _t, d in items if not d)
    lines = [f"⚔ Today's march — {open_n} open task"
             f"{'' if open_n == 1 else 's'}"
             + (f" (of {len(items)})" if len(items) != open_n else "")
             + ":"]
    for t, d in items[:6]:
        lines.append(f"   {'✔' if d else '▫'} {t}")
    if len(items) > 6:
        lines.append(f"   … and {len(items) - 6} more")
    if do_count > 0:
        lines.append(f"🎯 Do Now holds {do_count} item"
                     f"{'' if do_count == 1 else 's'}.")
    lines.append("🛡 The Sentinel walks with you — Begin when ready.")
    return "\n".join(lines)


def is_duplicate_task(existing_titles, candidate: str) -> bool:
    """Case- and whitespace-insensitive dedupe against a day's task
    list — the carry must never double a day by re-saving. An empty
    candidate counts as a duplicate (there is nothing to add)."""
    key = " ".join((candidate or "").lower().split())
    if not key:
        return True
    return any(" ".join((t or "").lower().split()) == key
               for t in existing_titles)
