import streamlit as st
from resume import ResumePDF, generate_resume_content
import tempfile
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import speech_recognition as sr
import google.generativeai as genai
import json

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyB8Ab3gXsAb9TXl38UeeJ9hMiH1c8dj--I"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')  # Using the latest stable version

st.set_page_config(page_title="AI Resume + Job Matcher", page_icon="📝", layout="centered")

# Initialize session states
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "name": "",
        "age": 0,
        "education": "",
        "skills": [],
        "experience": "",
        "courses": [],
        "profile_photo": ""
    }

if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None

if 'resume_file' not in st.session_state:
    st.session_state.resume_file = None

# Load job data
csv_file_path = 'rural_women_jobs_dataset_expanded.csv'
df_jobs = pd.read_csv(csv_file_path)
df_jobs["Skill"] = df_jobs["Skill"].fillna("").astype(str)

# Sidebar with tabs
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100)
st.sidebar.title("SARANI")

# Add tabs in sidebar
selected_tab = st.sidebar.radio(
    "Navigation",
    ["AI Resume Generator", "Job Matching Analytics", "Job Recommendations"]
)

# Initialize speech recognizer
recognizer = sr.Recognizer()

def process_voice_input():
    """Process voice input and extract user profile information using Gemini API"""
    try:
        with sr.Microphone() as source:
            st.info("Please speak about yourself...")
            audio = recognizer.listen(source)
            st.success("Voice recorded! Processing...")
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            st.write("You said:", text)
            
            # Create prompt for Gemini
            prompt = f"""Extract the following information from this text in JSON format:
            {text}
            
            Required fields:
            - name
            - age
            - education
            - skills (as a list)
            - experience
            - courses (as a list of dictionaries with course_name, marks, and date)
            
            If any information is missing, use appropriate default values.
            Return only the JSON object, nothing else."""
            
            # Get response from Gemini
            response = model.generate_content(prompt)
            
            # Parse the response
            try:
                # Clean the response text to ensure it's valid JSON
                response_text = response.text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                profile_data = json.loads(response_text)
                return profile_data
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse the response: {e}")
                st.write("Raw response:", response.text)
                return None
                
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def generate_and_store_resume():
    """Generate resume and store it in session state"""
    resume_text = generate_resume_content(st.session_state.user_profile)
    
    structured_resume = {
        "name": st.session_state.user_profile["name"],
        "profile_photo": st.session_state.user_profile.get("profile_photo", ""),
        "summary": resume_text.split("**Professional Summary**")[-1].split("**Education**")[0].strip()
            if "**Professional Summary**" in resume_text else "A hardworking and aspiring individual with a strong will to learn and grow.",
        "education": st.session_state.user_profile["education"],
        "skills": st.session_state.user_profile["skills"],
        "experience": st.session_state.user_profile["experience"],
        "courses": st.session_state.user_profile["courses"],
        "languages": ["Hindi", "English"]
    }
    
    # Store resume data
    st.session_state.resume_data = structured_resume
    
    # Generate and store PDF
    pdf = ResumePDF()
    pdf.print_resume(structured_resume)
    output_filename = f"{st.session_state.user_profile['name'].lower().replace(' ', '_')}_resume.pdf"
    pdf.output(output_filename)
    
    # Store the file path
    st.session_state.resume_file = output_filename
    return output_filename

def generate_job_analytics(resume_data):
    """Generate job analytics using Gemini"""
    prompt = f"""Based on the following resume data, generate a detailed job market analysis:
    {json.dumps(resume_data, indent=2)}
    
    Generate a JSON response with:
    1. skill_demand: List of top 5 most in-demand skills related to the user's skills
    2. industry_trends: List of 3 relevant industry trends
    3. salary_insights: Average salary ranges for different experience levels
    4. growth_opportunities: List of 3 potential career growth paths
    
    Return only the JSON object, nothing else."""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        return json.loads(response_text.strip())
    except Exception as e:
        st.error(f"Error generating analytics: {e}")
        return None

def generate_job_recommendations(resume_data):
    """Generate personalized job recommendations using Gemini"""
    prompt = f"""Based on the following resume data, generate detailed job recommendations:
    {json.dumps(resume_data, indent=2)}
    
    Generate a JSON response with a list of 5 job recommendations. Each recommendation should include:
    - job_title
    - company
    - location
    - required_skills
    - salary_range
    - job_type
    - match_score (percentage)
    - growth_potential
    - learning_opportunities
    
    Return only the JSON object, nothing else."""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        return json.loads(response_text.strip())
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return None

