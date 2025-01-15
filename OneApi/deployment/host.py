class Host:
  async def host(self, user_id: int, project_id: int):
    database = self.database
    user = await self.find(user_id)
    project = await database.find(f"p{user_id}{project_id}", project=True)
    
