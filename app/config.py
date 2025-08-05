import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not SECRET_KEY or not isinstance(SECRET_KEY, str):
    raise ValueError("JWT_SECRET is missing or not a string!")
