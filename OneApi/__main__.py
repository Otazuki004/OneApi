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
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(run_quart())
    else:
        loop.run_until_complete(run_quart())

async def o():
    asyncio.create_task(main())

if __name__ == '__main__':
    print("Starting bot")
    bot.start()
    idle(asyncio.run(o()))
    print("Bot stoped")
