import traceback
import logging

class DeleteUser:
  async def delete_user(self, user_id: int):
    try:
      user = await self.find(user_id)
      if not user: "not exists"
      db, cb = self.db, self.cb
      await db.update_one({"_id": 1}, {"$pull": {"users": user_id}})
      await db.delete_one({"_id": user_id})
      for x in user.get('projects'):
        if x.get('project_id'):
          try: await db.delete_one({"_id": {user_id}{int(x.get('project_id'))}})
          except: pass
      try:
        await cb.update_one({"_id": 1}, {"$pull": {"users": user_id}})
        await cb.delete_one({"_id": user_id})
      except Exception as e: logging.error("Error on deleting user callback data ^_^: {user_id}, {e}")
      return True
    except Exception as e:
      logging.error(traceback.format_exc())
      return f"Error: {e}"
      
    
