def clamp(score: float) -> float:
    # STRICT (0,1)
    return max(0.05, min(score, 0.95))


def classification_grader(history):
    # always >= 0.2
    count = sum(1 for h in history if h["action_type"] == "classify")
    score = 0.2 + 0.2 * count
    return clamp(score)


def action_grader(history):
    count = sum(1 for h in history if h["action_type"] in ["refund", "escalate"])
    score = 0.2 + 0.2 * count
    return clamp(score)


def resolution_grader(history):
    resolved = any(h["action_type"] == "resolve" for h in history)
    score = 0.3 if not resolved else 0.8
    return clamp(score)
