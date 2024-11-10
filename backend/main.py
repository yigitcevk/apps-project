from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx # asenkron

from src.config.database import engine
from src.util.db_dependency import get_db

from src.routes import auth, users

from src.routes.users import schemas, models
from src.routes.auth import auth, schemas

users.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # frontend origins
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
@app.get("/proxy/assets", response_model=List[users.schemas.Asset], dependencies=[Depends(auth.verify_token)])
async def proxy_get_assets():
    internal_endpoint = "http://localhost:8000/internal/assets"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(internal_endpoint)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")


# Route to get all campaigns stored in the list.
@app.get("/proxy/campaigns", response_model=List[users.schemas.Campaign], dependencies=[Depends(auth.verify_token)])
async def proxy_get_campaigns(db: Session = Depends(get_db)):
    return db.query(users.models.Campaign).all()

# Route to get all insights stored in the list.
@app.get("/proxy/insights", response_model=List[users.schemas.Insight], dependencies=[Depends(auth.verify_token)])
async def proxy_get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.Insight).all()

# Route to get all campaign_creatives stored in the list.
@app.get("/proxy/campaign_creatives", response_model=List[users.schemas.CampaignCreative], dependencies=[Depends(auth.verify_token)])
async def proxy_get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.CampaignCreative).all()

# Internal route
@app.get("/internal/assets", response_model=List[users.schemas.Asset])
async def get_assets(db: Session = Depends(get_db)):
    return db.query(users.models.Asset).all()




