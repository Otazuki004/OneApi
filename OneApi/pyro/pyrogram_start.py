from pyrogram import Client
from .. import *
import logging
import asyncio
import time

def start():
    time.sleep(2.5)
    logging.info("Starting Pyrogram...")

    # Create and set a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Run the bot manually in the custom loop
    bot.start()  # Starts the Pyrogr
    idle()

start()
