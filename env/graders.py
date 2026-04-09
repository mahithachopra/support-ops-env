def clamp_score(score):
    if score <= 0:
        return 0.1
    if score >= 1:
        return 0.9
    return score


def classification_grader(history):
    score = sum(0.3 for h in history if h["action_type"] == "classify")
    return clamp_score(min(score, 0.9))


def action_grader(history):
    score = sum(0.4 for h in history if h["action_type"] in ["refund", "escalate"])
    return clamp_score(min(score, 0.9))


def resolution_grader(history):
    score = 0.8 if any(h["action_type"] == "resolve" for h in history) else 0.2
    return clamp_score(score)
