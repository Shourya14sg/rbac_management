"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///models.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #db session

Base = declarative_base()
"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,String
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    role =  Column(String)
    def dict(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "role": self.role
        }

