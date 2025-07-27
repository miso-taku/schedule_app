from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse


class ScheduleRepositoryInterface(ABC):
    
    @abstractmethod
    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        pass

    @abstractmethod
    def get_by_id(self, schedule_id: int) -> Optional[ScheduleResponse]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        pass

    @abstractmethod
    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        pass

    @abstractmethod
    def delete(self, schedule_id: int) -> bool:
        pass