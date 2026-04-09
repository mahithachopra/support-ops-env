import requests

BASE_URL = "http://localhost:7860"


def safe_post(endpoint, data=None):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}", flush=True)
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


def run_episode(task_name="support_task"):
    print(f"[START] task={task_name}", flush=True)

    obs = safe_post("/reset")
    if not obs:
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    total_reward = 0
    done = False
    step_count = 0

    while not done and step_count < 10:
        step_count += 1

        action = {
            "action_type": "classify",
            "content": "billing"
        }

        result = safe_post("/step", action)
        if not result:
            break

        reward_value = extract_reward(result)
        total_reward += reward_value

        print(f"[STEP] step={step_count} reward={reward_value}", flush=True)

        done = result.get("done", True)

    print(f"[END] task={task_name} score={total_reward} steps={step_count}", flush=True)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception as e:
        print(f"[END] task=error score=0 steps=0", flush=True)
