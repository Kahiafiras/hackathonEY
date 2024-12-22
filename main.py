from src.config.config import get_settings
from src.extract_text_pdf.CV_text_extraction import process_pdf_files_in_folder
from src.job_desc.extract_skills import extract_skills

settings = get_settings()

if __name__ == "__main__":
