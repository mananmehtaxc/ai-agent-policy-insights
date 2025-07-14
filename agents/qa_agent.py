from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import huggingface_hub
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader


# Load prompt template from prompt/qa_prompt.txt
with open('prompts/qa_prompt.txt', 'r') as file:
    qa_prompt = file.read() 

# Initialize the prompt template
qa_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_prompt
)   
# st.write("Prompt Template Loaded Successfully")
# st.write("Prompt Template:", qa_prompt_template.template)
# st.write("Input Variables:", qa_prompt_template.input_variables)

# Initialize the LLM with the Hugging Face model
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"  # Updated to a more recent model
llm = huggingface_hub.HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.1, "max_new_tokens": 2048}
)

# Initialize the embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
)
# st.write("Text Splitter Type:", type(text_splitter))

# Build FAISS vector store from text chunks
faiss_vector_store = FAISS.from_texts( chunks=[], 
    embedding=embeddings,
)

# Initialize the RetrievalQA chain with the prompt template, LLM, and vector store
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=faiss_vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": qa_prompt_template},
    verbose=True
)

def answer_question(document_text: str, question: str) -> str:
    """
    Answer a question based on the provided document text using the RetrievalQA chain.
    
    :param document_text: The text of the document to be used for answering the question.
    :param question: The question to be answered.
    :return: The answer to the question along with source documents.
    """
    # Load and split the document text into chunks
    documents = text_splitter.split_text(document_text)
    # st.write("Number of chunks created:", len(documents))
    
    # Add chunks to the FAISS vector store
    faiss_vector_store.add_texts(documents)
    
    # Run the RetrievalQA chain with the provided question
    result = qa_chain.run(question=question)
    # st.write("Result from RetrievalQA:", result)

    # Return the answer and source documents
    answer = result['result']
    source_documents = result['source_documents']

    # If no source documents are found, return an empty answer
    if not source_documents:
        return "", []       
    return answer, source_documents