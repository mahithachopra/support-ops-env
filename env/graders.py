def clamp_score(score: float) -> float:
    """
    Ensure score is strictly between 0 and 1
    """
    if score <= 0:
        return 0.1
    if score >= 1:
        return 0.9
    return score


def classification_grader(history):
    score = 0.0

    for h in history:
        if h["action_type"] == "classify":
            score += 0.3

    score = min(score, 0.9)
    return clamp_score(score)


def action_grader(history):
    score = 0.0

    for h in history:
        if h["action_type"] in ["refund", "escalate"]:
            score += 0.4

    score = min(score, 0.9)
    return clamp_score(score)


def resolution_grader(history):
    score = 0.0

    for h in history:
        if h["action_type"] == "resolve":
            score = 0.8

    return clamp_score(score)
