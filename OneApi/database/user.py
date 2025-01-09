from .. import DATABASE
import logging

db = DATABASE['user']

class user:
    async def find(self, user_id):
        user = await db.find_one({"_id": user_id})
        return user
    async def add(self, name: str, user_id: int):
        if await self.find(user_id): return "exists"
        await db.update_one({"_id": 1}, {"$addToSet": {"users": user_id}}, upsert=True)
        await db.update_one(
            {"_id": user_id},
            {"$set": {"name": name, "coins": 1000000, "projects": [{"name": "Basic Project", "project_id": 1}]}},
            upsert=True
        )
