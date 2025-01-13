from ..database import *
from quart import *
from .. import *

user = user()
delete_user_bp = Blueprint('delete_user', __name__)

@app.route('/delete_user/', methods=['POST'])
async def delete_user():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  d = await user.delete_user(user_id)
  if d is True:
    return jsonify({"message": "Successfully deleted user!"}), 200
  elif "Error" in d:
    return jsonify({"error": d}), 400
