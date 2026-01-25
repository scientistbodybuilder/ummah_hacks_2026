"""FastAPI app entry point for SHARAH backend."""

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import shariah_router

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SHARAH API",
    description="Shariah compliance validation for Islamic financial products",
    version="1.0.0",
)

# CORS: allow frontend origins (local + production)
_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://sharah-frontend.vercel.app",
    "https://sharah.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(shariah_router)


@app.get("/health")
async def health() -> dict:
    """Health check for load balancers and monitoring."""
    return {"status": "ok", "service": "sharah-api"}
