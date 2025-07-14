import os
import streamlit as st
from scrapper.discover_legal_links import fetch_legal_links
from scrapper.scrape_legal_text import scrape_legal_text
from scrapper.file_loader import load_file
from agents.qa_agent import answer_question
from agents.summerize_agent import summarize_text


st.set_page_config(
    page_title="Policy Analyzer",
    page_icon="📝",
    initial_sidebar_state="expanded"
    )

st.title("Policy Analyzer: AI Policy Analyst)")
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
    choice = st.radio("Choose how tou like to provide policy information:", ["Use Website URL", "Use Policy URL", "File Upload"],
    captions=[
        "🌐 Analyze from Website URL (ie: https://www.example.com). Agent will parse avaiable links and present you to analyze",
        "🔗 Analyze using URL of policy, disclamier, ToS Page etc. (ie. https://www.example.com/policy.html)",
        "📄 Analyze through Document.Upload a File to analyze"
        ],
    index = 0
    )
    
if choice == "Use Website URL":
    st.write("### Enter Websitie URL (ie. ***www.example.com***)")
    st.caption("Enter the URL of the website you want to analyze. The AI will scrape and summarize the policy for you.")
    website_url = st.text_input("🌐 Enter Website URL",placeholder="www.example.com")
if choice == "Use Policy URL":
    st.write("### Enter Policy URL (ie. ***www.example.com/policy.html***)")
    st.caption("Enter the URL of the policy document you want to analyze. The AI will summarize the policy and answer questions based on it.")
    policy_url = st.text_input("🔗 Enter Policy URL",placeholder="www.example.com/policy.html")
if choice == "File Upload":
    st.write("### Document Analysis")
    st.caption("Upload a legal document or provide a URL to analyze its content. The AI will summarize the policy and answer questions based on it.")
    document = st.file_uploader("📄 Upload File", type=["PDF", 'DOCX'])


# Test website: https://1path.com
# Test website: https://www.vccircle.com

# Call discovery legal links for websiste_url
'''
if choice == "Use Website URL" and website_url:
    st.info("Fetching legal links from the website...")
    st.spinner("Checking Webiste...")
    st.spinner("Fetching Links...")
    legal_links = fetch_legal_links(website_url)
    if legal_links:
        st.spinner("Loading Links...")
        st.success("Legal links found:")
        for link in legal_links:
            # Display index and link
            st.write(f"{legal_links.index} - {link}")
            st.button("Analyze", key=f"analyze_{legal_links.index}", on_click=lambda l=link: 
                    st.session_state.update({"selected_link": l}))
    else:
        st.warning("No legal links found on the website.") 
'''