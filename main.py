from src.config.config import get_settings
from src.extract_text_pdf.CV_text_extraction import process_pdf_files_in_folder

settings = get_settings()

if __name__ == "__main__":
    # Input PDF file path
    pdf_path = r"C:\Users\DEV 1\Desktop\CVs"

    process_pdf_files_in_folder(pdf_path)