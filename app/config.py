import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # .../app

class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # In-memory DB; resets on every process start/reload
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Auto-create the schema on startup
    AUTO_CREATE_DB = True
    # Optional tiny seed so you can see data immediately
    AUTO_SEED = True

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False