# agents/summarize_agent.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from langchain_core.runnables import RunnableSequence
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load environment variables from .env (ensure GOOGLE_API_KEY is set there)
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM using Google Generative AI
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",  # or "gemini-pro" for more power
    google_api_key=google_api_key,
    temperature=0.2,
    top_p=1.0,
    top_k=40,
    max_output_tokens=2048
)

# Load summarization prompt from file
with open("prompts/summarize_prompt.txt", "r") as f:
    template = f.read()

# Create LangChain prompt template
prompt = PromptTemplate(
    input_variables=["legal_text"],
    template=template
)

# Build the LLM chain
summarize_chain : RunnableSequence  = prompt | llm

# Function to summarize text
def summarize_text(text: str) -> str:
    """Summarizes legal or policy text using Google Generative AI."""
    result = summarize_chain.invoke({"legal_text": text})
    #if result is empty not not legnth, return a default message
    if not result or len(result) == 0:
        return "No summary available. Please try another url to analyze."
    return result


def cleaned_file(text: str) -> str:
    """
    Basic cleaning for PDF extracted text:
    - Remove repeated headers/footers (example)
    - Remove excessive empty lines
    """
    lines = text.splitlines()
    cleaned_lines = []
    seen_headers = set()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue  # skip empty lines
        if stripped in seen_headers:
            continue  # skip repeated headers
        if len(stripped) > 50:
            seen_headers.add(stripped)
        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=500,
    separators=["\n\n", "\n", " ", ""]
)

def summarize_document(text: str) -> str:
    """Summarizes the entire document intelligently using Google Gemini."""
    
    if not text or len(text.strip()) == 0:
        return "No content to summarize."

    # If text is short, summarize directly
    if len(text) < 8000:
        result = summarize_chain.invoke({"legal_text": text})
        return result or "No summary available."

    # For longer documents: split and recompose
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    partial_summaries = []

    for i, chunk in enumerate(chunks[:10]):  # Limit to 10 chunks max for performance
        result = summarize_chain.invoke({"legal_text": chunk})
        if result:
            partial_summaries.append(result)

    # Combine the partial summaries and summarize that
    combined_summary = "\n".join(partial_summaries)
    final_summary = summarize_chain.invoke({"legal_text": combined_summary})
    return final_summary or "No summary available."