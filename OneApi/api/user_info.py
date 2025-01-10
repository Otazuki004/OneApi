from ..database import *
from quart import *
from .. import *

user = user()
user_info_bp = Blueprint('user_info', __name__)

@app.route('/user_info/', methods=['POST'])
async def user_info():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  d = await user.user_info(user_id)
  if d == 'not exists': return jsonify({'message': "user not found"}), 404
  elif 'error' in d: return jsonify({'error': d}), 400
  return jsonify({'message': d}), 200
