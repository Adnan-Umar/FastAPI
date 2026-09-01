from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

#create database connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

session_local = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# Create API
@app.post("/todos")
def create_todo(title:str, db: Session = Depends(get_db)):
    todo = Todo(title= title, completed = False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message":"Todo created",
        "data":todo
    }