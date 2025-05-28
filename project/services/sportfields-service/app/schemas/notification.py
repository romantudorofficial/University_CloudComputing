from pydantic import BaseModel
from datetime import datetime

class NotificationRead(BaseModel):
    notification_id: int
    owner_id: str
    rental_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True