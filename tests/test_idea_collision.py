"""Headless tests for the Idea Collision kernel (lyceum.idea_collision).

Pure core, no GUI, no DB — deterministic via injected rng.
"""
import random
import unittest

from lyceum.idea_collision import draw_collision


class DrawCollisionTest(unittest.TestCase):
    def test_two_distinct_concepts_and_prompt(self):
        out = draw_collision(["Recursion", "Compound interest", "Pack order"],
                             rng=random.Random(0))
        self.assertIsNotNone(out)
        a, b, prompt = out
        self.assertNotEqual(a, b)
        self.assertIn(a, prompt)
        self.assertIn(b, prompt)
        self.assertIn("IDEA COLLISION", prompt)

    def test_deterministic_with_seed(self):
        items = ["alpha", "beta", "gamma", "delta"]
        first = draw_collision(items, rng=random.Random(7))
        second = draw_collision(items, rng=random.Random(7))
        self.assertEqual(first[:2], second[:2])

    def test_declines_below_two_distinct(self):
        self.assertIsNone(draw_collision([]))
        self.assertIsNone(draw_collision(["only-one"]))
        self.assertIsNone(draw_collision(["dup", "dup", "  dup  "]))

    def test_blank_and_none_items_ignored(self):
        out = draw_collision(["", "  ", None, "real-a", "real-b"],
                             rng=random.Random(1))
        a, b, _ = out
        self.assertIn(a, ("real-a", "real-b"))
        self.assertIn(b, ("real-a", "real-b"))


if __name__ == "__main__":
    unittest.main()
