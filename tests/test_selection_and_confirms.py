"""Regression gates: CRUD listbox selections survive; confirms stay on top.

Owner QA (2026-07-25): the Topics section could not be cleared — the last
section blocking a fully empty dashboard. Root cause: Tk's default
``exportselection=1`` makes the application's selection a SINGLE token, so
clicking any other selectable widget (the entries list, the compose pane)
silently deselected the topic, and the toolbar 🗑 found ``curselection()``
empty and declined. Second defect: the delete confirms had no ``parent=``,
so they could open behind the Study workspace window and look like a dead
button.

Two kinds of proof here:
  * static ast gates over the live app file (headless, same approach as
    test_designlaws) locking the exportselection flag and confirm parenting;
  * a real-Tk demonstration (withdrawn root via gui_base) that the flag is
    what makes two listbox selections coexist — the mechanism, on the
    actual platform.

Run from the repo root:   python -m unittest discover -s tests
"""
import ast
import os
import unittest

from gui_base import GuiTestCase

try:
    import tkinter as tk
except Exception:                     # pragma: no cover
    tk = None

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_APP = os.path.join(_REPO, "sentinel_personal_development.py")

_TREE = None

_CRUD_LISTBOXES = ("_topics_listbox", "_topic_entries_listbox",
                   "_glossary_listbox", "_commentary_listbox")


def _app_tree() -> ast.Module:
    global _TREE
    if _TREE is None:
        with open(_APP, encoding="utf-8") as f:
            _TREE = ast.parse(f.read())
    return _TREE


def _listbox_ctor_keywords(attr_name: str) -> set:
    """Keyword names on the tk.Listbox(...) call assigned to self.<attr>."""
    for node in ast.walk(_app_tree()):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Attribute) and t.attr == attr_name
                   for t in node.targets):
            continue
        if isinstance(node.value, ast.Call):
            return {k.arg for k in node.value.keywords}
    raise AssertionError(f"assignment of {attr_name} = tk.Listbox(...) "
                         "not found in app source")


def _askyesno_keywords(func_name: str) -> set:
    """Keyword names on messagebox.askyesno(...) inside ``func_name``."""
    for node in ast.walk(_app_tree()):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call)
                        and isinstance(sub.func, ast.Attribute)
                        and sub.func.attr == "askyesno"):
                    return {k.arg for k in sub.keywords}
            raise AssertionError(f"no askyesno call in {func_name}")
    raise AssertionError(f"{func_name} not found in app source")


class CrudSelectionGateTest(unittest.TestCase):
    def test_crud_listboxes_keep_their_selection(self):
        if not os.path.exists(_APP):
            self.skipTest("app file not found")
        for name in _CRUD_LISTBOXES:
            self.assertIn(
                "exportselection", _listbox_ctor_keywords(name),
                f"{name} lost exportselection=False — clicking another "
                "widget will steal its selection and toolbar 🗑 will "
                "decline with nothing selected")

    def test_topic_delete_confirms_are_parented(self):
        if not os.path.exists(_APP):
            self.skipTest("app file not found")
        for fn in ("_delete_selected_topic", "_delete_topic_entry"):
            self.assertIn(
                "parent", _askyesno_keywords(fn),
                f"{fn}'s confirm lost parent= — it can open behind the "
                "Study workspace and the delete looks dead")


class ExportSelectionMechanismTest(GuiTestCase):
    """Real-Tk proof of WHY the flag matters: with the default, selecting
    in the second listbox steals the first's selection; with
    exportselection=False both selections coexist."""

    def _pair(self, export: bool):
        a = tk.Listbox(self.root, exportselection=export)
        b = tk.Listbox(self.root, exportselection=export)
        for lb in (a, b):
            lb.insert(tk.END, "row0", "row1")
        return a, b

    def test_default_steals_the_selection(self):
        a, b = self._pair(export=True)
        a.selection_set(0)
        b.selection_set(1)     # exporting: this takes the selection token
        self.root.update()
        self.assertEqual(a.curselection(), (),
                         "expected the default to steal listbox A's "
                         "selection — platform behavior changed?")

    def test_flag_keeps_both_selections(self):
        a, b = self._pair(export=False)
        a.selection_set(0)
        b.selection_set(1)
        self.root.update()
        self.assertEqual(a.curselection(), (0,))
        self.assertEqual(b.curselection(), (1,))


if __name__ == "__main__":
    unittest.main()
