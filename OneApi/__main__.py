from quart_cors import cors
from quart import *
from . import *
import os

app = cors(app, allow_origin="*")

@app.route('/')
def home():
  return jsonify({'success': 'server online'})

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 8080))
  app.run(debug=True, host="0.0.0.0", port=port)
