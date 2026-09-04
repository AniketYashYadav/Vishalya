import os
from pathlib import Path

# Base directory of backend package
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Database configuration (defaults to SQLite vault inside project root)
DEFAULT_DB_PATH = PROJECT_ROOT / "vishalya_vault.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Weather API settings
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
OPENWEATHER_GEO_URL = "http://api.openweathermap.org/geo/1.0/zip"

# Fallback AQI if live fetch is disabled or offline
FALLBACK_AQI = float(os.getenv("FALLBACK_AQI", "100.0"))

# Project metadata
PROJECT_NAME = "Vishalya Backend API"
API_VERSION = "1.0.0"
