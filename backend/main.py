from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import engine
from src.util.db_dependency import get_db

from src.routes import auth, users

from src.routes.users import schemas, models
from src.routes.auth import *

users.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect / -> Swagger-UI documentation
@app.get("/")
def home():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")


# Route to get all assets stored in the list.
@app.get("/assets", response_model=List[users.schemas.Asset])
async def get_assets(db: Session = Depends(get_db)):
    return db.query(users.models.Asset).all()

# Route to get all campaigns stored in the list.
@app.get("/campaigns", response_model=List[users.schemas.Campaign])
async def get_campaigns(db: Session = Depends(get_db)):
    return db.query(users.models.Campaign).all()

# Route to get all insights stored in the list.
@app.get("/insights", response_model=List[users.schemas.Insight])
async def get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.Insight).all()

# Route to get all campaign_creatives stored in the list.
@app.get("/campaign_creatives", response_model=List[users.schemas.CampaignCreative])
async def get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.CampaignCreative).all()
