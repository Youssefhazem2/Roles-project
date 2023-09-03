from sqlalchemy.orm import Session
import scemas
import models
from fastapi import Response, HTTPException, status


def get_all(db: Session):
    roles = db.query(models.Role).all()
    return roles


def create(db: Session, name: str):
    new_role = models.Role(name=name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def delete(db: Session, role_id: int):
    Role = db.query(models.Role).filter(models.Role.id == role_id)
    if not Role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {role_id} doesn't exist")
    Role.delete()
    db.commit()
    return {"Message": "blog deleted successfully"}


def update(db: Session, role_id: int, request: scemas.Role):
    Role = db.query(models.Role).filter(models.Role.id == role_id)
    if not Role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} doesn't exist")

    Role.update(dict(request))
    db.commit()
    return "updated"


def show(role_id: int, response: Response, db: Session):
    Role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not Role:
        response.status_code = status.HTTP_404_NOT_FOUND
    return Role


def assign_function(db: Session, function_id: int, role_id: int):
    new = models.role_function(function_id=function_id, role_id=role_id)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def delete_function(db: Session, function_id: int, role_id: int):
    role = db.query(models.role_function).filter(models.role_function.function_id == function_id, models.role_function.role_id == role_id)
    if not role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this role doesn't have this function")
    role.delete()
    db.commit()
    return {"Message": "role deleted successfully"}