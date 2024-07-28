import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ROSSUM_API_KEY = os.getenv("ROSSUM_API_KEY")
ROSSUM_BASE_URL = os.getenv("ROSSUM_BASE_URL")

DUMMY_ENDPOINT = os.getenv("DUMMY_ENDPOINT")
CACHE_DURATION = int(os.getenv("CACHE_DURATION", 3600))

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")