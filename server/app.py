from fastapi import FastAPI
import sys
import os
import uvicorn

# ✅ FIX import path (CRITICAL for HF)
sys.path.append(os.getcwd())

from env.core import SupportOpsEnv
from env.models import Action

app = FastAPI()
env = SupportOpsEnv()


# ✅ ROOT (prevents 404 confusion)
@app.get("/")
def root():
    return {"status": "running"}


# ✅ SAFE RESET
@app.post("/reset")
def reset():
    try:
        obs = env.reset()
        return obs.dict()
    except Exception as e:
        return {"error": str(e)}


# ✅ SAFE STEP
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


# ✅ STATE
@app.get("/state")
def state():
    try:
        return env.state()
    except Exception as e:
        return {"error": str(e)}


# ✅ REQUIRED BY VALIDATOR
def main():
    return app


# ✅ RUN SERVER
if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)
