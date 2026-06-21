#!/usr/bin/env python3
"""
Resource Finder Agent
---------------------
An interactive Python script that helps students and professionals find learning resources.
Categorizes resources into Beginner, Intermediate, and Advanced levels for five core subjects,
and supports dynamic web search query generation as a fallback for any custom subject.
"""

import os
from datetime import date
import urllib.parse

# Curated high-quality learning resources database
RESOURCES_DB = {
    "Artificial Intelligence": {
        "Beginner": [
            {
                "name": "AI for Everyone (Coursera)",
                "url": "https://www.coursera.org/learn/ai-for-everyone",
                "desc": "Non-technical introduction to AI concepts, workflows, and business strategy by Andrew Ng."
            },
            {
                "name": "Elements of AI",
                "url": "https://www.elementsofai.com/",
                "desc": "Free interactive online course covering foundations of AI and basic algorithms with no math required."
            },
            {
                "name": "Artificial Intelligence: A Modern Approach (Introductory Chapters)",
                "url": "http://aima.cs.berkeley.edu/",
                "desc": "The foundational chapters of the world's most popular AI textbook by Russell & Norvig."
            }
        ],
        "Intermediate": [
            {
                "name": "Intro to Artificial Intelligence (Udacity)",
                "url": "https://www.udacity.com/course/intro-to-artificial-intelligence--cs271",
                "desc": "Course covering logic, probabilistic reasoning, planning, machine learning, and game search."
            },
            {
                "name": "Berkeley CS188 Intro to AI",
                "url": "https://inst.eecs.berkeley.edu/~cs188/sp21/",
                "desc": "Highly recommended interactive programming assignments using Pacman to implement search and RL algorithms."
            },
            {
                "name": "Artificial Intelligence: A Modern Approach (Core Agent Sections)",
                "url": "http://aima.cs.berkeley.edu/",
                "desc": "Middle chapters of Russell & Norvig covering constraint satisfaction, knowledge representation, and planning."
            }
        ],
        "Advanced": [
            {
                "name": "Deep Learning Specialization (Coursera)",
                "url": "https://www.coursera.org/specializations/deep-learning",
                "desc": "Comprehensive deep-dive course series by DeepLearning.AI covering CNNs, RNNs, and Transformers."
            },
            {
                "name": "Spinning Up in Deep RL (OpenAI)",
                "url": "https://spinningup.openai.com/",
                "desc": "A premium educational resource for learning the concepts and implementation details of deep reinforcement learning."
            },
            {
                "name": "ArXiv CS.AI Section",
                "url": "https://arxiv.org/list/cs.AI/recent",
                "desc": "Repository of the latest research papers, preprints, and state-of-the-art advances in artificial intelligence."
            }
        ]
    },
    "Machine Learning": {
        "Beginner": [
            {
                "name": "Machine Learning Specialization (Coursera)",
                "url": "https://www.coursera.org/specializations/machine-learning-introduction",
                "desc": "The gold-standard foundational course series by Andrew Ng covering regression, classification, and unsupervised learning."
            },
            {
                "name": "Kaggle Learn - Intro to Machine Learning",
                "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
                "desc": "Free interactive notebook-based coding tutorials covering basic model building and validation."
            },
            {
                "name": "Introduction to Machine Learning with Python",
                "url": "https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/",
                "desc": "Practical, code-driven guide by Andreas Müller and Sarah Guido focusing on scikit-learn."
            }
        ],
        "Intermediate": [
            {
                "name": "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
                "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125837/",
                "desc": "Excellent book by Aurélien Géron that bridges ML concepts and engineering implementations."
            },
            {
                "name": "Machine Learning Zoomcamp (DataTalks.Club)",
                "url": "https://datatalks.club/courses/machine-learning-zoomcamp.html",
                "desc": "Free, hands-on, engineering-focused course teaching model training, deployment, and monitoring."
            },
            {
                "name": "Kaggle Competitions",
                "url": "https://www.kaggle.com/competitions",
                "desc": "Competitions and datasets where you can apply algorithms to real-world problems and learn from public notebooks."
            }
        ],
        "Advanced": [
            {
                "name": "Pattern Recognition and Machine Learning",
                "url": "https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf",
                "desc": "Comprehensive textbook by Christopher Bishop focusing on Bayesian methods and probabilistic ML theory."
            },
            {
                "name": "The Elements of Statistical Learning",
                "url": "https://hastie.su.domains/ElemStatLearn/",
                "desc": "A mathematically rigorous treatise on statistical machine learning by Hastie, Tibshirani, and Friedman."
            },
            {
                "name": "Stanford CS229 Lecture Notes & Videos",
                "url": "https://cs229.stanford.edu/",
                "desc": "Mathematical derivations of algorithms including SVMs, EM, kernel methods, and learning theory."
            }
        ]
    },
    "Data Science": {
        "Beginner": [
            {
                "name": "Google Data Analytics Certificate (Coursera)",
                "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
                "desc": "Introductory guide mapping spreadsheets, SQL, visualization, and R programming basics."
            },
            {
                "name": "Python for Data Analysis",
                "url": "https://wesmckinney.com/book/",
                "desc": "Practical guide written by Wes McKinney, the creator of the pandas library."
            },
            {
                "name": "DataCamp: Introduction to Data Science in Python",
                "url": "https://www.datacamp.com/courses/intro-to-data-science-in-python",
                "desc": "Interactive coding challenges introducing data structures, pandas, and matplotlib."
            }
        ],
        "Intermediate": [
            {
                "name": "Practical Statistics for Data Scientists",
                "url": "https://www.oreilly.com/library/view/practical-statistics-for/9781492072935/",
                "desc": "Useful guide by Bruce & Bruce focusing on applying statistical concepts directly to Python data workflows."
            },
            {
                "name": "Applied Data Science with Python (Coursera)",
                "url": "https://www.coursera.org/specializations/data-science-python",
                "desc": "University of Michigan's series focusing on data representation, charting, and text mining."
            },
            {
                "name": "DrivenData Competitions",
                "url": "https://www.drivendata.org/",
                "desc": "Platform hosting data science challenges with social impact themes (health, education, environment)."
            }
        ],
        "Advanced": [
            {
                "name": "Designing Data-Intensive Applications",
                "url": "https://www.oreilly.com/library/view/designing-data-intensive-applications/9781449373320/",
                "desc": "The industry bible by Martin Kleppmann on databases, consistency models, and distributed data systems."
            },
            {
                "name": "Advanced Data Science Specialization (Coursera)",
                "url": "https://www.coursera.org/specializations/advanced-data-science-ibm",
                "desc": "IBM series covering deep learning, signal processing, and big data scaling using Apache Spark."
            },
            {
                "name": "Towards Data Science & KDnuggets",
                "url": "https://towardsdatascience.com/",
                "desc": "Aggregated platforms featuring expert write-ups on state-of-the-art methodology and technical tutorials."
            }
        ]
    },
    "Python Programming": {
        "Beginner": [
            {
                "name": "Automate the Boring Stuff with Python",
                "url": "https://automatetheboringstuff.com/",
                "desc": "Highly practical programming book by Al Sweigart. Focuses on writing scripts to automate daily tasks."
            },
            {
                "name": "Python for Everybody (Coursera)",
                "url": "https://www.py4e.com/",
                "desc": "Accessible introduction to python programming, data structures, and database basics by Charles Severance."
            },
            {
                "name": "Official Python Tutorial",
                "url": "https://docs.python.org/3/tutorial/",
                "desc": "The official documentation's walkthrough of core syntax, standard libraries, and modules."
            }
        ],
        "Intermediate": [
            {
                "name": "Fluent Python",
                "url": "https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/",
                "desc": "Detailed guide by Luciano Ramalho explaining how to write clean, idiomatic Python using the language's best features."
            },
            {
                "name": "Corey Schafer's Python Playlist",
                "url": "https://www.youtube.com/c/CoreySchafer",
                "desc": "YouTube channel containing clear, comprehensive deep dives into OOP, decorators, databases, and scripting."
            },
            {
                "name": "Exercism - Python Track",
                "url": "https://exercism.org/tracks/python",
                "desc": "Hands-on programming platform with structured exercises and free mentorship code reviews."
            }
        ],
        "Advanced": [
            {
                "name": "Effective Python",
                "url": "https://effectivepython.com/",
                "desc": "Book by Brett Slatkin outlining 90 specific ways to write robust, efficient, and maintainable Python."
            },
            {
                "name": "Real Python Advanced Tutorials",
                "url": "https://realpython.com/tutorials/advanced/",
                "desc": "In-depth online tutorials covering concurrent programming, memory management, and compiler internals."
            },
            {
                "name": "Architecture Patterns with Python",
                "url": "https://www.cosmicpython.com/book/preface.html",
                "desc": "Online book showing how to implement Domain-Driven Design (DDD), Repository patterns, and Unit of Work in Python."
            }
        ]
    },
    "Interview Preparation": {
        "Beginner": [
            {
                "name": "Grokking Algorithms",
                "url": "https://www.manning.com/books/grokking-algorithms",
                "desc": "A heavily illustrated, friendly guide to data structures and algorithms by Aditya Bhargava."
            },
            {
                "name": "LeetCode (Explore Section)",
                "url": "https://leetcode.com/explore/",
                "desc": "Interactive cards covering elementary arrays, strings, stacks, queues, and tree traversal."
            },
            {
                "name": "NeetCode.io Beginners Roadmap",
                "url": "https://neetcode.io/practice",
                "desc": "Curated, structured layout for understanding basic data structures before doing hard problems."
            }
        ],
        "Intermediate": [
            {
                "name": "Cracking the Coding Interview",
                "url": "https://www.crackingthecodinginterview.com/",
                "desc": "The classic prep book by Gayle L. McDowell containing 189 programming questions and solutions."
            },
            {
                "name": "NeetCode 150",
                "url": "https://neetcode.io/practice",
                "desc": "A carefully curated set of 150 LeetCode problems covering all major categories (graphs, DP, trees, etc.)."
            },
            {
                "name": "Pramp / Interviewing.io",
                "url": "https://www.pramp.com/",
                "desc": "Platforms offering peer-to-peer or expert-level mock technical interviews to practice explaining your code."
            }
        ],
        "Advanced": [
            {
                "name": "LeetCode (Hard Level)",
                "url": "https://leetcode.com/problemset/all/?difficulty=HARD",
                "desc": "Practice environment for complex algorithmic problems (sliding windows, segment trees, hard dynamic programming)."
            },
            {
                "name": "System Design Interview - An Insider's Guide",
                "url": "https://bytebytego.com/",
                "desc": "Alex Xu's highly visual guides explaining how to design large-scale web systems (load balancers, chats, storage)."
            },
            {
                "name": "Tech Interview Handbook",
                "url": "https://techinterviewhandbook.org/",
                "desc": "Open-source handbook by Yangshun Tay covering advanced behavioral answers, resumes, and cheat sheets."
            }
        ]
    }
}


