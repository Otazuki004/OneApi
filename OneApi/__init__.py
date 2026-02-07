import logging
from fastapi import FastAPI, APIRouter
from .ws.client import Client

logging.basicConfig(
    format="[OneApi] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logger = logging.getLogger("OneApi")

app = FastAPI()

ws_router = APIRouter(prefix="/ws", tags=["websockets"])

ws_client = Client(ws_router)  # ✅ FIXED

app.include_router(ws_router)

# load_modules_from_folder("OneApi/routes")

@app.get("/")
async def home():
    return {"status": "ok", "message": "Welcome to OneApi!"}

__version__ = "02.2026"
