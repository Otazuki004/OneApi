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
            repos = []
            ohi = []
            
            while url:
                async with httpx.AsyncClient() as mano:
                    r = await mano.get(url, headers=headers)
                    if r.status_code == 200:
                        data = r.json()
                        if not data["repositories"]: 
                            return []
                        
                        for x in data["repositories"]:
                            name, id = x.get('name'), x.get('id')
                            repos.append({'name': name, 'id': id})
                        
                        link_header = r.headers.get('Link', '')
                        if 'rel="next"' in link_header and ((link_header.replace('\n', '')).split(',')[0].split(';')[0][1:-1]) not in ohi:
                            url = ((link_header.replace('\n', '')).split(',')[0].split(';')[0][1:-1])
                        else:
                            url = None
                    else:
                        logging.info(f"Failed to get repos of user: {user_id}: {r.text}")
                        return "failed"
            
            return repos
        except Exception as w:
            logging.error(traceback.format_exc())
            return f"Error: {w}"
