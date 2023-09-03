from fastapi import APIRouter, Depends, status
import scemas
from database import get_db
from sqlalchemy.orm import Session
from repository import user

# from oauth2 import get_current_user
router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("", status_code=status.HTTP_201_CREATED)
def creat(request: scemas.User, db: Session = Depends(get_db)):
    return user.create(db, request)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=scemas.UsersSchema)
def show(user_id: int, db: Session = Depends(get_db)):
    return user.show(user_id, db)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(user_id: int, db: Session = Depends(get_db)):
    return user.delete(db, user_id)


@router.put("/update")
def update_user(request: scemas.change_password, db: Session = Depends(get_db)):
    return user.update(db, request)


@router.post("/assign_role/{user_id}/{role_id}", status_code=status.HTTP_201_CREATED)
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return user.assign_role(db, user_id, role_id)


@router.delete("/delete_role/{user_id}/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return user.delete_role(db, user_id, role_id)
