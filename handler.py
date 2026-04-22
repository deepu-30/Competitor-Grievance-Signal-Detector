import json
import sys
import os

# Make sure Python can find your modules
sys.path.insert(0, os.path.dirname(__file__))

from fetchers.reddit_fetcher import fetch_reddit_posts
from fetchers.rss_fetcher import fetch_rss_posts
from fetchers.serp_fetcher import fetch_ddg_snippets
from signals.competitor_grievance import run_detector
from utils.output import save_json, save_sqlite
from config import COMPETITORS


def build_response(status_code, body):
    """Helper to build HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, indent=2)
    }


def health_check(event, context):
    """GET /health — check if service is running."""
    return build_response(200, {
        "status": "ok",
        "message": "Signal Detector is running",
        "competitors_tracked": COMPETITORS
    })


def fetch_reddit(event, context):
    """POST /fetch/reddit — fetch posts for a competitor from Reddit."""
    try:
        body = json.loads(event.get("body") or "{}")
        competitor = body.get("competitor", "HackerRank")

        posts = fetch_reddit_posts(competitor)

        return build_response(200, {
            "competitor": competitor,
            "source": "reddit",
            "total_posts": len(posts),
            "posts": posts
        })

    except Exception as e:
        return build_response(500, {"error": str(e)})


def fetch_rss(event, context):
    """POST /fetch/rss — fetch RSS articles mentioning a competitor."""
    try:
        body = json.loads(event.get("body") or "{}")
        competitor = body.get("competitor", "HackerRank")

        posts = fetch_rss_posts(competitor)

        return build_response(200, {
            "competitor": competitor,
            "source": "rss",
            "total_posts": len(posts),
            "posts": posts
        })

    except Exception as e:
        return build_response(500, {"error": str(e)})


def fetch_ddg(event, context):
    """POST /fetch/ddg — fetch DuckDuckGo snippets for a competitor."""
    try:
        body = json.loads(event.get("body") or "{}")
        competitor = body.get("competitor", "HackerRank")

        posts = fetch_ddg_snippets(competitor)

        return build_response(200, {
            "competitor": competitor,
            "source": "duckduckgo",
            "total_posts": len(posts),
            "posts": posts
        })

    except Exception as e:
        return build_response(500, {"error": str(e)})


def detect_signals(event, context):
    """POST /detect — run full detection pipeline and save output."""
    try:
        body = json.loads(event.get("body") or "{}")
        output_format = body.get("output", "json")  # json | sqlite | both

        # Run the full detection pipeline
        signals = run_detector()

        # Save output
        if output_format in ("json", "both"):
            save_json(signals)
        if output_format in ("sqlite", "both"):
            save_sqlite(signals)

        return build_response(200, {
            "message": "Detection complete",
            "total_signals": len(signals),
            "output_format": output_format,
            "signals": signals
        })

    except Exception as e:
        return build_response(500, {"error": str(e)})