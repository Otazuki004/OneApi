import logging 
import traceback 

class GetRepo:
  async def get_repo(self, user_id: int, repo_id: int):
    try:
      db, cb = self.db, self.cb
      user = await self.find(user_id)
      if not user: return 'not exists'
      hmm = await self.get_repos(user_id)
      
      if not hmm: return False
      
      yes = False
      for x in hmm:
        if int(x.get('id', 0)) == int(repo_id):
          yes = x
          break
      if yes: return yes
    except: logging.error(traceback.format_exc())
    return False
