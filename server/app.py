from fastapi import FastAPI
from env.core import SupportOpsEnv
from env.models import Action
import uvicorn

app = FastAPI()
env = SupportOpsEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: dict):
    act = Action(**action)
    obs, reward, done, info = env.step(act)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()


def main():
    return app


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)
