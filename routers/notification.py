from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import jwt
import os

router = APIRouter()

connections = {}

async def notify_user(user_id: int, message: str):
    if user_id in connections.keys():
        websocket = connections[user_id]
        await websocket.send_text(message)

@router.websocket("/api/notification")
async def websocket_endpoint(websocket: WebSocket, token = Query()):
    decode_data = jwt.decode(token, os.getenv("TOKEN_SECRET_KEY"), algorithms="HS256")
    user_id = decode_data["id"]
    if not user_id:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    await websocket.accept()
    connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        del connections[user_id]