import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

if os.environ["POSTFOLIO_ENV"] == "PROD":
    database_url = os.environ["POSTFOLIO_DATABASE_URL"]
    ENGINE_SYNC = create_engine(database_url)
    ENGINE_ASYNC = create_async_engine(database_url.replace("postgresql://", "postgresql+asyncpg://"))
else:
    ENGINE_SYNC = create_engine("sqlite:///db.sqlite?cache=shared", connect_args={"check_same_thread": False, "uri": True})
    ENGINE_ASYNC = ENGINE_SYNC