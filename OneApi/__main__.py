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
    await bot.start()
    # Ensure the bot stays alive by calling idle()
    await bot.idle()

async def run_quart():
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

async def main():
    # Create a task for both the Quart app and Pyrogram bot to run concurrently
    bot_task = asyncio.create_task(run_bot())
    quart_task = asyncio.create_task(run_quart())
    
    # Await both tasks to ensure they run concurrently and don't stop prematurely
    await asyncio.gather(bot_task, quart_task)

if __name__ == '__main__':
    # Run the event loop with both Quart and Pyrogram tasks
    asyncio.run(main())
