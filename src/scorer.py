from src.model import MatchResult

def calculate_score(match_result: MatchResult) -> float:
    """
    Returns a score between 0 and 100.
    """
    score = match_result.score

    if score <= 1:
        score *= 100

    return round(score, 2)
