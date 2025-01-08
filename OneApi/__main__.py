from quart_cors import cors
from quart import Quart
import asyncio
import os
from . import *
from OneApi.pyro.pyrogram_start import *

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return jsonify({'success': 'server online'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
