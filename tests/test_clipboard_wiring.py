"""Regression gate: entry dialogs must carry the right-click clipboard menu.

Owner QA find (2026-07-25, screenshot evidence): the Glossary entry dialog's
Term and Definition fields had no right-click Cut/Copy/Paste menu, so a title
highlighted and copied in the Library could not be pasted into a new glossary
entry. The Commentary entry dialog mirrors that dialog and had mirrored the
missing menu too.

Pure static analysis (ast over the live app file, same approach as
test_designlaws) — no GUI needed, so the gate runs headless. It asserts that
each dialog builder calls self._attach_clipboard_menu at least twice: once for
the single-line title/term Entry, once for the scrolled body.

Run from the repo root:   python -m unittest discover -s tests
"""
import ast
import os
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_APP = os.path.join(_REPO, "sentinel_personal_development.py")


def _clipboard_menu_calls(func_name: str) -> int:
    """Count self._attach_clipboard_menu(...) calls inside ``func_name``."""
    with open(_APP, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return sum(
                1 for sub in ast.walk(node)
                if isinstance(sub, ast.Call)
                and isinstance(sub.func, ast.Attribute)
                and sub.func.attr == "_attach_clipboard_menu")
    raise AssertionError(f"{func_name} not found in app source")


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


if __name__ == "__main__":
    unittest.main()
