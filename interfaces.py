"""Interfaces and data models for the schedule management application.

This module defines the abstract interfaces and Pydantic models used
throughout the schedule management system.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    """Pydantic model for creating a new schedule.
    
    Attributes:
        title: The title of the schedule.
        description: Optional description of the schedule.
        start_time: The start time of the schedule.
        end_time: The end time of the schedule.
    """
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class ScheduleUpdate(BaseModel):
    """Pydantic model for updating an existing schedule.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: The new title of the schedule.
        description: The new description of the schedule.
        start_time: The new start time of the schedule.
        end_time: The new end time of the schedule.
        is_completed: Whether the schedule is completed.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_completed: Optional[bool] = None


class ScheduleResponse(BaseModel):
    """Pydantic model for schedule responses.
    
    This model represents a complete schedule with all fields.
    
    Attributes:
        id: The unique identifier of the schedule.
        title: The title of the schedule.
        description: The description of the schedule.
        start_time: The start time of the schedule.
        end_time: The end time of the schedule.
        is_completed: Whether the schedule is completed.
        created_at: When the schedule was created.
        updated_at: When the schedule was last updated.
    """
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


class ScheduleRepositoryInterface(ABC):
    """Abstract interface for schedule data persistence operations.
    
    This interface defines the methods required for managing schedule data
    in a persistent storage system.
    """
    
    @abstractmethod
    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """Create a new schedule in the repository.
        
        Args:
            schedule_data: The schedule data to create.
            
        Returns:
            The created schedule response.
        """
        pass

    @abstractmethod
    def get_by_id(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """Retrieve a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to retrieve.
            
        Returns:
            The schedule response if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """Retrieve all schedules with pagination.
        
        Args:
            skip: Number of schedules to skip.
            limit: Maximum number of schedules to return.
            
        Returns:
            List of schedule responses.
        """
        pass

    @abstractmethod
    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """Update an existing schedule.
        
        Args:
            schedule_id: The ID of the schedule to update.
            update_data: The update data.
            
        Returns:
            The updated schedule response if found, None otherwise.
        """
        pass

    @abstractmethod
    def delete(self, schedule_id: int) -> bool:
        """Delete a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to delete.
            
        Returns:
            True if the schedule was deleted, False if not found.
        """
        pass


class ScheduleServiceInterface(ABC):
    """Abstract interface for schedule business logic operations.
    
    This interface defines the business logic methods for managing schedules.
    It acts as a facade over the repository layer.
    """
    
    @abstractmethod
    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """Create a new schedule.
        
        Args:
            schedule_data: The schedule data to create.
            
        Returns:
            The created schedule response.
        """
        pass

    @abstractmethod
    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """Retrieve a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to retrieve.
            
        Returns:
            The schedule response if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """Retrieve all schedules with pagination.
        
        Args:
            skip: Number of schedules to skip.
            limit: Maximum number of schedules to return.
            
        Returns:
            List of schedule responses.
        """
        pass

    @abstractmethod
    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """Update an existing schedule.
        
        Args:
            schedule_id: The ID of the schedule to update.
            update_data: The update data.
            
        Returns:
            The updated schedule response if found, None otherwise.
        """
        pass

    @abstractmethod
    def delete_schedule(self, schedule_id: int) -> bool:
        """Delete a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to delete.
            
        Returns:
            True if the schedule was deleted, False if not found.
        """
        pass