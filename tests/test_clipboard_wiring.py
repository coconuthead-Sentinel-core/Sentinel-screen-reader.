"""Regression gates: entry dialogs must be paste-able AND save-able.

Owner QA finds (2026-07-25, screenshot evidence), one session, two tickets:

1. The Glossary entry dialog's Term and Definition fields had no right-click
   Cut/Copy/Paste menu, so a title copied in the Library could not be pasted
   in. The Commentary entry dialog mirrors that dialog and mirrored the miss.
2. Once pasted, the text could not be SAVED: (a) grab_set() made the dialogs
   modal, freezing the floating toolbar's yellow 💾 Save; (b) the dialog's own
   Save row was packed AFTER the expanding body, so Tk starved it first and a
   short window clipped it off-screen; (c) the toolbar's find-a-save-button
   fallback skipped every Toplevel ancestor, and the dialogs keep 💾 Save in
   a frame BESIDE the text field, making it unreachable.

Pure static analysis (ast over the live app file, same approach as
test_designlaws) — no GUI needed, so the gates run headless.

Run from the repo root:   python -m unittest discover -s tests
"""
import ast
import os
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_APP = os.path.join(_REPO, "sentinel_personal_development.py")

_TREE = None


def _app_tree() -> ast.Module:
    global _TREE
    if _TREE is None:
        with open(_APP, encoding="utf-8") as f:
            _TREE = ast.parse(f.read())
    return _TREE


def _find_func(func_name: str) -> ast.FunctionDef:
    for node in ast.walk(_app_tree()):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    raise AssertionError(f"{func_name} not found in app source")


def _clipboard_menu_calls(func_name: str) -> int:
    """Count self._attach_clipboard_menu(...) calls inside ``func_name``."""
    return sum(
        1 for sub in ast.walk(_find_func(func_name))
        if isinstance(sub, ast.Call)
        and isinstance(sub.func, ast.Attribute)
        and sub.func.attr == "_attach_clipboard_menu")


def _calls_in(func_name: str, method: str) -> list:
    """All ``<anything>.<method>(...)`` Call nodes inside ``func_name``."""
    return [sub for sub in ast.walk(_find_func(func_name))
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and sub.func.attr == method]


def _pack_line(func_name: str, receiver: str) -> int:
    """Line number of ``<receiver>.pack(...)`` inside ``func_name``."""
    for call in _calls_in(func_name, "pack"):
        v = call.func.value
        if isinstance(v, ast.Name) and v.id == receiver:
            return call.lineno
    raise AssertionError(f"{receiver}.pack(...) not found in {func_name}")


class EntryDialogClipboardTest(unittest.TestCase):
    def test_glossary_entry_dialog_has_clipboard_menus(self):
        if not os.path.exists(_APP):
            self.skipTest("app file not found")
        self.assertGreaterEqual(
            _clipboard_menu_calls("_edit_glossary_entry"), 2,
            "Glossary entry dialog lost its right-click clipboard menus "
            "(Term + Definition must each get _attach_clipboard_menu)")

    def test_commentary_entry_dialog_has_clipboard_menus(self):
        if not os.path.exists(_APP):
            self.skipTest("app file not found")
        self.assertGreaterEqual(
            _clipboard_menu_calls("_edit_commentary_entry"), 2,
            "Commentary entry dialog lost its right-click clipboard menus "
            "(Title + Commentary must each get _attach_clipboard_menu)")


class EntryDialogSaveReachableTest(unittest.TestCase):
    """The 2026-07-25 'stuck with no way to save' gates."""

    _EDITORS = ("_edit_glossary_entry", "_edit_commentary_entry")

    def test_editors_are_not_modal(self):
        """grab_set() freezes the floating toolbar — banned in the entry
        dialogs so the yellow 💾 Save stays clickable."""
        for fn in self._EDITORS:
            self.assertEqual(
                _calls_in(fn, "grab_set"), [],
                f"{fn} regained grab_set() — the floating toolbar's Save "
                "cannot be clicked while a grab is held")

    def test_button_row_packs_before_the_body(self):
        """Tk starves the LAST-packed widget first: the Save/Close row must
        pack (side=BOTTOM) before the expanding body, or a short window
        clips the buttons off-screen."""
        for fn, body_name in (("_edit_glossary_entry", "body"),
                              ("_edit_commentary_entry", "body_w"),
                              ("_show_glossary_entry", "body")):
            self.assertLess(
                _pack_line(fn, "row"), _pack_line(fn, body_name),
                f"{fn}: the button row packs after the body again — a short "
                "window will clip the buttons off-screen")

    def test_toolbar_fallback_searches_toplevel_dialogs(self):
        """_ftb_invoke_context_button must not skip Toplevel ancestors:
        the entry dialogs keep 💾 Save in a frame BESIDE the text field,
        so the Toplevel is the only shared ancestor. (The descendant-count
        guard is what keeps big windows out — not a Toplevel skip.)"""
        fn = _find_func("_ftb_invoke_context_button")
        toplevel_refs = [n for n in ast.walk(fn)
                         if isinstance(n, ast.Attribute)
                         and n.attr == "Toplevel"]
        self.assertEqual(
            toplevel_refs, [],
            "_ftb_invoke_context_button skips Toplevels again — dialog "
            "Save buttons become unreachable from the floating toolbar")


if __name__ == "__main__":
    unittest.main()
