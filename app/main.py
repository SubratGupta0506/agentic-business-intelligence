from fastapi import FastAPI

app = FastAPI(
    title="Agentic Business Decision Intelligence System"
)


@app.get("/")
def root():
    return {
        "message": "Agentic Business Decision Intelligence System is running"
    }