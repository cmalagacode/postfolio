from schema.user import Base
from schema.connection import ENGINE_SYNC


def initialize_database():
    print("Creating database tables...")
    Base.metadata.create_all(ENGINE_SYNC)
    print("Tables created (if they didn't exist).")