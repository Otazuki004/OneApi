from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import asyncio
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return jsonify({'success': 'server online'})

async def run_quart():
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

async def main():
    await bot.start()  # Start the Pyrogram bot
    await asyncio.gather(run_quart(), idle())  # Run both Quart and Pyrogram concurrently

if __name__ == '__main__':
    asyncio.run(main())
