from fastapi import FastAPI
import sys
import os
import uvicorn

sys.path.append(os.getcwd())

from env.core import SupportOpsEnv
from env.models import Action

app = FastAPI()
env = SupportOpsEnv()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/reset")
def reset():
    try:
        obs = env.reset()
        return obs.dict()
    except Exception as e:
        return {"error": str(e)}


@app.post("/step")
def step(action: dict):
    try:
        act = Action(**action)
        obs, reward, done, info = env.step(act)

        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/state")
def state():
    return env.state()


# REQUIRED for validator
def main():
    return app


# REQUIRED for runtime
if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)
