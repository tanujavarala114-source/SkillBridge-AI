
from flask import Flask, render_template, request
import sqlite3
import fitz
import re

from database import create_database, save_analysis, get_history

app = Flask(__name__)

# --------------------------------
# 1. CAREER ROLE REQUIREMENTS
# --------------------------------

CAREER_ROLES = {
    "Data Analyst": {
        "skills": [
            "python", "sql", "excel", "pandas",
            "numpy", "statistics", "power bi",
            "data visualization"
        ],
        "projects": [
            "Sales Data Analysis Dashboard",
            "Customer Behavior Analysis",
            "Student Performance Analysis"
        ]
    },

    "Python Developer": {
        "skills": [
            "python", "sql", "git", "flask",
            "html", "css", "api", "debugging"
        ],
        "projects": [
            "Task Management Web App",
            "Student Record Management System",
            "REST API using Flask"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python", "numpy", "pandas", "scikit-learn",
            "statistics", "machine learning",
            "data preprocessing", "model evaluation"
        ],
        "projects": [
            "House Price Prediction",
            "Customer Churn Prediction",
            "Image Classification System"
        ]
    },

    "Web Developer": {
        "skills": [
            "html", "css", "javascript", "python",
            "flask", "sql", "git", "api"
        ],
        "projects": [
            "Personal Portfolio Website",
            "Online Bookstore",
            "Student Management Website"
        ]
    }
}


# --------------------------------
# 2. NLP SKILL SYNONYMS
# --------------------------------

SKILL_SYNONYMS = {
    "python": [
        "python programming",
        "python language"
    ],

    "machine learning": [
        "ml",
        "machine-learning"
    ],

    "scikit-learn": [
        "sklearn",
        "scikit learn"
    ],

    "data preprocessing": [
        "data cleaning",
        "preprocessing",
        "data pre-processing"
    ],

    "model evaluation": [
        "model validation",
        "evaluation metrics",
        "model performance evaluation"
    ],

    "statistics": [
        "statistical analysis"
    ],

    "power bi": [
        "powerbi"
    ],

    "data visualization": [
        "data visualisation",
        "data viz"
    ],

    "sql": [
        "structured query language"
    ],

    "javascript": [
        "js"
    ]
}


# --------------------------------
# 3. EXTRACT PDF TEXT
# --------------------------------

def extract_resume_text(file):

    document = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


# --------------------------------
# 4. FIND SKILLS USING NLP ALIASES
# --------------------------------

def find_skills(text, required_skills):

    text = text.lower()

    found = []

    for skill in required_skills:

        aliases = SKILL_SYNONYMS.get(skill, [])

        all_names = [skill] + aliases

        for name in all_names:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(name)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):

                found.append(skill)
                break

    return found


# --------------------------------
# 5. CREATE LEARNING ROADMAP
# --------------------------------

def create_roadmap(missing_skills):

    roadmap = []

    for number, skill in enumerate(
        missing_skills, start=1
    ):

        roadmap.append({
            "week": number,
            "skill": skill.title(),
            "task": (
                f"Learn {skill.title()} basics "
                "and complete a practical exercise."
            )
        })

    return roadmap

# --------------------------------
# 5. PERSONALIZED LEARNING RESOURCES
# --------------------------------

