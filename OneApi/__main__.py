from quart_cors import cors
from quart import *
from pyrogram import *
import os
import asyncio
from . import bot, app

# Enable CORS for the app
app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_bot():
    print("Starting Pyrogram...")
    await bot.start()
    print("Bot started successfully")
    await idle()

async def run_quart():
    print("Starting Quart...")
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Quart stopped.")

def main():
    # Create a new event loop for Quart
    quart_loop = asyncio.new_event_loop()

    # Start Quart in its own loop
    quart_task = quart_loop.create_task(run_quart())

    # Run Quart's loop in a background task
    def start_quart():
        asyncio.set_event_loop(quart_loop)
        quart_loop.run_forever()

    # Run Quart in the background
    asyncio.run_coroutine_threadsafe(start_quart(), quart_loop)

    # Run Pyrogram in the main loop
    print("Starting Pyrogram loop...")
    asyncio.run(run_bot())

if __name__ == '__main__':
    main()
