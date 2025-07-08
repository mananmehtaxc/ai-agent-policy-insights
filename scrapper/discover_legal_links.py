# scraper/discover_legal_links.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

LEGAL_KEYWORDS = [
    "privacy", "terms", "cookie", "legal", "policy",
    "disclaimer", "refund", "return", "gdpr", "ccpa",
    "accessibility", "license", "agreement"
]

def is_valid_legal_link(url):
    return any(keyword in url.lower() for keyword in LEGAL_KEYWORDS)

def fetch_legal_links(base_url: str) -> list[str]:
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Discoverer] Error fetching {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    found_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc != urlparse(base_url).netloc:
            continue

        if is_valid_legal_link(href) or is_valid_legal_link(a.text):
            found_links.add(full_url)

    return sorted(found_links)


#how to use
# from scraper.discover_legal_links import fetch_legal_links

# urls = fetch_legal_links("https://www.dotdashmeredith.com")
# for link in urls:
    # print(link)