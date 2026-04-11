"""
Task definitions for the Support Ops Environment.
Each task has an id, description, and a grader function that returns
a float strictly between 0 and 1.
"""
from env.graders import classification_grader, action_grader, resolution_grader

TASKS = [
    {
        "id": "classification_easy",
        "name": "classification_easy",
        "description": "Classify support ticket by category (billing, technical, account)",
        "difficulty": "easy",
        "grader": classification_grader,
    },
    {
        "id": "action_medium",
        "name": "action_medium",
        "description": "Take correct action on support ticket (refund, escalate, resolve)",
        "difficulty": "medium",
        "grader": action_grader,
    },
    {
        "id": "resolution_hard",
        "name": "resolution_hard",
        "description": "Fully resolve the support ticket end-to-end",
        "difficulty": "hard",
        "grader": resolution_grader,
    },
]

def get_task(task_id: str):
    return next((t for t in TASKS if t["id"] == task_id), None)
