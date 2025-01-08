from quart_cors import cors
from quart import *
from pyrogram import Client
import os
from . import *
import asyncio

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

async def run_():
    await bot.start()
    asyncio.create_task(app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))))
    await idle()
    
if __name__ == '__main__':
    asyncio.run(run_())
