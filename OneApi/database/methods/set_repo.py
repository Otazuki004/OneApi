import traceback
import logging

class SetRepo:
  async def set_repo(self, user_id: int, project_id: int, repo_id: int):
    db, cb = self.db, self.cb
    user = await self.find(user_id)
    project = await db.find_one({"_id": f"{user_id}{project_id}"})
    if not user: return 'not exists'
    elif not project: return 'Project not found'
    
    
