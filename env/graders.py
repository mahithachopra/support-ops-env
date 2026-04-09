def clamp_score(score):
    return max(0.01, min(0.99, score))


def classification_grader(state):
    total = max(1, state.get("total_classifications", 1))
    correct = state.get("correct_classifications", 0)
    return clamp_score(correct / total)


def action_grader(state):
    total = max(1, state.get("total_actions", 1))
    correct = state.get("correct_actions", 0)
    return clamp_score(correct / total)


def resolution_grader(state):
    resolved = state.get("resolved", False)
    score = 0.7 if resolved else 0.3
    return clamp_score(score)
