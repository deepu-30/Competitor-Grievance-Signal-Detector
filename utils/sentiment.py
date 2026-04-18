from config import NEGATIVE_KEYWORDS, PAIN_POINT_MAP

def extract_pain_points(text):
    """
    Match negative keywords in text and map them to pain point categories.
    Returns: (matched_keywords list, pain_points list)
    """
    text_lower = text.lower()

    # Find all negative keywords present in the text
    matched_keywords = [kw for kw in NEGATIVE_KEYWORDS if kw in text_lower]

    # Map keywords to pain point categories
    pain_points = set()
    for category, keywords in PAIN_POINT_MAP.items():
        if any(kw in text_lower for kw in keywords):
            pain_points.add(category)

    return matched_keywords, list(pain_points)