from .. import *
import logging
import traceback 
import asyncio
import aiofiles 
import aiofiles.os

class Host:
  async def host(self, user_id: int, project_id: int):
    database = self.database
    user = await database.find(user_id)
    project = await database.find(f"p{user_id}{project_id}", project=True)
    if not user: return 'not exists'
    elif not project: return 'Project not found'
    repo_id = project.get('repo', 0)
    repo = await database.get_repo(user_id, repo_id)
    if not repo: return "Repo not found"
      
    installation_id = (await self.cb.find_one({"_id": int(user_id)})).get('installation_id', None)
    if not installation_id: return "not exists"
    token = await database.gen_token(installation_id)
    
    try:
      folder = f"deployment{user_id}"
      await database.add_log(user_id, project_id, "Clonning repo from github...")
      await run(f"rm -rf {folder}")
      await run(f"mkdir {folder}")
      ok = await run(f"cd {folder} && git clone https://x-access-token:{token}@github.com/{repo.get('full_name')}/")
      repo_folder = f"{folder}/{repo.get('name')}"
      
      if not await aiofiles.os.path.isfile(repo_folder):
        await database.add_log(user_id, project_id, f"Error on clonning repo: {ok}")
        return 'Failed to host repo'
      ls = await run(f"ls {repo_folder}")
      ls2 = await run(f"ls {folder}")
      
      await database.add_log(
        user_id,
        project_id, 
        f"Successfully clonned repo!\nDebug: Files in repo {ls}"
      )
      
      
      if not await aiofiles.os.path.isfile(f"{repo_folder}/ElevenHost.yaml"):
        await database.add_log(
        user_id,
        project_id, 
        f"Error:\nCannot find ElevenHost.yaml on your repo"
        )
      return True
    except Exception as w:
      logging.error(traceback.format_exc())
      return f"Error: {w}"
      
      
    
