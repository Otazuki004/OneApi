from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from . import bot, app
from . import *

# Enable CORS for the app
app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_bot():
    await bot.start()
    await bot.idle()  # Keeps the bot running

async def run_quart():
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def start_quart():
    # Run the Quart app's event loop in a separate thread
    asyncio.run(run_quart())

def start_bot():
    # Run the Pyrogram bot's event loop in a separate thread
    asyncio.run(run_bot())

if __name__ == '__main__':
    # Use ThreadPoolExecutor to run both the bot and Quart in separate threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(start_quart)
        executor.submit(start_bot)
