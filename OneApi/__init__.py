import logging
from fastapi import FastAPI, APIRouter
from .ws.client import Client
from loader import load_modules_from_folder

logging.basicConfig(
  format="[OneApi] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)
logger = logging.getLogger("OneApi")

app = FastAPI()
wsRouter: APIRouter = APIRouter(prefix="/ws", tags=["websockets"])

Client = Client(wsRouter)

app.include_router(wsRouter)

load_modules_from_folder("OneApi/routes")

@app.get("/")
async def home():
    return {"status": "ok", "message": "Welcome to OneApi!"}

__version__ = "02.2026"