from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx # asenkron
import shutil
from datetime import datetime, timedelta
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

# Status
CAMPAIGN_CREATIVE_STATUSES = ["Pending", "Approved", "Rejected", "Serving", "Completed", "Removed"]
ASSET_STATUSES = ["Processing", "Eligible", "Error"]


# Start scheduler
scheduler = BackgroundScheduler()
@scheduler.scheduled_job("interval", seconds=60)  # 1 minute
def call_update_status_api():
    try:
        with httpx.Client() as client:
            # schedule asset status
            response1 = client.get("http://localhost:8000/background/assets/all")
            if response1.status_code == 200:
                print("Asset status update triggered successfully.")
            else:
                print(f"Failed to trigger asset status update. Status: {response1.status_code}")

            # schedule campaign_creative status
            response2 = client.get("http://localhost:8000/background/campaign_creatives/all")
            if response2.status_code == 200:
                print("Campaign Creative status update triggered successfully.")
            else:
                print(f"Failed to trigger Campaign Creative status update. Status: {response2.status_code}")
        
        db_generator = get_db()
        try:
            db = next(db_generator)  
            handle_insights(db) 
        finally:
            db_generator.close()

    except Exception as e:
        print(f"Error while calling update_status API: {e}")

scheduler.start()

# Background task for handling insights.
def handle_insights(db: Session):
    now = datetime.now()

    # 10 minute
    active_campaigns = db.query(models.Campaign).filter(models.Campaign.active == True).all()
    for campaign in active_campaigns:
        time_since_creation = now - campaign.created_at
        if time_since_creation > timedelta(minutes=10):
            creatives = db.query(models.CampaignCreative).filter(
                models.CampaignCreative.campaign_id == campaign.id
            ).all()

            for creative in creatives:
                if not db.query(models.Insight).filter(models.Insight.campaign_creative_id == creative.id).first():
                    new_insight = models.Insight(
                        campaign_creative_id=creative.id,
                        impressions=random.randint(100, 1000),
                        cpi=round(random.uniform(0.1, 1.0), 2),
                        ctr=round(random.uniform(0.01, 0.1), 2),
                        cpm=round(random.uniform(1.0, 10.0), 2),
                        ipm=round(random.uniform(0.1, 1.0), 2),
                        created_at=datetime.now(),
                    )
                    db.add(new_insight)
                    db.commit()
                    print(f"Insight {new_insight.id} created for CampaignCreative {creative.id}")

    # 30 Minute
    insights = db.query(models.Insight).all()
    for insight in insights:
        time_since_creation = now - insight.created_at
        if time_since_creation > timedelta(minutes=30):
            db.delete(insight)
            db.commit()
            print(f"Insight {insight.id} deleted after 30 minutes.")

# Background Task for Asset Status
def update_asset_status(db: Session):
    assets = db.query(users.models.Asset).filter(users.models.Asset.status == "Processing").all()
    for asset in assets:
        new_status = random.choice(ASSET_STATUSES[1:])  # Randomly assign eligible or error
        asset.status = new_status
        db.commit()
        db.refresh(asset)
    print("Asset statuses updated.")

# Background Task for CampaignCreative Status
def update_campaign_creative_status(db: Session):
    campaign_creatives = db.query(users.models.CampaignCreative).filter(users.models.CampaignCreative.status == "Pending").all()
    for creative in campaign_creatives:
        creative.status = random.choice(CAMPAIGN_CREATIVE_STATUSES[1:]) # Randomly assign others
        db.commit()
        db.refresh(creative)
    print("CampaignCreative statuses updated.")


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
@app.get("/proxy/insights/all", response_model=List[users.schemas.Insight], dependencies=[Depends(auth.verify_token)])
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
async def proxy_get_campaign_creatives():
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
        
# Proxy route to upload an campaign_Creative.
@app.post("/proxy/campaign_creatives", response_model=users.schemas.CampaignCreative, dependencies=[Depends(auth.verify_token)])
async def proxy_upload_campaign_creative(campaign_creative: users.schemas.CampaignCreativeBase):
    internal_endpoint = "http://localhost:8000/internal/campaign_creatives"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(internal_endpoint, json=campaign_creative.dict())
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with internal API: {str(e)}")
        
# Proxy route to edit a campaign.
@app.put("/proxy/campaigns/{campaign_id}/status", response_model=users.schemas.Campaign, dependencies=[Depends(auth.verify_token)])
async def proxy_edit_campaign(campaign_id: int, payload: dict):
    # fix the payload
    internal_endpoint = "http://localhost:8000/internal/campaigns/" + str(campaign_id) + "/status"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(internal_endpoint, json=payload)
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

# Proxy route to delete an campaign_creative.
@app.delete("/proxy/campaign_creatives/{creative_id}", response_model=dict, dependencies=[Depends(auth.verify_token)])
async def proxy_delete_campaign_creative(creative_id: int):
    internal_endpoint = "http://localhost:8000/internal/campaign_creatives/" + str(creative_id)
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
async def get_campaign_creatives(db: Session = Depends(get_db)):
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
@app.put("/internal/campaigns/{campaign_id}/status", response_model=users.schemas.Campaign)
async def edit_campaign(campaign_id: int, payload: dict, db: Session = Depends(get_db)):
    active = payload.get("active")
    existing_campaign = db.query(users.models.Campaign).filter(users.models.Campaign.id == campaign_id).first()
    if not existing_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    existing_campaign.active = active
    
    db.commit()
    db.refresh(existing_campaign)
    return existing_campaign

# Route to add a CampaigmCreative
@app.post("/internal/campaign_creatives", response_model=users.schemas.CampaignCreative)
async def create_campaign_creative(campaign_creative: users.schemas.CampaignCreativeBase, db: Session = Depends(get_db)):
    new_creative = models.CampaignCreative(
        campaign_id=campaign_creative.campaign_id,
        asset_id=campaign_creative.asset_id,
        status="Pending",
        created_at=datetime.now(),
    )
    db.add(new_creative)
    db.commit()
    db.refresh(new_creative)
    return new_creative

# Route to delete a CampaignCreative
@app.delete("/internal/campaign_creatives/{creative_id}", response_model=dict)
async def delete_campaign_creative(creative_id: int, db: Session = Depends(get_db)):
    creative = db.query(users.models.CampaignCreative).filter(users.models.CampaignCreative.id == creative_id).first()
    if not creative:
        raise HTTPException(status_code=404, detail="CampaignCreative not found")
    db.delete(creative)
    db.commit()
    return {"detail": "CampaignCreative deleted successfully"}

# Route to trigger assets states.
@app.get("/background/assets/all")
async def trigger_asset_status_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(update_asset_status, db)
    return {"message": "Background status update started."}

# # Route to trigger campaign_Creatives states.
@app.get("/background/campaign_creatives/all")
async def trigger_campaign_creative_status_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(update_campaign_creative_status, db)
    return {"message": "Background status update for CampaignCreatives started."}


