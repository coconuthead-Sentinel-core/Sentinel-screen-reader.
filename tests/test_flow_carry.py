"""Headless tests for the flow-carry kernel (lyceum.flow_carry).

Blueprint §12 Phase B: a saved goal's next action travels into the
Do-Now quadrant. Pure logic, no GUI, no DB.
"""
import unittest

from lyceum.flow_carry import next_action


class NextActionTest(unittest.TestCase):
    def test_first_plan_line_wins(self):
        text, used = next_action("Refill ADHD meds",
                                 "Call the pharmacy\nThen drive over")
        self.assertEqual(text, "Call the pharmacy")
        self.assertTrue(used)

    def test_bullets_and_blanks_stripped(self):
        text, used = next_action("Goal",
                                 "\n  \n• - [ ] Open the savings account\n")
        self.assertEqual(text, "Open the savings account")
        self.assertTrue(used)

    def test_title_stands_in_without_a_plan(self):
        text, used = next_action("Walk 20 minutes daily", "")
        self.assertEqual(text, "Walk 20 minutes daily")
        self.assertFalse(used)

    def test_whitespace_plan_falls_back_to_title(self):
        text, used = next_action("  Budget the week  ", "   \n  \n")
        self.assertEqual(text, "Budget the week")
        self.assertFalse(used)

    def test_both_blank_declines(self):
        self.assertEqual(next_action("", ""), ("", False))
        self.assertEqual(next_action(None, None), ("", False))


if __name__ == "__main__":
    unittest.main()