# AI Resume Generator Tab
if selected_tab == "AI Resume Generator":
    st.title("📝 AI Resume Generator")
    
    # Voice Input Section
    st.markdown("### 🎤 Voice Input")
    if st.button("🎤 Start Recording", key="record_button"):
        profile_data = process_voice_input()
        if profile_data:
            st.session_state.user_profile.update(profile_data)
            st.success("Profile updated successfully!")
            # Generate and store resume when profile is updated
            generate_and_store_resume()
    
    # Display Profile Section
    st.markdown("### 👤 Candidate Profile")
    
    col1, col2 = st.columns([1, 3])
    if st.session_state.user_profile["profile_photo"]:
        col1.image(st.session_state.user_profile["profile_photo"], caption=st.session_state.user_profile['name'], width=100)
    else:
        col1.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)
    
    col2.markdown(f"**Name:** {st.session_state.user_profile['name']}")
    col2.markdown(f"**Age:** {st.session_state.user_profile['age']}")
    col2.markdown(f"**Education:** {st.session_state.user_profile['education']}")
    col2.markdown(f"**Skills:** {', '.join(st.session_state.user_profile['skills'])}")
    col2.markdown(f"**Experience:** {st.session_state.user_profile['experience']}")
    
    # --- Generate Resume ---
    if st.session_state.user_profile['name']:  # Only show if we have user data
        st.markdown("### 📄 Resume Generation")
        if st.session_state.resume_file:
            with open(st.session_state.resume_file, "rb") as f:
                st.download_button("📥 Download Resume", f, file_name=st.session_state.resume_file)
            st.success("✅ Resume generated successfully!")

# Job Matching Analytics Tab
elif selected_tab == "Job Matching Analytics":
    st.title("📊 Job Matching Analytics")
    
    if not st.session_state.resume_data:
        st.warning("Please generate a resume first in the AI Resume Generator tab.")
    else:
        # Generate analytics using Gemini
        analytics = generate_job_analytics(st.session_state.resume_data)
        
        if analytics:
            # Display Skill Demand
            st.markdown("### 🎯 Skill Demand Analysis")
            for skill in analytics.get('skill_demand', []):
                st.markdown(f"- {skill}")
            
            # Display Industry Trends
            st.markdown("### 📈 Industry Trends")
            for trend in analytics.get('industry_trends', []):
                st.markdown(f"- {trend}")
            
            # Display Salary Insights
            st.markdown("### 💰 Salary Insights")
            st.write(analytics.get('salary_insights', {}))
            
            # Display Growth Opportunities
            st.markdown("### 🚀 Growth Opportunities")
            for opportunity in analytics.get('growth_opportunities', []):
                st.markdown(f"- {opportunity}")
            
            # Generate and display skill match visualization
            skills = st.session_state.resume_data['skills']
            if skills:
                st.markdown("### 🎨 Skill Match Distribution")
                fig, ax = plt.subplots()
                ax.pie([1] * len(skills), labels=skills, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

# Job Recommendations Tab
elif selected_tab == "Job Recommendations":
    st.title("🎯 Job Recommendations")
    
    if not st.session_state.resume_data:
        st.warning("Please generate a resume first in the AI Resume Generator tab.")
    else:
        # Generate recommendations using Gemini
        recommendations = generate_job_recommendations(st.session_state.resume_data)
        
        if recommendations:
            # Display job recommendations
            st.markdown("### 📋 Personalized Job Recommendations")
            for idx, job in enumerate(recommendations, 1):
                with st.container():
                    st.markdown(f"""
**{idx}️⃣ {job['job_title']}**
> 🏢 *{job['company']}*  
> 📍 **Location**: {job['location']}  
> 💼 **Type**: {job['job_type']}  
> 💰 **Salary**: {job['salary_range']}  
> 🧠 **Required Skills**: {', '.join(job['required_skills'])}  
> 🟢 **Match Score**: {job['match_score']}  
> 📈 **Growth Potential**: {job['growth_potential']}  
> 🎓 **Learning Opportunities**: {job['learning_opportunities']}  
👉 [Click here to Apply (dummy)](https://example.com)
---
""")
            
            # Display top recommendation with more details
            if recommendations:
                top_job = recommendations[0]
                st.markdown(f"""
### 📢 **Top Career Recommendation**
Based on your profile, we strongly recommend the **{top_job['job_title']}** role at **{top_job['company']}**.

**Why this role?**
- Perfect match with your skills ({top_job['match_score']} match)
- Competitive salary range: {top_job['salary_range']}
- Strong growth potential: {top_job['growth_potential']}
- Excellent learning opportunities: {top_job['learning_opportunities']}

**Next Steps:**
1. Review the required skills
2. Update your resume to highlight relevant experience
3. Prepare for common interview questions in this field
""")
