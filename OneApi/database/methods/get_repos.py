import traceback
import logging
import httpx

class GetRepos:
    async def get_repos(self, user_id: int):
        try:
            db, cb = self.db, self.cb
            user = await self.find(user_id)
            if not user:
                return 'User not exists'

            token = (await cb.find_one({"_id": int(user_id)})).get('token', None)
            if not token:
                return "Token not exists"

            url = "https://api.github.com/installation/repositories"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                
                # Explicitly raise an exception for HTTP errors
                response.raise_for_status()

                data = response.json()
                if not data.get("repositories"):
                    return []

                return [{"name": repo["name"], "id": repo["id"]} for repo in data["repositories"]]

        except httpx.HTTPStatusError as http_err:
            if http_err.response.status_code == 401:
                return "Unauthorized: Invalid or expired token"
            elif http_err.response.status_code == 404:
                return "Not Found: Endpoint is incorrect"
            else:
                logging.error(f"HTTP error occurred: {http_err.response.text}")
                return f"Failed with status {http_err.response.status_code}"

        except Exception as e:
            logging.error(traceback.format_exc())
            return f"Error: {e}"