class ResourceFinderAgent:
    """
    Agent responsible for taking a user's subject query, matching it against
    a curated database, and generating helpful links, fallback search options,
    and a Markdown summary document.
    """

    def __init__(self):
        self.subject = ""
        self.predefined_subjects = list(RESOURCES_DB.keys())

    def clear_screen(self):
        """Clears the terminal screen for clean presentation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints a styled terminal header for the Resource Finder Agent."""
        print("=" * 60)
        print("         🎓 AI STUDY MENTOR - RESOURCE FINDER AGENT 🎓         ")
        print("=" * 60)
        print()

    def get_valid_string(self, prompt_text):
        """Helper to ensure a non-empty string is entered."""
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            print("❌ Input cannot be empty. Please try again.")

    def collect_input(self):
        """Displays menu, maps choices, or grabs a custom topic input."""
        self.clear_screen()
        self.print_header()
        
        print("Welcome! Let's discover high-quality learning resources.")
        print("-" * 60)
        print("Predefined Curated Subjects:")
        for idx, subj in enumerate(self.predefined_subjects, 1):
            print(f"  {idx}. {subj}")
        print("  6. [Search Custom Subject/Topic]")
        print("-" * 60)

        while True:
            choice = self.get_valid_string("👉 Select an option (1-6) or enter your topic name: ")
            
            # Check if input matches predefined indexes
            if choice.isdigit():
                val = int(choice)
                if 1 <= val <= len(self.predefined_subjects):
                    self.subject = self.predefined_subjects[val - 1]
                    break
                elif val == 6:
                    self.subject = self.get_valid_string("\n📚 Enter the custom subject/topic name: ")
                    break
                else:
                    print(f"❌ Invalid selection. Please enter a number between 1 and 6.")
            else:
                # Direct entry of a string
                self.subject = choice
                break
                
        print(f"\n🔍 Searching resources for: '{self.subject}'...")

    def search_resources(self, subject):
        """
        Searches the curated database. Returns resources if found.
        Performs case-insensitive matching and partial matching.
        """
        normalized_subj = subject.strip().lower()

        # 1. Exact match check
        for db_subj in RESOURCES_DB:
            if db_subj.lower() == normalized_subj:
                return db_subj, RESOURCES_DB[db_subj]

        # 2. Substring match check
        partial_matches = []
        for db_subj in RESOURCES_DB:
            if normalized_subj in db_subj.lower() or db_subj.lower() in normalized_subj:
                partial_matches.append(db_subj)

        # If exactly one partial match is found, use it
        if len(partial_matches) == 1:
            matched_subj = partial_matches[0]
            print(f"💡 Matching '{subject}' with curated category: '{matched_subj}'")
            return matched_subj, RESOURCES_DB[matched_subj]
        elif len(partial_matches) > 1:
            print(f"💡 Multiple curated subjects match your search:")
            for i, match in enumerate(partial_matches, 1):
                print(f"   {i}. {match}")
            while True:
                select = self.get_valid_string(f"Select match (1-{len(partial_matches)}) or press Enter to run fallback search: ")
                if not select:
                    break
                if select.isdigit():
                    val = int(select)
                    if 1 <= val <= len(partial_matches):
                        matched_subj = partial_matches[val - 1]
                        return matched_subj, RESOURCES_DB[matched_subj]
                print("❌ Invalid selection.")

        # 3. If no matches, generate fallbacks dynamically
        return subject, self.generate_fallback(subject)

    def generate_fallback(self, subject):
        """
        Dynamically generates structured learning platform query links
        as resources for topics not present in the curated database.
        """
        # URL encode subject for safety
        encoded = urllib.parse.quote_plus(subject)

        # Build dynamic queries targeting beginner, intermediate, and advanced levels
        fallback_resources = {
            "Beginner": [
                {
                    "name": f"Introductory Courses on {subject} (Coursera)",
                    "url": f"https://www.coursera.org/search?query=Introduction+to+{encoded}",
                    "desc": "Academic foundation courses covering the basics of the topic."
                },
                {
                    "name": f"Beginner Video Guides on {subject} (YouTube)",
                    "url": f"https://www.youtube.com/results?search_query={encoded}+tutorial+for+beginners",
                    "desc": "Curated search for foundational visual guides and step-by-step introductions."
                },
                {
                    "name": f"Introduction to {subject} (edX)",
                    "url": f"https://www.edx.org/search?q={encoded}",
                    "desc": "University and enterprise courses starting from the basics."
                }
            ],
            "Intermediate": [
                {
                    "name": f"Intermediate Projects and Concepts on {subject} (YouTube)",
                    "url": f"https://www.youtube.com/results?search_query={encoded}+crash+course+project",
                    "desc": "Hands-on coding walkthroughs and project implementation tutorials."
                },
                {
                    "name": f"Open Source {subject} Projects (GitHub)",
                    "url": f"https://github.com/search?q={encoded}+topic%3Aproject",
                    "desc": "Search repositories related to this topic to read real code and project setups."
                },
                {
                    "name": f"Intermediate Courses on {subject} (Coursera)",
                    "url": f"https://www.coursera.org/search?query={encoded}",
                    "desc": "Deep dives into practical workflows and standard libraries."
                }
            ],
            "Advanced": [
                {
                    "name": f"Advanced Techniques and Architecture of {subject} (GitHub)",
                    "url": f"https://github.com/search?q=advanced+{encoded}",
                    "desc": "Search repositories containing libraries, developer tools, and best-practice templates."
                },
                {
                    "name": f"Expert and Advanced Design Patterns for {subject} (YouTube)",
                    "url": f"https://www.youtube.com/results?search_query=advanced+{encoded}+architecture+design+patterns",
                    "desc": "Visual breakdowns of large-scale architecture, internals, and expert concepts."
                },
                {
                    "name": f"Academic and Research Papers on {subject} (Google Scholar)",
                    "url": f"https://scholar.google.com/scholar?q={encoded}",
                    "desc": "Google Scholar search for highly cited academic papers and breakthroughs."
                }
            ]
        }
        return fallback_resources

    def display_results(self, subject, resources):
        """Prints the curated or generated learning resources on the terminal."""
        self.clear_screen()
        self.print_header()

        print(f"🗺️  RECOMMENDED RESOURCES FOR: {subject.upper()}")
        print("=" * 60)
        print()

        for level in ["Beginner", "Intermediate", "Advanced"]:
            print(f"🌟 {level.upper()} LEVEL RESOURCES")
            print("-" * 40)
            for item in resources[level]:
                print(f"🔗 Name: {item['name']}")
                print(f"   URL:  {item['url']}")
                print(f"   Note: {item['desc']}")
                print()
            print("-" * 60)
            print()

        print("=" * 60)
        print("💾 A detailed Markdown page has been saved to: learning_resources.md")
        print("=" * 60)
        print()

    def export_to_markdown(self, subject, resources):
        """Saves the output as a formatted Markdown document in the workspace."""
        content = []
        content.append(f"# Recommended Resources: {subject}")
        content.append(f"Generated on {date.today().strftime('%B %d, %Y')}\n")
        
        content.append("Use these curated learning pathways to gain mastery from foundation to advanced system design.\n")

        for level in ["Beginner", "Intermediate", "Advanced"]:
            content.append(f"## 🌟 {level} Level")
            content.append("| Resource / Course | Platform/Link | Description |")
            content.append("|---|---|---|")
            for item in resources[level]:
                # Format url nicely
                link_text = item['name']
                url = item['url']
                desc = item['desc']
                content.append(f"| **{link_text}** | [Link]({url}) | {desc} |")
            content.append("\n")

        content.append("## 💡 Learning Strategies")
        content.append("1. **Pacing**: Dedicate consistent time blocks instead of cramming. Standard daily splits help retention.")
        content.append("2. **Active Recall**: Test yourself. Close the documentation or code editor and try to draft the architecture/syntax from scratch.")
        content.append("3. **Projects**: For intermediate and advanced levels, start building hands-on tools. Check the GitHub search links to find layouts.")
        content.append("4. **Documentation**: Make official documentations your primary source of truth.")

        with open("learning_resources.md", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    def run(self):
        """Execution flow of the agent."""
        self.collect_input()
        final_subj, resources = self.search_resources(self.subject)
        self.display_results(final_subj, resources)
        self.export_to_markdown(final_subj, resources)


if __name__ == "__main__":
    agent = ResourceFinderAgent()
    agent.run()
