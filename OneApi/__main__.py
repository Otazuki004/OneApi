from quart_cors import cors
from quart import Quart
import asyncio
import os
from . import *

# BLUEPRINTS _____________________
from .api.exists import exists_bp
from .api.create_user import create_user_bp
from .api.get_projects import get_projects_bp
from .create_project import create_project_bp 

app.register_blueprint(exists_bp)
app.register_blueprint(create_user_bp)
app.register_blueprint(get_projects_bp)
app.register_blueprint(create_project_bp)
# ---------------------------------

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return jsonify({'success': 'server online'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
