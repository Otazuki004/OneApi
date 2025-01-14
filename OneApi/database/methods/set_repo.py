import traceback
import logging

class SetRepo:
  async def set_repo(self, user_id: int, project_id: int, repo_id: int):
    db, cb = self.db, self.cb
    user = await self.find(user_id)
    project = await db.find_one({"_id": f"{user_id}{project_id}"})
    if not user: return 'not exists'
    elif not project: return 'Project not found'

    hmm = await self.get_repos(user_id)
    if not hmm: return 'Repo not found'

    yes = False
    for x in hmm:
      if int(x.get('id')) == project_id:
        yes = True
        break
    if not yes: return 'Repo not found'

    log = project.get('logs')
    log += f"{self.lf}: Repo linked successfully"

    await db.update_one(
      {"_id": f"{user_id}{project_id}"},
      {"$set": {
        "logs": log,
        "repo": repo_id
      }}
    )
    
