import traceback
import logging

class addLog:
  async def add_log(user_id: int, project_id: int, log_text: str):
    try:
      db, cb = self.db, self.cb
      user = await self.find(user_id)
      project = await db.find_one({"_id": f"p{user_id}{project_id}"})
      if not user: return 'not exists'
      elif not project: return 'Project not found'

      log = project.get('logs')
      log += f"{self.lf}: {log_text}"
      
      await db.update_one(
        {"_id": f"p{user_id}{project_id}"},
        {"$set": {
          "logs": log
        }}
      )
      return True
    except Exception as r:
      logging.error(traceback.format_exc())
      return False
