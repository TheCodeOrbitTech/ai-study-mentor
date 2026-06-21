#!/usr/bin/env python3
"""
Test script for StudyPlannerAgent
--------------------------------
Validates schedule calculation and generation logic.
"""

from study_planner import StudyPlannerAgent
from datetime import date, timedelta


def test_calculations():
    agent = StudyPlannerAgent()
    agent.subject = "Artificial Intelligence"
    agent.hours_per_day = 2.5
    
    # Set target date to 14 days from today (exactly 2 weeks)
    agent.target_date = date.today() + timedelta(days=14)
    agent.topics = ["Supervised Learning", "Unsupervised Learning", "Neural Networks", "Reinforcement Learning"]
    
    total_days, total_weeks, total_hours = agent.calculate_durations()
    assert total_days == 14, f"Expected 14 days, got {total_days}"
    assert total_weeks == 2, f"Expected 2 weeks, got {total_weeks}"
    assert total_hours == 35.0, f"Expected 35.0 total hours, got {total_hours}"
    
    daily_schedule = agent.generate_daily_schedule()
    assert len(daily_schedule) > 0, "Daily schedule should not be empty"
    
    weekly_schedule = agent.generate_weekly_schedule(total_weeks)
    assert len(weekly_schedule) == 2, f"Expected weekly plan for 2 weeks, got {len(weekly_schedule)}"
    
    print("✅ All unit tests passed successfully!")


if __name__ == "__main__":
    test_calculations()
