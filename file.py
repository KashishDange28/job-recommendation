'''import streamlit as st
from resume import ResumePDF, generate_resume_content
import tempfile
import os
from PIL import Image
import pandas as pd

st.set_page_config(page_title="AI Resume + Job Matcher", page_icon="📝", layout="centered")

# Sidebar with a decorative image and title
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100)
st.sidebar.title("👩‍🎓 Rural Women's Upliftment")
st.sidebar.info("Empowering girls like Amina Begum with opportunities! 💪")

st.title("📝 AI Resume Generator + 🎯 Job Matcher (Powered by Gemini)")

# --- Dummy user profile ---
user_profile = {
    "name": "Amina Begum",
    "age": 19,
    "education": "Completed secondary education from Government Girls School, Barabanki, UP",
    "skills": ["Tailoring", "Basic Computer", "Communication"],
    "experience": "Helped run a small tailoring unit in her village and conducted local computer literacy workshops for young girls.",
    "courses": [
        {"course_name": "Digital Literacy for Women", "marks": "87%", "date": "2024-10-15"},
        {"course_name": "Entrepreneurship Basics", "marks": "91%", "date": "2025-02-20"}
    ],
    "profile_photo": "village_girl_photo.png"  # Replace with a real path
}

# Convert photo if available
if user_profile["profile_photo"] and os.path.exists(user_profile["profile_photo"]):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
        image = Image.open(user_profile["profile_photo"]).convert("RGB")
        image.save(tmpfile, format="JPEG")
        user_profile["profile_photo"] = tmpfile.name
else:
    user_profile["profile_photo"] = ""

# --- Display Profile Section ---
st.markdown("### 👤 Candidate Profile")

col1, col2 = st.columns([1, 3])
if user_profile["profile_photo"]:
    col1.image(user_profile["profile_photo"], caption="Amina Begum", width=100)
else:
    col1.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)

col2.markdown(f"**Name:** {user_profile['name']}")
col2.markdown(f"**Age:** {user_profile['age']}")
col2.markdown(f"**Education:** {user_profile['education']}")
col2.markdown(f"**Skills:** {', '.join(user_profile['skills'])}")
col2.markdown(f"**Experience:** {user_profile['experience']}")

# --- Generate Resume ---
st.markdown("### 📄 Resume Generation")
resume_text = generate_resume_content(user_profile)

structured_resume = {
    "name": user_profile["name"],
    "profile_photo": user_profile.get("profile_photo", ""),
    "summary": resume_text.split("**Professional Summary**")[-1].split("**Education**")[0].strip()
        if "**Professional Summary**" in resume_text else "A hardworking and aspiring girl from a rural background with a strong will to learn and grow.",
    "education": user_profile["education"],
    "skills": user_profile["skills"],
    "experience": user_profile["experience"],
    "courses": user_profile["courses"],
    "languages": ["Hindi", "English"]
}

pdf = ResumePDF()
pdf.print_resume(structured_resume)
output_filename = f"{user_profile['name'].lower().replace(' ', '_')}_resume.pdf"
pdf.output(output_filename)

with open(output_filename, "rb") as f:
    st.download_button("📥 Download Amina's Resume", f, file_name=output_filename)

st.success("✅ Resume generated successfully!")

# --- Load Job Data ---
st.markdown("---")
st.markdown("### 🔍 Matching Jobs Based on Skills")

csv_file_path = 'rural_women_jobs_dataset_expanded.csv'
df_jobs = pd.read_csv(csv_file_path)
df_jobs["Skill"] = df_jobs["Skill"].fillna("").astype(str)

def match_jobs(user_skills):
    matched_jobs = []
    for _, row in df_jobs.iterrows():
        job_skills = row['Skill'].split(", ")
        match_count = len(set(user_skills).intersection(set(job_skills)))

        if match_count > 0:
            matched_jobs.append({
                "job_title": row.get("Job Title", "Unknown"),
                "company": row.get("Company", "Unknown"),
                "platform": row.get("Platform", "N/A"),
                "location": row.get("Location", "N/A"),
                "salary_range": row.get("Salary Range", "N/A"),
                "job_type": row.get("Job Type", "N/A"),
                "match_count": match_count
            })

    return sorted(matched_jobs, key=lambda x: x["match_count"], reverse=True)

matched_jobs = match_jobs(user_profile["skills"])

if matched_jobs:
    for job in matched_jobs[:5]:
        with st.container():
            st.markdown(f"#### 🧵 {job['job_title']} at {job['company']}")
            st.markdown(f"📍 **Location:** {job['location']}")
            st.markdown(f"💼 **Platform:** {job['platform']} | **Type:** {job['job_type']}")
            st.markdown(f"💰 **Salary:** {job['salary_range']}")
            st.markdown(f"✅ **Matching Skills:** {job['match_count']}")
            st.markdown("---")
else:
    st.warning("😕 No matching jobs found. Consider adding more skills or courses.")
'''

import streamlit as st
from resume import ResumePDF, generate_resume_content
import tempfile
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Resume + Job Matcher", page_icon="📝", layout="centered")

# Sidebar with a decorative image and title
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100)
st.sidebar.title("👩‍🎓 Rural Women's Upliftment")
st.sidebar.info("Empowering girls like Amina Begum with opportunities! 💪")

st.title("📝 AI Resume Generator + 🎯 Job Matcher (Powered by Gemini)")

# --- Dummy user profile ---
user_profile = {
    "name": "Amina Begum",
    "age": 19,
    "education": "Completed secondary education from Government Girls School, Barabanki, UP",
    "skills": ["Tailoring", "Basic Computer", "Communication"],
    "experience": "Helped run a small tailoring unit in her village and conducted local computer literacy workshops for young girls.",
    "courses": [
        {"course_name": "Digital Literacy for Women", "marks": "87%", "date": "2024-10-15"},
        {"course_name": "Entrepreneurship Basics", "marks": "91%", "date": "2025-02-20"}
    ],
    "profile_photo": "village_girl_photo.png"  # Replace with a real path
}

