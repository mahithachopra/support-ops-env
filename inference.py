def extract_reward(result):
    try:
        reward = result.get("reward", 0)

        # Case 1: reward is number
        if isinstance(reward, (int, float)):
            return reward

        # Case 2: reward is dict
        if isinstance(reward, dict):
            # try common keys
            return (
                reward.get("score") or
                reward.get("value") or
                reward.get("reward") or
                0
            )

        return 0

    except Exception:
        return 0
