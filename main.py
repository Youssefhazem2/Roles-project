from fastapi import FastAPI
from database import engine
import models
from router import authentication, role, user, function
# uvicorn main:app --reload
app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(role.router)
app.include_router(user.router)
app.include_router(function.router)
app.include_router(authentication.router)
