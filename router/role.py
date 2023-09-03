from typing import List

from fastapi import APIRouter, Depends, status, Response

import scemas
from oauth2 import get_current_user
from database import get_db
from sqlalchemy.orm import Session
from repository import role

router = APIRouter(
    prefix="/role",
    tags=['roles']
)


@router.get("", response_model=List[scemas.RoleSchema])
def all(db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    roles = role.get_all(db)
    if not roles:
        Response.status_code = status.HTTP_404_NOT_FOUND
    return roles


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
def creat(name: str, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.create(db, name)


@router.get("/{role_id}", status_code=status.HTTP_200_OK, response_model=scemas.RoleSchema)
def show(role_id: int, response: Response, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.show(role_id, response, db)


@router.delete("/delete/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(role_id: int, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.delete(db, role_id)


@router.put("/update/{role_id}")
def update_blog(role_id: int, request: scemas.Role, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.update(db, role_id, request)


@router.post("/assign_function/{role_id}/{function_id}", status_code=status.HTTP_201_CREATED)
def assign_function(function_id: int, role_id: int, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.assign_function(db, function_id, role_id)


@router.delete("/delete_function/{function_id}/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_function(function_id: int, role_id: int, db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    return role.delete_function(db, function_id, role_id)
