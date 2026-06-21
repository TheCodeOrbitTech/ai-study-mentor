#!/usr/bin/env python3
"""
Test Suite for ProgressTrackerAgent
----------------------------------
Validates progress math calculations, ASCII progress bar rendering,
and data serialization/deserialization.
"""

import unittest
import os
import json
from progress_tracker import ProgressTrackerAgent


class TestProgressTrackerAgent(unittest.TestCase):
    """Unit tests for ProgressTrackerAgent class logic."""

    def setUp(self):
        """Set up temporary filenames and initialize the agent before each test."""
        self.test_json = "temp_test_progress.json"
        self.test_md = "temp_test_report.md"
        # Make sure no leftover files exist
        self.cleanup_files()
        
        # Initialize agent with temp files
        self.agent = ProgressTrackerAgent(data_file=self.test_json, report_file=self.test_md)

    def tearDown(self):
        """Clean up temporary files created during testing."""
        self.cleanup_files()

    def cleanup_files(self):
        """Helper to delete temporary test files if they exist."""
        for filename in [self.test_json, self.test_md]:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except OSError:
                    pass

    def test_calculate_metrics(self):
        """Verify remaining topics and percentage calculations (including rounding)."""
        # Test basic 50% case
        rem, pct = self.agent.calculate_metrics(10, 5)
        self.assertEqual(rem, 5)
        self.assertEqual(pct, 50.0)

        # Test rounding (1/3 should be 33.3%)
        rem, pct = self.agent.calculate_metrics(3, 1)
        self.assertEqual(rem, 2)
        self.assertEqual(pct, 33.3)

        # Test 0% case
        rem, pct = self.agent.calculate_metrics(8, 0)
        self.assertEqual(rem, 8)
        self.assertEqual(pct, 0.0)

        # Test 100% case
        rem, pct = self.agent.calculate_metrics(12, 12)
        self.assertEqual(rem, 0)
        self.assertEqual(pct, 100.0)

        # Edge case: total_topics is 0 or less
        rem, pct = self.agent.calculate_metrics(0, 0)
        self.assertEqual(rem, 0)
        self.assertEqual(pct, 0.0)

    def test_progress_bar_generation(self):
        """Verify ASCII progress bar styling and sizing matches expected percentages."""
        # 0% completion bar (width=10)
        bar_0 = self.agent.generate_progress_bar(0.0, width=10)
        self.assertEqual(bar_0, "[░░░░░░░░░░]")

        # 50% completion bar (width=10)
        bar_50 = self.agent.generate_progress_bar(50.0, width=10)
        self.assertEqual(bar_50, "[█████░░░░░]")

        # 100% completion bar (width=10)
        bar_100 = self.agent.generate_progress_bar(100.0, width=10)
        self.assertEqual(bar_100, "[██████████]")

        # Width default is 20
        bar_default = self.agent.generate_progress_bar(50.0)
        self.assertEqual(bar_default, "[██████████░░░░░░░░░░]")

        # Out-of-bounds boundary handling
        bar_underflow = self.agent.generate_progress_bar(-10.0, width=5)
        self.assertEqual(bar_underflow, "[░░░░░]")
        bar_overflow = self.agent.generate_progress_bar(150.0, width=5)
        self.assertEqual(bar_overflow, "[█████]")

    def test_persistence_json(self):
        """Verify saving and reloading progress to/from JSON works correctly."""
        # Setup mock subject progress
        self.agent.subjects_data = {
            "Algorithms": {
                "total_topics": 15,
                "completed_topics": 6,
                "last_updated": "2026-06-20 12:00:00"
            },
            "Web Development": {
                "total_topics": 8,
                "completed_topics": 8,
                "last_updated": "2026-06-20 12:05:00"
            }
        }

        # Save progress
        self.agent.save_progress()
        self.assertTrue(os.path.exists(self.test_json))

        # Re-initialize another agent pointing to the same file
        new_agent = ProgressTrackerAgent(data_file=self.test_json, report_file=self.test_md)
        self.assertIn("Algorithms", new_agent.subjects_data)
        self.assertIn("Web Development", new_agent.subjects_data)

        # Check content match
        self.assertEqual(new_agent.subjects_data["Algorithms"]["total_topics"], 15)
        self.assertEqual(new_agent.subjects_data["Algorithms"]["completed_topics"], 6)
        self.assertEqual(new_agent.subjects_data["Web Development"]["completed_topics"], 8)

    def test_persistence_markdown_report(self):
        """Verify markdown report generation builds the expected visual overview file."""
        self.agent.subjects_data = {
            "Machine Learning": {
                "total_topics": 10,
                "completed_topics": 4,
                "last_updated": "2026-06-20 12:10:00"
            }
        }
        self.agent.export_markdown_report()
        self.assertTrue(os.path.exists(self.test_md))

        # Read markdown report contents
        with open(self.test_md, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Verify key parts exist in the report
        self.assertIn("# 📈 Study Progress Report", md_content)
        self.assertIn("Machine Learning", md_content)
        self.assertIn("4", md_content) # completed topics
        self.assertIn("10", md_content) # total topics
        self.assertIn("40.0%", md_content) # percentage
        self.assertIn("Study Coach Advice", md_content)


if __name__ == "__main__":
    unittest.main()
