from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Task, Base

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.post("/tasks")
def create_task(task: dict, db: Session = Depends(get_db)):
    new_task = Task(title=task["title"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    # null check
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    db.delete(task)
    db.commit()
    return {"message": "deleted"}