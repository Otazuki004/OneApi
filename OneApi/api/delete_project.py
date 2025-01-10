from ..database import *
from quart import *
from .. import *

user = user()
delete_project_bp = Blueprint('delete_project', __name__)

@app.route('/delete_project/', methods=['POST'])
async def delete_project():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'project_id' in data:
    return jsonify({'error': 'missing user_id or project_id'}), 400
  user_id = int(data.get('user_id'))
  project_id = int(data.get('project_id'))
  mano = await user.delete_project(user_id, project_id)
  if mano == 'Project not found' or mano == 'not exists':
    return jsonify({'message': mano}), 404
  elif 'Error' in mano:
    return jsonify({'error': mano}), 400
  elif 'ok' in mano:
    return jsonify({'message': mano}), 200
