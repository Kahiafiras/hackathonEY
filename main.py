from src.config.config import get_settings
from src.extract_text_pdf.CV_text_extraction import convert_pdf_to_markdown

settings = get_settings()

if __name__ == "__main__":
    # Input PDF file path
    pdf_path = r"C:\Users\DEV 1\Desktop\Ahmed-Ben-Jannet-Resume.pdf"
    # Output Markdown file path
    output_file = "cv_md.md"

    convert_pdf_to_markdown(pdf_path, output_file)