# Convert photo if available
if user_profile["profile_photo"] and os.path.exists(user_profile["profile_photo"]):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
        image = Image.open(user_profile["profile_photo"]).convert("RGB")
        image.save(tmpfile, format="JPEG")
        user_profile["profile_photo"] = tmpfile.name
else:
    user_profile["profile_photo"] = ""

# --- Display Profile Section ---
st.markdown("### 👤 Candidate Profile")

col1, col2 = st.columns([1, 3])
if user_profile["profile_photo"]:
    col1.image(user_profile["profile_photo"], caption="Amina Begum", width=100)
else:
    col1.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)

col2.markdown(f"**Name:** {user_profile['name']}")
col2.markdown(f"**Age:** {user_profile['age']}")
col2.markdown(f"**Education:** {user_profile['education']}")
col2.markdown(f"**Skills:** {', '.join(user_profile['skills'])}")
col2.markdown(f"**Experience:** {user_profile['experience']}")

# --- Generate Resume ---
st.markdown("### 📄 Resume Generation")
resume_text = generate_resume_content(user_profile)

structured_resume = {
    "name": user_profile["name"],
    "profile_photo": user_profile.get("profile_photo", ""),
    "summary": resume_text.split("**Professional Summary**")[-1].split("**Education**")[0].strip()
        if "**Professional Summary**" in resume_text else "A hardworking and aspiring girl from a rural background with a strong will to learn and grow.",
    "education": user_profile["education"],
    "skills": user_profile["skills"],
    "experience": user_profile["experience"],
    "courses": user_profile["courses"],
    "languages": ["Hindi", "English"]
}

pdf = ResumePDF()
pdf.print_resume(structured_resume)
output_filename = f"{user_profile['name'].lower().replace(' ', '_')}_resume.pdf"
pdf.output(output_filename)

with open(output_filename, "rb") as f:
    st.download_button("📥 Download Amina's Resume", f, file_name=output_filename)

st.success("✅ Resume generated successfully!")

# --- Load Job Data ---
st.markdown("---")
st.markdown("### 🔍 Matching Jobs Based on Skills")

csv_file_path = 'rural_women_jobs_dataset_expanded.csv'
df_jobs = pd.read_csv(csv_file_path)
df_jobs["Skill"] = df_jobs["Skill"].fillna("").astype(str)

# Job Matcher + Report Generator Function
def generate_job_report(user_profile, df_jobs):
    st.markdown("## 📊 Match Insights + Career Suggestions")

    matched_jobs = []
    skill_match_chart = {}

    for _, row in df_jobs.iterrows():
        job_skills = row['Skill'].split(", ")
        match_count = len(set(user_profile["skills"]).intersection(set(job_skills)))
        if match_count > 0:
            matched_jobs.append({
                "job_title": row.get("Job Title", "Unknown"),
                "company": row.get("Company", "Unknown"),
                "platform": row.get("Platform", "N/A"),
                "location": row.get("Location", "N/A"),
                "salary_range": row.get("Salary Range", "N/A"),
                "job_type": row.get("Job Type", "N/A"),
                "required_skills": job_skills,
                "match_count": match_count
            })

            for skill in set(user_profile["skills"]).intersection(set(job_skills)):
                skill_match_chart[skill] = skill_match_chart.get(skill, 0) + 1

    matched_jobs = sorted(matched_jobs, key=lambda x: x["match_count"], reverse=True)

    # 🎨 Pie Chart for Skills Matched
    if skill_match_chart:
        st.markdown("### 🎨 Skill Match Distribution")
        fig, ax = plt.subplots()
        ax.pie(skill_match_chart.values(), labels=skill_match_chart.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    # 📊 Bar Chart: Top 5 Jobs Match Count
    if matched_jobs:
        st.markdown("### 📈 Top Matched Jobs Overview")
        top_jobs = matched_jobs[:5]
        fig2, ax2 = plt.subplots()
        ax2.barh(
            [f"{j['job_title']} ({j['company']})" for j in top_jobs],
            [j['match_count'] for j in top_jobs],
            color='skyblue'
        )
        ax2.set_xlabel("Skills Matched")
        st.pyplot(fig2)

    # 🧾 Full Report
    st.markdown("### 📋 Personalized Job Report")
    for idx, job in enumerate(matched_jobs[:5], 1):
        with st.container():
            st.markdown(f"""
**{idx}️⃣ {job['job_title']}**
> 🏢 *{job['company']}*  
> 📍 **Location**: {job['location']}  
> 💼 **Platform**: {job['platform']} | ⏱️ **Type**: {job['job_type']}  
> 💰 **Salary**: {job['salary_range']}  
> 🧠 **Matching Skills**: {', '.join(set(user_profile['skills']).intersection(set(job['required_skills'])))}  
> 🟢 **Match Score**: {job['match_count']} skills matched  
👉 [Click here to Apply (dummy)](https://example.com)
---
""")
    if not matched_jobs:
        st.warning("😕 No matching jobs found. Consider adding more skills or courses.")

    # 📢 Recommendation
    if matched_jobs:
        top_job = matched_jobs[0]
        st.markdown(f"""
### 📢 **Career Recommendation**
Based on your strongest skills like **{', '.join(skill_match_chart.keys())}**, we recommend applying for the **{top_job['job_title']}** role at **{top_job['company']}**.
""")

# Run the function to generate job recommendations
generate_job_report(user_profile, df_jobs)
