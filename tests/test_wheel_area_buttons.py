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

    def test_front_door_wheel_tab(self):
        """F3 Phase A (Blueprint §12): the Session window opens on the
        Wheel, the wheel tab wears its own identity color (also WCAG AA
        vs white), and a fresh goal's save advances the flow to the
        Matrix."""
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "_WHEEL_TAB_COLOR"
                    for t in node.targets):
                color = ast.literal_eval(node.value)
                break
        else:
            self.fail("_WHEEL_TAB_COLOR missing — the front door lost "
                      "its identity color")
        self.assertGreaterEqual(
            _contrast_vs_white(color), 4.5,
            f"wheel tab color {color} fails WCAG AA vs white text")
        areas = _class_dict_literal("_WHEEL_AREA_COLORS")
        self.assertNotIn(color, areas.values(),
                         "front-door color must be distinct from every "
                         "area color")
        ss = _func_consts("_build_session_start_panel")
        self.assertIn("wheel", ss)
        goals = None
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_goals_panel":
                goals = {n.attr for n in ast.walk(node)
                         if isinstance(n, ast.Attribute)}
        self.assertIn("open_study_workspace", goals,
                      "Save-goal no longer advances the flow to the Matrix")
        self.assertIn("_show_study_tab", goals)

    def test_mural_palette_visible_on_its_canvas(self):
        """G5i (owner QA 2026-07-26): the skyline rendered INVISIBLE on
        the real display — sky bands measured 1.17:1 vs the window and
        the vignette was tuned against the wrong background. Art values
        are now measured: structures hold ~3:1 vs their actual canvas
        (WCAG 1.4.11 spirit), atmospheric sky stays hazy but >= 1.5:1,
        and shadow accents keep separation from the stone they sit on.
        Headless probes cannot see contrast; this gate can."""
        BG_DARK, BG_PANEL = "#0f172a", "#1e293b"

        def cr(a, b):
            la, lb = _rel_luminance(a), _rel_luminance(b)
            hi, lo = max(la, lb), min(la, lb)
            return (hi + 0.05) / (lo + 0.05)
        wall = _class_dict_literal("_WALL_PALETTE")
        mins = {"sky_lo": 1.5, "sky_hi": 1.6, "haze": 2.8,
                "haze2": 3.0, "domec": 3.0, "stone": 2.8,
                "lite": 3.5, "wood": 2.4, "gold": 3.5}
        for key, m in mins.items():
            self.assertGreaterEqual(
                cr(wall[key], BG_DARK), m,
                f"wall '{key}' {wall[key]} fades below {m}:1 vs the "
                "dark canvas — invisible-art regression")
        self.assertGreaterEqual(cr(wall["stone"], wall["edge"]), 1.7,
                                "gatehouse no longer reads darker than "
                                "the wall around it")
        self.assertGreaterEqual(cr(wall["stone"], wall["dark"]), 1.3,
                                "mortar lines vanish into the stone")
        for key, color in _class_dict_literal(
                "_VIGNETTE_PALETTE").items():
            self.assertGreaterEqual(
                cr(color, BG_PANEL), 1.55,
                f"vignette '{key}' {color} fades below 1.55:1 vs the "
                "PANEL background it actually sits on")

    def test_city_wall_art_is_never_a_control(self):
        """G5a: the drawn city wall is decoration ONLY — no click
        bindings on the art canvas. The shop's own ledger (A−/A+
        canvas buttons dropping clicks) is why: controls stay real
        tk.Buttons, art stays art."""
        fn = None
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_wheel_panel":
                fn = node
        self.assertIsNotNone(fn)
        names = {n.name for n in ast.walk(fn)
                 if isinstance(n, ast.FunctionDef)}
        self.assertIn("_draw_city_wall", names,
                      "the city wall art is gone from the gates panel")
        self.assertIn("_draw_city_proper", names,
                      "the city-proper vignette is gone from the header")
        consts = {n.value for n in ast.walk(fn)
                  if isinstance(n, ast.Constant)
                  and isinstance(n.value, str)}
        for click in ("<Button-1>", "<ButtonPress-1>", "<Double-Button-1>"):
            self.assertNotIn(click, consts,
                             "a click binding appeared in the gates "
                             "panel — art must never be a control")

    def test_color_law_red_reserved_and_doors_distinct(self):
        """F6: red means stop/delete ONLY — no room or door identity may
        be red-family (a red Study door said 'stop' beside the red 🗑 in
        the same window). The three door colors must be mutually
        distinct and hold WCAG AA contrast vs their white text."""
        def _class_str(attr):
            for node in ast.walk(_app_tree()):
                if isinstance(node, ast.Assign) and any(
                        isinstance(t, ast.Name) and t.id == attr
                        for t in node.targets):
                    return ast.literal_eval(node.value)
            self.fail(f"{attr} missing")
        doors = {k: _class_str(k) for k in
                 ("_WHEEL_TAB_COLOR", "_TRACK_TAB_COLOR",
                  "_STUDY_TAB_COLOR")}
        self.assertEqual(len(set(doors.values())), 3,
                         "door identity colors must be mutually distinct")
        identities = dict(doors)
        identities.update(_class_dict_literal("_WHEEL_AREA_COLORS"))
        for name, color in identities.items():
            self.assertGreaterEqual(
                _contrast_vs_white(color), 4.5,
                f"{name} {color} fails WCAG AA vs white text")
            r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
            # True red = strong red channel with LITTLE green and blue
            # (orange and brown carry real green and are not reds —
            # first draft flagged them; the 3x ratio separates the
            # categories: #b91c1c r/g≈6.6 is red, #c2410c r/g≈3.0 is
            # orange, #7c2d12 r/g≈2.8 is brown).
            self.assertFalse(
                r >= 120 and r > 3 * g and r > 3 * b,
                f"{name} {color} is red-family — red is reserved for "
                "stop/delete (F6 color law; ISO 3864)")

    def test_toolbar_shell_controls_pack_before_the_body(self):
        """F5: ❓ Tour and Dock/Undock must be created (and packed)
        BEFORE the toolbar's expanding _FlowFrame body — packed after
        it, Tk starves them first and the labels clip off the right
        edge (owner QA 2026-07-26: '❓ Tou')."""
        fn = None
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_floating_toolbar_widgets":
                fn = node
        self.assertIsNotNone(fn)
        tour_line = flow_line = None
        for n in ast.walk(fn):
            if isinstance(n, ast.Constant) and n.value == "❓ Tour" \
                    and tour_line is None:
                tour_line = n.lineno
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id == "_FlowFrame" and flow_line is None:
                flow_line = n.lineno
        self.assertIsNotNone(tour_line, "❓ Tour button missing")
        self.assertIsNotNone(flow_line, "_FlowFrame body missing")
        self.assertLess(tour_line, flow_line,
                        "shell controls pack after the expanding body "
                        "again — they will clip when the bar runs narrow")

    def test_one_front_door_no_orphaned_rooms(self):
        """F4: the dashboard's four-button exterior row is gone, the
        Session tab bar carries the three doors (wheel/Track/Study), and
        the Planning hub + Money panel keep interior doors — a room you
        can't reach is a regression (Blueprint §12 trap rule)."""
        src_attrs = None
        for node in ast.walk(_app_tree()):
            if isinstance(node, ast.FunctionDef) \
                    and node.name == "_build_session_start_panel":
                src_attrs = {n.attr for n in ast.walk(node)
                             if isinstance(n, ast.Attribute)}
        self.assertIsNotNone(src_attrs)
        for door in ("open_track_hub", "open_study_workspace",
                     "open_planning_hub", "open_money_panel"):
            self.assertIn(door, src_attrs,
                          f"{door} lost its door — orphaned room "
                          "(Blueprint §12 trap rule)")
        with open(_APP, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("TOPBAR_BUTTONS", src,
                         "the exterior four-button row is back — the "
                         "house has one front door")

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
