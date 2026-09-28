from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.agent import chat_with_customer
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="MemoryDesk",
    description="AI Customer Support Agent with Hindsight Memory"
)


class ChatRequest(BaseModel):
    customer_name: str
    message: str

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    result = chat_with_customer(
    request.customer_name,
    request.message
)

    return {
        "answer": result["answer"],
        "memories": result["memories"]
    }

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)