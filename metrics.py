def score_exact_match(response: str, expected: str) -> float:
    """
    Returns 1.0 if response matches expected exactly, else 0.0
    """
    return 1.0 if response.strip().lower() == expected.strip().lower() else 0.0


def score_keyword_match(response: str, keywords: list) -> float:
    """
    Returns % of keywords found in the response.
    """
    if not keywords:
        return 0.0
    response_lower = response.lower()
    matched = sum(1 for kw in keywords if kw.lower() in response_lower)
    return round(matched / len(keywords), 2)


def score_length_penalty(response: str, min_words: int = 10, max_words: int = 500) -> float:
    """
    Penalizes responses that are too short or too long.
    Returns 1.0 if within range, scaled score otherwise.
    """
    word_count = len(response.split())
    if min_words <= word_count <= max_words:
        return 1.0
    elif word_count < min_words:
        return round(word_count / min_words, 2)
    else:
        return round(max_words / word_count, 2)


def compute_final_score(response: str, expected: str = "", keywords: list = [], min_words: int = 10, max_words: int = 500) -> float:
    """
    Combines all metrics into one final score (0.0 to 1.0)
    """
    scores = []

    if expected:
        scores.append(score_exact_match(response, expected))

    if keywords:
        scores.append(score_keyword_match(response, keywords))

    scores.append(score_length_penalty(response, min_words, max_words))

    return round(sum(scores) / len(scores), 2)