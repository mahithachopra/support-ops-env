import random
from env.core import SupportOpsEnv
from env.models import Action

random.seed(42)


def simple_policy(obs):
    text = obs.current_ticket.text.lower()

    # Check last action
    last_action = obs.history[-1] if obs.history else ""

    # If last was classify → now act
    if "classify" in last_action:
        if "charged" in text:
            return Action(action_type="refund")
        elif "crash" in text:
            return Action(action_type="escalate")
        elif "password" in text:
            return Action(action_type="resolve")

    # Otherwise classify first
    if "charged" in text:
        return Action(action_type="classify", content="billing")
    elif "crash" in text:
        return Action(action_type="classify", content="technical")
    elif "password" in text:
        return Action(action_type="classify", content="account")

    return Action(action_type="resolve")


def run():
    env = SupportOpsEnv()
    obs = env.reset()
    total = 0

    max_steps = 20
    step_num = 0

    while step_num < max_steps:
        step_num += 1

        action = simple_policy(obs)

        obs, reward, done, info = env.step(action)
        total += reward.score

        print(f"\nStep {step_num}")
        print(f"Action: {action}")
        print(f"Reward: {reward.score}")
        print(f"Cumulative Score: {round(total, 3)}")

        if done:
            print("\n=== EPISODE COMPLETE ===")
            print("Final Score:", round(total, 3))
            print("Task Scores:", info.get("scores", {}))
            break

    if step_num >= max_steps:
        print("\n⚠️ Stopped due to max step limit (possible loop)")


if __name__ == "__main__":
    run()