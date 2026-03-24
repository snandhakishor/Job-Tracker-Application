from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from datetime import datetime
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(200), nullable=False)
    job_title = Column(String(200), nullable=False)
    salary = Column(Float, nullable=True)
    applied = Column(String(50), default="yes")
    job_added_at = Column(DateTime, default=datetime.now)
    job_board = Column(String(200), nullable=True)
    job_location = Column(String(200), nullable=True)
    status = Column(String(200), default="pending")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)