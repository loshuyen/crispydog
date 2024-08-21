from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from database import notification as db
from routers.user import get_auth_user
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

@router.get("/api/notifications")
def get_notifications(is_read: int | None = None, user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_notifications(user["id"], is_read)
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})