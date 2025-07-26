"""Main FastAPI application for the schedule management system.

This module contains the FastAPI application and API endpoints for
managing schedules. It serves as the entry point for the application.
"""

from fastapi import FastAPI, HTTPException
from typing import List
from interfaces import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from implementations import create_schedule_service

app = FastAPI(title="Schedule Management API", version="1.0.0")

schedule_service = create_schedule_service()


@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        A dictionary containing a welcome message.
    """
    return {"message": "Schedule Management API"}


@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate):
    """Create a new schedule.
    
    Args:
        schedule: The schedule data to create.
        
    Returns:
        The created schedule response.
    """
    return schedule_service.create_schedule(schedule)


@app.get("/schedules/", response_model=List[ScheduleResponse])
def read_schedules(skip: int = 0, limit: int = 100):
    """Retrieve all schedules with pagination.
    
    Args:
        skip: Number of schedules to skip for pagination.
        limit: Maximum number of schedules to return.
        
    Returns:
        List of schedule responses.
    """
    return schedule_service.get_schedules(skip, limit)


@app.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
def read_schedule(schedule_id: int):
    """Retrieve a specific schedule by its ID.
    
    Args:
        schedule_id: The ID of the schedule to retrieve.
        
    Returns:
        The schedule response.
        
    Raises:
        HTTPException: If the schedule is not found (404).
    """
    schedule = schedule_service.get_schedule(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@app.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate):
    """Update an existing schedule.
    
    Args:
        schedule_id: The ID of the schedule to update.
        schedule_update: The update data.
        
    Returns:
        The updated schedule response.
        
    Raises:
        HTTPException: If the schedule is not found (404).
    """
    schedule = schedule_service.update_schedule(schedule_id, schedule_update)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int):
    """Delete a schedule by its ID.
    
    Args:
        schedule_id: The ID of the schedule to delete.
        
    Returns:
        A success message.
        
    Raises:
        HTTPException: If the schedule is not found (404).
    """
    success = schedule_service.delete_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}


if __name__ == "__main__":
    """Run the FastAPI application with uvicorn server.
    
    This block is executed when the script is run directly.
    It starts the uvicorn server on all interfaces (0.0.0.0) at port 8000.
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)