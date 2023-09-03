from pydantic import BaseModel
from typing import List


class Role(BaseModel):
    name: str


class function(BaseModel):
    name: str


class User(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UsersBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RolesBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FunctionBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RoleSchema(RolesBase):
    functions: List[FunctionBase]


class UsersSchema(UsersBase):
    roles: List[RolesBase]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class login(BaseModel):
    email: str
    password: str


class change_password(BaseModel):
    email: str
    new_password: str
    old_password: str
