from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.services.auth_service import AuthService

router = APIRouter(tags=["tasks"])

# Initialize auth service
auth_service = AuthService()

# Tasks within a specific list
@router.get("/lists/{list_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(list_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Get all tasks in a list"""
    return TaskService.get_tasks(list_id)

@router.get("/lists/{list_id}/tasks/ordered", response_model=List[TaskResponse])
async def get_tasks_ordered_by_deadline(list_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Get tasks ordered by deadline in a list"""
    return TaskService.get_tasks_ordered_by_deadline(list_id)

@router.get("/lists/{list_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(list_id: str, task_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Get a specific task by ID"""
    task = TaskService.get_task(list_id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found in list {list_id}"
        )
    return task

@router.post("/lists/{list_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def add_task(list_id: str, task: TaskCreate, current_user: dict = Depends(auth_service.get_current_user)):
    """Add a task to a list"""
    created_task = TaskService.add_task(list_id, task)
    if created_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found"
        )
    return created_task

@router.put("/lists/{list_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(list_id: str, task_id: str, task: TaskUpdate, current_user: dict = Depends(auth_service.get_current_user)):
    """Update a task"""
    updated_task = TaskService.update_task(list_id, task_id, task)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found in list {list_id}"
        )
    return updated_task

@router.delete("/lists/{list_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(list_id: str, task_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Delete a task"""
    deleted = TaskService.delete_task(list_id, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found in list {list_id}"
        )
    return None

@router.patch("/lists/{list_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(list_id: str, task_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Toggle task completion status"""
    updated_task = TaskService.toggle_task_completion(list_id, task_id)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found in list {list_id}"
        )
    return updated_task

# Special task endpoints
@router.get("/tasks/due-this-week", response_model=List[TaskResponse])
async def get_tasks_due_this_week(current_user: dict = Depends(auth_service.get_current_user)):
    """Get tasks due this week across all lists"""
    return TaskService.get_tasks_due_this_week()

@router.get("/lists/{list_id}/tasks/ordered", response_model=List[TaskResponse])
async def get_tasks_ordered_by_deadline(list_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Get tasks ordered by deadline in a list"""
    return TaskService.get_tasks_ordered_by_deadline(list_id)
