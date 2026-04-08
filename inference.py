import requests
import time

BASE_URL = "http://localhost:7860"

def safe_post(endpoint, data=None):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error calling {endpoint}: {e}")
        return None


def run_episode():
    obs = safe_post("/reset")
    if not obs:
        return 0

    total_reward = 0
    done = False

    while not done:
        action = {
            "action_type": "classify",
            "content": "billing"
        }

        result = safe_post("/step", action)

        if not result:
            break

        total_reward += result.get("reward", 0)
        done = result.get("done", True)

    return total_reward


if __name__ == "__main__":
    score = run_episode()
    print("Final Score:", score)
