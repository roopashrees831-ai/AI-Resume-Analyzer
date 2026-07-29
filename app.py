import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_detector import detect_skills, skills_database
from utils.resume_parser import (
    extract_contact_details,
    extract_education
)

# -------------------------------
# Load Groq API
# -------------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get an instant AI-powered analysis.")

# -------------------------------
# Upload Resume
# -------------------------------
uploaded_file = st.file_uploader(
    "Choose Resume (PDF)",
    type=["pdf"]
)

# -------------------------------
# After Upload
# -------------------------------
if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)

    # Contact Details
    name, email, phone = extract_contact_details(text)

    # Education
    education = extract_education(text)

    st.success("✅ Resume Uploaded Successfully")

    # ---------------------------------
    # Candidate Information
    # ---------------------------------

    st.subheader("👤 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")

    with col2:
        st.write(f"**Phone:** {phone}")

    st.subheader("🎓 Education")

    if education:
        for edu in education:
            st.write(f"• {edu}")
    else:
        st.write("Education details not detected.")

    # ---------------------------------
    # Resume Content
    # ---------------------------------

    st.subheader("📄 Extracted Resume")

    st.text_area(
        "Resume Content",
        text,
        height=250
    )

    # ---------------------------------
    # Skills
    # ---------------------------------

    detected_skills = detect_skills(text)

    st.subheader("🛠 Skills Detected")

    if detected_skills:
        st.success(", ".join(detected_skills))
    else:
        st.warning("No matching skills found.")

    # ---------------------------------
    # Resume Score
    # ---------------------------------

    score = min(len(detected_skills) * 5, 100)

    st.subheader("📊 Resume Score")

    st.progress(score)

    st.metric(
        "Resume Score",
        f"{score}/100"
    )

    if score >= 80:
        st.balloons()

    # ---------------------------------
    # Missing Skills
    # ---------------------------------

    st.subheader("⚠️ Missing Skills")

    missing_skills = []

    for skill in skills_database:
        if skill.title() not in detected_skills:
            missing_skills.append(skill.title())

    if missing_skills:
        st.write(", ".join(missing_skills[:10]))
    else:
        st.success("Excellent! No important skills are missing.")

    # ---------------------------------
    # AI Suggestions (Groq)
    # ---------------------------------

    st.subheader("🤖 AI Suggestions")

    try:

        prompt = f"""
You are an expert Resume Reviewer.

Analyze the following resume and provide:

1. Resume Summary
2. Top Strengths
3. Weaknesses
4. Missing Skills
5. 5 Professional Suggestions
6. Final Verdict

Resume:

{text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Groq Error: {e}")

    # ---------------------------------
    # General Suggestions
    # ---------------------------------

    st.subheader("💡 General Suggestions")

    if score >= 80:

        st.success("""
Excellent Resume!

Keep improving by adding:

• New Projects
• Certifications
• Achievements
• Leadership Experience
""")

    elif score >= 60:

        st.info("""
Good Resume.

Suggestions:

• Add more technical skills
• Include certifications
• Mention measurable achievements
• Add GitHub & LinkedIn links
""")

    else:

        st.warning("""
Your resume needs improvement.

Suggestions:

• Add technical skills
• Mention projects
• Include internships
• Add certifications
• Improve formatting
• Quantify achievements
""")