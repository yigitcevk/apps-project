from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx # asenkron
import shutil
from datetime import datetime
import os, random
from apscheduler.schedulers.background import BackgroundScheduler


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


# Start scheduler
scheduler = BackgroundScheduler()
@scheduler.scheduled_job("interval", seconds=60)  # 1 minute
def call_update_status_api():
    try:
        with httpx.Client() as client:
            response1 = client.get("http://localhost:8000/background/assets/all")
            if response1.status_code == 200:
                print("Asset status update triggered successfully.")
            else:
                print(f"Failed to trigger asset status update. Status: {response1.status_code}")
    except Exception as e:
        print(f"Error while calling update_status API: {e}")

scheduler.start()


# Update asset status as a background task
def update_asset_status(db: Session):
    assets = db.query(users.models.Asset).filter(users.models.Asset.status == "processing").all()
    for asset in assets:
        new_status = random.choice(["eligible", "error"])  # Randomly assign eligible or error
        asset.status = new_status
        db.commit()
        db.refresh(asset)
    print("Asset statuses updated.")


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

# Proxy route to get all campaigns stored in the list.
@app.get("/proxy/campaigns", response_model=List[users.schemas.Campaign], dependencies=[Depends(auth.verify_token)])
async def proxy_get_campaigns():
    internal_endpoint = "http://localhost:8000/internal/campaigns"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(internal_endpoint)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")

# Proxy route to get all insights.
@app.get("/proxy/insights", response_model=List[users.schemas.Insight], dependencies=[Depends(auth.verify_token)])
async def proxy_get_insights():
    internal_endpoint = "http://localhost:8000/internal/insights"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(internal_endpoint)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")

# Proxy route to get all campaign_creatives.
@app.get("/proxy/campaign_creatives", response_model=List[users.schemas.CampaignCreative], dependencies=[Depends(auth.verify_token)])
async def proxy_get_insights():
    internal_endpoint = "http://localhost:8000/internal/campaign_creatives"
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
        
# Proxy route to edit a campaign.
@app.put("/proxy/campaigns/{campaign_id}", response_model=users.schemas.Campaign, dependencies=[Depends(auth.verify_token)])
async def proxy_edit_campaign(campaign_id: int, campaign: users.schemas.CampaignBase):
    internal_endpoint = "http://localhost:8000/internal/campaigns/" + str(campaign_id)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(internal_endpoint, json=campaign.dict())
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

# Route to get all campaigns.
@app.get("/internal/campaigns", response_model=List[users.schemas.Campaign])
async def get_campaigns(db: Session = Depends(get_db)):
    return db.query(users.models.Campaign).all()

# Route to get all insights.
@app.get("/internal/insights", response_model=List[users.schemas.Insight])
async def get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.Insight).all()

# Route to get all campaign_creatives.
@app.get("/internal/campaign_creatives", response_model=List[users.schemas.CampaignCreative])
async def get_insights(db: Session = Depends(get_db)):
    return db.query(users.models.CampaignCreative).all()

# Route to upload an asset.
@app.post("/internal/assets", response_model=users.schemas.Asset)
async def upload_asset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"{UPLOAD_DIR}{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # database add
    new_asset = models.Asset(
        title=file.filename,
        status="Processing",
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

# Route to edit a campaign
@app.put("/internal/campaigns/{campaign_id}", response_model=users.schemas.Campaign)
async def edit_campaign(campaign_id: int, campaign: users.schemas.CampaignBase, db: Session = Depends(get_db)):
    existing_campaign = db.query(users.models.Campaign).filter(users.models.Campaign.id == campaign_id).first()
    if not existing_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for key, value in campaign.dict().items():
        setattr(existing_campaign, key, value)
    
    db.commit()
    db.refresh(existing_campaign)
    return existing_campaign

# Route to check assets states.
@app.get("/background/assets/all")
async def trigger_asset_status_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(update_asset_status, db)
    return {"message": "Background status update started."}


