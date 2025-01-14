import traceback
import logging

class DisconnectGit:
  async def disconnect_git(self, user_id: int):
    try:
      user = await self.find(user_id, check=True)
      if not user: "not exists"
      db, cb = self.db, self.cb
      await cb.update_one({"_id": 1}, {"$pull": {"users": user_id}})
      await cb.delete_one({"_id": user_id})
      return True
    except Exception as e:
      logging.error(traceback.format_exc())
      return f"Error: {e}"
    
