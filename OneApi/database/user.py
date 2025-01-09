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
            {"$set": {"name": name, "coins": 1000000, "projects": [], 'latest_project': 0}},
            upsert=True
        )
        return 'ok'
      except Exception as w:
        e = traceback.format_exc()
        logging.error(e)
        return f"Error: {w}"
    async def get_projects(self, user_id: int):
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
    async def create_project(self, name: str, user_id: int):
      try:
        if not await self.find(user_id): return "not exists"
        elif not name and len(name) < 4:
          return 'Name too short'
        user = await self.find(user_id)
        name, latest_project = name[:15], user.get('latest_project') + 1
        
        if any(proj.get('name') == name for proj in user.get('projects', [])):
          return "Name already used"
        
        await db.update_one(
          {"_id": f'{user_id}{latest_project}'},
          {"$set": {
            "name": name,
            "id": latest_project,
            "data": {}
          }},
          upsert=True
        )
        await db.update_one(
          {"_id": user_id},
          {"$addToSet": {
            "projects": {
              'name': name,
              'project_id': latest_project
            }
          }}
        )
        await db.update_one({"_id": user_id}, {"$set": {"latest_project": latest_project}})
      except Exception as e:
        logging.error(traceback.format_exc())
        return f'Error: {e}'
