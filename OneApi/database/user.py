from .. import DATABASE
import logging
import traceback 
from .methods import *
import httpx

db = DATABASE['user_nel']

class user(Methods):
    def __init__(self):
      self.db = db
      self.cb = DATABASE['cb']
    async def find(self, user_id: int, check=False):
      try:
        if check:
          if await db.find_one({"_id": user_id}) and await cb.find_one({"_id": user_id}):
            return True
          return False
        user = await db.find_one({"_id": user_id})
        return user
      except Exception as w:
        e = traceback.format_exc()
        logging.error(e)
        return f"Error: {w}"
    async def create(self, name: str, user_id: int):
      try:
        if await self.find(user_id): return "exists"
        url = "https://api.github.com/installation/repositories"
        headers = {
          "Authorization": f"Bearer {(await self.cb.find_one({"_id": 5965055071})).get('token')}",
          "Accept": "application/vnd.github+json"
        }
        async with httpx.AsyncClient() as client:
          response = await client.get(url, headers=headers)
          if response.status_code == 200:
            data = response.json()
            if data["repositories"]:
              owner = data["repositories"][0]["owner"]
              return owner["login"]
            else: owner = 'CannotFound'
          else:
              logging.warn(response.text)
              return "Not connected"
        await db.update_one({"_id": 1}, {"$addToSet": {"users": user_id}}, upsert=True)
        await db.update_one(
            {"_id": user_id},
            {"$set": {"name": name, "coins": 0, "projects": [], 'latest_project': 0, 'git': owner}},
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
    async def create_project(self, name: str, user_id: int, plan: str):
      try:
        user = await self.find(user_id)
        if not user: return "not exists"
        elif name and len(name) < 4:
          return 'Name too short'
        
        name, latest_project = name[:15], int(user.get('latest_project', 0)) + 1
        coins = user.get('coins', 0)
        
        if any(proj.get('name') == name for proj in user.get('projects', [])):
          return "Name already used"
        
        if plan == 'free':
          plan_price = 0
        elif plan == 'basic':
          plan_price = 99
        elif plan == 'advance':
          plan_price = 199
        elif plan == 'pro':
          plan_price = 269
        else: return 'Plan not found'
        if coins < plan_price:
          return 'insufficient coins'

        if plan_price != 0: await db.update_one({"_id": user_id}, {"$set": {'coins': coins-plan_price}})
        
        await db.update_one(
          {"_id": f'{user_id}{latest_project}'},
          {"$set": {
            "name": name,
            "id": latest_project,
            "plan": plan,
            "ram": 'god',
            "rom": 'god',
            "repo": 'Not set',
            "apt-allowed": False,
            "language": 'Mano'
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
        return 'ok'
      except Exception as e:
        logging.error(traceback.format_exc())
        return f'Error: {e}'
    async def delete_project(self, user_id: int, project_id: int):
      try:
        user = await self.find(user_id)
        if not user:
          return "not exists"
        if not user.get('projects'):
          return "Project not found"
        if not any(proj.get('project_id') == project_id for proj in user.get('projects', [])):
          return "Project not found"
        await db.delete_one({"_id": f"{user_id}{project_id}"})
        await db.update_one(
          {"_id": user_id},
          {"$pull": {"projects": {"project_id": project_id}}}
        )
        return "ok"
      except Exception as e:
        logging.error(traceback.format_exc())
        return f"Error: {e}"
