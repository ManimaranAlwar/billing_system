import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - Use PostgreSQL on Vercel, SQLite for local dev
    DATABASE_URL = os.environ.get('DATABASE_URL') or ''
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///alwar_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Upload folders
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    BARCODE_FOLDER = os.environ.get('BARCODE_FOLDER', 'static/uploads/barcodes')
    
    # Shop settings
    SHOP_NAME_TA = 'ALWAR ஸ்டோர்'
    SHOP_NAME_EN = 'ALWAR Store'
    
    # Ensure folders exist (only for local dev)
    if not DATABASE_URL:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(BARCODE_FOLDER, exist_ok=True)