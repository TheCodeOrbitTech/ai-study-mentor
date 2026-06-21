#!/usr/bin/env python3
"""
Motivation Agent
----------------
An interactive Python CLI tool to boost student morale, provide tailored study tips,
and generate customized encouragement reports based on current study progress and goals.
"""

import os
import math
from datetime import datetime


class MotivationAgent:
    """
    Agent responsible for analyzing current study progress and goals,
    providing customized encouragement, and exporting a study motivation dashboard.
    """

    def __init__(self, report_file="study_motivation.md"):
        """
        Initializes the Motivation Agent.

        Args:
            report_file (str): Filename for saving the motivation report.
        """
        self.report_file = report_file
        self.study_goal = ""
        self.progress_percentage = 0.0

    def clear_screen(self):
        """Clears the terminal screen for a clean presentation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints a styled terminal header for the Motivation Agent."""
        print("=" * 65)
        print("        🔥 AI STUDY MENTOR - MOTIVATION AGENT 🔥        ")
        print("=" * 65)
        print()

    def get_valid_string(self, prompt_text):
        """
        Helper to ensure a non-empty string is entered by the user.

        Args:
            prompt_text (str): The prompt message to show the user.

        Returns:
            str: Verified non-empty stripped input string.
        """
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            print("❌ Input cannot be empty. Please try again.")

    def get_valid_percentage(self, prompt_text):
        """
        Helper to request and validate progress percentage between 0 and 100.

        Args:
            prompt_text (str): The prompt message to show the user.

        Returns:
            float: Verified percentage value.
        """
        while True:
            val = input(prompt_text).strip()
            try:
                pct = float(val)
                if 0.0 <= pct <= 100.0:
                    return pct
                else:
                    print("❌ Percentage must be between 0.0 and 100.0.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid number (e.g., 45.5).")

    def collect_inputs(self):
        """Interactively requests and validates inputs from the user."""
        self.clear_screen()
        self.print_header()

        print("Welcome! Let's fuel your study engine with custom motivation.")
        print("-" * 65)

        # 1. Ask for Study Goal
        self.study_goal = self.get_valid_string("🎯 What is your current study goal? (e.g., Learn Python, Pass Math Exam): ")

        # 2. Ask for Progress Percentage
        self.progress_percentage = self.get_valid_percentage("📈 What is your current progress percentage (0-100)? ")

        print("\n✨ Processing your data and preparing your motivation boost...")

    def get_progress_level(self):
        """
        Maps the progress percentage to a specific stage/level.

        Returns:
            dict: Details of the progress stage including label, description, and status emoji.
        """
        pct = self.progress_percentage
        if pct == 0:
            return {
                "stage": "Starting Block",
                "emoji": "🚀",
                "description": "Ready to launch! The hardest part is often just taking the first step. Let's build your momentum."
            }
        elif 0 < pct <= 25:
            return {
                "stage": "Foundation Phase",
                "emoji": "🌱",
                "description": "Roots are forming. You've taken key initial actions. Consistency now will build a strong routine."
            }
        elif 25 < pct <= 50:
            return {
                "stage": "Momentum Stage",
                "emoji": "⚙️",
                "description": "Getting into the groove! You're making noticeable headway. Keep pushing to reach the halfway point."
            }
        elif 50 < pct <= 75:
            return {
                "stage": "Valley of Persistence",
                "emoji": "🏔️",
                "description": "You've crossed the halfway mark! Don't let up now. This is where champions separate themselves."
            }
        elif 75 < pct <= 99:
            return {
                "stage": "Home Stretch",
                "emoji": "🏁",
                "description": "The finish line is in sight! Time to lock in, review, and finish strong. You've got this!"
            }
        else: # 100%
            return {
                "stage": "Champion's Circle",
                "emoji": "🏆",
                "description": "Complete victory! You hit your goal. Take a moment to celebrate, reflect, and set the next milestone."
            }

    def generate_motivation(self, level):
        """
        Generates personalized motivational quotes, advice, and tips based on the stage and goal.

        Args:
            level (dict): The current progress level dictionary.

        Returns:
            dict: Motivational message list, study tips list, and next step encouragement.
        """
        stage = level["stage"]
        goal = self.study_goal

        # Placeholders to customize based on stage
        messages = []
        tips = []
        encouragement = ""

        if stage == "Starting Block":
            messages = [
                f"The secret of getting ahead is getting started. Today is the perfect day to start working on: '{goal}'!",
                "Do not wait for the perfect moment. Take the moment and make it perfect.",
                "A journey of a thousand miles begins with a single step. Let's make that step today."
            ]
            tips = [
                "Break your target down into tiny, microscopic tasks. Instead of 'study for 3 hours', aim for 'read 2 pages'.",
                "Use the '5-Minute Rule': Tell yourself you'll study for just 5 minutes. If you want to stop after that, you can. (Usually, you won't!).",
                "Clean your workspace. A clutter-free desk leads to a focus-ready mind."
            ]
            encouragement = f"Zero progress only means you have a clean canvas! Let's write the first chapter of '{goal}' today."

        elif stage == "Foundation Phase":
            messages = [
                f"You're no longer at zero! You've officially begun your journey towards: '{goal}'.",
                "Small daily improvements over time lead to stunning results. Keep showing up!",
                "Success isn't always about greatness. It's about consistency. Consistent hard work leads to success."
            ]
            tips = [
                "Focus on building the habit loop: Choose a consistent time and place (cue), study for a short block (routine), and reward yourself (reward).",
                "Protect your energy. Do not burn out in the first week. 30 minutes every day is infinitely better than 5 hours once a week.",
                "Keep a distraction journal. When an unrelated thought pops up, write it down to address later, and return to studying."
            ]
            encouragement = f"You are building the foundation of your success in '{goal}'. Every small session is a brick in your wall."

        elif stage == "Momentum Stage":
            messages = [
                f"You are gaining speed! Keep moving toward your target of '{goal}'.",
                "Strength does not come from what you can do. It comes from overcoming the things you once thought you couldn't.",
                "Motivation is what gets you started. Habit is what keeps you going."
            ]
            tips = [
                "Implement Active Recall: Close your books and write down everything you remember, or quiz yourself, rather than just re-reading.",
                "Avoid the 'illusion of competence'—studying with answers open. Try solving problems independently first.",
                "Use site blockers (like Cold Turkey or Forest) to keep social media at bay during study blocks."
            ]
            encouragement = f"Look at how far you've come! You are close to the halfway mark for '{goal}'. Keep the fire burning!"

        elif stage == "Valley of Persistence":
            messages = [
                f"You've crossed the halfway mark for '{goal}'! This is where the magic happens.",
                "When you feel like quitting, think about why you started.",
                "It always seems impossible until it's done. You are closer to the end than the beginning!"
            ]
            tips = [
                "Try the Feynman Technique: Explain a difficult concept in simple terms, as if you were teaching it to a 10-year-old. This highlights knowledge gaps.",
                "Vary your study environments or formats. Listen to a podcast, draw a mind map, or change rooms to keep your brain active.",
                "Prioritize sleep. Memory consolidation happens during deep sleep. Don't sacrifice rest for cramming."
            ]
            encouragement = f"This is the crux! The momentum you sustain in this phase will guarantee you achieve your goal of '{goal}'."

        elif stage == "Home Stretch":
            messages = [
                f"The finish line is right there! Finish strong on your goal of '{goal}'.",
                "Don't stop when you're tired. Stop when you are done.",
                "You are so close. Give this final stretch everything you've got. Future you will thank you."
            ]
            tips = [
                "Simulate real conditions: Do practice tests or review sessions under timed, quiet conditions without notes.",
                "Focus on your remaining weak spots. Spend 80% of your time on the 20% of topics you still find challenging.",
                "Visualize success. Spend 2 minutes imagining yourself completing the goal and the feeling of accomplishment."
            ]
            encouragement = f"Almost there! Just a final push, and you will have successfully mastered '{goal}'!"

        else:  # Champion's Circle (100%)
            messages = [
                f"CONGRATULATIONS! You have fully achieved your goal: '{goal}'! 🎉",
                "Victory belongs to the most persevering. You proved you have what it takes.",
                "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice. You chose well."
            ]
            tips = [
                "Do a post-mortem review: What strategies worked best for you? What could you optimize next time?",
                "Reward yourself! Celebrate this win so your brain associates goal completion with positive reinforcement.",
                "Take a short rest block before planning your next challenge. Avoid immediate burnout."
            ]
            encouragement = f"You did it! '{goal}' is officially completed. You should be incredibly proud of your dedication and grit."

        return {
            "messages": messages,
            "tips": tips,
            "encouragement": encouragement
        }

    def generate_progress_bar(self, percentage, width=20):
        """
        Generates an ASCII progress bar representing the percentage.

        Args:
            percentage (float): Completion percentage (0 to 100).
            width (int): Character width of the progress bar.

        Returns:
            str: An ASCII progress bar e.g. '[██████░░░░░░]'
        """
        percentage = max(0.0, min(100.0, percentage))
        completed_blocks = int(round((percentage / 100.0) * width))
        remaining_blocks = width - completed_blocks
        bar = "█" * completed_blocks + "░" * remaining_blocks
        return f"[{bar}]"

    def display_report(self, level, payload):
        """
        Prints the motivation report beautifully to the terminal.

        Args:
            level (dict): Progress level info.
            payload (dict): Messages, tips, and encouragement details.
        """
        self.clear_screen()
        self.print_header()

        print("🔥 YOUR PERSONALIZED MOTIVATION REPORT 🔥")
        print("=" * 65)
        print(f"🎯 Goal:         {self.study_goal}")
        print(f"📈 Progress:     {self.progress_percentage}%")
        print(f"📊 Progress Bar: {self.generate_progress_bar(self.progress_percentage)}")
        print(f"📍 Current Stage: {level['emoji']} {level['stage']}")
        print(f"📝 Stage Info:   {level['description']}")
        print("=" * 65)
        print()

        print("🌟 PERSONALIZED INSPIRATION")
        print("-" * 30)
        for msg in payload["messages"]:
            print(f"✨ \"{msg}\"")
        print()

        print("💡 CUSTOM STUDY TIPS FOR THIS STAGE")
        print("-" * 35)
        for idx, tip in enumerate(payload["tips"], 1):
            print(f" {idx}. {tip}")
        print()

        print("💪 COACH'S ENCOURAGEMENT")
        print("-" * 30)
        print(payload["encouragement"])
        print()
        print("=" * 65)
        print(f"💾 Report saved successfully to: {self.report_file}")
        print("=" * 65)
        print()

    def export_report_to_markdown(self, level, payload):
        """
        Writes the motivation dashboard to a markdown file.

        Args:
            level (dict): Progress level info.
            payload (dict): Messages, tips, and encouragement details.
        """
        try:
            with open(self.report_file, "w", encoding="utf-8") as f:
                f.write(f"# 🎯 Study Motivation Report\n\n")
                f.write(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")

                f.write(f"## 📊 Progress Dashboard\n")
                f.write(f"- **Goal:** {self.study_goal}\n")
                f.write(f"- **Progress Percentage:** {self.progress_percentage}%\n")
                f.write(f"- **Progress Bar:** `{self.generate_progress_bar(self.progress_percentage)}`\n")
                f.write(f"- **Current Stage:** {level['emoji']} **{level['stage']}**\n\n")

                f.write(f"> **Stage Description:** {level['description']}\n\n")

                f.write(f"## 🌟 Personalized Inspiration\n")
                for msg in payload["messages"]:
                    f.write(f"- *\"{msg}\"*\n")
                f.write("\n")

                f.write(f"## 💡 Custom Study Tips for the {level['stage']}\n")
                for idx, tip in enumerate(payload["tips"], 1):
                    f.write(f"{idx}. {tip}\n")
                f.write("\n")

                f.write(f"## 💪 Coach's Encouragement\n")
                f.write(f"{payload['encouragement']}\n\n")

                f.write(f"---\n")
                f.write(f"*Keep going! Every effort counts toward mastering your goals. — AI Study Mentor Coach*\n")
        except IOError as e:
            print(f"❌ Failed to save motivation report: {e}")

    def run(self):
        """Main execution flow for the Motivation Agent."""
        self.collect_inputs()
        level = self.get_progress_level()
        payload = self.generate_motivation(level)
        self.display_report(level, payload)
        self.export_report_to_markdown(level, payload)


if __name__ == "__main__":
    agent = MotivationAgent()
    agent.run()
