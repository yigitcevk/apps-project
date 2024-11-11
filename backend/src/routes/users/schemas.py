from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InsightBase(BaseModel):
    impressions: int
    cpi: float
    ctr: float
    cpm: float
    ipm: float
    created_at: Optional[datetime] = None

class CampaignCreativeBase(BaseModel):
    campaign_id: int
    asset_id: int
    status: str
    created_at: Optional[datetime] = None

class AssetBase(BaseModel):
    service_asset_id: int
    title: str
    status: str
    created_at: Optional[datetime] = None
    image_path: str

class CampaignBase(BaseModel):
    service_campaign_id: int
    title: str
    active: bool
    created_at: Optional[datetime] = None

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
    
    class Config:
        orm_mode = True