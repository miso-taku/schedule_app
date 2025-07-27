from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_completed: Optional[bool] = None


class ScheduleResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True