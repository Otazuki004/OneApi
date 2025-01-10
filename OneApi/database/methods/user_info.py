import traceback
import logging

class UserInfo:
  async def user_info(self, user_id):
    try:
      from ..user import db
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
