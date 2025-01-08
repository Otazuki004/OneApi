from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import asyncio
from . import bot, app

# Enable CORS for the app
app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_bot():
    await bot.start()
    print("Bot started successfully")
    await bot.idle()

async def run_quart(loop):
    # Set a new event loop for Quart
    asyncio.set_event_loop(loop)
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def main():
    # Default loop for Pyrogram
    pyrogram_loop = asyncio.get_event_loop()

    # Create a new event loop for Quart
    quart_loop = asyncio.new_event_loop()

    # Run Pyrogram in the default loop
    pyrogram_task = pyrogram_loop.create_task(run_bot())

    # Run Quart in its own loop
    quart_loop.run_until_complete(run_quart(quart_loop))

    # Run Pyrogram loop until it's done
    pyrogram_loop.run_forever()

if __name__ == '__main__':
    main()
