from env.models import Observation, Action
from env.graders import (
    classification_grader,
    action_grader,
    resolution_grader
)
from env.reward import compute_reward


class SupportOpsEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_step = 0
        self.done = False

        # State tracking
        self.state_data = {
            "correct_classifications": 0,
            "total_classifications": 0,
            "correct_actions": 0,
            "total_actions": 0,
            "resolved": False
        }

        self.current_ticket = {
            "text": "Customer was charged twice for subscription",
            "label": "billing"
        }

        return Observation(
            ticket=self.current_ticket["text"],
            step=self.current_step
        )

    def step(self, action: Action):
        if self.done:
            return self._get_observation(), 0.0, True, {}

        self.current_step += 1

        reward = 0.0

        # ---------------------------
        # CLASSIFICATION TASK
        # ---------------------------
        if action.action_type == "classify":
            self.state_data["total_classifications"] += 1

            if action.content == self.current_ticket["label"]:
                self.state_data["correct_classifications"] += 1
                reward += 0.5
            else:
                reward += 0.2

        # ---------------------------
        # ACTION TASK
        # ---------------------------
        elif action.action_type in ["refund", "escalate"]:
            self.state_data["total_actions"] += 1

            # Simple logic: billing → refund is correct
            if (
                self.current_ticket["label"] == "billing"
                and action.action_type == "refund"
            ):
                self.state_data["correct_actions"] += 1
                reward += 0.5
            else:
                reward += 0.3

        # ---------------------------
        # RESOLUTION TASK
        # ---------------------------
        elif action.action_type == "resolve":
            self.state_data["resolved"] = True
            reward += 0.4

        # ---------------------------
        # END CONDITION
        # ---------------------------
        if self.current_step >= 6 or self.state_data["resolved"]:
            self.done = True

        # ---------------------------
        # TASK SCORES (STRICT RANGE)
        # ---------------------------
        task_scores = {
            "classification": classification_grader(self.state_data),
            "action": action_grader(self.state_data),
            "resolution": resolution_grader(self.state_data),
        }

        observation = self._get_observation()

        info = {
            "task_scores": task_scores
        }

        return observation, reward, self.done, info

    def state(self):
        return self.state_data

    def _get_observation(self):
        return Observation(
            ticket=self.current_ticket["text"],
            step=self.current_step
        )
