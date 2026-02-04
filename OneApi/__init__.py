import logging
from fastapi import FastAPI, APIRouter
from .auth import Auth

logging.basicConfig(
  format="[OneApi] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)
logger = logging.getLogger("OneApi")

app = FastAPI()
authRouter: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

auth = Auth()

__version__ = "02.2026"