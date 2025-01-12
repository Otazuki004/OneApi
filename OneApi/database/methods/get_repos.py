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
    
      url = "https://api.github.com/installation/repositories"
      headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
      }
      ily = []
      async with httpx.AsyncClient() as mano:
        while url:
          r = await mano.get(url, headers=headers)
          if r.status_code == 200:
            data = r.json()
            if not data["repositories"]: break
            for x in data["repositories"]:
              name, id = x.get('name'), x.get('id')
              ily.append({'name': name, 'id': id})
            if "Link" in r.headers:
              links = r.headers["Link"]
              next_link = [link.split(";")[0].strip("<>") for link in links.split(",") if 'rel="next"' in link]
              url = next_link[0] if next_link else None
              if url and not url.startswith("http"):
                url = f"https://api.github.com{url}"  # Ensure the URL is absolute
            else:
              break
          else:
            logging.info(f"Failed to get repos of user: {user_id}: {r.text}")
            return "failed"
      return ily
    except Exception as w:
      logging.error(traceback.format_exc())
      return f"Error: {w}"
