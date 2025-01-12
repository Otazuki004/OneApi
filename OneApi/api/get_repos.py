from ..database import *
from quart import *
from .. import *

user = user()
get_repos_bp = Blueprint('get_repos', __name__)

@app.route('/get_repos/', methods=['POST'])
async def get_repos():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  d = await user.get_repos(user_id)
  if d == "not exists":
    return jsonify({'message': 'user not exists'}), 404
  elif d == 'failed':
    return jsonify({'message': "Failed to get user repos"}), 400
  elif 'Error' in d:
    return jsonify({'error': d}), 400
  else:
    return jsonify({'message': d}), 200
