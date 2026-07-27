"""Headless tests for the flow-carry kernel (lyceum.flow_carry).

Blueprint §12 Phase B: a saved goal's next action travels into the
Do-Now quadrant. Pure logic, no GUI, no DB.
"""
import unittest

from lyceum.flow_carry import (next_action, planner_task_title,
                               is_duplicate_task)


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


class PlannerTaskTitleTest(unittest.TestCase):
    def test_step_carries_goal_context(self):
        self.assertEqual(
            planner_task_title("Call the pharmacy", "Refill meds", True),
            "🎯 Refill meds: Call the pharmacy")

    def test_title_only_when_no_step(self):
        self.assertEqual(
            planner_task_title("Walk 20 minutes daily",
                               "Walk 20 minutes daily", False),
            "🎯 Walk 20 minutes daily")

    def test_blank_carry_declines(self):
        self.assertEqual(planner_task_title("", "Goal", False), "")
        self.assertEqual(planner_task_title(None, None, True), "")


class IsDuplicateTaskTest(unittest.TestCase):
    def test_exact_match_is_duplicate(self):
        self.assertTrue(is_duplicate_task(
            ["🎯 Refill meds: Call the pharmacy"],
            "🎯 Refill meds: Call the pharmacy"))

    def test_case_and_spacing_insensitive(self):
        self.assertTrue(is_duplicate_task(
            ["🎯  refill MEDS:   call the pharmacy"],
            "🎯 Refill meds: Call the pharmacy"))

    def test_fresh_task_is_not_duplicate(self):
        self.assertFalse(is_duplicate_task(
            ["🎯 Other goal: other step"], "🎯 New: thing"))

    def test_empty_candidate_counts_as_duplicate(self):
        self.assertTrue(is_duplicate_task([], ""))
        self.assertTrue(is_duplicate_task(["x"], "   "))

    def test_empty_day_accepts_anything_real(self):
        self.assertFalse(is_duplicate_task([], "🎯 First of the day"))


if __name__ == "__main__":
    unittest.main()
