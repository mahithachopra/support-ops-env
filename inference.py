import requests

BASE_URL = "http://localhost:7860"

def run_episode():
    total_reward = 0

    # Reset environment
    obs = requests.post(f"{BASE_URL}/reset").json()

    done = False

    while not done:
        # Simple baseline policy
        action = {
            "action_type": "classify",
            "content": "billing"
        }

        response = requests.post(f"{BASE_URL}/step", json=action).json()

        reward = response["reward"]
        done = response["done"]

        total_reward += reward

    return total_reward


if __name__ == "__main__":
    score = run_episode()
    print(f"Final Score: {score}")