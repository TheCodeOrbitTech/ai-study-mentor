from study_planner import StudyPlannerAgent
from resource_finder import ResourceFinderAgent
from progress_tracker import ProgressTrackerAgent
from career_guidance import CareerGuidanceAgent
from motivation_agent import MotivationAgent


def main():

    while True:
        print("\n" + "=" * 60)
        print("🎓 AI STUDY MENTOR - MULTI AGENT SYSTEM")
        print("=" * 60)

        print("1. Study Planner Agent")
        print("2. Resource Finder Agent")
        print("3. Progress Tracker Agent")
        print("4. Career Guidance Agent")
        print("5. Motivation Agent")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            StudyPlannerAgent().run()

        elif choice == "2":
            ResourceFinderAgent().run()

        elif choice == "3":
            ProgressTrackerAgent().run()

        elif choice == "4":
            CareerGuidanceAgent().run()

        elif choice == "5":
            MotivationAgent().run()

        elif choice == "6":
            print("Thank you for using AI Study Mentor!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()