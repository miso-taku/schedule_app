from fastapi import APIRouter
from typing import List
from domain.entities.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from presentation.controllers.schedule_controller import ScheduleController

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate):
    return ScheduleController.create_schedule(schedule)


@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(skip: int = 0, limit: int = 100):
    return ScheduleController.get_schedules(skip, limit)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int):
    return ScheduleController.get_schedule(schedule_id)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate):
    return ScheduleController.update_schedule(schedule_id, schedule_update)


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int):
    return ScheduleController.delete_schedule(schedule_id)