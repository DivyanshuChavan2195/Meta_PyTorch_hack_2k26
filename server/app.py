from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    return {
        "observation": {},
        "info": {}
    }

@app.post("/step")
def step(action: dict):
    return {
        "observation": {},
        "reward": 0,
        "done": False,
        "info": {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)