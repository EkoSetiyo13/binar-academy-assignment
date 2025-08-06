from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.schemas.list_schema import ListCreate, ListUpdate, ListResponse
from app.services.list_service import ListService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/lists", tags=["lists"])

# Initialize auth service
auth_service = AuthService()

@router.get("/", response_model=List[ListResponse])
async def get_lists(current_user: dict = Depends(auth_service.get_current_user)):
    """Get all lists with their tasks"""
    return ListService.get_lists()

@router.get("/{list_id}", response_model=ListResponse)
async def get_list(list_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Get a specific list by ID"""
    list_data = ListService.get_list(list_id)
    if list_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found"
        )
    return list_data

@router.post("/", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(list_data: ListCreate, current_user: dict = Depends(auth_service.get_current_user)):
    """Create a new list"""
    return ListService.create_list(list_data)

@router.put("/{list_id}", response_model=ListResponse)
async def update_list(list_id: str, list_data: ListUpdate, current_user: dict = Depends(auth_service.get_current_user)):
    """Update an existing list"""
    updated_list = ListService.update_list(list_id, list_data)
    if updated_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found"
        )
    return updated_list

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(list_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    """Delete a list"""
    deleted = ListService.delete_list(list_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found"
        )
    return None
