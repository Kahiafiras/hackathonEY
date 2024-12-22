import base64
import json
from io import BytesIO

from fpdf import FPDF
import streamlit as st

from src.job_desc.extract_skills import extract_skills
from src.job_desc.generate_test import generate_test


# Function to create a PDF
class PDF(FPDF):
    def sanitize_text(self, text):
        # Replace unsupported characters with their ASCII equivalents
        replacements = {
            "œ": "oe",
            "’": "'",
            "–": "-",
            "“": '"',
            "”": '"',
            "é": "e",
            "à": "a",
            # Add more replacements as needed
        }
        for original, replacement in replacements.items():
            text = text.replace(original, replacement)
        return text

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 10, 'Generated Test Questions', align='C', ln=True)
        self.ln(10)

    def chapter_title(self, skill):
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 10, self.sanitize_text(f'Skill: {skill}'))
        self.ln(5)

    def chapter_body(self, questions):
        self.set_font('Arial', '', 10)
        for question in questions:
            try:
                # Adjust width by respecting margins
                page_width = self.w - self.l_margin - self.r_margin

                # Render the question text
                self.multi_cell(page_width, 10, self.sanitize_text(f"Question: {question['question']}"))

                if question['type'] == 'QCM':
                    self.multi_cell(page_width, 10, "Options:")
                    for index, option in enumerate(question['options'], start=1):
                        label = chr(64 + index)  # Convert index (1, 2, ...) to letters (A, B, ...)
                        self.multi_cell(page_width, 10, self.sanitize_text(f"{label}. {option}"))
                elif question['type'] == 'Open-ended':
                    self.multi_cell(page_width, 10, "Answer Type: Open-ended (No options provided)")

                self.ln(5)
            except Exception as e:
                print(f"Error rendering question: {question['question']}. Error: {e}")
                raise


# Streamlit UI
st.set_page_config(page_title="Test Generator", layout="centered")

# App title
st.title("✨ Test Generator ✨")
st.subheader("Effortlessly create candidate tests from job descriptions")

# Description input
st.write("Paste your job description below:")
job_description = st.text_area("Job Description", placeholder="Paste the job description here...", height=200)

if st.button("Generate Test ✨"):
    if job_description.strip():
        with st.spinner("Analyzing the job description and generating the test..."):
            skills = extract_skills(job_description)
            skills = json.loads(skills)
            pdf = PDF()
            pdf.add_page()
            for skill_item in skills["skills"]:  # Iterate directly over the list of skills
                skill = skill_item['skill']
                difficulty = skill_item['difficulty']

                # Generate test questions for the skill
                questions = generate_test(skill, difficulty)
                questions = json.loads(questions)
                questions = questions['test']

                # Add skill title and questions to PDF
                pdf.chapter_title(skill)
                pdf.chapter_body(questions)

            # Generate and write PDF content
            pdf_output = BytesIO()
            pdf_bytes = pdf.output(dest="S")  # Generate PDF content as bytes
            pdf_output.write(pdf_bytes)
            pdf_output.seek(0)

            # Encode the PDF to display it in the interface
            base64_pdf = base64.b64encode(pdf_output.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'

        st.success("Test generated successfully!")
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("Please provide a job description to generate the test.")

# Footer
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    .reportview-container .main {background-color: #f0f5ff; border-radius: 10px; padding: 20px;}
    </style>
    """,
    unsafe_allow_html=True
)
