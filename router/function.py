from typing import List

from fastapi import APIRouter, Depends, status, Response

import scemas
from oauth2 import get_current_user
from database import get_db
from sqlalchemy.orm import Session
from repository.function import *

router = APIRouter(
    prefix="/function",
    tags=['functions']
)


@router.get("", response_model=List[scemas.function])
def all(db: Session = Depends(get_db), current_user: scemas.User = Depends(get_current_user)):
    functions = get_all(db)
    if not functions:
        Response.status_code = status.HTTP_404_NOT_FOUND
    return functions


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
def creat(name: str, db: Session = Depends(get_db)):
    return create(db, name)


@router.get("/{function_id}", status_code=status.HTTP_200_OK, response_model=scemas.FunctionBase)
def show(function_id: int, response: Response, db: Session = Depends(get_db)):
    return Show(function_id, response, db)


@router.delete("/delete/{function_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(function_id: int, db: Session = Depends(get_db)):
    return delete(db, function_id)


@router.put("/update/{function_id}")
def update_blog(function_id: int, request: scemas.function, db: Session = Depends(get_db)):
    return update(db, function_id, request)

