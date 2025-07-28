# 🧠 AI Legal Document Assistant

## 📌 Overview

An AI-powered agent that ingests common legal documents from websites (via URL) or file uploads (e.g., PDFs, DOCX), generates detailed summaries with key clauses, and enables users to ask contextual questions through an interactive chat interface.

Designed for privacy policies, terms of service, disclaimers, cookie policies, and more.

---

## 📄 Supported Legal Document Types

1. Privacy Policy
2. Terms and Conditions (Terms of Service / Terms of Use)
3. Cookie Policy
4. Disclaimer
5. Copyright Notice / IP Policy
6. Accessibility Statement
7. Refund / Return Policy
8. Security Policy
9. User Agreement / Service Agreement
10. End User License Agreement (EULA)
11. Code of Conduct
12. Data Protection Policy
13. Legal Notice / Imprint

## Detailed list 

| Category           | Document Type                           | Description                                           |
| ------------------ | --------------------------------------- | ----------------------------------------------------- |
| 📃 Agreements      | Service-Level Agreement (SLA)           | Outlines service standards, uptime, support, etc.     |
|                    | Master Service Agreement (MSA)          | Governs long-term vendor-client relationships         |
|                    | Licensing Agreement                     | Legal use of software or content                      |
|                    | Non-Disclosure Agreement (NDA)          | Protects confidential information                     |
| ⚖️ Compliance      | GDPR Policy                             | European privacy regulation                           |
|                    | CCPA Statement                          | California Consumer Privacy Act                       |
|                    | HIPAA Policy                            | U.S. health data compliance                           |
|                    | DMCA Policy                             | Copyright takedown rules                              |
|                    | FERPA Policy                            | Educational data privacy in U.S.                      |
|                    | COPPA Notice                            | Privacy notice for children’s websites                |
| 📦 Commerce        | Shipping Policy                         | Shipping timelines and methods                        |
|                    | Payment Policy                          | Payment terms, supported methods                      |
|                    | Billing Terms                           | Recurring billing, invoicing rules                    |
|                    | Cancellation Policy                     | How users can cancel subscriptions                    |
|                    | Warranty Policy                         | Coverage and limits of product warranties             |
| 👤 User Rights     | User Data Request Procedure             | How users request, edit, or delete data               |
|                    | Account Deletion Policy                 | Steps to permanently delete user accounts             |
|                    | Moderation or Abuse Policy              | What content/behavior is prohibited                   |
| 🛠️ Operational    | Maintenance Notice / SLA Schedule       | Scheduled downtimes and update cycles                 |
|                    | Incident Response Policy                | How site responds to data breaches or security issues |
| 🌍 Region-specific | Terms localized for EU, UK, India, etc. | Tailored terms depending on legal region              |


---

Here's your updated **README `Tech Stack` section**, reflecting the shift from Hugging Face to Google Gemini via `langchain_google_genai`:

---

## ⚙️ Tech Stack

* **LangChain**: Framework for chaining LLMs, agents, and tools
* **Google Gemini via `langchain_google_genai`**: Used for both summarization and Q\&A 
* **BeautifulSoup**: For extracting legal/policy content from web pages
* **PyMuPDF / python-docx / pdfplumber**: For parsing uploaded PDF and DOCX documents
* **Streamlit**: Web interface for URL input, policy summarization, and Q\&A chat
* **FAISS**: Vector store for semantic document chunking and retrieval (used in RAG-style Q\&A)
* **dotenv**: Secure handling of API keys and environment variables

---

Let me know if you also want to include a diagram, setup instructions, or feature overview in the README.


---

## 🧩 Functional Components

### 1. Document Ingestion

* Accepts: URL input or file upload
* Detects document type based on keywords in title/content or URL
* Extracts raw text using:

  * `requests` + `bs4` for URLs
  * `PyMuPDF`, `pdfplumber`, or `python-docx` for uploads

### 2. Summarization Agent

* Generates detailed, structured summaries with key clauses
* Uses prompt engineering for clarity, compliance relevance, and structure

### 3. Question Answering Agent (not working)

* Uses retrieved document chunks and context to answer user queries
* Powered by Google Gemini
* Optionally integrates LangChain's `RetrievalQA` or custom prompt chaining

### 4. Chat Interface

* Streamlit-based chat experience
* Displays history of Q\&A
* Allows follow-up questions with context memory

---

## 🔄 Flow Diagram (High-Level)

```
Input (URL or File Upload)
        ↓
  Text Extraction Layer
        ↓
  Document Type Classification
        ↓
  Summarization Agent (LangChain + HF LLM)
        ↓
      Store in Memory
        ↓
User Chat Query → LangChain Q&A Chain → Answer
```

---

## 🚀 Generic Project Setup

```
# Clone and enter project
git clone <repo-url>
cd <repo-folder>

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py

    ## This project uses streamlit run streamlit
    streamlit run main.py

# Deactivate when done
deactivate

# Freeze requirements.txt after installing new package
pip freeze > requirements.txt

```

---

## 📁 Folder Structure

```
ai-agent-policy-insights/
├── app.py                  # Streamlit UI
├── agents/
│   ├── summarize_agent.py  # Summarization logic
│   └── qa_agent.py         # Q&A logic
├── scapper/
│   ├── discover_legal_links.py      # Given a main site URL, finds legal page URLs
│   ├── scrape_legal_text.py      # Given a specific legal page URL, extracts the text content
│   └── file_loader.py          # PDF/DOCX parser
├── prompts/
│   ├── summarize_prompt.txt
│   └── qa_prompt.txt
├── data/
│   └── uploads/            # Uploaded files storage
├── requirements.txt
└── README.md
```

---

## 🧠 Example Prompt Templates

### Summarization Prompt

```
You are a policy analyzer assistant. Read the following policy and disclaimer document and generate a structured summary with key sections, legal obligations, user rights, and limitations.

Document:
{document_text}
```

### Question Answering Prompt

```
Use the following policy document context to answer the user's question accurately. Answer only based on the provided context.

Context:
{context}

Question:
{question}
```

---

## 🔧 Suggested RAG Setup

| Component | Tool                                   |
| --------- | -------------------------------------- |
| Chunking  | RecursiveCharacterTextSplitter         |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | FAISS or Chroma                        |
| Retriever | langchain.vectorstores.Retriever       |
| LLM       | HuggingFaceHub (Mistral or Lexi-7B)    |
| Chain     | RetrievalQA                            |

---

## 🧠 Example Questions

* What data does this company collect under its Privacy Policy?
* What are the refund terms?
* Does this policy mention GDPR compliance?
* Is arbitration required in dispute resolution?

---

## 📌 Future Enhancements

* Add support for multilingual documents
* Summarization toggle (brief vs detailed)

---

## 🛡️ Disclaimer

This AI tool is for informational purposes only and does not provide legal advice.

---

## 👥 Contributors

* Manan Mehta
* \[Your Team or Contributors Here]

---

# Test website: https://1path.com
# Test website: https://www.apple.com
