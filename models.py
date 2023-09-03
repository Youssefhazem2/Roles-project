from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


class user_roles(Base):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("Users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("Roles.id"), primary_key=True)


class role_function(Base):
    __tablename__ = "role_function"
    function_id = Column(Integer, ForeignKey("Functions.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("Roles.id"), primary_key=True)


class Role(Base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", secondary="user_roles", back_populates="roles")
    functions = relationship("Function", secondary="role_function", back_populates="roles")


class Function(Base):
    __tablename__ = "Functions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roles = relationship("Role", secondary="role_function", back_populates="functions")


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)
    roles = relationship("Role", secondary="user_roles", back_populates="users")