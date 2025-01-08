from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import threading

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

def run_quart():
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def run_pyrogram():
    bot.start()
    idle()

if __name__ == '__main__':
    quart_thread = threading.Thread(target=run_quart)
    quart_thread.start()
    run_pyrogram()
