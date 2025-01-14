from ..database import *
from quart import *
from .. import *

user = user()
set_repo_bp = Blueprint('set_repo', __name__)

@app.route('/set_repo/', methods=['POST'])
async def set_repo():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'project_id' in data and not 'repo_id' in data: return jsonify({'error': 'missing user_id or project_id or repo_id'}), 400
  user_id = int(data.get('user_id'))
  project_id = int(data.get('project_id'))
  repo_id = int(data.get('repo_id'))

  mano = await self.set_repo(user_id, project_id, repo_id)
  if mano == 'ok':
    return jsonify({'message': mano}), 200
  elif 'Error' in str(mano):
    return jsonify({'error': mano}), 400
  return jsonify({'message': mano}), 400
