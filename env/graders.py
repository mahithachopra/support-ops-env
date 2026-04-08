def grade_classification(ticket, action):
    if action.action_type != "classify":
        return 0.0
    return 1.0 if action.content == ticket["category"] else 0.0


def grade_action(ticket, action):
    if ticket["category"] == "billing" and action.action_type == "refund":
        return 1.0
    if ticket["priority"] == "high" and action.action_type == "escalate":
        return 1.0
    if ticket["category"] == "account" and action.action_type == "resolve":
        return 1.0
    return 0.0


def grade_resolution(ticket, actions):
    has_classify = any(a.action_type == "classify" for a in actions)
    has_action = any(a.action_type in ["refund", "escalate", "resolve"] for a in actions)

    if has_classify and has_action:
        return 1.0
    elif has_classify or has_action:
        return 0.5
    else:
        return 0.0