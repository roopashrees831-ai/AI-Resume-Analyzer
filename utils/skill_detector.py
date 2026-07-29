skills_database = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "react",
    "node.js",
    "git",
    "github",
    "streamlit",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "data science",
    "power bi",
    "excel"
]

def detect_skills(text):

    resume_text = text.lower()

    detected_skills = []

    for skill in skills_database:
        if skill in resume_text:
            detected_skills.append(skill.title())

    return detected_skills