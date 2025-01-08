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

async def main():
    print("Main triggered")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_quart())

if __name__ == '__main__':
    print("Starting bot")
    bot.start()
    asyncio.create_task(main())
    idle()
    print("Bot stoped")
