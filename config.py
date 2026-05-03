import os
from dotenv import load_dotenv

load_dotenv()

METER_SERVICE_URL = os.getenv("METER_SERVICE_URL")
COLLECTION_SERVICE_URL = os.getenv("COLLECTION_SERVICE_URL")
ANALYSIS_SERVICE_URL = os.getenv("ANALYSIS_SERVICE_URL")