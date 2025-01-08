from quart_cors import cors
from quart import *
from pyrogram import *
import os
import asyncio
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
def home():
    return jsonify({'success': 'server online'})

async def run():
    asyncio.create_task(bot.start())
    asyncio.create_task(app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))))
    await idle()

if __name__ == '__main__':
    asyncio.run(run())
