import requests
import time

HEADERS = {"User-Agent": "grievance-detector/1.0"}

def fetch_reddit_posts(competitor, limit=20):
    """Fetch Reddit posts mentioning the competitor using free JSON API."""
    query = f"{competitor} interview tool review"
    url = f"https://www.reddit.com/search.json?q={query}&sort=new&limit={limit}"
    results = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        posts = response.json()["data"]["children"]

        for post in posts:
            d = post["data"]
            text = d.get("title", "") + " " + d.get("selftext", "")
            results.append({
                "text": text,
                "url": "https://reddit.com" + d.get("permalink", ""),
                "source": "reddit"
            })

        time.sleep(1)  # respectful delay to avoid rate-limiting

    except Exception as e:
        print(f"[Reddit] Error fetching '{competitor}': {e}")

    return results