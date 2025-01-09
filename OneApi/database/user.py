from .. import DATABASE
import logging
import traceback 

db = DATABASE['user']

class user:
    async def find(self, user_id: int):
      try:
        user = await db.find_one({"_id": user_id})
        return user
      except Exception as w:
        e = traceback.format_exc()
        logging.error(e)
        return f"Error: {w}"
    async def create(self, name: str, user_id: int):
      try:
        if await self.find(user_id): return "exists"
        await db.update_one({"_id": 1}, {"$addToSet": {"users": user_id}}, upsert=True)
        await db.update_one(
            {"_id": user_id},
            {"$set": {"name": name, "coins": 1000000, "projects": [{"name": "Basic Project", "project_id": 1}]}},
            upsert=True
        )
        return 'ok'
      except Exception as w:
        e = traceback.format_exc()
        logging.error(e)
        return f"Error: {w}"
    async def get_projects(self, user_id):
      try:
        if not await self.find(user_id): return "not exists"
        user = await self.find(user_id)
        if user.get('projects'):
          return user.get('projects')
        return 'projects not found'
      except Exception as oh:
        e = traceback.format_exc()
        logging.error(e)
        return f"Error: {oh}"
