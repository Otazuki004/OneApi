import traceback
import logging
import httpx 

class GetRepos:
  async def get_repos(self, user_id: int):
    try:
      db, cb = self.db, self.cb
      user = await self.find(user_id)
      if not user: return 'not exists'
      token = (await cb.find_one({"_id": int(user_id)})).get('token', None)
      if not token: return "not exists"
    
      url = "https://api.github.com/installation/repositories?page=1"
      headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
      }
      async with httpx.AsyncClient() as mano:
        r = await mano.get(url, headers=headers)
        if r.status_code == 200:
          data = r.json()
          if not data.get("repositories"): return []
          ily = []
          for x in data.get("repositories"):
            name, id = x.get('name'), x.get('id')
            ily.append({'name': name, 'id': id})
          try: pages = list(range(2, int(str(r.headers.get('Link', ''))[126])+1))
          except Exception as w:
            logging.error(f"GetRepos 30: {w}")
            pages = []
          for x in pages:
            url = f"https://api.github.com/installation/repositories?page={x}"
            k = await mano.get(url, headers=headers)
            data = k.json()
            if k.status_code == 200 and data.get("repositories"):
              for x in data["repositories"]:
                name, id = x.get('name'), x.get('id')
                ily.append({'name': name, 'id': id})
          return ily
        else:
          logging.info(f"Failed to get repos of user: {user_id}: {r.text}")
          return "failed"
    except Exception as w:
      logging.error(traceback.format_exc())
      return f"Error: {w}"
