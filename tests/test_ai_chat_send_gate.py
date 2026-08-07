"""Regression gate for the AI-chat send path (owner field report
2026-08-07: pressing Enter left the text in the box, no message sent,
no feedback).

Root cause: `_send` trusted a launch-time availability snapshot and
declined SILENTLY when the brain was offline — a Law 3 violation
(a decline must breadcrumb and tell). Secondary: the numeric-keypad
Enter (keysym KP_Enter) was unhandled and inserted a newline instead
of sending (Law 6 platform trap).

Two proofs, both headless and deterministic:
1. Functional — LocalBrain.recheck() flips .available when the daemon
   comes up after construction (fake ollama, no network).
2. Static gate — the _build_tab_ai_chat send path must re-probe
   (recheck), breadcrumb its decline (_qlog "ai-send:"), speak to the
   user (_append_msg), and handle KP_Enter. If any of those strings
   leave the source, this gate fails before the field does.
"""
import os
import re
import sys
import unittest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHELL = os.path.join(_REPO_ROOT, "sentinel_personal_development.py")
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import ai_brain


class _FakeOllamaDown:
    """Daemon unreachable: list() raises like a refused connection."""
    @staticmethod
    def list():
        raise ConnectionError("connection refused")


class _FakeOllamaUp:
    """Daemon up with the default model pulled."""
    @staticmethod
    def list():
        return {"models": [{"model": ai_brain.DEFAULT_MODEL}]}


class RecheckTest(unittest.TestCase):
    """recheck() makes availability a live fact, not a launch snapshot."""

    def setUp(self):
        self._saved = (ai_brain.ollama if ai_brain._OLLAMA_IMPORTED else None,
                       ai_brain._OLLAMA_IMPORTED)

    def tearDown(self):
        saved_ollama, saved_imported = self._saved
        ai_brain._OLLAMA_IMPORTED = saved_imported
        if saved_ollama is not None:
            ai_brain.ollama = saved_ollama

    def test_daemon_started_after_launch_is_picked_up(self):
        ai_brain._OLLAMA_IMPORTED = True
        ai_brain.ollama = _FakeOllamaDown
        brain = ai_brain.LocalBrain()
        self.assertFalse(brain.available)
        self.assertIn("not reachable", brain.last_error)
        # ... user starts Ollama, then presses Enter again:
        ai_brain.ollama = _FakeOllamaUp
        self.assertTrue(brain.recheck())
        self.assertTrue(brain.available)
        self.assertIsNone(brain.last_error)

    def test_daemon_going_down_is_reported(self):
        ai_brain._OLLAMA_IMPORTED = True
        ai_brain.ollama = _FakeOllamaUp
        brain = ai_brain.LocalBrain()
        self.assertTrue(brain.available)
        ai_brain.ollama = _FakeOllamaDown
        self.assertFalse(brain.recheck())
        self.assertIn("not reachable", brain.last_error)

    def test_missing_package_still_declines_with_reason(self):
        ai_brain._OLLAMA_IMPORTED = False
        brain = ai_brain.LocalBrain()
        self.assertFalse(brain.available)
        self.assertFalse(brain.recheck())
        self.assertIn("not installed", brain.last_error)


class SendPathGate(unittest.TestCase):
    """Static gate over the chat-tab source (test_ftb_decline_gate style)."""

    @classmethod
    def setUpClass(cls):
        with open(_SHELL, encoding="utf-8") as f:
            src = f.read()
        m = re.search(r"def _build_tab_ai_chat\(self.*?(?=\n    def )",
                      src, re.S)
        assert m, "_build_tab_ai_chat not found"
        cls.body = m.group(0)

    def test_offline_decline_reprobes(self):
        self.assertIn("recheck()", self.body,
                      "send path must re-probe availability, not trust "
                      "the launch-time snapshot")

    def test_offline_decline_breadcrumbs(self):
        self.assertIn("ai-send:", self.body,
                      "offline decline must _qlog a breadcrumb (Law 3)")
        self.assertIn("_qlog", self.body)

    def test_offline_decline_tells_the_user(self):
        self.assertIn('_append_msg("Error"', self.body,
                      "offline decline must post a visible message (Law 3)")

    def test_keypad_enter_sends(self):
        self.assertIn("KP_Enter", self.body,
                      "numeric-keypad Enter must send, not insert a newline")


if __name__ == "__main__":
    unittest.main()
