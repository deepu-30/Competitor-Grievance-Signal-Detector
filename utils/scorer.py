SOURCE_WEIGHTS = {
    "reddit":     30,
    "rss":        25,
    "duckduckgo": 20
}

def score_signal(matched_keywords, pain_points, source):
    """
    Score a signal from 0 to 100.
    - Source credibility:  up to 30 pts
    - Keyword matches:     up to 40 pts (10 per keyword)
    - Pain point coverage: up to 30 pts (10 per category)
    """
    base_score    = SOURCE_WEIGHTS.get(source, 15)
    keyword_score = min(len(matched_keywords) * 10, 40)
    pain_score    = min(len(pain_points) * 10, 30)

    total = base_score + keyword_score + pain_score
    return min(total, 100)  # cap at 100