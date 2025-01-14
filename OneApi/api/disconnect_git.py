from ..database import *
from quart import *
from .. import *
import logging 

user = user()
disconnect_git_bp = Blueprint('disconnect_git', __name__)

@app.route('/disconnect_git/', methods=['POST'])
async def disconnect_git():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  mano = await user.disconnect_git(user_id)
  if mano is True:
    return jsonify({"message": "Successfully disconnected git"}), 200
  elif 'Error' in mano:
    return jsonify({'error': mano}), 400
