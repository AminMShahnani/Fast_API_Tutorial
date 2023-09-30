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

def http_exception() :
    return HTTPException(status_code=404, detail="Todo Not Found!")