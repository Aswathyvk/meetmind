from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MeetingOut(BaseModel):
    id: int
    title: str
    audio_filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True