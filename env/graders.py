def clamp(score: float) -> float:
    return max(0.05, min(score, 0.95))

def classification_grader(history=None):
    if history is None:
        return 0.5  # default probe score — strictly between 0 and 1
    count = sum(1 for h in history if h["action_type"] == "classify")
    score = 0.2 + 0.2 * count
    return clamp(score)

def action_grader(history=None):
    if history is None:
        return 0.5
    count = sum(1 for h in history if h["action_type"] in ["refund", "escalate"])
    score = 0.2 + 0.2 * count
    return clamp(score)

def resolution_grader(history=None):
    if history is None:
        return 0.5
    resolved = any(h["action_type"] == "resolve" for h in history)
    score = 0.3 if not resolved else 0.8
    return clamp(score)
