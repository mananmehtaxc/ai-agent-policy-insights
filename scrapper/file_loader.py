import os
from pathlib import Path
from typing import Union
import pdfplumber
import docx

def load_file(file_path: Union[str, Path]) -> str:
    """
    Load the content of a file given its path.
    
    :param file_path: Path to the file to be loaded.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        #check for file extension pdf or docx
        ext = Path(file_path).suffix.lower()
        if ext not in ['.pdf', '.docx']:
            print(f"[File Loader] Unsupported file type: {ext}. Please use text files.")
            raise ValueError(f"Unsupported file type: {ext}. Please use text files.")
        else:
            print(f"[File Loader] Successfully loaded file")
            if ext == '.pdf':
                with pdfplumber.open(file_path) as pdf:
                    text = "" # Initialize an empty string to hold the text
                    for page in pdf.pages: # Extract text from each page
                        text += page.extract_text() + "\n" # Extract text from each page
                    return text.strip() # Remove leading/trailing whitespace
            elif ext == '.docx':
                doc = docx.Document(file_path) # Load the docx file
                text = "\n".join(paragraph.text for paragraph in doc.paragraphs) # Join paragraphs with newlines
                return text.strip() # Remove leading/trailing whitespace
    except FileNotFoundError:
        print(f"[File Loader] File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
