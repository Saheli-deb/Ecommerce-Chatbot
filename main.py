# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from chatbot import get_bot_response

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="An OpenAI-powered chatbot API for e-commerce platforms",
    version="1.0.0"
)

# CORS for frontend (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with deployed site later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response schemas
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

# Health check
@app.get("/", tags=["Root"], summary="Root")
async def root():
    return {"message": "E-commerce chatbot is up and running!"}

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    try:
        response = get_bot_response(request.query)
        return {"response": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
