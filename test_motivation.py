#!/usr/bin/env python3
"""
Test Suite for MotivationAgent
------------------------------
Validates progress level mapping, motivational payload generation,
ASCII progress bar rendering, and markdown report exportation.
"""

import unittest
import os
from motivation_agent import MotivationAgent


class TestMotivationAgent(unittest.TestCase):
    """Unit tests for MotivationAgent class logic."""

    def setUp(self):
        """Initialize the agent before each test and set up temp output file."""
        self.test_md = "temp_study_motivation.md"
        self.cleanup_files()
        self.agent = MotivationAgent(report_file=self.test_md)

    def tearDown(self):
        """Clean up generated files after each test."""
        self.cleanup_files()

    def cleanup_files(self):
        """Helper to delete temporary test report files."""
        if os.path.exists(self.test_md):
            try:
                os.remove(self.test_md)
            except OSError:
                pass

    def test_progress_bar_generation(self):
        """Verify ASCII progress bar styling and boundaries."""
        # 0% completion
        bar_0 = self.agent.generate_progress_bar(0.0, width=10)
        self.assertEqual(bar_0, "[░░░░░░░░░░]")

        # 50% completion
        bar_50 = self.agent.generate_progress_bar(50.0, width=10)
        self.assertEqual(bar_50, "[█████░░░░░]")

        # 100% completion
        bar_100 = self.agent.generate_progress_bar(100.0, width=10)
        self.assertEqual(bar_100, "[██████████]")

        # Boundaries & clipping
        bar_under = self.agent.generate_progress_bar(-10.0, width=5)
        self.assertEqual(bar_under, "[░░░░░]")

        bar_over = self.agent.generate_progress_bar(120.0, width=5)
        self.assertEqual(bar_over, "[█████]")

    def test_get_progress_level_mapping(self):
        """Verify percentages map to correct progress stages."""
        test_cases = [
            (0, "Starting Block"),
            (10, "Foundation Phase"),
            (25, "Foundation Phase"),
            (30, "Momentum Stage"),
            (50, "Momentum Stage"),
            (55, "Valley of Persistence"),
            (75, "Valley of Persistence"),
            (80, "Home Stretch"),
            (99, "Home Stretch"),
            (100, "Champion's Circle")
        ]

        for pct, expected_stage in test_cases:
            self.agent.progress_percentage = pct
            level_info = self.agent.get_progress_level()
            self.assertEqual(
                level_info["stage"],
                expected_stage,
                f"Expected {pct}% to map to '{expected_stage}', got '{level_info['stage']}'"
            )

    def test_generate_motivation_contains_goal(self):
        """Verify generated payloads are personalized with the user's study goal."""
        self.agent.study_goal = "Master Quantum Computing"

        # Check a few stages
        for pct in [0, 40, 75, 100]:
            self.agent.progress_percentage = pct
            level = self.agent.get_progress_level()
            payload = self.agent.generate_motivation(level)

            # The goal should appear in messages and/or encouragement
            all_text = " ".join(payload["messages"]) + " " + payload["encouragement"]
            self.assertIn(
                "Quantum Computing",
                all_text,
                f"Expected goal 'Master Quantum Computing' to be in payload for {pct}% stage"
            )
            self.assertGreater(len(payload["tips"]), 0, f"Expected tips for {pct}% stage")

    def test_export_report_to_markdown(self):
        """Verify markdown report generation builds the expected structured dashboard file."""
        self.agent.study_goal = "Learn Docker Containers"
        self.agent.progress_percentage = 45.0

        level = self.agent.get_progress_level()
        payload = self.agent.generate_motivation(level)

        self.agent.export_report_to_markdown(level, payload)

        self.assertTrue(os.path.exists(self.test_md), "Report file was not created")

        with open(self.test_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Check headers and parameters in markdown report
        self.assertIn("# 🎯 Study Motivation Report", content)
        self.assertIn("Learn Docker Containers", content)
        self.assertIn("45.0%", content)
        self.assertIn("Momentum Stage", content)
        self.assertIn("## 💡 Custom Study Tips", content)
        self.assertIn("## 💪 Coach's Encouragement", content)


if __name__ == "__main__":
    unittest.main()
