from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Task, Base


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # run on startup
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield  # app runs here

app = FastAPI(lifespan=lifespan)


# command line: uvicorn main:app --reload
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    task = db.query(Task).get(task_id)

    # null check
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.delete(task)
    db.commit()
    return {"message": "completed"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    db.delete(task)
    db.commit()
    return {"message": "deleted"}