import os

# config.py
SECRET_KEY = os.environ["POSTFOLIO_SECRET_KEY"]  # strong, random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30