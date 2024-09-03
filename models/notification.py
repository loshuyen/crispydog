from pydantic import BaseModel

class Sender(BaseModel):
    id: int
    username: str

class Notification(BaseModel):
    id: int
    sender: Sender
    product_id: int | None
    commission_id: int | None
    message_type: int
    message: str | None
    is_read: int
    created_at: str

class NotificationListData(BaseModel):
    data: list[Notification]