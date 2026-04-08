from .models import Reward

def reward_fn(ticket, action, history):
    score = 0.0

    if action.action_type == "classify":
        if action.content == ticket["category"]:
            score += 0.5
        else:
            score -= 0.2

    if action.action_type == "refund" and ticket["category"] == "billing":
        score += 0.5

    if action.action_type == "escalate" and ticket["priority"] == "high":
        score += 0.3

    if action.action_type == "resolve":
        score += 0.2

    # partial progress reward
    score += 0.05 * len(history)

    return Reward(score=score, feedback="step evaluated")