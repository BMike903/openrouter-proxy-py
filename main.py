import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

load_dotenv()

ALLOWED_ORIGINS = [
    "https://bmike903.github.io",
]

TRUSTED_CLIENT_TOKEN = os.getenv("TRUSTED_CLIENT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Proxy is working"}

@app.get("/returnJson")
async def return_json(request: Request):
    return dict(request.query_params)

@app.post("/message")
async def message(request: Request):
    body = await request.json()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions", 
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=body,
                timeout=60
            )
            return JSONResponse(content=response.json())
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))