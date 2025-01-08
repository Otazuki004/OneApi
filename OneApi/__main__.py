from quart_cors import cors
from quart import *
from . import *
import os
from pyrogram import *
import asyncio

app = cors(app, allow_origin="*")

@app.route('/')
def home():
  return jsonify({'success': 'server online'})

async def run():
    await asyncio.gather(
        bot.start(),
        app.run_task(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    )
    await idle()
if __name__ == '__main__':
  asyncio.run(run())
