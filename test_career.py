#!/usr/bin/env python3
"""
Test Suite for CareerGuidanceAgent
---------------------------------
Validates career matchmaking, skill gap calculations,
and dynamic fallback pathways.
"""

import unittest
import os
from career_guidance import CareerGuidanceAgent, CAREER_DATABASE


class TestCareerGuidanceAgent(unittest.TestCase):
    """Unit tests for CareerGuidanceAgent class logic."""

    def setUp(self):
        """Initialize the agent before each test."""
        self.agent = CareerGuidanceAgent()
        self.test_output_md = "career_recommendation.md"
        self.cleanup_files()

    def tearDown(self):
        """Clean up generated files."""
        self.cleanup_files()

    def cleanup_files(self):
        """Helper to delete temporary files if they exist."""
        if os.path.exists(self.test_output_md):
            try:
                os.remove(self.test_output_md)
            except OSError:
                pass

    def test_matching_curated_path(self):
        """Verify the scoring engine matches standard goals with curated career profiles."""
        # Setup input targeting Machine Learning Engineer
        self.agent.area_of_interest = "AI and Data Science"
        self.agent.career_goal = "I want to become a Machine Learning Engineer"
        self.agent.skills = ["Python", "SQL"]

        recommendation = self.agent.match_career()
        
        self.assertTrue(recommendation["is_curated"])
        self.assertEqual(recommendation["name"], "Machine Learning Engineer")
        self.assertGreater(recommendation["score"], 5)
        self.assertIn("Python", recommendation["required_skills"])

    def test_matching_another_curated_path(self):
        """Verify matching for a Frontend Developer profile."""
        self.agent.area_of_interest = "Web Development"
        self.agent.career_goal = "Frontend Developer"
        self.agent.skills = ["HTML", "CSS", "JavaScript"]

        recommendation = self.agent.match_career()

        self.assertTrue(recommendation["is_curated"])
        self.assertEqual(recommendation["name"], "Frontend Developer")
        self.assertIn("React/Vue/Angular", recommendation["required_skills"])

    def test_skill_gap_analysis(self):
        """Verify the skill gap analysis correctly separates acquired and missing skills."""
        required = ["Python", "Git", "Docker", "Kubernetes", "Linux"]
        self.agent.skills = ["python", "git", "bash"]

        acquired, missing = self.agent.analyze_skill_gap(required)

        # Case-insensitive substring checks should match Python and Git
        self.assertIn("Python", acquired)
        self.assertIn("Git", acquired)
        
        # Missing should include Docker, Kubernetes, Linux
        self.assertIn("Docker", missing)
        self.assertIn("Kubernetes", missing)
        self.assertIn("Linux", missing)
        self.assertEqual(len(acquired), 2)
        self.assertEqual(len(missing), 3)

    def test_fallback_logic(self):
        """Verify fallback triggers and generates custom structure for non-matching goals."""
        self.agent.area_of_interest = "Embedded Game Design"
        self.agent.career_goal = "Nintendo Console Hacker"
        self.agent.skills = ["C++"]

        recommendation = self.agent.match_career()

        # Should fallback since goal is not in curated database
        self.assertFalse(recommendation["is_curated"])
        self.assertEqual(recommendation["name"], "Nintendo Console Hacker")
        self.assertIn("Nintendo", recommendation["required_skills"])
        self.assertIn("Console", recommendation["required_skills"])
        self.assertIn("Hacker", recommendation["required_skills"])
        self.assertEqual(len(recommendation["roadmap"]), 4)

    def test_export_markdown_report(self):
        """Verify markdown report generation builds the expected visual overview file."""
        self.agent.area_of_interest = "Security"
        self.agent.career_goal = "Cybersecurity Analyst"
        self.agent.skills = ["Linux"]

        recommendation = self.agent.match_career()
        acquired, missing = self.agent.analyze_skill_gap(recommendation["required_skills"])
        
        self.agent.export_to_markdown(recommendation, acquired, missing)
        
        self.assertTrue(os.path.exists(self.test_output_md))

        # Check file content
        with open(self.test_output_md, 'r', encoding='utf-8') as f:
            md_content = f.read()

        self.assertIn("# Career Roadmap & Guidance Report", md_content)
        self.assertIn("Cybersecurity Analyst", md_content)
        self.assertIn("Linux", md_content)
        self.assertIn("Networking (TCP/IP)", md_content)
        self.assertIn("Phase 1: Computer Networking & OS Fundamentals", md_content)


if __name__ == "__main__":
    unittest.main()
