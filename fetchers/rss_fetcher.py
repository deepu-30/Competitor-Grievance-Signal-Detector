import feedparser

RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://feeds.feedburner.com/TechCrunch",
    "https://medium.com/feed/tag/hiring",
    "https://medium.com/feed/tag/recruiting",
]

def fetch_rss_posts(competitor):
    """Scan public RSS feeds for articles mentioning the competitor."""
    results = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                text = title + " " + summary

                if competitor.lower() in text.lower():
                    results.append({
                        "text": text,
                        "url": entry.get("link", ""),
                        "source": "rss"
                    })
        except Exception as e:
            print(f"[RSS] Error parsing feed {feed_url}: {e}")

    return results