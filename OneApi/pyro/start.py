from .. import *
from pyrogram import *
import logging 
import traceback 

logging.info("Plugin loaded")

@Client.on_message(filters.command('start'))
async def start(_, message):
  logging.info("Triggered")
  try: await message.reply("Hmm I'm alive probably")
  except: logging.error(traceback.format_exc())
