from sqlalchemy.orm import Session
import scemas
import models
from fastapi import Response, HTTPException, status


def get_all(db: Session):
    functions = db.query(models.Function).all()
    return functions


def create(db: Session, name: str):
    new_function = models.Function(name=name)
    db.add(new_function)
    db.commit()
    db.refresh(new_function)
    return new_function


def delete(db: Session, role_id: int):
    Function = db.query(models.Function).filter(models.Function.id == role_id)
    if not Function.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {role_id} doesn't exist")
    Function.delete()
    db.commit()
    return {"Message": "blog deleted successfully"}


def update(db: Session, Function_id: int, request: scemas.function):
    Function = db.query(models.Function).filter(models.Function.id == Function_id)
    if not Function.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {Function_id} doesn't exist")

    Function.update(dict(request))
    db.commit()
    return "updated"


def Show(function_id: int, response: Response, db: Session):
    function = db.query(models.Function).filter(models.Function.id == function_id).first()
    if not function:
        response.status_code = status.HTTP_404_NOT_FOUND
    return function


