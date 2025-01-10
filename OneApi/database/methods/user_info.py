from ..user import db
import traceback
import logging

async def user_info(self, user_id):
  try:
    user = await self.find(user_id)
    if not user: return "not exists"

    data = {
      "name": user.get('name'),
      "coins": user.get('coins'),
      "projects": len(user.get('projects'))
    }
    return data
  except Exception as w:
    logging.error(traceback.format_exc())
    return f'Error: {w}'
