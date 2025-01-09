from ..database import *
from quart import *
from .. import *

user = user()
create_user_bp = Blueprint('create_user', __name__)

@app.route('/create_user/', methods=['POST'])
async def create_user():
  data = await request.get_json()
  if not data or not 'user_id' in data and not 'name' in data: return jsonify({'error': 'missing user_id & name'}), 400
  user_id = int(data.get('user_id'))
  name = data.get('name')
  d = await user.create(name, user_id)
  if d == 'exists': 
    return jsonify({'message': "user exists"}), 400
  elif 'Error' in d: 
    return jsonify({'error': d}), 400
  elif d =='ok':
    return jsonify({'message': 'done'}), 200
