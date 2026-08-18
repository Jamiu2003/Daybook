from sqlalchemy import String, Column, Integer, Boolean, DateTime,func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    completed = Column(Boolean, default=False)

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(String, nullable=False)
    mood = Column(String, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())





class Milestone(Base):
    __tablename__ = "milestones"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    time_created = Column(DateTime(timezone=True), server_default = func.now())

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    target_date = Column(DateTime, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default = func.now())
    milestones = relationship("Milestone", cascade="all,delete-orphan", order_by =Milestone.time_created)

    