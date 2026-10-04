import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

class Config:
    APP_ENV = os.getenv('APP_ENV', 'development').lower()
    DEBUG = APP_ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'vitalynx.db'}")
    DEV_VERIFICATION_MODE = os.getenv('DEV_VERIFICATION_MODE', 'true').lower() == 'true'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ESP32_API_KEY = os.getenv('ESP32_API_KEY', 'dev-esp32-key')
    AI_API_KEY = os.getenv('AI_API_KEY')
    AI_MODEL = os.getenv('AI_MODEL', 'optional')
    AI_API_BASE = os.getenv('AI_API_BASE', 'https://api.openai.com/v1')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', str(APP_ENV == 'production')).lower() == 'true'
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', str(APP_ENV == 'production')).lower() == 'true'
    ENABLE_HSTS = os.getenv('ENABLE_HSTS', str(APP_ENV == 'production')).lower() == 'true'
    TRUST_PROXY_COUNT = int(os.getenv('TRUST_PROXY_COUNT', '0'))
    HSTS_MAX_AGE = 31536000
