from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# TODO: Configure your production db
DATABASE_URL = "postgresql://postgres:12345@localhost/apps" # user:password
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@db:5432/apps")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
