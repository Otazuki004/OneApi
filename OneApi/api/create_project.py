from ..database import *
from quart import *
from .. import *

user = user()
create_project_bp = Blueprint('create_project', __name__)

@app.route('/create_project/', methods=['POST'])
async def create_project():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'name' in data:
    return jsonify({'error': 'missing user_id or name'}), 400
  user_id = int(data.get('user_id'))
  name = data.get('name')
  mano = await user.create_project(name, user_id)
  if mano == 'Name too short' or mano == 'Name already used':
    return jsonify({'message': mano}), 400
  elif mano == 'ok':
    return jsonify({'message': 'Successfully created'}), 200
  elif 'Error' in mano:
    return jsonify({'error': mano}), 400
