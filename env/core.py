import json
from .models import Observation, Ticket
from .reward import reward_fn
from .graders import grade_classification, grade_action, grade_resolution


class SupportOpsEnv:
    def __init__(self):
        with open("env/data/tickets.json") as f:
            self.tickets = json.load(f)
        self.reset()

    def reset(self):
        self.current_index = 0
        self.history = []
        self.score = 0
        self.ticket_actions = {}

        return self._get_observation()

    def _get_observation(self):
        ticket_dict = self.tickets[self.current_index]
        ticket = Ticket(**ticket_dict)

        return Observation(
            current_ticket=ticket,
            history=self.history
        )

    def step(self, action):
        ticket = self.tickets[self.current_index]

        # Reward
        reward = reward_fn(ticket, action, self.history)

        # Update state
        self.score += reward.score
        self.history.append(str(action))

        # Track per-ticket actions
        if self.current_index not in self.ticket_actions:
            self.ticket_actions[self.current_index] = []

        self.ticket_actions[self.current_index].append(action)

        info = {}
        done = False

        # Move to next ticket ONLY after resolution action
        if action.action_type in ["refund", "escalate", "resolve"]:
            if self.current_index >= len(self.tickets) - 1:
                done = True
            else:
                self.current_index += 1

        # Final grading
        if done:
            scores = {
                "classification": 0.0,
                "action": 0.0,
                "resolution": 0.0
            }

            for idx, ticket in enumerate(self.tickets):
                actions = self.ticket_actions.get(idx, [])

                classification_actions = [
                    a for a in actions if a.action_type == "classify"
                ]

                action_actions = [
                    a for a in actions
                    if a.action_type in ["refund", "escalate", "resolve"]
                ]

                if classification_actions:
                    scores["classification"] += grade_classification(
                        ticket, classification_actions[0]
                    )

                if action_actions:
                    scores["action"] += grade_action(
                        ticket, action_actions[0]
                    )

                scores["resolution"] += grade_resolution(ticket, actions)

            n = len(self.tickets)
            scores = {k: round(v / n, 2) for k, v in scores.items()}

            info["scores"] = scores

        return self._get_observation(), reward, done, info

    def state(self):
        return {
            "index": self.current_index,
            "score": self.score,
            "steps": len(self.history)
        }