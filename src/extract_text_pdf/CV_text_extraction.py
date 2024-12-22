import nest_asyncio
import os
from llama_parse import LlamaParse
from src.config.config import get_settings


settings = get_settings()

def convert_pdf_to_markdown(pdf_path: str):
    """
    Converts a PDF file to Markdown format and returns the content as a UTF-8 encoded string.

    Args:
        pdf_path (str): Path to the input PDF file.

    Returns:
        str: The content of the Markdown file as a single string, encoded in UTF-8.
    """
    nest_asyncio.apply()

    # Load API key from settings
    settings = get_settings()
    api_key = settings.LLAMA_CLOUD_API

    # Load and process the document
    document = LlamaParse(result_type="markdown", api_key=api_key).load_data(pdf_path)

    # Combine all parts of the document into a single string
    markdown_content = "\n".join(doc.text for doc in document)
    print(markdown_content)
    # Return the content as a UTF-8 encoded string
    return markdown_content


def process_pdf_files_in_folder(folder_path):
    """
    Iterates through all .pdf files in a folder and applies a processing function to each file.

    Args:
        folder_path (str): Path to the folder containing .pdf files.
        convert_pdf_to_markdown (function): Function to apply to each .pdf file. 
                                         The function should accept the file path as an argument.

    Returns:
        list: A list of results returned by the processing function for each file.
    """
    results = []
    
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        raise ValueError(f"The folder path {folder_path} does not exist or is not a directory.")
    
    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        ext = os.path.splitext(file_name)[1]
        file_name=os.path.splitext(file_name)[0]
        if ext == ".pdf":  # Check if the file has a .pdf extension
            file_path = os.path.join(folder_path, f"{file_name}{ext}")
            print(f"Processing file: {file_path}")
            
            # Apply the processing function and collect the result
            result = convert_pdf_to_markdown(file_path)
            results.append(result)
    
    return results
