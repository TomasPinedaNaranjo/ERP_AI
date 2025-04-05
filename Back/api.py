from fastapi import FastAPI, Depnends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import localSession, engine
from models import Base
from schemas import UserData, UserId

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return  "Hello World"

@app.get("/api/users/", response_model=list[UserId])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

