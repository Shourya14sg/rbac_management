"""from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from app.models.db import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    #email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)
    role=Column(String)#,ForeignKey("roles.name"))
    """
from pydantic import BaseModel
from enum import Enum

class Group(str,Enum):
    admin="admin",
    developer="developer",
    viewer="viewer"
class choose_group(BaseModel):
    group:Group

class User(BaseModel):
    username: str
    access_key_id: str
    secret_access_key: str

class Config:
    anystr_strip_whitespace = True 