LEARNING_RESOURCES = {

    "python": {
        "title": "Python Official Tutorial",
        "url": "https://docs.python.org/3/tutorial/"
    },

    "numpy": {
        "title": "NumPy Learning Resources",
        "url": "https://numpy.org/learn/"
    },

    "pandas": {
        "title": "Pandas Getting Started Tutorials",
        "url": "https://pandas.pydata.org/docs/getting_started/"
    },

    "scikit-learn": {
        "title": "Scikit-learn User Guide",
        "url": "https://scikit-learn.org/stable/user_guide.html"
    },

    "statistics": {
        "title": "Khan Academy Statistics",
        "url": "https://www.khanacademy.org/math/statistics-probability"
    },

    "machine learning": {
        "title": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course"
    },

    "data preprocessing": {
        "title": "Scikit-learn Preprocessing Guide",
        "url": "https://scikit-learn.org/stable/modules/preprocessing.html"
    },

    "model evaluation": {
        "title": "Model Evaluation Guide",
        "url": "https://scikit-learn.org/stable/modules/model_evaluation.html"
    },

    "sql": {
        "title": "SQL Tutorial",
        "url": "https://www.w3schools.com/sql/"
    },

    "excel": {
        "title": "Microsoft Excel Training",
        "url": "https://support.microsoft.com/en-us/excel"
    },

    "power bi": {
        "title": "Microsoft Power BI Learning",
        "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"
    },

    "data visualization": {
        "title": "Matplotlib Tutorials",
        "url": "https://matplotlib.org/stable/tutorials/"
    },

    "git": {
        "title": "Git Official Documentation",
        "url": "https://git-scm.com/doc"
    },

    "flask": {
        "title": "Flask Documentation",
        "url": "https://flask.palletsprojects.com/en/stable/tutorial/"
    },

    "html": {
        "title": "HTML Learning Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/HTML"
    },

    "css": {
        "title": "CSS Learning Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/CSS"
    },

    "javascript": {
        "title": "JavaScript Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
    },

    "api": {
        "title": "REST API Learning Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP"
    },

    "debugging": {
        "title": "Python Debugging Guide",
        "url": "https://docs.python.org/3/library/pdb.html"
    }
}


# --------------------------------
# 6. CREATE PERSONALIZED ROADMAP
# --------------------------------

def create_roadmap(missing_skills):

    roadmap = []

    for number, skill in enumerate(
        missing_skills, start=1
    ):

        resource = LEARNING_RESOURCES.get(
            skill,
            {
                "title": "Search Learning Tutorials",
                "url": "https://www.google.com/search?q="
                       + skill.replace(" ", "+")
                       + "+tutorial"
            }
        )

        roadmap.append({

            "week": number,

            "skill": skill.title(),

            "task": (
                f"Learn {skill.title()} basics "
                "and complete a practical exercise."
            ),

            "resource_title": resource["title"],

            "resource_url": resource["url"]

        })

    return roadmap



# --------------------------------
# 6. HOME PAGE
# --------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        role = request.form.get("role", "")
        resume_file = request.files.get("resume")

        resume_text = request.form.get(
            "resume_text", ""
        ).strip()

        # Validate career role

        if role not in CAREER_ROLES:

            error = "Please select a valid career role."

        # Read uploaded PDF

        elif resume_file and resume_file.filename:

            if not resume_file.filename.lower().endswith(".pdf"):

                error = "Please upload a PDF resume."

            else:

                try:

                    resume_text = extract_resume_text(
                        resume_file
                    )

                    if not resume_text.strip():

                        error = (
                            "No readable text found. "
                            "Try a text-based PDF or "
                            "enter your skills manually."
                        )

                except Exception:

                    error = (
                        "Unable to read this PDF. "
                        "Please try another file."
                    )

        # Check manual input

        if not error and not resume_text:

            error = (
                "Please upload a resume or "
                "enter your skills manually."
            )

        # Perform skill analysis

        if not error:

            required_skills = CAREER_ROLES[role]["skills"]

            found = find_skills(
                resume_text,
                required_skills
            )

            missing = [
                skill for skill in required_skills
                if skill not in found
            ]

            score = round(
                (len(found) / len(required_skills)) * 100
            )

            result = {
                "role": role,
                "score": score,
                "found": found,
                "missing": missing,
                "projects": CAREER_ROLES[role]["projects"],
                "roadmap": create_roadmap(missing)
            }

            # Save analysis to SQLite

            save_analysis(
                role,
                score,
                found,
                missing
            )

    # Fetch previous analysis records

    history = get_history()

    # Always return a valid webpage

    return render_template(
        "index.html",
        roles=CAREER_ROLES,
        result=result,
        error=error,
        history=history
    )


# --------------------------------
# 7. START APPLICATION
# --------------------------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)
