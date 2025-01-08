from pyrogram import Client, idle
from .. import *
import logging
import asyncio
import time
import threading

def start():
  time.sleep(2.5)
  logging.info("Starting pyrogram...")
  bot.run()

oh = threading.Thread(target=start)
oh.start()
