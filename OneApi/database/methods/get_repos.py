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

            repos = set()  # Use a set to prevent duplicates
            async with httpx.AsyncClient() as client:
                while url:
                    # Validate the URL
                    if not url.startswith(("http://", "https://")):
                        raise ValueError(f"Invalid URL: {url}")

                    response = await client.get(url, headers=headers)
                    response.raise_for_status()

                    data = response.json()
                    repos.update({(repo["id"], repo["name"]) for repo in data["repositories"]})

                    # Parse 'Link' header to find the next page
                    link_header = response.headers.get("Link")
                    if link_header:
                        links = {
                            rel.split('=')[1].strip('"'): url.strip("<>")
                            for url, rel in [link.split(";") for link in link_header.split(",")]
                        }
                        url = links.get("next")  # Update the URL for the next page, or None
                    else:
                        url = None

            # Return repos as a list of dictionaries
            return [{"id": repo[0], "name": repo[1]} for repo in repos]

        except httpx.HTTPStatusError as http_err:
            if http_err.response.status_code == 401:
                return "Unauthorized: Invalid or expired token"
            elif http_err.response.status_code == 404:
                return "Not Found: Endpoint is incorrect"
            else:
                logging.error(f"HTTP error occurred: {http_err.response.text}")
                return f"Failed with status {http_err.response.status_code}"

        except ValueError as ve:
            logging.error(f"ValueError: {ve}")
            return str(ve)

        except Exception as e:
            logging.error(traceback.format_exc())
            return f"Error: {e}"
