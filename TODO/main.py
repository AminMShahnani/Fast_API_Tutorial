from typing import Optional

from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, LocalSession
import models

app = FastAPI()

def get_db() :
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title: str
    description:  Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between1-5")
    complete: bool

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_all(db: Session = Depends(get_db) ) :
    return db.query(models.Todos).all()

@app.get('/todo/{todo_id}')
async def read_todo(todo_id: int, db: Session =Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise http_exception()

@app.post("/")
async def create_db(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.complete = todo.complete
    todo_model.priority = todo.priority

    db.add(todo_model)
    db.commit()

    return successful_response(201)

@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        return http_exception()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.complete = todo.complete
    todo_model.priority = todo.priority

    db.add(todo_model)
    db.commit()

    return successful_response(200)

@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None :
        return http_exception()
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    return successful_response(200)


def successful_response(status_code: int) :
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception() :
    return HTTPException(status_code=404, detail="Todo Not Found!")