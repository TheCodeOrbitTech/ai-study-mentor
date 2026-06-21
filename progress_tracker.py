#!/usr/bin/env python3
"""
Progress Tracker Agent
---------------------
An interactive Python CLI tool to track and visualize study progress.
Calculates completion percentage, remaining topics, and exports report files.
"""

import os
import json
import math
from datetime import datetime


class ProgressTrackerAgent:
    """
    Agent responsible for tracking learning progress across multiple subjects.
    Provides CLI menus, validates input metrics, generates ASCII progress bars,
    and exports persistent reports.
    """

    def __init__(self, data_file="study_progress.json", report_file="progress_report.md"):
        """
        Initializes the Progress Tracker Agent.
        
        Args:
            data_file (str): Filename for saving raw state (JSON format).
            report_file (str): Filename for saving the human-readable dashboard (Markdown format).
        """
        self.data_file = data_file
        self.report_file = report_file
        self.subjects_data = {}
        self.load_progress()

    def clear_screen(self):
        """Clears the terminal screen for a clean presentation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints a styled terminal header for the Progress Tracker Agent."""
        print("=" * 65)
        print("        🎓 AI STUDY MENTOR - PROGRESS TRACKER AGENT 🎓        ")
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

    def get_valid_integer(self, prompt_text, min_val=0, max_val=None):
        """
        Helper to request and validate an integer input within a specified range.
        
        Args:
            prompt_text (str): The prompt message to show the user.
            min_val (int): Minimum acceptable value (inclusive).
            max_val (int, optional): Maximum acceptable value (inclusive).
            
        Returns:
            int: Verified integer value.
        """
        while True:
            val = input(prompt_text).strip()
            try:
                num = int(val)
                if num < min_val:
                    print(f"❌ Value must be at least {min_val}.")
                    continue
                if max_val is not None and num > max_val:
                    print(f"❌ Value cannot exceed {max_val}.")
                    continue
                return num
            except ValueError:
                print("❌ Invalid input. Please enter a valid integer.")

    def load_progress(self):
        """Loads subjects progress from the local JSON file if it exists."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.subjects_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("⚠️  Warning: Progress file was corrupted or couldn't be read. Starting fresh.")
                self.subjects_data = {}
        else:
            self.subjects_data = {}

    def save_progress(self):
        """Saves current subjects progress to the local JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.subjects_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Failed to save progress data to file: {e}")

    def calculate_metrics(self, total_topics, completed_topics):
        """
        Calculates remaining topics and completion percentage.
        
        Args:
            total_topics (int): Total number of topics.
            completed_topics (int): Number of completed topics.
            
        Returns:
            tuple: (remaining_topics (int), completion_percentage (float))
        """
        if total_topics <= 0:
            return 0, 0.0
            
        remaining = total_topics - completed_topics
        percentage = (completed_topics / total_topics) * 100
        # Round to 1 decimal place
        percentage = round(percentage, 1)
        
        return remaining, percentage

    def generate_progress_bar(self, percentage, width=20):
        """
        Generates an ASCII progress bar representing the percentage.
        
        Args:
            percentage (float): Completion percentage (0 to 100).
            width (int): Character width of the progress bar.
            
        Returns:
            str: An ASCII progress bar e.g. '[██████░░░░░░]'
        """
        # Ensure percentage is within bounds
        percentage = max(0.0, min(100.0, percentage))
        completed_blocks = int(round((percentage / 100.0) * width))
        remaining_blocks = width - completed_blocks
        
        # Build bar string using solid block block '█' and shaded block '░'
        bar = "█" * completed_blocks + "░" * remaining_blocks
        return f"[{bar}]"

    def add_new_subject(self):
        """Prompts user to add a new subject and its associated topic metrics."""
        self.clear_screen()
        self.print_header()
        print("📚 TRACK NEW SUBJECT PROGRESS")
        print("-" * 65)
        
        # 1. Ask for Subject Name
        subject = self.get_valid_string("👉 Enter subject name (e.g., Data Science): ")
        
        # Check if subject already exists
        if subject.lower() in [s.lower() for s in self.subjects_data]:
            print(f"\n⚠️  Subject '{subject}' is already being tracked!")
            print("💡 Use the 'Update Progress' option in the main menu to modify it.")
            input("\nPress Enter to return to main menu...")
            return

        # 2. Ask for Total Topics
        print("\n🔢 Total topics/units in this subject?")
        total_topics = self.get_valid_integer("👉 Enter total topics: ", min_val=1)
        
        # 3. Ask for Completed Topics
        print(f"\n✅ How many topics have you completed so far? (0 to {total_topics})")
        completed_topics = self.get_valid_integer("👉 Enter completed topics: ", min_val=0, max_val=total_topics)
        
        # Calculate initial metrics
        remaining, percentage = self.calculate_metrics(total_topics, completed_topics)
        
        # Store data
        self.subjects_data[subject] = {
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save state and update reports
        self.save_progress()
        self.export_markdown_report()
        
        # Success visual feedback
        print("\n🎉 Subject added successfully!")
        print("-" * 40)
        print(f"📊 Progress: {self.generate_progress_bar(percentage)} {percentage}%")
        print(f"👉 Completed {completed_topics}/{total_topics} topics ({remaining} remaining).")
        print("-" * 40)
        
        input("\nPress Enter to return to main menu...")

    def update_existing_subject(self):
        """Lists existing subjects and allows updating their completed topics."""
        self.clear_screen()
        self.print_header()
        print("🔄 UPDATE SUBJECT PROGRESS")
        print("-" * 65)
        
        if not self.subjects_data:
            print("📭 No subjects currently tracked. Add a subject first!")
            input("\nPress Enter to return to main menu...")
            return

        # List subjects for selection
        subjects_list = list(self.subjects_data.keys())
        for idx, subj in enumerate(subjects_list, 1):
            data = self.subjects_data[subj]
            _, pct = self.calculate_metrics(data["total_topics"], data["completed_topics"])
            print(f"  {idx}. {subj:<25} {self.generate_progress_bar(pct, width=12)} {pct}%")
        print("-" * 65)
        
        # Select Subject
        choice = self.get_valid_integer("👉 Select a subject number to update (or 0 to cancel): ", min_val=0, max_val=len(subjects_list))
        if choice == 0:
            return
            
        selected_subject = subjects_list[choice - 1]
        data = self.subjects_data[selected_subject]
        
        print(f"\nUpdating: {selected_subject}")
        print(f"Current completion: {data['completed_topics']} out of {data['total_topics']} topics.")
        
        # Input new completed topics
        new_completed = self.get_valid_integer(
            f"👉 Enter new completed topics (0 to {data['total_topics']}): ",
            min_val=0,
            max_val=data["total_topics"]
        )
        
        # Update details
        data["completed_topics"] = new_completed
        data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subjects_data[selected_subject] = data
        
        # Save state and update reports
        self.save_progress()
        self.export_markdown_report()
        
        # Calculate new metrics for display
        remaining, percentage = self.calculate_metrics(data["total_topics"], new_completed)
        
        print("\n✅ Progress updated successfully!")
        print("-" * 40)
        print(f"📊 New Progress: {self.generate_progress_bar(percentage)} {percentage}%")
        print(f"👉 Completed {new_completed}/{data['total_topics']} topics ({remaining} remaining).")
        print("-" * 40)
        
        input("\nPress Enter to return to main menu...")

    def display_dashboard(self):
        """Displays the progress summary dashboard of all subjects in the console."""
        self.clear_screen()
        self.print_header()
        print("📊 STUDY PROGRESS DASHBOARD")
        print("=" * 65)
        
        if not self.subjects_data:
            print("📭 No progress data found. Choose Option 1 to start tracking!")
            print("=" * 65)
            input("\nPress Enter to return to main menu...")
            return

        total_global_topics = 0
        total_global_completed = 0
        
        # Print metrics for each subject
        for subj, data in self.subjects_data.items():
            tot = data["total_topics"]
            comp = data["completed_topics"]
            rem, pct = self.calculate_metrics(tot, comp)
            
            total_global_topics += tot
            total_global_completed += comp
            
            print(f"📚 Subject: {subj}")
            print(f"   Progress:  {self.generate_progress_bar(pct, width=25)} {pct}%")
            print(f"   Topics:    {comp} completed / {tot} total ({rem} remaining)")
            print(f"   Updated:   {data.get('last_updated', 'N/A')}")
            print("-" * 65)

        # Global Statistics
        _, global_pct = self.calculate_metrics(total_global_topics, total_global_completed)
        global_rem = total_global_topics - total_global_completed
        
        print("\n📈 OVERALL METRICS")
        print("=" * 65)
        print(f"Overall Progress: {self.generate_progress_bar(global_pct, width=25)} {global_pct}%")
        print(f"Total Completed:  {total_global_completed} / {total_global_topics} topics across all subjects")
        print(f"Total Remaining:  {global_rem} topics")
        print("=" * 65)
        print(f"💾 Report saved to: {self.report_file}")
        print("=" * 65)
        
        input("\nPress Enter to return to main menu...")

    def export_markdown_report(self):
        """Exports the subjects progress metrics into a stylized Markdown file."""
        if not self.subjects_data:
            return

        content = []
        content.append("# 📈 Study Progress Report")
        content.append(f"Generated on: {datetime.now().strftime('%B %d, %Y - %H:%M:%S')}\n")
        
        content.append("## 📊 Subjects Overview")
        content.append("| Subject | Progress Bar | Completed | Total | Remaining | Completion % | Last Updated |")
        content.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |")
        
        total_global_topics = 0
        total_global_completed = 0
        
        for subj, data in self.subjects_data.items():
            tot = data["total_topics"]
            comp = data["completed_topics"]
            rem, pct = self.calculate_metrics(tot, comp)
            
            total_global_topics += tot
            total_global_completed += comp
            
            # Form markdown friendly progress bar
            # Uses filled and empty blocks inside markdown
            bar_width = 10
            filled = int(round((pct / 100.0) * bar_width))
            empty = bar_width - filled
            md_bar = f"`{'█' * filled}{'░' * empty}`"
            
            content.append(f"| **{subj}** | {md_bar} | {comp} | {tot} | {rem} | {pct}% | {data.get('last_updated', 'N/A')} |")
            
        content.append("\n")
        
        # Calculate Global summary
        _, global_pct = self.calculate_metrics(total_global_topics, total_global_completed)
        global_rem = total_global_topics - total_global_completed
        
        # Overall Summary Section
        content.append("## 📈 Overall Summary Statistics")
        content.append(f"- **Total Subjects Tracked:** {len(self.subjects_data)}")
        content.append(f"- **Total Completed Topics:** {total_global_completed} topics")
        content.append(f"- **Total Topics to Learn:** {total_global_topics} topics")
        content.append(f"- **Total Remaining Topics:** {global_rem} topics")
        
        # Add visual global progress bar
        global_filled = int(round((global_pct / 100.0) * 20))
        global_empty = 20 - global_filled
        global_bar = f"`{'█' * global_filled}{'░' * global_empty}`"
        content.append(f"- **Overall Completion Rate:** {global_bar} **{global_pct}%**\n")
        
        # Motivational Section based on progress levels
        content.append("## 💡 Study Coach Advice")
        if global_pct == 100.0:
            content.append("🎉 **Outstanding!** You have completed 100% of all tracked topics! Give yourself a reward and keep testing your knowledge via active recall.")
        elif global_pct >= 75.0:
            content.append("🚀 **Almost there!** You are in the home stretch with over 75% completion. Focus on the remaining complex topics and prepare for practice exams.")
        elif global_pct >= 40.0:
            content.append("⚡ **Great momentum!** You are making steady progress. Keep up the consistent daily study schedule and review older topics once a week.")
        else:
            content.append("🌱 **Beginning your journey!** You are laying the foundation. Focus on establishing a solid study habit, start with small goals, and avoid burnout.")
            
        try:
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
        except IOError as e:
            print(f"❌ Failed to write Markdown report: {e}")

    def run(self):
        """Main execution loop for the CLI agent."""
        while True:
            self.clear_screen()
            self.print_header()
            print("Main Menu:")
            print("  1. 📚 Add a New Subject")
            print("  2. 🔄 Update Progress of an Existing Subject")
            print("  3. 📊 View Progress Dashboard")
            print("  4. 🚪 Exit")
            print("-" * 65)
            
            choice = self.get_valid_integer("👉 Select an option (1-4): ", min_val=1, max_val=4)
            
            if choice == 1:
                self.add_new_subject()
            elif choice == 2:
                self.update_existing_subject()
            elif choice == 3:
                self.display_dashboard()
            elif choice == 4:
                print("\n👋 Thank you for using AI Study Mentor! Keep up the good work.")
                break


if __name__ == "__main__":
    agent = ProgressTrackerAgent()
    agent.run()
