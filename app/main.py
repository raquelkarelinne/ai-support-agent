from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from .agent import run_agent
from .mock_api import router as mock_router

load_dotenv()
app = FastAPI(title="AI Support Agent")
app.include_router(mock_router)

class ChatIn(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(body: ChatIn):  # def (não async) para permitir a chamada HTTP à API mock
    return run_agent(body.message)
