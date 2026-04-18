import requests
from bs4 import BeautifulSoup
import time

def fetch_ddg_snippets(competitor):
    """Scrape DuckDuckGo HTML search results for complaints about competitor."""
    query = f"{competitor} interview tool complaints problems reviews"
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    results = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = soup.select(".result__snippet")

        for snippet in snippets[:10]:
            results.append({
                "text": snippet.get_text(strip=True),
                "url": "",
                "source": "duckduckgo"
            })

        time.sleep(1)

    except Exception as e:
        print(f"[DuckDuckGo] Error fetching '{competitor}': {e}")

    return results