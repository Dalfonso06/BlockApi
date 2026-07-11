from fastapi import FastAPI

app = FastAPI(
    title="Block API",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {
        "message": "Block API is running"
    }