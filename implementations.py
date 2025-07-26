"""Concrete implementations of schedule management interfaces.

This module contains the concrete implementations of the repository and service
interfaces, as well as the SQLAlchemy database models.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional
from interfaces import (
    ScheduleCreate, 
    ScheduleUpdate, 
    ScheduleResponse, 
    ScheduleRepositoryInterface, 
    ScheduleServiceInterface
)


DATABASE_URL = "sqlite:///./schedule.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Schedule(Base):
    """SQLAlchemy model for the schedules table.
    
    This model represents a schedule record in the database.
    
    Attributes:
        id: Primary key identifier.
        title: Title of the schedule.
        description: Optional description of the schedule.
        start_time: Start time of the schedule.
        end_time: End time of the schedule.
        is_completed: Whether the schedule is completed.
        created_at: Timestamp when the schedule was created.
        updated_at: Timestamp when the schedule was last updated.
    """
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScheduleRepository(ScheduleRepositoryInterface):
    """Concrete implementation of the schedule repository interface.
    
    This class provides data persistence operations for schedules using SQLAlchemy.
    """
    
    def __init__(self):
        """Initialize the repository and create database tables."""
        Base.metadata.create_all(bind=engine)

    def _get_db(self) -> Session:
        """Get a database session.
        
        Returns:
            A SQLAlchemy database session.
        """
        return SessionLocal()

    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """Create a new schedule in the database.
        
        Args:
            schedule_data: The schedule data to create.
            
        Returns:
            The created schedule response.
        """
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
        """Retrieve a schedule by its ID from the database.
        
        Args:
            schedule_id: The ID of the schedule to retrieve.
            
        Returns:
            The schedule response if found, None otherwise.
        """
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule:
                return ScheduleResponse.from_orm(schedule)
            return None
        finally:
            db.close()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """Retrieve all schedules with pagination from the database.
        
        Args:
            skip: Number of schedules to skip.
            limit: Maximum number of schedules to return.
            
        Returns:
            List of schedule responses.
        """
        db = self._get_db()
        try:
            schedules = db.query(Schedule).offset(skip).limit(limit).all()
            return [ScheduleResponse.from_orm(schedule) for schedule in schedules]
        finally:
            db.close()

    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """Update an existing schedule in the database.
        
        Args:
            schedule_id: The ID of the schedule to update.
            update_data: The update data.
            
        Returns:
            The updated schedule response if found, None otherwise.
        """
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
        """Delete a schedule from the database.
        
        Args:
            schedule_id: The ID of the schedule to delete.
            
        Returns:
            True if the schedule was deleted, False if not found.
        """
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


class ScheduleService(ScheduleServiceInterface):
    """Concrete implementation of the schedule service interface.
    
    This class provides business logic operations for schedules.
    It acts as a facade over the repository layer.
    """
    
    def __init__(self, repository: ScheduleRepositoryInterface):
        """Initialize the service with a repository.
        
        Args:
            repository: The schedule repository implementation.
        """
        self.repository = repository

    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """Create a new schedule.
        
        Args:
            schedule_data: The schedule data to create.
            
        Returns:
            The created schedule response.
        """
        return self.repository.create(schedule_data)

    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """Retrieve a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to retrieve.
            
        Returns:
            The schedule response if found, None otherwise.
        """
        return self.repository.get_by_id(schedule_id)

    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """Retrieve all schedules with pagination.
        
        Args:
            skip: Number of schedules to skip.
            limit: Maximum number of schedules to return.
            
        Returns:
            List of schedule responses.
        """
        return self.repository.get_all(skip, limit)

    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """Update an existing schedule.
        
        Args:
            schedule_id: The ID of the schedule to update.
            update_data: The update data.
            
        Returns:
            The updated schedule response if found, None otherwise.
        """
        return self.repository.update(schedule_id, update_data)

    def delete_schedule(self, schedule_id: int) -> bool:
        """Delete a schedule by its ID.
        
        Args:
            schedule_id: The ID of the schedule to delete.
            
        Returns:
            True if the schedule was deleted, False if not found.
        """
        return self.repository.delete(schedule_id)


def get_db():
    """Dependency function to get a database session.
    
    This function is used as a FastAPI dependency to provide
    database sessions to endpoints.
    
    Yields:
        A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_schedule_service() -> ScheduleService:
    """Factory function to create a schedule service instance.
    
    Creates a schedule service with a repository implementation.
    
    Returns:
        A configured schedule service instance.
    """
    repository = ScheduleRepository()
    return ScheduleService(repository)