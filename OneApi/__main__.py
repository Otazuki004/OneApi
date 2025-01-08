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
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Quart stopped.")

async def main():
    print("Starting bot...")
    await bot.start()  # Start the Pyrogram bot
    print("Bot started.")
    
    # Run Quart and idle concurrently
    await asyncio.gather(
        run_quart(),
        idle()  # Keep Pyrogram running
    )

if __name__ == '__main__':
    asyncio.run(main())
