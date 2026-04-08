import requests

BASE_URL = "http://localhost:7860"


def safe_post(endpoint, data=None):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def extract_reward(result):
    try:
        reward = result.get("reward", 0)

        if isinstance(reward, (int, float)):
            return reward

        if isinstance(reward, dict):
            return (
                reward.get("score") or
                reward.get("value") or
                reward.get("reward") or
                0
            )

        return 0
    except:
        return 0


def run_episode():
    obs = safe_post("/reset")
    if not obs:
        return 0

    total_reward = 0
    done = False
    steps = 0

    while not done and steps < 10:
        action = {
            "action_type": "classify",
            "content": "billing"
        }

        result = safe_post("/step", action)
        if not result:
            break

        total_reward += extract_reward(result)
        done = result.get("done", True)
        steps += 1

    return total_reward


if __name__ == "__main__":
    try:
        score = run_episode()
        print("Final Score:", score)
    except Exception as e:
        print("Fatal Error:", e)
