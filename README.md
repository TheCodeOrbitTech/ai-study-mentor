# AI Study Mentor

AI Study Mentor is a collection of interactive Python CLI tools designed to help students, developers, and professionals structure and optimize their learning journeys. It currently includes five specialized agents:

1.  **Study Planner Agent (`study_planner.py`)**: Analyzes study availability, target date, and topics to generate a personalized roadmap with daily study templates and weekly milestones.
2.  **Resource Finder Agent (`resource_finder.py`)**: Interactively takes a subject or topic and recommends categorized learning resources (Beginner, Intermediate, Advanced) with descriptions and direct links.
3.  **Progress Tracker Agent (`progress_tracker.py`)**: Tracks study progress across multiple subjects, calculates completion rates, maintains persistent logs, and exports a progress dashboard.
4.  **Career Guidance Agent (`career_guidance.py`)**: Gathers user interest, skills, and goals to suggest matching career paths, analyze skill gaps, and generate step-by-step learning roadmaps.
5.  **Motivation Agent (`motivation_agent.py`)**: Prompts for study progress percentage and goals, providing progress-level based motivational quotes, tailored study tips, and custom encouragement dashboards.

---

## 🚀 Features

### 📅 Study Planner Agent
-   **Interactive Setup**: Prompts for subject name, daily study availability, and target deadline.
-   **Dynamic Time Calculations**: Computes exact days, weeks, and total study hours remaining.
-   **Topic Distribution**: Evenly distributes your study chapters across the available weeks.
-   **Structured Routines**: Generates hourly daily breakdowns using productivity practices (e.g., Pomodoro blocks).
-   **Persistent Exports**: Saves a customized Markdown plan (`study_plan.md`) in your workspace.

### 🔍 Resource Finder Agent
-   **Predefined Subjects**: Instant access to curated, high-quality resources for core subjects:
    -   *Artificial Intelligence*
    -   *Machine Learning*
    -   *Data Science*
    -   *Python Programming*
    -   *Interview Preparation*
-   **Fuzzy Matching**: Intelligent matching logic that maps sub-topics (e.g., "python" or "interview") to the closest curated categories.
-   **Dynamic Fallback Search**: Generates structured, clickable search queries targeting beginner, intermediate, and advanced queries on major learning platforms (Coursera, edX, YouTube, GitHub, Google Scholar) if a custom topic is entered.
-   **Persistent Exports**: Exports recommendations to `learning_resources.md` for offline reference.

### 📈 Progress Tracker Agent
-   **Multi-Subject Tracking**: Allows tracking multiple subjects simultaneously.
-   **Interactive Updates**: Add a new subject or update the number of completed topics for an existing subject.
-   **ASCII Progress Visuals**: Generates visual progress bars (e.g., `[████████░░░░░░░░]`) in the console for each subject and for overall progress.
-   **Automatic Metrics**: Computes completion percentages (rounded to 1 decimal place) and remaining topics automatically.
-   **Dual Exports**: Saves raw state to `study_progress.json` and compiles a beautiful Markdown dashboard to `progress_report.md` with personalized study recommendations.

### 💼 Career Guidance Agent
-   **Matchmaking Engine**: Matches user interests and career goals with standard database paths or custom fallback pathways.
-   **Skill Gap Analysis**: Compares current user skills against target career requirements to identify acquired and missing skills.
-   **Actionable Roadmaps**: Generates a structured multi-phase study guide to build necessary skills.
-   **Markdown Export**: Exports matching results and learning paths to `career_recommendation.md`.

### 🔥 Motivation Agent
-   **Goal-Driven Prompts**: Prompts for study goals and current progress percentage.
-   **Progress Categorization**: Maps completion levels into 6 distinct stages (Starting Block, Foundation, Momentum, Valley of Persistence, Home Stretch, Champion's Circle).
-   **Tailored Encouragement**: Generates stage-specific study tips (e.g. Feynman technique, Pomodoro habit loops), inspirational quotes, and personalized advice.
-   **ASCII Progress Indicator**: Visualizes current achievement with console-rendered progress bars.
-   **Motivation Report**: Generates `study_motivation.md` with structured highlights of recommendations.

---

## 🛠️ Technologies Used

-   **Python 3.x**: Core scripting language.
-   **Standard Library Modules**:
    -   `os`: Terminal screen management.
    -   `json`: Save and load study progress state.
    -   `datetime`: Real-time target date parsing and timestamps.
    -   `math`: Rounding and progress bar width calculation.
    -   `urllib.parse`: Safe URL encoding for dynamic fallback searches.
    -   `unittest`: Test framework for automated verification.

---

## 📦 Installation Steps

1.  **Prerequisites**: Ensure you have Python 3 installed. Check your version by running:
    ```bash
    python --version
    ```
2.  **Navigate to the Directory**:
    ```bash
    cd "ai study mentor"
    ```

---

## 🏃 How to Run the Programs

### Run the Study Planner Agent
```bash
python study_planner.py
```

### Run the Resource Finder Agent
```bash
python resource_finder.py
```

### Run the Progress Tracker Agent
```bash
python progress_tracker.py
```

### Run the Career Guidance Agent
```bash
python career_guidance.py
```

### Run the Motivation Agent
```bash
python motivation_agent.py
```

### Run the Automated Test Suite
To run the automated tests validating the agents' backend calculations:
```bash
# Test Study Planner Agent
python test_planner.py

# Test Resource Finder Agent
python test_finder.py

# Test Progress Tracker Agent
python test_tracker.py

# Test Career Guidance Agent
python test_career.py

# Test Motivation Agent
python test_motivation.py
```

---

## 📝 Example Usage: Resource Finder Agent

### 1. Predefined Topic Selection
When launching `resource_finder.py`, select from the menu:
```text
============================================================
         🎓 AI STUDY MENTOR - RESOURCE FINDER AGENT 🎓         
============================================================

Welcome! Let's discover high-quality learning resources.
------------------------------------------------------------
Predefined Curated Subjects:
  1. Artificial Intelligence
  2. Machine Learning
  3. Data Science
  4. Python Programming
  5. Interview Preparation
  6. [Search Custom Subject/Topic]
------------------------------------------------------------
👉 Select an option (1-6) or enter your topic name: 4
```

This generates `learning_resources.md` with curated Python books (like *Fluent Python* and *Effective Python*), websites, and interactive courses.

### 2. Custom Topic Fallback
If you choose `6` or enter a custom topic like `Docker`, the agent generates dynamic links:
```markdown
# Recommended Resources: Docker

## 🌟 Beginner Level
| Resource / Course | Platform/Link | Description |
|---|---|---|
| **Introductory Courses on Docker (Coursera)** | [Link](https://www.coursera.org/search?query=Introduction+to+Docker) | Academic foundation courses covering the basics of the topic. |
| **Beginner Video Guides on Docker (YouTube)** | [Link](https://www.youtube.com/results?search_query=Docker+tutorial+for+beginners) | Curated search for foundational visual guides and step-by-step introductions. |
```
## Privacy and Security

The AI Study Mentor project prioritizes user privacy and secure data handling.

### Security Features
- Input validation is implemented to prevent invalid or malicious user inputs.
- Date validation ensures users enter future target dates only.
- Study hours are restricted to realistic values (0.1 to 24 hours).
- Error handling mechanisms prevent application crashes caused by invalid inputs.

### Privacy Policy
- This project does not collect, store, or share personal information with third parties.
- All user data is processed locally on the user's device.
- Generated study plans and progress reports remain under the user's control.

### Best Practices
- Users should avoid entering sensitive personal information.
- Future versions may include authentication and encrypted storage for enhanced security.
