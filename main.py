from fastapi import FastAPI, HTTPException, Depends, Request 
from pydantic import BaseModel, Field
from typing import Optional, List
import enum
from sqlalchemy import Enum
from model import StatusEnum
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import select
from model import Task
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import  Page, add_pagination
import auth
from fastapi.responses import JSONResponse
from auth import get_current_user
from starlette import status

app = FastAPI()
app.include_router(auth.router)
model.Base.metadata.create_all(bind = engine)

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = 500,
        content = {"detail": f"Unhandled error: {repr(exc)}"},
    )

class User_Model(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    username: str
    password: str = Field(..., min_length = 6)


class StatusEnum(str, enum.Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"


class Task_Model(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum
    user_id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

#####------------------------------------------------------Task 3

@app.get('/tasks', status_code = status.HTTP_200_OK, response_model = Page[Task_Model])
async def get_all_tasks(user: user_dependency, db: Session = Depends(get_db)) -> Page[Task_Model]:
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    return paginate(db, select(Task).order_by(Task.id))

@app.get("/tasks/user/{user_id}", status_code = status.HTTP_200_OK, response_model = Page[Task_Model])
async def get_user_tasks(user: user_dependency, user_id: int, db: Session = Depends(get_db)) -> Page[Task_Model]:
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    return paginate(db, select(Task).where(Task.user_id == user_id).order_by(Task.id))

add_pagination(app)

@app.get("/tasks/{task_id}", status_code = status.HTTP_200_OK, response_model=Task_Model)
async def get_task(user: user_dependency, task_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code = status.HTTP_200_OK)
async def create_task(user: user_dependency, task: Task_Model, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    new_task = model.Task(
        title = task.title,
        description = task.description,
        status = task.status,
        user_id = task.user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_current_user():
    return model.User(id=1, username="Aysel", first_name="Test", last_name="Dadasheva", password="123456")

@app.put("/tasks/{task_id}", status_code = status.HTTP_200_OK, response_model=Task_Model)
async def update_task(user: user_dependency, task_id: int, task_data: Task_Model, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    task = db.query(model.Task).filter(model.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own tasks")
    
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.user_id = task.user_id
    db.commit()
    db.refresh(task)
    
    return task

@app.delete("/tasks/{task_id}", status_code = status.HTTP_200_OK)
async def delete_task(user: user_dependency, task_id: int, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    task = db.query(model.Task).filter(model.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tasks")
    
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}

######--------------------------------------------------------------------------Task 4


@app.get("/tasks-by-status", status_code = status.HTTP_200_OK)
async def filter_tasks(user: user_dependency, status: Optional[model.StatusEnum] = None, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    query = db.query(model.Task)
    if status:
        query = query.filter(model.Task.status == status)
    return query.all()


@app.post("/tasks/{task_id}/complete", status_code = status.HTTP_200_OK)
async def mark_completed(user: user_dependency, task_id: int, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication failed')
    task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    task.status = model.StatusEnum.completed
    db.commit()
    db.refresh(task)
    return task
