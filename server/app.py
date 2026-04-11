from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from env.core import SupportOpsEnv
from env.models import Action
import os

app = FastAPI()
env = SupportOpsEnv()

# Serve the web UI
@app.get("/", response_class=HTMLResponse)
def root():
    web_path = os.path.join(os.path.dirname(__file__), "web.html")
    with open(web_path) as f:
        return f.read()

@app.get("/web", response_class=HTMLResponse)
def web():
    web_path = os.path.join(os.path.dirname(__file__), "web.html")
    with open(web_path) as f:
        return f.read()

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
                "name": "classification_easy",
                "description": "Classify support ticket by category",
                "grader": "env.graders:classification_grader",
                "score": classification_grader([{"action_type": "classify", "content": "billing"}]),
            },
            {
                "id": "action_medium",
                "name": "action_medium",
                "description": "Take correct action on support ticket",
                "grader": "env.graders:action_grader",
                "score": action_grader([{"action_type": "refund", "content": "processed"}]),
            },
            {
                "id": "resolution_hard",
                "name": "resolution_hard",
                "description": "Fully resolve the support ticket",
                "grader": "env.graders:resolution_grader",
                "score": resolution_grader([{"action_type": "resolve", "content": "closed"}]),
            },
        ]
    })

@app.post("/grade")
async def grade(request: Request):
    from env.graders import classification_grader, action_grader, resolution_grader
    body = await request.json()
    task_id = body.get("task_id", "")
    history = body.get("history", [])
    graders = {
        "classification_easy": classification_grader,
        "action_medium": action_grader,
        "resolution_hard": resolution_grader,
    }
    grader = graders.get(task_id)
    if not grader:
        return JSONResponse({"error": f"Unknown task_id: {task_id}"}, status_code=404)
    score = grader(history) if history else grader()
    return {"task_id": task_id, "score": score}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
