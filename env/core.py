from typing import Tuple, Dict, Any
from env.models import Action, Observation


class SupportOpsEnv:
    def __init__(self):
        self.tickets = [
            "Customer was charged twice for subscription",
            "App crashes when clicking checkout button",
            "Unable to login to account"
        ]
        self.index = 0
        self.history = []

    def reset(self) -> Observation:
        self.index = 0
        self.history = []

        return Observation(
            current_ticket=self.tickets[self.index],
            history=self.history
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        reward = 0.5
        done = False

        # Track history
        self.history.append({
            "action_type": action.action_type,
            "content": action.content
        })

        if action.action_type == "resolve":
            reward = 0.8
            done = True
        elif action.action_type == "escalate":
            reward = 0.6
        elif action.action_type == "refund":
            reward = 0.7
        elif action.action_type == "classify":
            reward = 0.65

        obs = Observation(
            current_ticket=self.tickets[self.index],
            history=self.history
        )

        return obs, reward, done, {}
