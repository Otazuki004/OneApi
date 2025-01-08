from pyrogram import Client
from .. import *
import logging
import asyncio
import time
import threading

def start():
    time.sleep(2.5)
    logging.info("Starting Pyrogram...")

    # Create and set a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Run the bot manually in the custom loop
    bot.start()  # Starts the Pyrogram client
    try:
        logging.info("Bot is running...")
        loop.run_forever()  # Keeps the event loop running
    finally:
        bot.stop()  # Clean up when stopping the loop
        logging.info("Bot stopped.")

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create a thread and start the bot
oh = threading.Thread(target=start)
oh.start()
