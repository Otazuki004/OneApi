from quart_cors import cors
from quart import *
from pyrogram import Client
import os
import threading
from . import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return {'success': 'server online'}

def run_pyrogram():
    bot.start()
    idle()
    
if __name__ == '__main__':
    pyrogram_thread = threading.Thread(target=run_pyrogram)
    pyrogram_thread.daemon = True
    pyrogram_thread.start()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
