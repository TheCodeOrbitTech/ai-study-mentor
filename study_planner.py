#!/usr/bin/env python3
"""
Study Planner Agent
-------------------
An interactive Python script that asks for subject details, study availability,
and target date, and then generates structured daily and weekly study plans.
"""

import os
from datetime import datetime, date
import math


class StudyPlannerAgent:
    """
    Agent responsible for collecting user parameters and generating customized
    daily and weekly study schedules.
    """

    def __init__(self):
        self.subject = ""
        self.hours_per_day = 0.0
        self.target_date = None
        self.topics = []

    def clear_screen(self):
        """Clears the terminal screen for clean presentation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints a styled terminal header for the Study Planner Agent."""
        print("=" * 60)
        print("         🎓 AI STUDY MENTOR - STUDY PLANNER AGENT 🎓         ")
        print("=" * 60)
        print()

    def get_valid_string(self, prompt_text):
        """Helper to ensure a non-empty string is entered."""
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            print("❌ Input cannot be empty. Please try again.")

    def get_valid_hours(self, prompt_text):
        """Validates and returns a positive float for daily study hours."""
        while True:
            val = input(prompt_text).strip()
            try:
                hours = float(val)
                if 0.1 <= hours <= 24.0:
                    return hours
                else:
                    print("❌ Please enter a realistic duration between 0.1 and 24.0 hours.")
            except ValueError:
                print("❌ Invalid number. Please enter a numerical value (e.g., 2.5).")

    def get_valid_date(self, prompt_text):
        """Validates that target date format is YYYY-MM-DD and is in the future."""
        today = date.today()
        while True:
            val = input(prompt_text).strip()
            try:
                target_dt = datetime.strptime(val, "%Y-%m-%d").date()
                if target_dt > today:
                    return target_dt
                else:
                    print(f"❌ Target date must be in the future (after today: {today}).")
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD format.")

    def collect_inputs(self):
        """Interactively requests and validates input parameters from the user."""
        self.clear_screen()
        self.print_header()
        
        print("Welcome! Let's setup your study roadmap.")
        print("-" * 60)
        
        # 1. Ask for Subject Name
        self.subject = self.get_valid_string("📚 Enter the subject name: ")
        
        # 2. Ask for Study Hours Per Day
        self.hours_per_day = self.get_valid_hours("⏱️  Enter your available study hours per day: ")
        
        # 3. Ask for Target Completion Date
        self.target_date = self.get_valid_date("📅 Enter your target completion date (YYYY-MM-DD): ")
        
        # 4. Optional: Chapters or topics list
        print("\n💡 (Optional) Enter the main topics/chapters separated by commas.")
        print("   Leave empty to let the Agent automatically generate standard learning phases.")
        topics_input = input("👉 Enter topics: ").strip()
        if topics_input:
            self.topics = [t.strip() for t in topics_input.split(",") if t.strip()]
        else:
            # Default learning phases if no specific topics are entered
            self.topics = [
                "Foundational Concepts & Terminology",
                "Core Principles & Detailed Mechanics",
                "Advanced Topics & Complex Applications",
                "Comprehensive Practice & Problem Solving",
                "Review, Self-Testing & Final Adjustments"
            ]
            
        print("\n✅ All inputs collected successfully! Generating your personalized plan...")

    def calculate_durations(self):
        """Calculates days, weeks, and total hours available until target date."""
        today = date.today()
        delta = self.target_date - today
        total_days = delta.days
        total_weeks = math.ceil(total_days / 7)
        total_hours = total_days * self.hours_per_day
        return total_days, total_weeks, total_hours

    def generate_daily_schedule(self):
        """
        Creates a structured daily hour breakdown based on total study hours.
        Incorporates productivity practices like the Pomodoro technique.
        """
        schedule = []
        minutes = int(self.hours_per_day * 60)
        
        if self.hours_per_day <= 1.0:
            # Single session layout
            schedule.append(f"• 00 mins - {minutes} mins: Focused Study Session (no distractions)")
            schedule.append("• Last 5 mins: Quick daily summary and reflection")
        elif self.hours_per_day <= 3.0:
            # Dual session layout with a break
            session_len = int(minutes * 0.45)
            break_len = int(minutes * 0.1)
            schedule.append(f"• Phase 1 ({session_len}m): Deep Study / New Topic Acquisition")
            schedule.append(f"• Break ({break_len}m): Active rest (stretch, walk, hydrate)")
            schedule.append(f"• Phase 2 ({session_len}m): Practical Exercises & Active Recall")
            schedule.append("• Review (10m): Summarize concepts learned")
        else:
            # Multiple sessions / blocks layout
            session_len = 50  # 50 mins focus block
            break_len = 10    # 10 mins break
            total_blocks = int(minutes / (session_len + break_len))
            
            for i in range(1, total_blocks + 1):
                schedule.append(f"• Block {i} (50m Focus): Study Module & Active Practice")
                schedule.append("• Interval (10m Break): Disconnect from screen")
            
            remaining = minutes - (total_blocks * (session_len + break_len))
            if remaining > 0:
                schedule.append(f"• Final wrap-up ({remaining}m): Daily alignment & tomorrow setup")
                
        return schedule

    def generate_weekly_schedule(self, total_weeks):
        """
        Distributes topics/chapters evenly across available weeks.
        """
        weekly_plan = {}
        num_topics = len(self.topics)
        
        if total_weeks >= num_topics:
            # More weeks than topics: spread them out with extra review weeks
            topics_per_week = 1
            for w in range(1, total_weeks + 1):
                if w <= num_topics:
                    weekly_plan[w] = {
                        "topic": self.topics[w - 1],
                        "focus": f"Comprehensive study of '{self.topics[w - 1]}'."
                    }
                else:
                    # Review phases or practice phases for later weeks
                    weekly_plan[w] = {
                        "topic": "Consolidation & Practice",
                        "focus": "Review previous topics, take practice assessments, and fill knowledge gaps."
                    }
        else:
            # Fewer weeks than topics: group topics together
            step = num_topics / total_weeks
            for w in range(1, total_weeks + 1):
                start_idx = int((w - 1) * step)
                end_idx = int(w * step)
                if w == total_weeks:
                    end_idx = num_topics  # Make sure last week gets all remaining
                
                week_topics = self.topics[start_idx:end_idx]
                weekly_plan[w] = {
                    "topic": ", ".join(week_topics),
                    "focus": f"Study topics: {', '.join(week_topics)}."
                }
                
        return weekly_plan

    def display_plan(self, total_days, total_weeks, total_hours, daily_schedule, weekly_schedule):
        """Prints the generated daily and weekly study roadmap to the terminal."""
        self.clear_screen()
        self.print_header()
        
        print("🗺️  YOUR STUDY ROADMAP GENERATED")
        print("=" * 60)
        print(f"📚 Subject:         {self.subject}")
        print(f"📅 Target Date:     {self.target_date} ({total_days} days remaining)")
        print(f"⏱️  Daily Allocation: {self.hours_per_day} hours/day")
        print(f"📊 Total Effort:     {total_hours:.1f} study hours across {total_weeks} weeks")
        print("=" * 60)
        print()

        # Print Daily Study Plan
        print("📅 DAILY STUDY PLAN PATTERN")
        print("-" * 30)
        print("Follow this structured sequence daily to maximize retention:")
        for step in daily_schedule:
            print(step)
        print()

        # Print Weekly Study Plan
        print("📅 WEEKLY STUDY PLAN ROADMAP")
        print("-" * 30)
        for week, details in weekly_schedule.items():
            print(f"Week {week}: {details['topic']}")
            print(f"  └─ Focus: {details['focus']}")
        print()
        print("=" * 60)
        print("💾 A detailed Markdown plan has been saved to: study_plan.md")
        print("=" * 60)
        print()

    def export_to_markdown(self, total_days, total_weeks, total_hours, daily_schedule, weekly_schedule):
        """Writes the study roadmap to a markdown file for persistent usage."""
        content = []
        content.append(f"# Study Roadmap: {self.subject}")
        content.append(f"Generated on {date.today().strftime('%B %d, %Y')}\n")
        
        content.append("## 📊 Plan Overview")
        content.append(f"- **Subject:** {self.subject}")
        content.append(f"- **Target Completion Date:** {self.target_date} ({total_days} days remaining)")
        content.append(f"- **Daily Study Time:** {self.hours_per_day} hours")
        content.append(f"- **Total Weeks:** {total_weeks} weeks")
        content.append(f"- **Total Dedicated Study Hours:** {total_hours:.1f} hours\n")
        
        content.append("## ⏱️ Daily Study Template")
        content.append("Use this sequence daily to keep yourself structured and focused:")
        for step in daily_schedule:
            content.append(step)
        content.append("\n")
        
        content.append("## 📅 Weekly Milestones")
        content.append("| Week | Topics & Milestones | Action Focus |")
        content.append("|---|---|---|")
        for week, details in weekly_schedule.items():
            content.append(f"| Week {week} | **{details['topic']}** | {details['focus']} |")
        content.append("\n")
        
        content.append("## 💡 Study Tips for Success")
        content.append("1. **Active Recall**: Don't just re-read. Close the book/notes and write down everything you remember.")
        content.append("2. **Spaced Repetition**: Re-evaluate older topics weekly to prevent the forgetting curve.")
        content.append("3. **Keep it Consistent**: Studying 2 hours a day is much better than studying 14 hours in one day.")
        content.append("4. **Buffer Days**: Use weekends or the last day of each week to catch up on topics you fell behind on.")
        
        with open("study_plan.md", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    def run(self):
        """Execution entrypoint for the agent."""
        self.collect_inputs()
        total_days, total_weeks, total_hours = self.calculate_durations()
        daily_schedule = self.generate_daily_schedule()
        weekly_schedule = self.generate_weekly_schedule(total_weeks)
        
        # Display plan in terminal
        self.display_plan(total_days, total_weeks, total_hours, daily_schedule, weekly_schedule)
        
        # Save plan to markdown file
        self.export_to_markdown(total_days, total_weeks, total_hours, daily_schedule, weekly_schedule)


if __name__ == "__main__":
    agent = StudyPlannerAgent()
    agent.run()
