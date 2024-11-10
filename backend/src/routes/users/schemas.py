from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InsightBase(BaseModel):
    impressions: int
    cpi: float
    ctr: float
    cpm: float
    ipm: float
    created_at: datetime

class CampaignCreativeBase(BaseModel):
    status: str
    created_at: datetime

class AssetBase(BaseModel):
    service_asset_id: int
    title: str
    status: str
    created_at: datetime
    image_path: str

class CampaignBase(BaseModel):
    service_campaign_id: int
    title: str
    active: bool
    created_at: datetime

class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True

class Campaign(CampaignBase):
    id: int

    class Config:
        orm_mode = True

class Insight(InsightBase):
    id: int
    campaign_creative_id: int
    
    class Config:
        orm_mode = True

class CampaignCreative(CampaignCreativeBase):
    id: int
    campaign_id: int
    asset_id: int
    
    class Config:
        orm_mode = True