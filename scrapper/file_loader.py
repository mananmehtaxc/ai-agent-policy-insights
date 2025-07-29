import os
from pathlib import Path
from typing import Union
import pdfplumber
import docx

def load_file(file_input: Union[str, Path, 'UploadedFile']) -> str:
    """
    Load the content of a file given its path or UploadedFile object.
    
    :param file_input: Path to the file or Streamlit UploadedFile.
    :return: Content of the file as a string.
    """
    try:
        # Determine file extension
        if hasattr(file_input, "name"):  # It's a Streamlit UploadedFile
            ext = Path(file_input.name).suffix.lower()
        else:
            ext = Path(file_input).suffix.lower()

        if ext == ".txt":
            if hasattr(file_input, "read"):
                return file_input.read().decode("utf-8")
            else:
                with open(file_input, 'r', encoding='utf-8') as file:
                    print("File uploaded successfully.")
                    return file.read()

        elif ext == ".pdf":
            with pdfplumber.open(file_input) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        elif ext == ".docx":
            doc = docx.Document(file_input)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        raise RuntimeError(f"Error loading file: {e}")
