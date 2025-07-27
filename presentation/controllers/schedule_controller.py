from fastapi import HTTPException
from typing import List
from domain.entities.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from application.services.schedule_service import ScheduleServiceInterface
from infrastructure.dependencies import get_schedule_service


class ScheduleController:
    
    @staticmethod
    def create_schedule(schedule: ScheduleCreate) -> ScheduleResponse:
        service = get_schedule_service()
        return service.create_schedule(schedule)

    @staticmethod
    def get_schedules(skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        service = get_schedule_service()
        return service.get_schedules(skip, limit)

    @staticmethod
    def get_schedule(schedule_id: int) -> ScheduleResponse:
        service = get_schedule_service()
        schedule = service.get_schedule(schedule_id)
        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule

    @staticmethod
    def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate) -> ScheduleResponse:
        service = get_schedule_service()
        schedule = service.update_schedule(schedule_id, schedule_update)
        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule

    @staticmethod
    def delete_schedule(schedule_id: int) -> dict:
        service = get_schedule_service()
        success = service.delete_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return {"message": "Schedule deleted successfully"}