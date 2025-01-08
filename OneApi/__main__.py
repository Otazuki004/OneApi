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
    return jsonify({'success': 'server online'}), 200

async def run_bot():
    await bot.start()  # Start the Pyrogram bot
    await idle()  # Keeps the bot running indefinitely

async def run_quart(loop):
    # Run Quart app in a new event loop
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def start_quart_loop():
    # Create a new event loop for Quart
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # Set the new loop
    loop.run_until_complete(run_quart(loop))  # Run Quart in this new loop

if __name__ == '__main__':
    # Create the event loop for Pyrogram and run it
    pyrogram_loop = asyncio.get_event_loop()
    
    # Run Quart on a separate thread or process
    from threading import Thread
    quart_thread = Thread(target=start_quart_loop)
    quart_thread.start()

    # Run Pyrogram in the main event loop
    pyrogram_loop.run_until_complete(run_bot())  # Start bot in the main event loop
