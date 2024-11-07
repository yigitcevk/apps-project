from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base, get_db
from . import models, schemas
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome!"}

@app.get("/assets", response_model=List[schemas.Asset])
def read_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()

@app.get("/campaigns", response_model=List[schemas.Campaign])
def read_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()
