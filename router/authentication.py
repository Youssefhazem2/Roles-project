from fastapi import APIRouter, Depends, status, HTTPException
import models
import scemas
from database import get_db
from sqlalchemy.orm import Session
from hashing import Hash
import tokens as tokens

router = APIRouter(
    tags=["Authentcation"]
)


@router.post('/login')
async def login(request: scemas.login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not Hash.verify(user.password, request.password) or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect username or password")
    access_token = tokens.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
