import json
from graders import classification_grader, action_grader, resolution_grader

# Load your tickets
with open("env/data/tickets.json") as f:
    tickets = json.load(f)

tasks = [
    {
        "id": f"task_{tickets[0]['id']}_classify",
        "prompt": (
            f"Support ticket: '{tickets[0]['text']}'. "
            "Classify this ticket by category (e.g. billing, technical, account)."
        ),
        "ticket": tickets[0],
        "grader": classification_grader,
    },
    {
        "id": f"task_{tickets[1]['id']}_action",
        "prompt": (
            f"Support ticket: '{tickets[1]['text']}'. "
            "Decide the appropriate action: refund, escalate, or resolve."
        ),
        "ticket": tickets[1],
        "grader": action_grader,
    },
    {
        "id": f"task_{tickets[2]['id']}_resolve",
        "prompt": (
            f"Support ticket: '{tickets[2]['text']}'. "
            "Handle this ticket end-to-end and resolve the issue."
        ),
        "ticket": tickets[2],
        "grader": resolution_grader,
    },
]
