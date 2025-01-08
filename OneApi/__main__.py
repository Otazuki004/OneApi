from quart_cors import cors
from quart import *
from pyrogram import *
import os
import asyncio
from signal import SIGINT, SIGTERM
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_quart():
    print("Starting Quart...")
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Quart stopped.")

async def run_bot():
    print("Starting Pyrogram bot...")
    await bot.start()
    print("Bot started successfully")
    await idle()
    print("Idle isn't idling ")

async def shutdown():
    print("Shutting down...")
    await bot.stop()
    print("Bot stopped.")
    print("Shutdown complete.")

async def main():
    # Concurrently run both Pyrogram and Quart
    tasks = [run_bot(), run_quart()]
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error occurred: {e}")
        await shutdown()

if __name__ == '__main__':
    # Create the asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Add signal handlers for shutdown
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: asyncio.create_task(shutdown()))

    try:
        print("Starting the application...")
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("Finalizing shutdown...")
        loop.run_until_complete(shutdown())
        loop.close()
