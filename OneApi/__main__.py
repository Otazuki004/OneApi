from quart_cors import cors
from quart import *
from pyrogram import *
import os
import asyncio
from signal import SIGINT, SIGTERM
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

async def shutdown():
    print("Shutting down...")
    await bot.stop()
    print("Bot stopped.")

async def main():
    # Use asyncio.gather to run both Pyrogram and Quart concurrently
    try:
        await asyncio.gather(run_bot(), run_quart())
    except (KeyboardInterrupt, asyncio.CancelledError):
        await shutdown()

if __name__ == '__main__':
    # Handle shutdown signals (Ctrl+C)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: asyncio.create_task(shutdown()))

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(shutdown())
        loop.close()
