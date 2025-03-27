# config.py
import os

DATA_DIR = os.getenv("DATA_DIR", "data")
DATABASE_URL = os.getenv("DATABASE_URL")
TIMEGPT_API_KEY = os.getenv("TIMEGPT_API_KEY")
