from ..database import *
from quart import *
from .. import *

user = user()
create_user_bp = Blueprint('create_user', __name__)

@app.route('/exists/', methods=['POST'])
async def exists():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'name' in data: return jsonify({'error': 'missing user_id & name'}), 400
  user_id = int(data.get('user_id'))
  d = await user.find(user_id)
  if not d: return jsonify({'message': "user not found"}), 404
  elif 'error' in d: return jsonify({'error': d}), 400
  return jsonify({'message': 'user exists'}), 200
