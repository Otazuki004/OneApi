from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import asyncio
from . import bot, app
from . import *

# Enable CORS for the app
app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_bot():
    await bot.start()  # Start the Pyrogram bot
    await idle()  # Keeps the bot running indefinitely

async def run_quart():
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

async def main():
    # Run both Quart and Pyrogram in separate tasks
    bot_task = asyncio.create_task(run_bot())
    quart_task = asyncio.create_task(run_quart())
    
    # Ensure both tasks run concurrently in the same event loop
    await bot_task
    await quart_task

if __name__ == '__main__':
    # Run the event loop with both tasks
    asyncio.run(main())
