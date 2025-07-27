from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from domain.repositories.schedule_repository import ScheduleRepositoryInterface
from domain.entities.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from infrastructure.database.models import Schedule
from infrastructure.database.connection import SessionLocal


class ScheduleRepositoryImpl(ScheduleRepositoryInterface):
    
    def __init__(self):
        from infrastructure.database.connection import create_tables
        create_tables()

    def _get_db(self) -> Session:
        return SessionLocal()

    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        db = self._get_db()
        try:
            db_schedule = Schedule(**schedule_data.dict())
            db.add(db_schedule)
            db.commit()
            db.refresh(db_schedule)
            return ScheduleResponse.from_orm(db_schedule)
        finally:
            db.close()

    def get_by_id(self, schedule_id: int) -> Optional[ScheduleResponse]:
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule:
                return ScheduleResponse.from_orm(schedule)
            return None
        finally:
            db.close()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        db = self._get_db()
        try:
            schedules = db.query(Schedule).offset(skip).limit(limit).all()
            return [ScheduleResponse.from_orm(schedule) for schedule in schedules]
        finally:
            db.close()

    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                return None
            
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(schedule, field, value)
            
            schedule.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(schedule)
            return ScheduleResponse.from_orm(schedule)
        finally:
            db.close()

    def delete(self, schedule_id: int) -> bool:
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                return False
            
            db.delete(schedule)
            db.commit()
            return True
        finally:
            db.close()