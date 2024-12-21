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
        if ext == ".pdf":  # Check if the file has a .pdf extension
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            
            # Apply the processing function and collect the result
            result = convert_pdf_to_markdown(file_path,f"./output/{file_name}.txt")
            results.append((file_name, result))
    
    return results
