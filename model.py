from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
import enum
from sqlalchemy import Enum as SqlEnum

class StatusEnum(str, enum.Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SqlEnum(StatusEnum, name="status_enum"), default=StatusEnum.new)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))