from dotenv import load_dotenv

print("===== Starting SHL Assessment Recommender =====")

# ------------------------------------
# Load environment variables
# ------------------------------------

load_dotenv()

print("Environment variables loaded.")

# ------------------------------------
# Imports
# ------------------------------------

from fastapi import FastAPI

print("FastAPI imported.")

from app.models import ChatRequest, ChatResponse

print("Models imported.")

from app.agent import SHLAgent

print("SHLAgent imported.")

# ------------------------------------
# Create FastAPI app
# ------------------------------------

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)

print("FastAPI application created.")

# ------------------------------------
# Initialize Agent
# ------------------------------------

print("Initializing SHLAgent...")

agent = SHLAgent()

print("SHLAgent initialized successfully.")

# ------------------------------------
# Root Endpoint
# ------------------------------------

@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommender API",
        "status": "running"
    }

# ------------------------------------
# Health Check
# ------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# ------------------------------------
# Chat Endpoint
# ------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    print("Received chat request.")

    response = agent.process(request.messages)

    print("Returning response.")

    return ChatResponse(**response)