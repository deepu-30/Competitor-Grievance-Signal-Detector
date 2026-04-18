from datetime import datetime, timezone
from fetchers.reddit_fetcher import fetch_reddit_posts
from fetchers.rss_fetcher import fetch_rss_posts
from fetchers.serp_fetcher import fetch_ddg_snippets
from utils.sentiment import extract_pain_points
from utils.scorer import score_signal
from config import COMPETITORS

def run_detector():
    """
    Main detection loop.
    For each competitor, fetch posts from all sources,
    extract pain points, score them, and return structured signals.
    """
    all_signals = []

    for competitor in COMPETITORS:
        print(f"\n🔍 Scanning: {competitor}")

        # Collect posts from all 3 sources
        posts = (
            fetch_reddit_posts(competitor) +
            fetch_rss_posts(competitor) +
            fetch_ddg_snippets(competitor)
        )

        print(f"   Found {len(posts)} raw posts")

        for post in posts:
            matched_keywords, pain_points = extract_pain_points(post["text"])

            # Skip posts with no negative signals at all
            if not matched_keywords:
                continue

            score = score_signal(matched_keywords, pain_points, post["source"])

            signal = {
                "company":          competitor,
                "signal_type":      "competitor_grievance",
                "source_url":       post["url"],
                "source":           post["source"],
                "matched_keywords": matched_keywords,
                "pain_points":      pain_points,
                "signal_score":     score,
                "detected_at":      datetime.now(timezone.utc).isoformat(),
                "reason": (
                    f"Negative feedback about {competitor} detected. "
                    f"Pain points: {', '.join(pain_points) if pain_points else 'general negativity'}"
                )
            }
            all_signals.append(signal)

        print(f"   ✅ {sum(1 for s in all_signals if s['company'] == competitor)} signals extracted")

    # Sort by score descending
    all_signals.sort(key=lambda x: x["signal_score"], reverse=True)
    return all_signals