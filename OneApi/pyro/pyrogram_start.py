from pyrogram import Client, idle
from .. import *
import logging
import asyncio
import time
import threading

def start():
    time.sleep(2.5)
    logging.info("Starting pyrogram...")
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)    # Set it as the current event loop
    bot.run()  # Run the bot within this loop

oh = threading.Thread(target=start)
oh.start()
