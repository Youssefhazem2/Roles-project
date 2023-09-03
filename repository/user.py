from sqlalchemy.orm import Session, joinedload
import models
import scemas
from fastapi import HTTPException, status
from hashing import Hash
import re


def is_complex_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return True

    # Check if the password contains at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return True

    # Check if the password contains at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return True

    # Check if the password contains at least one digit
    if not re.search(r"\d", password):
        return True

    # Check if the password contains at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return True

    # If all criteria are met, the password is considered complex
    return False


def check_phone(s):
    if re.search("(011|010|012|015)[0-9]{8}", s):
        return False
    else:
        return True


def create(db: Session, request: scemas.User):
    if is_complex_password(request.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="this password isn't complex")
    if check_phone(request.phone):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="this phone number isn't correct")
    hashedPassword = Hash.bcrypt(request.password)
    newUser = models.User(name=request.name, email=request.email, password=hashedPassword, phone=request.phone)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


def show(user_id: int, db: Session):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} doesn't exist")
    return user


def delete(db: Session, user_id: int):
    User = db.query(models.User).filter(models.User.id == user_id)
    if not User.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {user_id} doesn't exist")
    User.delete()
    db.commit()
    return {"Message": "blog deleted successfully"}


def update(db: Session, request: scemas.change_password):
    user = db.query(models.User).filter(models.User.email == request.email)
    if not user.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email")
    if not Hash.verify(user.first().password, request.old_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    if is_complex_password(request.new_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="this password isn't complex")

    new_password = Hash.bcrypt(request.new_password)
    newUser = scemas.User(name=user.first().name, email=user.first().email, password=new_password,
                          phone=user.first().phone)
    user.update(dict(newUser))
    db.commit()
    return "updated"


def assign_role(db: Session, user_id: int, role_id: int):
    new = models.user_roles(user_id=user_id, role_id=role_id)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def delete_role(db: Session, user_id: int, role_id: int):
    role = db.query(models.user_roles).filter(models.user_roles.user_id == user_id,
                                              models.user_roles.role_id == role_id)
    if not role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user doesn't have this role")
    role.delete()
    db.commit()
    return {"Message": "role deleted successfully"}
