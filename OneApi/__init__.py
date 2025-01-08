from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
from variables import *
import os
from quart import Quart
from pyrogram import *
from variables import *

logging.basicConfig(
  format="[OneApi] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

MONGO_DB_URL = os.environ.get("MONGO_DB_URL") or VAR_MONGO_DB_URI
API_ID = os.environ.get("API_ID") or VAR_API_ID
API_HASH = os.environ.get("API_HASH") or VAR_API_HASH
HANDLER = ["/"]
TOKEN = os.environ.get("TOKEN") or VAR_TOKEN
MY_VERSION = 0.1
DEVS = os.environ.get("DEVS") or VAR_DEVS
# _______________________________________
if not API_ID or not API_HASH or not TOKEN or not MONGO_DB_URI:
  raise ValueError("Bro thought he can run anything lol, i mean you forgot some vars put on variables.py")
  exit()
# _-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_|
if len(TOKEN) > 50: bot = Client("OneApi", session_string=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="OneApi/pyro"))
else: bot = Client("OneApi", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="OneApi/pyro"))
# ———— R U N ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
async def run(command):
  try:
    process = await asyncio.create_subprocess_shell(
      command,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
      start_new_session=True
    )
    stdout, stderr = await process.communicate()
    if stdout:
      return stdout.decode().strip()
    if stderr:
      return stderr.decode().strip()
  except Exception as e:
    logging.error(f"Failed to run command '{command}': {e}")
    return False
# _______________________________________________________________
DATABASE = AsyncIOMotorClient(MONGO_DB_URL)["OneApi"]
app = Quart(__name__)
