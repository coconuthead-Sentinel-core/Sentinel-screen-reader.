"""Room-signs kernel tests + the static wiring gate (punch item #11).

The registry is pure data; these tests are the inspection that every
sign is fit to hang, plus a source-scan gate proving the shell is
actually wired (a sweep without a gate misses one — shop law 5).
"""
import os
import unittest

from lyceum.room_signs import SIGNS, Sign, get_sign, validate

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHELL = os.path.join(_REPO_ROOT, "sentinel_personal_development.py")

# The eight study-workspace rooms the seam covers tonight.
STUDY_TAB_KEYS = (
    "study_notes", "ai_chat", "topics", "glossary",
    "commentary", "journal", "matrix", "planner",
)


class TestRoomSignsRegistry(unittest.TestCase):
    def test_registry_validates_clean(self):
        self.assertEqual(validate(), [])

    def test_all_study_tabs_have_signs(self):
        for key in STUDY_TAB_KEYS:
            self.assertIn(key, SIGNS)

    def test_every_sign_has_both_parts(self):
        for room_id, sign in SIGNS.items():
            self.assertTrue(sign.pictogram.strip(), room_id)
            self.assertTrue(sign.word.strip(), room_id)

    def test_words_read_as_signage(self):
        for room_id, sign in SIGNS.items():
            self.assertEqual(sign.word, sign.word.upper(), room_id)

    def test_matrix_sign_carries_four_quadrant_cluster(self):
        pictogram = get_sign("matrix").pictogram
        self.assertEqual(len(pictogram.split()), 4)

    def test_unknown_room_raises_key_error(self):
        with self.assertRaises(KeyError):
            get_sign("no_such_room")


class TestValidateCatchesDefects(unittest.TestCase):
    def test_missing_word(self):
        bad = {"a": Sign("🔧", "")}
        self.assertTrue(any("no word" in d for d in validate(bad)))

    def test_missing_pictogram(self):
        bad = {"a": Sign("", "TOOLS")}
        self.assertTrue(any("no pictogram" in d for d in validate(bad)))

    def test_lowercase_word(self):
        bad = {"a": Sign("🔧", "tools")}
        self.assertTrue(any("uppercase" in d for d in validate(bad)))

    def test_duplicate_pictogram_one_symbol_one_meaning(self):
        bad = {"a": Sign("🔧", "TOOLS"), "b": Sign("🔧", "WRENCH")}
        self.assertTrue(any("already means" in d for d in validate(bad)))

    def test_duplicate_word(self):
        bad = {"a": Sign("🔧", "TOOLS"), "b": Sign("⚙", "TOOLS")}
        self.assertTrue(any("already used" in d for d in validate(bad)))


class TestShellWiringGate(unittest.TestCase):
    """Static gate: the seam must exist in the shell source."""

    def setUp(self):
        with open(_SHELL, encoding="utf-8") as f:
            self.src = f.read()

    def test_draw_room_sign_defined(self):
        self.assertIn("def _draw_room_sign(", self.src)

    def test_study_tab_loop_calls_the_seam(self):
        self.assertIn("self._draw_room_sign(f, key)", self.src)

    def test_decline_path_breadcrumbs(self):
        # Law 3: an unsigned room must LOG, never just return.
        start = self.src.index("def _draw_room_sign(")
        body = self.src[start:start + 1500]
        self.assertIn("_qlog", body)


if __name__ == "__main__":
    unittest.main()
