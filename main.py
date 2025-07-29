import os
from dotenv import load_dotenv
import time
from scrapper.discover_legal_links import fetch_legal_links
from scrapper.scrape_legal_text import scrape_legal_link
from scrapper.file_loader import load_file
from agents.qa_agent import answer_question
from agents.summerize_agent import summarize_text, summarize_document
import streamlit as st


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="Policy Analyzer",
    page_icon="📝",
    initial_sidebar_state="expanded"
    )

st.title("Policy Analyzer: AI Policy Analyst")
st.caption(
    "Upload or provide URLs of Privacy Policies, Terms & Conditions, and other legal documents. "
    "Get clear summaries and ask questions in a chat-like interface powered by AI."
)

st.sidebar.header("Choose your input method");
st.sidebar.markdown(
    """
    1. Upload a legal document (PDF or DOCX) or enter a URL.
    2. The AI will scrape and summarize the policy for you.
    3. Ask questions in the chat section to get detailed answers.
    """
)

# select options from below for analysis
with st.sidebar:
    choice = st.radio("Choose how tou like to provide policy information:", ["Use Website URL", "File Upload"],
    captions=[
        "🌐 Analyze from Website URL (ie: https://www.example.com). Agent will parse avaiable links and present you to analyze",
        "📄 Analyze through Document.Upload a File to analyze"
        ],
    index = 0
    )
    if st.button("Reset Session"):
        st.session_state.clear()
        st.success("Session reset successfully. You can start fresh now.")
        st.rerun()

# Initialize session state variables
if "legal_links" not in st.session_state:
    st.session_state.legal_links = None
if "legal_links_fetched" not in st.session_state:
    st.session_state.legal_links_fetched = False
if "summary" not in st.session_state:
    st.session_state.summary = None
if "scraped_text" not in st.session_state:
    st.session_state.scraped_text = None
if "analyze_link" not in st.session_state:
    st.session_state.analyze_link = None


# ---- Website URL Flow ----
if choice == "Use Website URL":
    st.write("### Enter Website URL")
    st.caption("Enter the URL to analyze. The AI will find and summarize the legal/policy links.")
    st.caption("URL format: https://www.example.com")
    website_url = st.text_input("🌐 Enter Website URL", placeholder="www.example.com")

    # Fetch legal links once
    if website_url and not st.session_state.legal_links_fetched:
        st.session_state.legal_links = fetch_legal_links(website_url)
        st.session_state.legal_links_fetched = True

    # Show fetched links
    if st.session_state.legal_links and st.session_state.analyze_link is None:
        with st.spinner("Fetching legal links...",show_time=True):
            time.sleep(1)
            st.write("### Legal Links Found:")
            for link in st.session_state.legal_links:
                left, right = st.columns([4, 1])
                left.markdown(f"- [{link}]({link})")
                if right.button("Analyze", key=link):
                    st.session_state.analyze_link = link
                    # st.rerun()

    # Summarize and Q&A flow
    if st.session_state.analyze_link:
        link = st.session_state.analyze_link
        st.info(f"Analyzing: {link}")

        # Scrape and summarize only if not already done
        if not st.session_state.scraped_text:
            with st.spinner("Scraping and summarizing..."):
                text = scrape_legal_link(link)
                summary = summarize_text(text)
                st.session_state.scraped_text = text
                st.session_state.summary = summary

        st.success("Summary complete")
        st.write("### Summary")
        st.write(st.session_state.summary)

        # Back button
        if st.button("🔙 Back"):
            st.session_state.analyze_link = None
            st.session_state.scraped_text = ""
            st.session_state.summary = ""
            st.rerun()

# ---- File Upload (optional, not implemented yet) ----
if choice == "File Upload":
    st.write("### Document Analysis")
    st.caption("Upload a legal document to analyze its content.")
    document = st.file_uploader("📄 Upload File", type=["PDF", "txt"])
    if document:
        with st.spinner("Loading file...", show_time=True):
            time.sleep(1)
            try:
                text = load_file(document)
                st.session_state.scraped_text = text
                st.spinner("Summarizing document...")
                st.session_state.summary = summarize_document(text)
                st.write("### Summary")
                st.write(st.session_state.summary)
                st.success("File loaded and summarized successfully.")
            except Exception as e:
                st.error(f"Error loading file: {e}")