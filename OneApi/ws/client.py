import json
import logging
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("OneApi.WebSockets")


# ============================================================
# Connection Manager
# ============================================================

class ConnectionManager:
    def __init__(self):
        # hazel_id -> WebSocket
        self.active_ub: Dict[str, WebSocket] = {}
        self.active_client: Dict[str, WebSocket] = {}

    # ---------------------------
    # UB side
    # ---------------------------
    async def connect_ub(self, hazel_id: str, ws: WebSocket):
        await ws.accept()

        old = self.active_ub.get(hazel_id)
        if old:
            await old.close(code=1000)

        self.active_ub[hazel_id] = ws

        # notify client
        await self._notify_client(hazel_id, {
            "type": "ub_joined",
            "hazel_id": hazel_id
        })

    async def disconnect_ub(self, hazel_id: str):
        self.active_ub.pop(hazel_id, None)

        await self._notify_client(hazel_id, {
            "type": "ub_left",
            "hazel_id": hazel_id
        })

    # ---------------------------
    # Client side
    # ---------------------------
    async def connect_client(self, hazel_id: str, ws: WebSocket):
        await ws.accept()

        old = self.active_client.get(hazel_id)
        if old:
            await old.close(code=1000)

        self.active_client[hazel_id] = ws

        # notify UB
        await self._notify_ub(hazel_id, {
            "type": "client_joined",
            "hazel_id": hazel_id
        })

    async def disconnect_client(self, hazel_id: str):
        self.active_client.pop(hazel_id, None)

        await self._notify_ub(hazel_id, {
            "type": "client_left",
            "hazel_id": hazel_id
        })

    # ---------------------------
    # Message relay
    # ---------------------------
    async def relay_from_ub(self, hazel_id: str, message: str):
        ws = self.active_client.get(hazel_id)
        if ws:
            await ws.send_text(message)

    async def relay_from_client(self, hazel_id: str, message: str):
        ws = self.active_ub.get(hazel_id)
        if ws:
            await ws.send_text(message)

    # ---------------------------
    # Internal notifications
    # ---------------------------
    async def _notify_ub(self, hazel_id: str, payload: dict):
        ws = self.active_ub.get(hazel_id)
        if ws:
            await ws.send_text(json.dumps(payload))

    async def _notify_client(self, hazel_id: str, payload: dict):
        ws = self.active_client.get(hazel_id)
        if ws:
            await ws.send_text(json.dumps(payload))


manager = ConnectionManager()


# ============================================================
# API Router
# ============================================================

class Client:
    def __init__(self, router: APIRouter):
        self.router = router

        self.router.websocket("/HazelUB")(self.HazelUBEndPoint)
        self.router.websocket("/HazelClient")(self.HazelClientEndPoint)

    # ---------------------------
    # Hazel UB WebSocket
    # ---------------------------
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

        except WebSocketDisconnect:
            logger.info(f"Hazel UB disconnected: Hazel_ID={hazel_id}")
            await manager.disconnect_ub(hazel_id)

        except Exception as e:
            logger.error(f"UB error [{hazel_id}]: {e}")
            await manager.disconnect_ub(hazel_id)

    # ---------------------------
    # Hazel Client WebSocket
    # ---------------------------
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

        except WebSocketDisconnect:
            logger.info(f"Hazel Client disconnected: Hazel_ID={hazel_id}")
            await manager.disconnect_client(hazel_id)

        except Exception as e:
            logger.error(f"Client error [{hazel_id}]: {e}")
            await manager.disconnect_client(hazel_id)
