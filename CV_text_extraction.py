import nest_asyncio
import os
from llama_parse import LlamaParse

def convert_pdf_to_markdown(pdf_path, output_file):
    """Converts a PDF file to Markdown format and saves it to a file."""
    nest_asyncio.apply()

    # Set API key for Llama Cloud
    os.environ["LLAMA_CLOUD_API_KEY"] = "llx-Oy4ATtyYWE4Bt8HmEBRKGCQ0sPil98mxtATX4vbz4iAcmhIw"

    # Load and process the document
    document = LlamaParse(result_type="markdown").load_data(pdf_path)

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
