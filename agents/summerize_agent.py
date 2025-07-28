# agents/summarize_agent.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from langchain_core.runnables import RunnableSequence
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
