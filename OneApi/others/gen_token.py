import jwt
from time import time
import httpx

with open("mano.pem", "r") as f:
  PRIVATE_KEY = f.read()
APP_ID = "1109508"

async def gen_token(installation_id):
    payload = {
        "iat": int(time()),
        "exp": int(time()) + 600,
        "iss": APP_ID,
    }
    jwt_token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 201:
            return response.json().get("token")
        return None
