from fpdf import FPDF
import os
import json
import google.generativeai as genai

# --------------------------
# 1. Gemini API Configuration
# --------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyB8Ab3gXsAb9TXl38UeeJ9hMiH1c8dj--I"
genai.configure(api_key=GEMINI_API_KEY)

# --------------------------
# 2. Prompt Builder for Gemini
# --------------------------
def build_prompt(user_data):
    prompt = f"""
You are a professional resume writer.
Generate a polished resume for the following user:

Name: {user_data['name']}
Age: {user_data['age']}
Education: {user_data['education']}
Skills: {', '.join(user_data['skills'])}
Experience: {user_data['experience']}

Courses Completed:
"""
    for course in user_data['courses']:
        prompt += f"- {course['course_name']} (Marks: {course['marks']}, Completed: {course['date']})\n"

    prompt += """
Structure the resume with:
- Professional Summary
- Education
- Skills
- Work Experience
- Courses Completed
- Languages (if inferred)
- Keep it clear, friendly, and 1-page long.
"""
    return prompt

# --------------------------
# 3. Call Gemini to Generate Resume Content
# --------------------------
def generate_resume_content(user_data):
    prompt = build_prompt(user_data)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# --------------------------
# 4. Resume PDF Class
# --------------------------
class ResumePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "Resume", ln=1, align="C")

    def print_resume(self, data):
        self.add_page()
        if data.get("profile_photo") and os.path.exists(data["profile_photo"]):
            self.image(data["profile_photo"], x=160, y=10, w=30)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, data["name"], ln=True)
        self.set_font("Arial", "", 10)
        self.ln(5)

        # Professional Summary
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Professional Summary", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, data["summary"])
        self.ln(3)

        # Education
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Education", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, data["education"])

        # Experience
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Experience", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, data["experience"])

        # Skills
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Skills", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, ", ".join(data["skills"]))

        # Courses
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Courses", ln=True)
        self.set_font("Arial", "", 10)
        for course in data["courses"]:
            self.cell(0, 10, f"{course['course_name']} - {course['marks']} ({course['date']})", ln=True)

        # Languages
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Languages", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, ", ".join(data.get("languages", ["English"])))

# --------------------------
# 5. Main Execution
# --------------------------
if __name__ == "__main__":
    with open("user_profile.json", "r") as file:
        user_profile = json.load(file)

    print("\nGenerating resume...")
    resume_text = generate_resume_content(user_profile)

    # Simulate parsing Gemini response — you can later parse the actual content better
    structured_resume = {
        "name": user_profile["name"],
        "profile_photo": user_profile.get("profile_photo", ""),
        "summary": "A motivated student passionate about technology and learning.",
        "education": user_profile["education"],
        "skills": user_profile["skills"],
        "experience": user_profile["experience"],
        "courses": user_profile["courses"],
        "languages": ["English"]
    }

    pdf = ResumePDF()
    pdf.print_resume(structured_resume)
    output_filename = f"{user_profile['name'].lower().replace(' ', '_')}_resume.pdf"
    pdf.output(output_filename)
    print(f"✅ Resume saved as: {output_filename}")
