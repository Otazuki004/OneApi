from ..database import *
from quart import *
from .. import *

user = user()
create_project_bp = Blueprint('create_project', __name__)

@app.route('/create_project/', methods=['POST'])
async def create_project():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'name' in data and not 'plan' in data:
    return jsonify({'error': 'missing user_id or name'}), 400
  user_id = int(data.get('user_id'))
  name = data.get('name')
  plan = data.get('plan')
  mano = await user.create_project(name, user_id, plan)
  if mano == 'ok':
    return jsonify({'message': 'Successfully created'}), 200
  elif 'Error' in mano:
    return jsonify({'error': mano}), 400
  else:
    return jsonify({'message': mano}), 400
