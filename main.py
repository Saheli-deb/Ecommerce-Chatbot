# # main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from chatbot import get_bot_response

# app = FastAPI(
#     title="E-Commerce Chatbot API",
#     description="An OpenAI-powered chatbot API for e-commerce platforms",
#     version="1.0.0"
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class ChatRequest(BaseModel):
#     query: str

# class ChatResponse(BaseModel):
#     response: str


# @app.get("/", tags=["Root"], summary="Root")
# async def root():
#     return {"message": "E-commerce chatbot is up and running!"}


# @app.post("/chat", response_model=ChatResponse, tags=["Chat"])
# async def chat(request: ChatRequest):
#     try:
#         response = get_bot_response(request.query)
#         return {"response": response}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from chatbot import get_bot_response
import base64

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="An OpenAI-powered chatbot API for e-commerce platforms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    file_name: Optional[str] = None
    file_data: Optional[str] = None  # base64-encoded

class ChatResponse(BaseModel):
    response: str

@app.get("/", tags=["Root"])
async def root():
    return {"message": "E-commerce chatbot is up and running!"}

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    try:
        if request.file_name and request.file_data:
            decoded_data = base64.b64decode(request.file_data)
            with open(f"received_{request.file_name}", "wb") as f:
                f.write(decoded_data)
            print(f"📄 Received file: {request.file_name}")

        response = get_bot_response(request.query)
        return {"response": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
