def clamp(score: float) -> float:
    return max(0.05, min(score, 0.95))

def _get_action_type(h):
    """Handle both dict and Pydantic HistoryEntry objects"""
    if isinstance(h, dict):
        return h["action_type"]
    return h.action_type

def classification_grader(history=None):
    if not history:
        return 0.5
    count = sum(1 for h in history if _get_action_type(h) == "classify")
    score = 0.2 + 0.2 * count
    return clamp(score)

def action_grader(history=None):
    if not history:
        return 0.5
    count = sum(1 for h in history if _get_action_type(h) in ["refund", "escalate"])
    score = 0.2 + 0.2 * count
    return clamp(score)

def resolution_grader(history=None):
    if not history:
        return 0.5
    resolved = any(_get_action_type(h) == "resolve" for h in history)
    score = 0.3 if not resolved else 0.8
    return clamp(score)
