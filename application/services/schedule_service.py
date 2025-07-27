from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from domain.repositories.schedule_repository import ScheduleRepositoryInterface


class ScheduleServiceInterface(ABC):
    
    @abstractmethod
    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        pass

    @abstractmethod
    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        pass

    @abstractmethod
    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        pass

    @abstractmethod
    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        pass

    @abstractmethod
    def delete_schedule(self, schedule_id: int) -> bool:
        pass


class ScheduleService(ScheduleServiceInterface):
    
    def __init__(self, repository: ScheduleRepositoryInterface):
        self.repository = repository

    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        return self.repository.create(schedule_data)

    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        return self.repository.get_by_id(schedule_id)

    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        return self.repository.get_all(skip, limit)

    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        return self.repository.update(schedule_id, update_data)

    def delete_schedule(self, schedule_id: int) -> bool:
        return self.repository.delete(schedule_id)