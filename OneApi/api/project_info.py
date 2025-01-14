from ..database import *
from quart import *
from .. import *

user = user()
project_info_bp = Blueprint('project_info', __name__)

@app.route('/project_info/', methods=['POST'])
async def project_info():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'project_id' in data: return jsonify({'error': 'missing user_id or project_id'}), 400
  user_id = int(data.get('user_id'))
  project_id = int(data.get('project_id'))

  mano = await self.find('p{user_id}{project_id}', project=True)
  if mano:
    return jsonify({'message': mano}), 200
  return jsonify({'message': 'Cannot find the project!'}), 400
