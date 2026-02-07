import logging
from typing import Dict
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("OneApi.WebSockets")

class ConnectionManager:
    def __init__(self):
        # hazel_id -> WebSocket
        self.active_ub: Dict[str, WebSocket] = {}
        # hazel_id -> WebSocket
        self.active_client: Dict[str, WebSocket] = {}

    async def connect_ub(self, hazel_id: str, websocket: WebSocket):
        await websocket.accept()
        if hazel_id in self.active_ub:
            await self.active_ub[hazel_id].close(code=1000)
        self.active_ub[hazel_id] = websocket

    async def connect_client(self, hazel_id: str, websocket: WebSocket):
        await websocket.accept()
        if hazel_id in self.active_client:
            await self.active_client[hazel_id].close(code=1000)
        self.active_client[hazel_id] = websocket

    def disconnect(self, hazel_id: str):
        self.active_ub.pop(hazel_id, None)
        self.active_client.pop(hazel_id, None)

    async def relay_from_ub(self, hazel_id: str, message: str):
        if hazel_id in self.active_client:
            await self.active_client[hazel_id].send_text(message)

    async def relay_from_client(self, hazel_id: str, message: str):
        if hazel_id in self.active_ub:
            await self.active_ub[hazel_id].send_text(message)

manager = ConnectionManager()

class Client:
    def __init__(self, router: APIRouter):
        self.router = router
        self.logger = logger

        # Register WebSocket endpoints
        self.router.websocket("/HazelUB")(self.HazelUBEndPoint)
        self.router.websocket("/HazelClient")(self.HazelClientEndPoint)
    
    async def HazelUBEndPoint(self, ws: WebSocket):
        hazel_id = ws.query_params.get("Hazel_ID")
        if not hazel_id:
            await ws.accept()
            await ws.send_text("Missing Hazel_ID")
            return await ws.close(code=1008)

        await manager.connect_ub(hazel_id, ws)
        logger.info(f"Hazel UB connected: Hazel_ID={hazel_id}")
        
        try:
            while True:
                data = await ws.receive_text()
                await manager.relay_from_ub(hazel_id, data)
        except Exception:
            manager.disconnect(hazel_id)

    async def HazelClientEndPoint(self, ws: WebSocket):
        hazel_id = ws.query_params.get("Hazel_ID")
        if not hazel_id:
            await ws.accept()
            await ws.send_text("Missing Hazel_ID")
            return await ws.close(code=1008)

        await manager.connect_client(hazel_id, ws)
        logger.info(f"Hazel Client connected: Hazel_ID={hazel_id}")
        
        try:
            while True:
                data = await ws.receive_text()
                await manager.relay_from_client(hazel_id, data)
        except Exception:
            manager.disconnect(hazel_id)