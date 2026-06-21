#!/usr/bin/env python3
"""
Career Guidance Agent
---------------------
An interactive Python script that gathers user interest, current skills,
and career goals, suggests matching career paths, calculates skill gaps,
and generates a structured learning roadmap.
"""

import os
from datetime import date


# Curated knowledge base of career paths, required skills, and roadmap phases.
CAREER_DATABASE = {
    "Machine Learning Engineer": {
        "description": "Designs, builds, and deploys machine learning models and systems to solve complex problems.",
        "area_keywords": ["ai", "ml", "artificial intelligence", "machine learning", "data science"],
        "required_skills": ["Python", "Mathematics", "Machine Learning", "Deep Learning", "SQL", "Git", "TensorFlow/PyTorch", "Docker"],
        "roadmap": [
            {
                "phase": "Phase 1: Mathematics & Programming Foundations",
                "focus": "Master Python basics, data structures, Git, and essential math (Linear Algebra, Calculus, Statistics)."
            },
            {
                "phase": "Phase 2: Core Machine Learning & Data Manipulation",
                "focus": "Learn Pandas, NumPy, Scikit-Learn, regression, classification, clustering, and data preprocessing."
            },
            {
                "phase": "Phase 3: Deep Learning & Frameworks",
                "focus": "Study neural networks, CNNs, RNNs, Transformers, and master either PyTorch or TensorFlow."
            },
            {
                "phase": "Phase 4: Deployment & MLOps",
                "focus": "Learn containerization with Docker, model serving APIs (FastAPI/Flask), cloud deployment (AWS/GCP), and CI/CD."
            }
        ]
    },
    "Data Scientist": {
        "description": "Analyzes complex datasets to extract insights, build predictive models, and guide business decisions.",
        "area_keywords": ["data science", "statistics", "data analytics", "analysis", "analytics"],
        "required_skills": ["Python", "SQL", "Statistics", "Data Visualization", "Machine Learning", "Tableau/PowerBI", "Pandas/NumPy"],
        "roadmap": [
            {
                "phase": "Phase 1: Programming & SQL Foundations",
                "focus": "Learn Python scripting, SQL query writing, relational database concepts, and version control with Git."
            },
            {
                "phase": "Phase 2: Data Wrangling & Applied Statistics",
                "focus": "Master Pandas/NumPy, data cleaning, exploratory data analysis (EDA), probability distributions, and hypothesis testing."
            },
            {
                "phase": "Phase 3: Machine Learning & Feature Engineering",
                "focus": "Study supervised and unsupervised ML algorithms, model evaluation metrics, and feature selection."
            },
            {
                "phase": "Phase 4: Data Storytelling & Business Intelligence",
                "focus": "Learn Tableau, PowerBI, Matplotlib/Seaborn, and how to communicate data findings to stakeholders."
            }
        ]
    },
    "Frontend Developer": {
        "description": "Builds the visual elements and interactive user interface of websites and web applications.",
        "area_keywords": ["web development", "frontend", "web design", "javascript", "ui/ux", "web"],
        "required_skills": ["HTML", "CSS", "JavaScript", "React/Vue/Angular", "Git", "Responsive Design", "Web APIs"],
        "roadmap": [
            {
                "phase": "Phase 1: Semantic Markup & Modern Styling",
                "focus": "Master semantic HTML5, modern CSS3 layouts (Flexbox, Grid), responsive design, and CSS frameworks (Bootstrap/Tailwind)."
            },
            {
                "phase": "Phase 2: JavaScript Foundations & DOM Manipulation",
                "focus": "Learn ES6+ syntax, asynchronous programming (Promises, Async/Await), and fetching data from Web APIs."
            },
            {
                "phase": "Phase 3: Frontend Frameworks & State Management",
                "focus": "Choose a framework (React, Vue, or Angular) and master its ecosystem, routing, state management, and component architecture."
            },
            {
                "phase": "Phase 4: Build Tools & Hosting",
                "focus": "Get familiar with Node package managers (NPM/Yarn), build tools (Vite/Webpack), unit testing, and deploy to Vercel/Netlify."
            }
        ]
    },
    "Backend Developer": {
        "description": "Constructs the server-side logic, databases, API architectures, and system infrastructure of web applications.",
        "area_keywords": ["web development", "backend", "databases", "software development", "api", "web"],
        "required_skills": ["Python/Node.js/Go", "SQL/NoSQL Databases", "RESTful APIs", "Git", "Docker", "System Design", "Linux"],
        "roadmap": [
            {
                "phase": "Phase 1: Backend Language Syntax",
                "focus": "Learn server-side programming (Python/Django/FastAPI, Node.js/Express, or Go) and OOP / asynchronous paradigms."
            },
            {
                "phase": "Phase 2: Database Management & Querying",
                "focus": "Master SQL databases (PostgreSQL/MySQL), relational schema design, indexing, and NoSQL databases (MongoDB)."
            },
            {
                "phase": "Phase 3: API Design & Authentication",
                "focus": "Learn RESTful and GraphQL API design principles, authentication protocols (JWT, OAuth2), and security best practices."
            },
            {
                "phase": "Phase 4: Architecture, Containers & Hosting",
                "focus": "Study basic system design patterns, caching (Redis), containerization (Docker), and cloud servers (AWS EC2, Heroku)."
            }
        ]
    },
    "Cybersecurity Analyst": {
        "description": "Monitors, detects, and defends organizations against cyber threats, vulnerabilities, and network security breaches.",
        "area_keywords": ["security", "cybersecurity", "networking", "information security", "networks"],
        "required_skills": ["Networking (TCP/IP)", "Linux", "Security Tools (Wireshark, Nmap)", "Python", "Incident Response", "Cryptography"],
        "roadmap": [
            {
                "phase": "Phase 1: Computer Networking & OS Fundamentals",
                "focus": "Master TCP/IP protocols, subnetting, network configurations, and basic Linux administration."
            },
            {
                "phase": "Phase 2: Cybersecurity Concepts & Cryptography",
                "focus": "Understand cryptography principles, threat landscapes, common attack vectors, firewalls, and IAM principles."
            },
            {
                "phase": "Phase 3: Security Tools & Vulnerability Scanning",
                "focus": "Learn to use packet analyzers (Wireshark), port scanners (Nmap), and vulnerability scanners (Nessus)."
            },
            {
                "phase": "Phase 4: Incident Response & Penetration Testing",
                "focus": "Study log analysis, incident remediation procedures, basic ethical hacking, and industry compliance frameworks (SOC2, ISO27001)."
            }
        ]
    },
    "Cloud Engineer": {
        "description": "Designs, implements, and maintains cloud computing environments and infrastructure architectures.",
        "area_keywords": ["cloud", "cloud computing", "aws", "azure", "infrastructure", "devops"],
        "required_skills": ["Linux", "AWS/Azure/GCP", "Terraform (IaC)", "Docker", "CI/CD", "Python/Bash", "Kubernetes"],
        "roadmap": [
            {
                "phase": "Phase 1: Linux Administration & Shell Scripting",
                "focus": "Master Linux CLI tools, user permissions, networking tools, and script automation using Bash or Python."
            },
            {
                "phase": "Phase 2: Cloud Architecture Foundations",
                "focus": "Choose a cloud vendor (AWS, Azure, GCP) and learn compute (EC2/VM), storage (S3/Blob), IAM, and VPC networking."
            },
            {
                "phase": "Phase 3: Infrastructure as Code & Containers",
                "focus": "Learn containerization with Docker and provisioning cloud infrastructure declaratively using Terraform."
            },
            {
                "phase": "Phase 4: DevOps Pipelines & Orchestration",
                "focus": "Implement CI/CD automation pipelines (GitHub Actions/Jenkins) and container orchestration using Kubernetes."
            }
        ]
    },
    "DevOps Engineer": {
        "description": "Bridges the gap between software development and IT operations by automating builds, deployments, and systems integration.",
        "area_keywords": ["devops", "ci/cd", "infrastructure", "deployment", "automation", "kubernetes"],
        "required_skills": ["Git", "CI/CD (GitHub Actions, Jenkins)", "Docker", "Kubernetes", "Linux", "Python/Bash", "Monitoring (Prometheus, Grafana)"],
        "roadmap": [
            {
                "phase": "Phase 1: Linux Systems & Version Control",
                "focus": "Deep dive into Linux administration, scripting, and advanced version control workflows with Git."
            },
            {
                "phase": "Phase 2: Continuous Integration & Deployment (CI/CD)",
                "focus": "Build pipelines to automate building, testing, and deployment (GitHub Actions, GitLab CI, or Jenkins)."
            },
            {
                "phase": "Phase 3: Containers & Orchestration",
                "focus": "Learn containerization workflows with Docker and deployment orchestration using Kubernetes (K8s) clusters."
            },
            {
                "phase": "Phase 4: Infrastructure monitoring & SRE",
                "focus": "Implement monitoring dashboards (Prometheus, Grafana), logging stacks (ELK), and study Site Reliability Engineering (SRE) principles."
            }
        ]
    },
    "Mobile App Developer": {
        "description": "Develops application software designed specifically to run on smartphones and tablets.",
        "area_keywords": ["mobile", "android", "ios", "swift", "kotlin", "flutter", "react native"],
        "required_skills": ["Swift/Kotlin/Flutter/React Native", "Git", "Mobile UI Design", "REST APIs", "App Store/Play Store deployment"],
        "roadmap": [
            {
                "phase": "Phase 1: Core Mobile Development Language",
                "focus": "Learn native coding (Swift for iOS, Kotlin for Android) or cross-platform framework languages (Dart for Flutter, JavaScript for React Native)."
            },
            {
                "phase": "Phase 2: UI Design & Layouts",
                "focus": "Study mobile design paradigms, navigation flows, styling structures, responsiveness, and state management frameworks."
            },
            {
                "phase": "Phase 3: Core API Integration & Storage",
                "focus": "Integrate REST APIs, parse JSON, manage device sensors/features, and set up offline storage (SQLite, Room, CoreData)."
            },
            {
                "phase": "Phase 4: Testing & App Store Submission",
                "focus": "Run automated device testing, configure build settings, package apps, and navigate the App Store / Google Play publishing guidelines."
            }
        ]
    }
}


