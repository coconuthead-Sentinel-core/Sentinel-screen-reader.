"""Headless tests for the flow-carry kernel (lyceum.flow_carry).

Blueprint §12 Phase B: a saved goal's next action travels into the
Do-Now quadrant. Pure logic, no GUI, no DB.
"""
import unittest

from lyceum.flow_carry import (next_action, planner_task_title,
                               is_duplicate_task, count_do_items,
                               session_briefing)


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


class CountDoItemsTest(unittest.TestCase):
    def test_bullets_counted_sources_ignored(self):
        body = ("• Call the pharmacy\n  (🎯 Refill · 💰 — 2026-07-27)\n"
                "• Walk 20 minutes\n  (2026-07-27)\n")
        self.assertEqual(count_do_items(body), 2)

    def test_unchecked_boxes_counted_checked_not(self):
        self.assertEqual(count_do_items("[ ] open one\n[x] done one\n"), 1)

    def test_empty_body_is_zero(self):
        self.assertEqual(count_do_items(""), 0)
        self.assertEqual(count_do_items(None), 0)


class SessionBriefingTest(unittest.TestCase):
    def test_empty_plan_speaks(self):
        out = session_briefing([], 0)
        self.assertIn("empty", out)
        self.assertIn("gate", out)

    def test_lists_tasks_with_marks_and_counts(self):
        out = session_briefing([("🎯 A: step", 0), ("🎯 B", 1)], 3)
        self.assertIn("1 open task (of 2)", out)
        self.assertIn("▫ 🎯 A: step", out)
        self.assertIn("✔ 🎯 B", out)
        self.assertIn("Do Now holds 3 items", out)
        self.assertIn("Begin", out)

    def test_caps_at_six_and_says_so(self):
        tasks = [(f"t{i}", 0) for i in range(9)]
        out = session_briefing(tasks, 0)
        self.assertIn("… and 3 more", out)
        self.assertNotIn("t7", out)

    def test_blank_titles_skipped(self):
        out = session_briefing([("", 0), ("  ", 1), ("real", 0)], 0)
        self.assertIn("1 open task:", out)
        self.assertIn("▫ real", out)


if __name__ == "__main__":
    unittest.main()
