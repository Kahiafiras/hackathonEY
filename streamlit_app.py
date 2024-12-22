import streamlit as st
from src.config.config import get_settings
from src.extract_text_pdf.CV_text_extraction import convert_pdf_to_markdown
from src.chat_completion.extract_chat import extract_cv_details
import json
import re

# Load settings
settings = get_settings()

# Streamlit App
def main():
    st.title("CV Analysis Application")
    st.write("Upload a folder of PDF CVs, and the app will analyze and extract details.")

    # File uploader for a single PDF or multiple files
    uploaded_files = st.file_uploader(
        "Upload PDF CVs (Multiple files supported)", 
        type="pdf", 
        accept_multiple_files=True
    )

    if uploaded_files:
        # Process uploaded files
        st.write("Processing CVs... Please wait.")
        results = []
        for uploaded_file in uploaded_files:
            # Save uploaded file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())

            # Extract text and analyze
            cv_text = convert_pdf_to_markdown(uploaded_file.name)
            llm_output = extract_cv_details(cv_text)

            # Regex to capture the dictionary portion of the string
            match = re.search(r'({.*})', llm_output, re.DOTALL)

            if match:
                # Extract the matched dictionary string
                dict_str = match.group(1)
                
                # Convert the string to a Python dictionary
                llm_dict = json.loads(dict_str)
                print(llm_dict)
            else:
                print("No match found.")
            results.append(llm_dict)

        # Display results
        st.success("CV analysis completed!")
        # Example loop to print the keys and values of the dictionary
        for result in results:  # Wrapping result in a list to iterate
            # Define some basic CSS for styling the "box"
            st.markdown("""
                <style>
                    .tech-card {
                        background-color: #f4f4f4;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        margin-bottom: 15px;
                    }
                    .tech-card h3 {
                        color: #2a2a2a;
                    }
                    .tech-card p {
                        font-size: 16px;
                        color: #555;
                    }
                    .tech-card ul {
                        padding-left: 20px;
                    }
                    .tech-card ul li {
                        margin-bottom: 5px;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Loop through each key-value pair and format it nicely in the "box"
            for key, value in result.items():
                if isinstance(value, list):  # For lists (like skills or suggested jobs)
                    if isinstance(value[0], dict):  # If the list contains dictionaries (like suggested jobs)
                        st.markdown(f"<h3><strong>{key.capitalize()}</strong></h3>", unsafe_allow_html=True)
                        for job in value:
                            st.markdown(f"<p><strong>Job Title:</strong> {job['job_title']}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p><strong>Estimated Level:</strong> {job['estimated_level']}</p>", unsafe_allow_html=True)
                        st.markdown(f'</div>', unsafe_allow_html=True)
                    else:  # If the list contains strings (like skills)
                        st.markdown(f"<h3><strong>{key.capitalize()}</strong></h3>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>{key.capitalize()}:</strong> {', '.join(value)}</p>", unsafe_allow_html=True)
                        st.markdown(f'</div>', unsafe_allow_html=True)
                else:
                    # For non-list values (like seniority, years_of_experience, profile_summary)
                    st.markdown(f"<h3><strong>{key.capitalize()}</strong></h3>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>{key.capitalize()}:</strong> {value}</p>", unsafe_allow_html=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
