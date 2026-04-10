import requests
import os
import time
from openai import OpenAI

BASE_URL = "http://localhost:7860"

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY"),
)


# ✅ WAIT FOR SERVER (CRITICAL FIX)
def wait_for_server():
    for _ in range(15):
        try:
            r = requests.get(f"{BASE_URL}/", timeout=2)
            if r.status_code == 200:
                return True
        except:
            time.sleep(2)
    return False


# ✅ SAFE POST WITH RETRIES
def safe_post(endpoint, data=None):
    for _ in range(5):
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            time.sleep(1)
    return None


def extract_reward(result):
    try:
        reward = result.get("reward", 0)

        if isinstance(reward, (int, float)):
            return reward

        if isinstance(reward, dict):
            return reward.get("score", 0)

        return 0
    except:
        return 0


def get_action_from_llm(observation):
    try:
        prompt = f"""
You are a customer support agent.

Observation:
{observation}

Choose best action:
- classify (billing/technical/account)
- refund
- escalate
- resolve

Respond ONLY in JSON:
{{"action_type": "...", "content": "..."}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"LLM error: {e}", flush=True)
        return {"action_type": "classify", "content": "billing"}


def run_episode(task_name="support_task"):
    print(f"[START] task={task_name}", flush=True)

    # 🔥 WAIT BEFORE CALLING API
    if not wait_for_server():
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    obs = safe_post("/reset", {})
    if not obs:
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    total_reward = 0
    done = False
    step_count = 0

    while not done and step_count < 10:
        step_count += 1

        action = get_action_from_llm(obs)

        result = safe_post("/step", action)
        if not result:
            break

        reward_value = extract_reward(result)
        total_reward += reward_value

        print(f"[STEP] step={step_count} reward={reward_value}", flush=True)

        obs = result.get("observation", {})
        done = result.get("done", True)

    print(f"[END] task={task_name} score={total_reward} steps={step_count}", flush=True)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception as e:
        print(f"[END] task=error score=0 steps=0", flush=True)
