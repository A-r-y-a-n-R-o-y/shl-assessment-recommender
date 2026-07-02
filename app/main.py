from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI

from app.models import ChatRequest, ChatResponse
from app.agent import SHLAgent
app = FastAPI(title="SHL Assessment Recommender")
agent = SHLAgent()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = agent.process(request.messages)

    return ChatResponse(**response)