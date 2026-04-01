from fastapi import FastAPI
from app.env import TrustTriageEnv
from app.models import Action

app = FastAPI(title="TrustTriageEnv")

env = TrustTriageEnv()


@app.get("/")
def root():
    return {"message": "TrustTriageEnv is running"}


@app.post("/reset")
def reset(task_id: str = "easy_1"):
    obs = env.reset(task_id=task_id)
    return obs.model_dump()


@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return result.model_dump()


@app.get("/state")
def state():
    st = env.state()
    return st.model_dump() if st else {"message": "No active episode"}