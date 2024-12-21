import nest_asyncio
import os
from llama_parse import LlamaParse
from src.config.config import get_settings


settings = get_settings()
def convert_pdf_to_markdown(pdf_path:str, output_file:str):
    """Converts a PDF file to Markdown format and saves it to a file."""
    nest_asyncio.apply()

    # Set API key for Llama Cloud
    api_key = settings.LLAMA_CLOUD_API

    # Load and process the document
    document = LlamaParse(result_type="markdown",api_key=api_key).load_data(pdf_path)

    # Write the output to a file
    with open(output_file, 'w') as file:
        for doc in document:
            file.write(doc.text)
    print(f"Markdown content saved to {output_file}")

if __name__ == "__main__":
    # Input PDF file path
    pdf_path = r"C:\Users\DEV 1\Desktop\Ahmed-Ben-Jannet-Resume.pdf"
    # Output Markdown file path
    output_file = "cv_md.md"

    convert_pdf_to_markdown(pdf_path, output_file)
