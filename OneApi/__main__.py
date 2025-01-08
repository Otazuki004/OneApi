from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import asyncio
from . import bot, app
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_():
    await bot.start()
    await app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    await bot.idle()

if __name__ == '__main__':
    asyncio.run(run_())
