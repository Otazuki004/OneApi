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
    await app.run_task(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Quart stopped.")

async def main():
    print("Starting bot and Quart together...")
    await bot.start()  # Start Pyrogram bot
    
    # Run both Quart and Pyrogram idle in the same loop
    quart_task = asyncio.create_task(run_quart())  # Run Quart server
    await idle()  # Keep Pyrogram running
    
    print("Stopping bot...")
    await bot.stop()  # Stop Pyrogram bot when idle exits
    quart_task.cancel()  # Cancel the Quart server task

if __name__ == '__main__':
    asyncio.run(main())
