from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx # asenkron
import shutil
from datetime import datetime
import os

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

# Asset upload directory
UPLOAD_DIR = "./apps/uploaded_assets/"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

# Redirect / -> Swagger-UI documentation
@app.get("/")
def home():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")





# Proxy route to get all assets stored in the list.
@app.get("/proxy/assets", response_model=List[users.schemas.Asset], dependencies=[Depends(auth.verify_token)])
async def proxy_get_assets():
    internal_endpoint = "http://localhost:8000/internal/assets"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(internal_endpoint)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")


# Proxy route to upload an asset.
@app.post("/proxy/assets", response_model=users.schemas.Asset, dependencies=[Depends(auth.verify_token)])
async def proxy_upload_asset(file: UploadFile = File(...)):
    internal_endpoint = "http://localhost:8000/internal/assets"
    async with httpx.AsyncClient() as client:
        try:
            formData = {
                "file": (file.filename, file.file, file.content_type)
            }
            response = await client.post(internal_endpoint, files=formData)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")


# Proxy route to delete an asset.
@app.delete("/proxy/assets/{asset_id}", response_model=dict, dependencies=[Depends(auth.verify_token)])
async def proxy_delete_asset(asset_id: int):
    internal_endpoint = "http://localhost:8000/internal/assets/" + str(asset_id)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(internal_endpoint)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")




# Route to get all assets.
@app.get("/internal/assets", response_model=List[users.schemas.Asset])
async def get_assets(db: Session = Depends(get_db)):
    return db.query(users.models.Asset).all()

# Route to upload an asset.
@app.post("/internal/assets", response_model=users.schemas.Asset)
async def upload_asset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"{UPLOAD_DIR}{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # database add
    new_asset = models.Asset(
        title=file.filename,
        status="eligible",
        created_at=datetime.now(),
        image_path=file_path,
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset

# Route to delete an asset.
@app.delete("/internal/assets/{asset_id}", response_model=dict)
async def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(users.models.Asset).filter(users.models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # remove the asset
    if asset.image_path:
        try:
            os.remove(asset.image_path)
        except FileNotFoundError:
            pass

    db.delete(asset)
    db.commit()
    return {"detail": "Asset deleted successfully"}





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





