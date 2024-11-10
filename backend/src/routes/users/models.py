from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base
import random


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    service_asset_id = Column(Integer, unique=True, default=lambda: random.randint(100000, 999999))
    title = Column(String, index=True)
    status = Column(String)
    created_at = Column(DateTime)
    image_path = Column(String) 

    campaign_creatives = relationship("CampaignCreative", back_populates="asset")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    service_campaign_id = Column(Integer)
    title = Column(String, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    campaign_creatives = relationship("CampaignCreative", back_populates="campaign")


class CampaignCreative(Base):
    __tablename__ = "campaign_creatives"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    created_at = Column(DateTime)

    campaign = relationship("Campaign", back_populates="campaign_creatives")
    asset = relationship("Asset", back_populates="campaign_creatives")
    insights = relationship("Insight", back_populates="campaign_creative")


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    impressions = Column(Integer)
    cpi = Column(Float)
    ctr = Column(Float)
    cpm = Column(Float)
    ipm = Column(Float)
    campaign_creative_id = Column(Integer, ForeignKey("campaign_creatives.id"))
    created_at = Column(DateTime)

    campaign_creative = relationship("CampaignCreative", back_populates="insights")
