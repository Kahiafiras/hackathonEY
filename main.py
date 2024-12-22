from src.config.config import get_settings
from src.extract_text_pdf.CV_text_extraction import process_pdf_files_in_folder
from src.chat_completion.extract_chat import extract_cv_details

settings = get_settings()

if __name__ == "__main__":
    # Input PDF file path
    pdf_path = r"C:\Users\DEV 1\Desktop\CVs"

    results = process_pdf_files_in_folder(pdf_path)
    for result in results:
        llm_output = extract_cv_details(result)
        print(llm_output)