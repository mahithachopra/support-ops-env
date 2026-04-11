from fastapi import FastAPI
from fastapi.responses import JSONResponse
from env.core import SupportOpsEnv
from env.models import Action

app = FastAPI()
env = SupportOpsEnv()

@app.get("/")
def root():
    return {"message": "Support Ops Environment is running", "status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return {"index": env.index, "history": env.history}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    from env.graders import classification_grader, action_grader, resolution_grader
    return JSONResponse({
        "tasks": [
            {
                "id": "classification_easy",
                "description": "Classify support ticket by category",
                "score": classification_grader([{"action_type": "classify", "content": "billing"}]),
            },
            {
                "id": "action_medium",
                "description": "Take correct action on support ticket",
                "score": action_grader([{"action_type": "refund", "content": "processed"}]),
            },
            {
                "id": "resolution_hard",
                "description": "Fully resolve the support ticket",
                "score": resolution_grader([{"action_type": "resolve", "content": "closed"}]),
            },
        ]
    })

# ✅ Required for openenv validate
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
