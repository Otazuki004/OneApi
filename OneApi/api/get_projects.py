from ..database import *
from quart import *
from .. import *

user = user()
get_projects_bp = Blueprint('get_projects', __name__)

@app.route('/get_projects/', methods=['POST'])
async def get_projects():
  data = await request.get_json()
  if not data or not 'user_id' in data: return jsonify({'error': 'missing user_id'}), 400
  user_id = int(data.get('user_id'))
  ohk = await user.get_projects(user_id)
  if ohk == "projects not found":
    return jsonify({"message": ohk}), 404
  elif 'Error' in ohk:
    return jsonify({"error": ohk}), 400
  return jsonify({"message": ohk}), 200
