from quart_cors import cors
from quart import *
import asyncio
import os
from . import *

# BLUEPRINTS _____________________
from .api.exists import exists_bp
from .api.create_user import create_user_bp
from .api.get_projects import get_projects_bp
from .api.create_project import create_project_bp 
from .api.delete_project import delete_project_bp
from .api.user_info import user_info_bp
from .api.get_repos import get_repos_bp
from .api.delete_user import delete_user_bp
from .api.disconnect_git import disconnect_git_bp
from .api.set_repo import set_repo_bp
from .api.project_info import project_info_bp
from .api.host import host_bp

app.register_blueprint(exists_bp)
app.register_blueprint(create_user_bp)
app.register_blueprint(get_projects_bp)
app.register_blueprint(create_project_bp)
app.register_blueprint(delete_project_bp)
app.register_blueprint(user_info_bp)
app.register_blueprint(get_repos_bp)
app.register_blueprint(delete_user_bp)
app.register_blueprint(disconnect_git_bp)
app.register_blueprint(set_repo_bp)
app.register_blueprint(project_info_bp)
app.register_blueprint(host_bp)
# ---------------------------------

app = cors(app, allow_origin="*")

@app.route('/')
async def home():
    return jsonify({'success': 'server online'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
