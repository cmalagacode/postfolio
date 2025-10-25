import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

ENGINE_SYNC = create_engine(os.environ["POSTFOLIO_DATABASE_URL"])
ENGINE_ASYNC = create_async_engine(os.environ["POSTFOLIO_DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://"))