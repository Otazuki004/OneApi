from quart_cors import cors
from quart import Quart
from pyrogram import Client, idle
import asyncio
import os
import threading
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

def run_quart_in_thread():
    """Run Quart in a separate thread."""
    print("Starting Quart...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_task(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))))

async def start_pyrogram():
    """Start Pyrogram bot and keep it running."""
    print("Starting Pyrogram bot...")
    await bot.start()  # Start Pyrogram bot
    await idle()  # Keep Pyrogram running

async def main():
    print("Starting both Pyrogram and Quart...")
    # Run Quart in a separate thread
    quart_thread = threading.Thread(target=run_quart_in_thread)
    quart_thread.start()

    # Run Pyrogram in the main event loop
    await start_pyrogram()

if __name__ == '__main__':
    asyncio.run(main())
