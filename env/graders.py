def clamp_score(score):
    # ensure STRICTLY between 0 and 1
    return max(0.01, min(0.99, score))


def classification_grader(state):
    correct = state.get("correct_classifications", 0)
    total = max(1, state.get("total_classifications", 1))

    score = correct / total
    return clamp_score(score)


def action_grader(state):
    correct = state.get("correct_actions", 0)
    total = max(1, state.get("total_actions", 1))

    score = correct / total
    return clamp_score(score)


def resolution_grader(state):
    resolved = state.get("resolved", False)

    score = 0.7 if resolved else 0.3
    return clamp_score(score)
