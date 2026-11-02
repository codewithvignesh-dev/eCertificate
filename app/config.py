import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "ecertificate")
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", "10"))
    DB_READ_TIMEOUT = int(os.getenv("DB_READ_TIMEOUT", "30"))
    DB_WRITE_TIMEOUT = int(os.getenv("DB_WRITE_TIMEOUT", "30"))
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    SESSION_COOKIE_HTTPONLY = os.getenv("SESSION_COOKIE_HTTPONLY", "true").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    REMEMBER_COOKIE_SECURE = os.getenv("REMEMBER_COOKIE_SECURE", "false").lower() == "true"
    REMEMBER_COOKIE_HTTPONLY = os.getenv("REMEMBER_COOKIE_HTTPONLY", "true").lower() == "true"
    REMEMBER_COOKIE_SAMESITE = os.getenv("REMEMBER_COOKIE_SAMESITE", "Lax")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))
    UPLOAD_FOLDER = str(BASE_DIR / os.getenv("UPLOAD_FOLDER", "storage/uploads"))
    GENERATED_FOLDER = str(BASE_DIR / os.getenv("GENERATED_FOLDER", "storage/generated"))
    TEMP_FOLDER = str(BASE_DIR / os.getenv("TEMP_FOLDER", "storage/temp"))
    ALLOWED_EXTENSIONS = {x.strip().lower() for x in os.getenv("ALLOWED_EXTENSIONS", "xlsx,xls,csv").split(",") if x.strip()}
    COMPANY_NAME = os.getenv("COMPANY_NAME", "GAMKERS")
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "")
    COMPANY_PHONE = os.getenv("COMPANY_PHONE", "")
    COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "")
