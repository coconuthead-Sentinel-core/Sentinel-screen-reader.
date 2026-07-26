"""Gates for finish-out F1 (2026-07-26): Wheel of Life colored area buttons.

Owner accessibility QA: each life area is a colored button (color-coding
aids scanning and cuts text-decoding load; color is never the only
signal — icon + word remain), and clicking it lands on a fresh Goals
worksheet with that area preselected so nothing is re-typed.

Static ast gates over the live app file plus a computed WCAG contrast
check: every area color must hold >= 4.5:1 against the white bold
button text (WCAG 2.1 AA for normal-size text), so a future palette
tweak cannot quietly break readability.

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


def _class_dict_literal(attr_name: str) -> dict:
    """Extract a class-level  NAME = {str: str}  literal from the app."""
    for node in ast.walk(_app_tree()):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == attr_name
                for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{attr_name} not found in app source")


def _class_list_literal(attr_name: str) -> list:
    for node in ast.walk(_app_tree()):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == attr_name
                for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{attr_name} not found in app source")


def _func_consts(func_name: str) -> set:
    for node in ast.walk(_app_tree()):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return {n.value for n in ast.walk(node)
                    if isinstance(n, ast.Constant)
                    and isinstance(n.value, str)}
    raise AssertionError(f"{func_name} not found in app source")


def _rel_luminance(hex_color: str) -> float:
    """WCAG 2.1 relative luminance of an #rrggbb color."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def chan(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast_vs_white(hex_color: str) -> float:
    lum = _rel_luminance(hex_color)
    return (1.0 + 0.05) / (lum + 0.05)


class WheelAreaButtonGateTest(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(_APP):
            self.skipTest("app file not found")

    def test_every_area_has_a_color(self):
        areas = {k for k, _ in _class_list_literal("_WHEEL_AREAS")}
        colors = _class_dict_literal("_WHEEL_AREA_COLORS")
        self.assertEqual(areas, set(colors.keys()),
                         "_WHEEL_AREA_COLORS keys must match _WHEEL_AREAS")

    def test_colors_meet_wcag_aa_against_white_text(self):
        for key, color in _class_dict_literal("_WHEEL_AREA_COLORS").items():
            self.assertRegex(color, r"^#[0-9a-fA-F]{6}$",
                             f"{key}: not an #rrggbb color")
            ratio = _contrast_vs_white(color)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"{key} color {color} has contrast {ratio:.2f}:1 vs white "
                "text — WCAG AA needs 4.5:1; pick a darker shade")

    def test_goals_area_is_a_colored_badge_not_a_dropdown(self):
        """F2: the Goals worksheet's life area renders as a colored badge
        (Menubutton painted from _WHEEL_AREA_COLORS, repainted on every
        area change) — not an always-open OptionMenu of 7 alternatives."""
        fn = None
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_goals_panel":
                fn = node
        self.assertIsNotNone(fn)
        attrs = {n.attr for n in ast.walk(fn)
                 if isinstance(n, ast.Attribute)}
        self.assertIn("_WHEEL_AREA_COLORS", attrs,
                      "goals area badge no longer painted from the "
                      "area color map")
        self.assertIn("Menubutton", attrs,
                      "goals area badge (Menubutton) is gone")
        self.assertIn("trace_add", attrs,
                      "badge no longer repaints when the area changes")

    def test_wheel_buttons_wired_to_goals_prefill(self):
        wheel = _func_consts("_build_wheel_panel")
        self.assertIn("_zz_prefill_goal_area", wheel,
                      "wheel area buttons no longer reach the Goals prefill")
        goals_assigns = False
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_goals_panel":
                goals_assigns = any(
                    isinstance(n, ast.Assign) and any(
                        isinstance(t, ast.Attribute)
                        and t.attr == "_zz_prefill_goal_area"
                        for t in n.targets)
                    for n in ast.walk(node))
        self.assertTrue(goals_assigns,
                        "_build_goals_panel no longer registers the "
                        "area-prefill hook")


if __name__ == "__main__":
    unittest.main()
