from ..database import *
from quart import *
from .. import *
from ..deployment.deployment import Deployment

user = user()
deploy = Deployment()
host_bp = Blueprint('host', __name__)

@app.route('/host/', methods=['POST'])
async def host():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'project_id' in data: return jsonify({'error': 'missing user_id or project_id'}), 400
  user_id = int(data.get('user_id'))
  project_id = int(data.get('project_id'))

  mm = await deploy.host(user_id, project_id)
  if mm is True:
    return jsonify({'message', 'Successfully hosted!'}), 200
  return jsonify({'message', mm}), 400
