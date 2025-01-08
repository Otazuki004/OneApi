from quart_cors import cors
from quart import Quart
from pyrogram import Client, idle
import asyncio
import os
from . import *

# Initialize Quart app and Pyrogram bot
app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_quart():
    print("Starting Quart...")
    # Run Quart server using Quart's internal event loop
    await app.run_task(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Quart stopped.")

async def start_pyrogram():
    print("Starting Pyrogram bot...")
    await bot.start()  # Start Pyrogram bot
    await idle()  # Keep Pyrogram running

async def main():
    print("Starting both Pyrogram and Quart...")
    # Run both Quart and Pyrogram in parallel
    await asyncio.gather(run_quart(), start_pyrogram())

if __name__ == '__main__':
    asyncio.run(main())
