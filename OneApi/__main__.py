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
    await idle()  # Keeps the bot running

async def run_quart():
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

async def main():
    # Run both the Quart app and Pyrogram bot concurrently in the same event loop
    await asyncio.gather(run_quart(), run_bot())

if __name__ == '__main__':
    # Run the event loop with both Quart and Pyrogram tasks
    asyncio.run(main())
