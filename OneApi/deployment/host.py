from .. import *
import logging
import traceback 

class Host:
  async def host(self, user_id: int, project_id: int):
    database = self.database
    user = await self.find(user_id)
    project = await database.find(f"p{user_id}{project_id}", project=True)
    if not user: return 'not exists'
    elif not project: return 'Project not found'
    repo_id = project.get('repo', 0)
    repo = await database.get_repo(user_id, repo_id)
    if not repo: return "Repo not found"
      
    installation_id = (await cb.find_one({"_id": int(user_id)})).get('installation_id', None)
    if not installation_id: return "not exists"
    token = await self.gen_token(installation_id)
    
    try:
      folder = f"deployment{user_id}")
      await database.add_log(user_id, project_id, "Clonning repo from github...")
      await run(f"rm -rf {folder}")
      await run(f"mkdir {folder}")
      await run(f"git clone https://x-access-token:{token}@github.com/{repo.get('full_name')}/")
      
      
    
