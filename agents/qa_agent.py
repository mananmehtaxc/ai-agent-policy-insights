# agents/qa_agent.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

import asyncio


# Load environment variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Load summarization prompt from file
with open("prompts/qa_prompt.txt", "r") as f:
    template = f.read()


def get_embeddings():
# Initialize embedding and language model
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    """Returns the Google Generative AI embeddings instance."""

# Event loop runner that works inside Streamlit
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if loop.is_running():
        # If inside Streamlit or Jupyter
        return asyncio.run(coro)
    return loop.run_until_complete(coro)

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0.2,
    top_p=1.0,
    top_k=40,
    max_output_tokens=2048
)

# Create a text splitter for long content
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
# Then create PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["context", "question", "summary"],
    template=template,
)

def build_vector_store(text: str):
    docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(text)]
    embedding_result = get_embeddings()

    async def async_build():
        return FAISS.from_documents(docs, embedding_result)


def create_qa_chain(text, summary:str = None) -> RetrievalQA:
    """Creates a QA chain with RAG using the vector store."""
    # Split the text into chunks
    # chunks = text_splitter.split_text(text)

    # Create document from chunks
    # documents = [Document(page_content=chunk) for chunk in chunks]

    # Build the vector store
    # vector_store = FAISS.from_documents(documents, embedding_result)

    # If a summary is provided, include it in the context
    if summary:
        chain_type_kwargs = {"prompt": prompt_template.partial(summary=summary)}
    
    vector_store = run_async(build_vector_store(text))

    # Create the RetrievalQA chain
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=False
    )
    return qa_chain

# Main function to answer questions based on full text (which is link/policy document)
def answer_question(full_text: str, question: str, summary: str = None) -> str:
    """Main interface for answering questions based on legal/policy text."""
    qa_chain = create_qa_chain(full_text, summary=summary)
    result = qa_chain.run({"question": question})
    return result
