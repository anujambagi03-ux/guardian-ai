from fastapi import FastAPI

app = FastAPI(
    title="Guardian AI",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "Guardian AI",
        "status": "Backend Running"
    }

@app.get("/health")
def health():
    return {
        "message": "System Healthy"
    }