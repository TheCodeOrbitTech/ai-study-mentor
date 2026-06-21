#!/usr/bin/env python3
"""
Test Suite for ResourceFinderAgent
----------------------------------
Validates curated database content, search matching logic, fuzzy mapping,
and dynamic fallback URL generation.
"""

import unittest
import urllib.parse
from resource_finder import ResourceFinderAgent, RESOURCES_DB


class TestResourceFinderAgent(unittest.TestCase):
    """Unit tests for ResourceFinderAgent class logic."""

    def setUp(self):
        self.agent = ResourceFinderAgent()

    def test_database_integrity(self):
        """Verify that all predefined subjects exist and contain valid resource blocks."""
        expected_subjects = [
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Python Programming",
            "Interview Preparation"
        ]
        
        # Verify all expected subjects are in the DB keys
        for subj in expected_subjects:
            self.assertIn(subj, RESOURCES_DB)
            
            # Check levels
            for level in ["Beginner", "Intermediate", "Advanced"]:
                self.assertIn(level, RESOURCES_DB[subj])
                resources = RESOURCES_DB[subj][level]
                
                # Check that there are resources in each category
                self.assertGreaterEqual(len(resources), 1)
                for res in resources:
                    self.assertIn("name", res)
                    self.assertIn("url", res)
                    self.assertIn("desc", res)
                    # Verify URLs are non-empty and start with http
                    self.assertTrue(res["url"].startswith("http"))

    def test_exact_match(self):
        """Verify that searching for an exact subject returns the correct entry."""
        for subj in RESOURCES_DB:
            matched_name, resources = self.agent.search_resources(subj)
            self.assertEqual(matched_name, subj)
            self.assertEqual(resources, RESOURCES_DB[subj])

    def test_case_insensitive_match(self):
        """Verify that exact matches are case-insensitive."""
        matched_name, resources = self.agent.search_resources("python programming")
        self.assertEqual(matched_name, "Python Programming")
        self.assertEqual(resources, RESOURCES_DB["Python Programming"])

    def test_fuzzy_substring_match(self):
        """Verify that substring searches map to the correct predefined subject."""
        # 'python' should match 'Python Programming'
        matched_name, resources = self.agent.search_resources("python")
        self.assertEqual(matched_name, "Python Programming")
        self.assertEqual(resources, RESOURCES_DB["Python Programming"])
        
        # 'interview' should match 'Interview Preparation'
        matched_name, resources = self.agent.search_resources("interview")
        self.assertEqual(matched_name, "Interview Preparation")

    def test_fallback_generation(self):
        """Verify that custom topics trigger dynamic search query links."""
        custom_topic = "Kubernetes"
        matched_name, resources = self.agent.search_resources(custom_topic)
        
        self.assertEqual(matched_name, custom_topic)
        self.assertIn("Beginner", resources)
        self.assertIn("Intermediate", resources)
        self.assertIn("Advanced", resources)
        
        # Verify query parameters are encoded
        encoded_topic = urllib.parse.quote_plus(custom_topic)
        
        # Check beginner links
        beginner_links = [res["url"] for res in resources["Beginner"]]
        self.assertTrue(any(encoded_topic in url for url in beginner_links))
        
        # Check that edx/youtube/coursera are targeted in fallback urls
        all_urls = []
        for level in ["Beginner", "Intermediate", "Advanced"]:
            for res in resources[level]:
                all_urls.append(res["url"])
                
        self.assertTrue(any("coursera.org" in url for url in all_urls))
        self.assertTrue(any("youtube.com" in url for url in all_urls))
        self.assertTrue(any("github.com" in url for url in all_urls))


if __name__ == "__main__":
    unittest.main()
