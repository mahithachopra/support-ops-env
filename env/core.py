from typing import Tuple, Dict, Any
from env.models import Action, Observation, Ticket
from env.graders import classification_grader, action_grader, resolution_grader

class SupportOpsEnv:
    def __init__(self):
        self.tickets = [
            {"id": "1", "text": "Customer was charged twice for subscription", "category": "billing",  "priority": "high"},
            {"id": "2", "text": "App crashes when clicking checkout button",    "category": "technical","priority": "high"},
            {"id": "3", "text": "Unable to login to account",                  "category": "account",  "priority": "medium"},
        ]
        self.index = 0
        self.history = []

    def reset(self) -> Observation:
        self.index = 0
        self.history = []
        return Observation(
            current_ticket=Ticket(**self.tickets[self.index]),
            history=self.history
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.history.append({
            "action_type": action.action_type,
            "content": action.content
        })
        reward = {"resolve": 0.8, "escalate": 0.6, "refund": 0.7, "classify": 0.65}.get(action.action_type, 0.5)
        done = action.action_type == "resolve"
        obs = Observation(
            current_ticket=Ticket(**self.tickets[self.index]),
            history=self.history
        )
        task_scores = {
            "classification": classification_grader(self.history),
            "action":         action_grader(self.history),
            "resolution":     resolution_grader(self.history),
        }
        return obs, reward, done, {"task_scores": task_scores}
