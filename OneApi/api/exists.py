from ..database import *
from quart import *
from .. import *
import logging 

user = user()
exists_bp = Blueprint('exists', __name__)

@app.route('/exists/', methods=['POST'])
async def exists():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  
  if bool(data.get('full_check')) is False: check = False
  else: check = True
  
  d = await user.find(user_id, check=check)
  if d: return jsonify({'message': 'user exists'}), 200
  elif not d: return jsonify({'message': "user not found"}), 404
  elif 'Error' in d: return jsonify({'error': d}), 400
  else: logging.info(d)
