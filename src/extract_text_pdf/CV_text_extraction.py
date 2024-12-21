import nest_asyncio
import os
from llama_parse import LlamaParse
from src.config.config import get_settings


settings = get_settings()
def convert_pdf_to_markdown(pdf_path: str, output_file: str):
    """
    Converts a PDF file to Markdown format and saves it to a .txt file.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_file (str): Path to the output .txt file.

    Returns:
        str: The content of the Markdown file as a single string.
    """
    nest_asyncio.apply()

    # Load API key from settings
    settings = get_settings()
    api_key = settings.LLAMA_CLOUD_API

    # Load and process the document
    document = LlamaParse(result_type="markdown", api_key=api_key).load_data(pdf_path)

    # Combine all parts of the document into a single string
    markdown_content = "\n".join(doc.text for doc in document)

    # Write the content to the output file
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"Markdown content saved to {output_file}")
    return markdown_content