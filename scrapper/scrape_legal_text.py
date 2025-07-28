import requests
from bs4 import BeautifulSoup

# scrape single legal link (this is when user provides a specific policy link to analyze)
def scrape_legal_link(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Scraper] Error scraping {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove irrelevant tags
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()

    # Extract and normalize text
    text = soup.get_text(separator="\n")
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    return cleaned_text