class CareerGuidanceAgent:
    """
    Agent responsible for collecting user parameters, scoring and matching
    them with career paths, performing skill gap analysis, and generating
    roadmaps.
    """

    def __init__(self):
        self.area_of_interest = ""
        self.skills = []
        self.career_goal = ""

    def clear_screen(self):
        """Clears the terminal screen for clean presentation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints a styled terminal header for the Career Guidance Agent."""
        print("=" * 65)
        print("        🎓 AI STUDY MENTOR - CAREER GUIDANCE AGENT 🎓        ")
        print("=" * 65)
        print()

    def get_valid_string(self, prompt_text):
        """Helper to ensure a non-empty string is entered."""
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            print("❌ Input cannot be empty. Please try again.")

    def collect_inputs(self):
        """Interactively requests and validates input parameters from the user."""
        self.clear_screen()
        self.print_header()

        print("Welcome! Let's map out your career path and learning roadmap.")
        print("-" * 65)

        # 1. Ask for Area of Interest
        self.area_of_interest = self.get_valid_string("💼 Enter your general area of interest (e.g. AI, Web Dev, Security): ")

        # 2. Ask for current skills
        skills_input = self.get_valid_string("🛠️  Enter your current skills (separated by commas, e.g. Python, SQL, Git): ")
        self.skills = [s.strip() for s in skills_input.split(",") if s.strip()]

        # 3. Ask for career goal
        self.career_goal = self.get_valid_string("🎯 Enter your career goal (e.g. Become a Machine Learning Engineer): ")

        print("\n✅ All inputs collected successfully! Analyzing your data...")

    def match_career(self):
        """
        Scores career paths based on keyword overlaps in Area of Interest,
        Career Goal, and matching current skills. Selects the best match.
        If the match score is low, triggers a dynamic fallback path generation.
        """
        best_score = -1
        best_match_name = None
        
        normalized_interest = self.area_of_interest.lower()
        normalized_goal = self.career_goal.lower()
        normalized_user_skills = {s.lower() for s in self.skills}

        for path_name, data in CAREER_DATABASE.items():
            score = 0
            
            # 1. Check goal matches path name (high weight)
            normalized_path_name = path_name.lower()
            if normalized_path_name in normalized_goal or normalized_goal in normalized_path_name:
                score += 8
            
            # Check individual keywords from path name in goal
            path_words = normalized_path_name.split()
            for pw in path_words:
                if len(pw) > 3 and pw in normalized_goal:
                    score += 2

            # 2. Check area keyword match (medium weight)
            for kw in data["area_keywords"]:
                if kw in normalized_interest or kw in normalized_goal:
                    score += 4

            # 3. Skill alignment (low weight per skill)
            for skill in data["required_skills"]:
                if skill.lower() in normalized_user_skills:
                    score += 1

            if score > best_score:
                best_score = score
                best_match_name = path_name

        # If the best match score is extremely low (e.g. < 3), we generate a dynamic fallback.
        if best_score < 3:
            return self.generate_dynamic_fallback()
        else:
            curated_path = CAREER_DATABASE[best_match_name]
            return {
                "name": best_match_name,
                "description": curated_path["description"],
                "required_skills": curated_path["required_skills"],
                "roadmap": curated_path["roadmap"],
                "score": best_score,
                "is_curated": True
            }

    def generate_dynamic_fallback(self):
        """
        Dynamically synthesizes required skills and a roadmap tailored to the
        user's inputs when no close curated match is found.
        """
        goal = self.career_goal.strip()
        interest = self.area_of_interest.strip().lower()
        goal_lower = goal.lower()

        # Build dynamic skills based on keyword matching
        dynamic_skills = []
        
        # Web development keywords
        if any(kw in goal_lower or kw in interest for kw in ["web", "front", "back", "react", "html", "api", "server", "website"]):
            dynamic_skills.extend(["HTML", "CSS", "JavaScript", "Git"])
            if "front" in goal_lower or "react" in goal_lower or "ui" in goal_lower:
                dynamic_skills.extend(["React/Vue", "Responsive Design", "Web APIs"])
            elif "back" in goal_lower or "server" in goal_lower or "api" in goal_lower or "database" in goal_lower:
                dynamic_skills.extend(["Databases (SQL)", "RESTful APIs", "Server scripting"])
            else:
                dynamic_skills.extend(["Web APIs", "Databases (SQL)", "Web Application Architecture"])
        
        # Data / AI / ML keywords
        elif any(kw in goal_lower or kw in interest for kw in ["data", "ml", "ai", "machine", "deep", "analyst", "statistic"]):
            dynamic_skills.extend(["Python", "SQL", "Statistics", "Git", "Pandas/NumPy"])
            if "ml" in goal_lower or "machine" in goal_lower or "deep" in goal_lower or "ai" in goal_lower:
                dynamic_skills.extend(["Machine Learning algorithms", "TensorFlow/PyTorch", "Model Evaluation"])
            else:
                dynamic_skills.extend(["Data Visualization (Tableau/Seaborn)", "Exploratory Data Analysis"])
        
        # Security / Network keywords
        elif any(kw in goal_lower or kw in interest for kw in ["security", "cyber", "network", "hack", "penetration", "defend"]):
            dynamic_skills.extend(["Networking (TCP/IP)", "Linux", "Security tools", "Incident response", "Cryptography"])
        
        # Cloud / DevOps keywords
        elif any(kw in goal_lower or kw in interest for kw in ["cloud", "devops", "aws", "azure", "kubernetes", "docker", "pipeline"]):
            dynamic_skills.extend(["Linux", "AWS/Azure/GCP", "Docker", "Kubernetes", "CI/CD pipelines", "Git"])
        
        # Mobile app keywords
        elif any(kw in goal_lower or kw in interest for kw in ["mobile", "android", "ios", "app", "swift", "kotlin", "flutter"]):
            dynamic_skills.extend(["Swift/Kotlin/Flutter", "Git", "Mobile UI Layouts", "REST APIs", "App Store deployment"])

        # Default fallback skills if nothing matches
        else:
            dynamic_skills.extend(["Programming Fundamentals", "Data Structures", "Algorithms", "Git", "Software Design"])

        # Add any skills from current interest/goal words that look like technical words
        # (Filter out very short words and common English words)
        candidate_words = [w.capitalize() for w in (goal.split() + interest.split()) 
                           if len(w) > 3 and w.lower() not in ["become", "want", "learn", "need", "like", "love", "developer", "engineer", "analyst"]]
        for word in candidate_words:
            if word not in dynamic_skills and len(dynamic_skills) < 8:
                dynamic_skills.append(word)

        # Ensure unique elements
        unique_skills = []
        for s in dynamic_skills:
            if s not in unique_skills:
                unique_skills.append(s)
        
        # Create dynamic roadmap phases
        dynamic_roadmap = [
            {
                "phase": f"Phase 1: Foundations of {goal}",
                "focus": f"Learn foundational programming syntax, essential math or theory, and basic version control (Git) relevant to {goal}."
            },
            {
                "phase": "Phase 2: Core Tools & Database Systems",
                "focus": "Master core application libraries, package managers, and databases or scripting tools required for daily workflows."
            },
            {
                "phase": "Phase 3: Project Building & Hands-on Implementation",
                "focus": f"Build 2-3 end-to-end practical projects that simulate a real-world environment for a {goal}."
            },
            {
                "phase": "Phase 4: Advanced Optimizations & Career Readiness",
                "focus": "Learn advanced design patterns, system testing, resume formulation, and start practicing technical interviews."
            }
        ]

        return {
            "name": goal,
            "description": f"Tailored pathway designed to help you transition into your career goal: '{goal}'.",
            "required_skills": unique_skills,
            "roadmap": dynamic_roadmap,
            "score": 0,
            "is_curated": False
        }

    def analyze_skill_gap(self, required_skills):
        """
        Splits skills into 'acquired' (user already possesses them)
        and 'missing' (skills user needs to learn).
        """
        user_skills_set = {s.lower().strip() for s in self.skills}
        acquired = []
        missing = []

        for skill in required_skills:
            # Check for substring match (e.g. 'Python' in user skills list)
            match_found = False
            for us in user_skills_set:
                if us in skill.lower() or skill.lower() in us:
                    match_found = True
                    break
            
            if match_found:
                acquired.append(skill)
            else:
                missing.append(skill)

        return acquired, missing

    def display_recommendations(self, recommendation, acquired, missing):
        """Prints the career roadmap and skill analysis to the terminal."""
        self.clear_screen()
        self.print_header()

        print("🗺️  YOUR CUSTOM CAREER GUIDE GENERATED")
        print("=" * 65)
        print(f"🎯 Career Goal:     {self.career_goal}")
        print(f"💼 Area Interest:   {self.area_of_interest}")
        print(f"🛣️  Suggested Path:  {recommendation['name']}")
        print(f"🔍 Path Status:     {'[Curated Match]' if recommendation['is_curated'] else '[Synthesized Fallback]'}")
        print(f"📝 Description:     {recommendation['description']}")
        print("=" * 65)
        print()

        # Print Skill Analysis
        print("🛠️  SKILL GAP ANALYSIS")
        print("-" * 35)
        print("✅ Relevant Skills You Have:")
        if acquired:
            for s in acquired:
                print(f"   • {s}")
        else:
            print("   (None identified for this target path yet)")
        print()

        print("🚨 Skills to Acquire (Gap):")
        if missing:
            for s in missing:
                print(f"   • {s}")
        else:
            print("   🎉 Awesome! You possess all core skills listed for this path.")
        print()

        # Print Roadmap
        print("📅 ACTIONABLE LEARNING ROADMAP")
        print("-" * 35)
        for step in recommendation["roadmap"]:
            print(f"📍 {step['phase']}")
            print(f"   └─ Focus: {step['focus']}")
            print()
        print("=" * 65)
        print("💾 A detailed Markdown guide has been saved to: career_recommendation.md")
        print("=" * 65)
        print()

    def export_to_markdown(self, recommendation, acquired, missing):
        """Writes the career roadmap to a markdown file for persistent usage."""
        content = []
        content.append(f"# Career Roadmap & Guidance Report")
        content.append(f"Generated on {date.today().strftime('%B %d, %Y')}\n")
        
        content.append("## 🎯 Profile Overview")
        content.append(f"- **Career Goal:** {self.career_goal}")
        content.append(f"- **Area of Interest:** {self.area_of_interest}")
        content.append(f"- **Suggested Career Path:** {recommendation['name']}")
        content.append(f"- **Path Type:** {'Curated Database Match' if recommendation['is_curated'] else 'Custom Synthesized Path'}")
        content.append(f"- **Description:** {recommendation['description']}\n")
        
        content.append("## 🛠️ Skill Gap Analysis")
        content.append("Evaluating your skills against the core requirements for this career path:")
        content.append("\n### ✅ Acquired Skills")
        if acquired:
            for s in acquired:
                content.append(f"- **{s}** (Already present in your profile)")
        else:
            content.append("- *No overlapping skills identified yet.*")
        
        content.append("\n### 🚨 Skill Gap (To Acquire)")
        if missing:
            for s in missing:
                content.append(f"- **{s}** (Recommended to learn)")
        else:
            content.append("- *🎉 None! You already possess the key skills for this path.*")
        content.append("\n")
        
        content.append("## 📅 Step-by-Step Learning Roadmap")
        content.append("Follow these structured phases to bridge your skills gap and attain your career goal:\n")
        
        for idx, step in enumerate(recommendation["roadmap"], 1):
            content.append(f"### {step['phase']}")
            content.append(f"{step['focus']}\n")
            
        content.append("## 💡 General Career Advice")
        content.append("1. **Build Projects**: Theoretical knowledge is good, but building projects cements your skills and showcases your abilities to recruiters.")
        content.append("2. **Contribute to Open Source**: Learn Git early and collaborate with others on platforms like GitHub.")
        content.append("3. **Networking**: Connect with industry experts on LinkedIn, attend local meetups, and find mentors in your target area.")
        content.append("4. **Continuous Learning**: Technologies evolve. Stay curious and update your skills regularly.")

        with open("career_recommendation.md", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    def run(self):
        """Execution entrypoint for the agent."""
        self.collect_inputs()
        recommendation = self.match_career()
        acquired, missing = self.analyze_skill_gap(recommendation["required_skills"])
        
        # Display recommendations in terminal
        self.display_recommendations(recommendation, acquired, missing)
        
        # Save recommendations to markdown file
        self.export_to_markdown(recommendation, acquired, missing)


if __name__ == "__main__":
    agent = CareerGuidanceAgent()
    agent.run()
